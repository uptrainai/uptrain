from __future__ import annotations
import typing as t

import polars as pl
import deltalake as dl

if t.TYPE_CHECKING:
    from uptrain.framework import Settings
from uptrain.operators.base import *

# -----------------------------------------------------------
# Read from text file formats - csv and json
# -----------------------------------------------------------


@register_op
class CsvReader(TableOp):
    """Reads data from a csv file.

    Args:
        fpath: Path to the csv file.
        batch_size: Number of rows to read at a time. Defaults to None, which reads the entire file.

    """

    fpath: str
    batch_size: t.Optional[int] = None
    _executor: TextReaderExecutor

    def setup(self, settings: Settings | None = None):
        self._executor = TextReaderExecutor(self)
        return self

    def run(self) -> TYPE_TABLE_OUTPUT:
        return {"output": self._executor.run()}


@register_op
class JsonReader(TableOp):
    """Reads data from a json file.

    Args:
        fpath: Path to the json file.
        batch_size: Number of rows to read at a time. Defaults to None, which reads the entire file.

    """

    fpath: str
    batch_size: t.Optional[int] = None
    _executor: TextReaderExecutor

    def setup(self, settings: Settings | None = None):
        self._executor = TextReaderExecutor(self)
        return self

    def run(self) -> TYPE_TABLE_OUTPUT:
        return {"output": self._executor.run()}


class TextReaderExecutor:
    op: t.Union[CsvReader, JsonReader]
    dataset: pl.DataFrame
    rows_read: int

    def __init__(self, op: t.Union[CsvReader, JsonReader]):
        self.op = op
        self.rows_read = 0
        if isinstance(self.op, CsvReader):
            self.dataset = pl.read_csv(self.op.fpath)
        elif isinstance(self.op, JsonReader):
            self.dataset = pl.read_ndjson(self.op.fpath)

    @property
    def is_incremental(self) -> bool:
        return self.op.batch_size is not None

    def run(self) -> pl.DataFrame | None:
        if not self.is_incremental:
            data = self.dataset
        else:
            if self.rows_read >= len(self.dataset):
                data = None
            else:
                assert self.op.batch_size is not None
                self.rows_read += self.op.batch_size
                data = self.dataset.slice(self.rows_read, self.op.batch_size)
        return data


# -----------------------------------------------------------
# Read from a Delta Table, which uses parquet files under the hood
# -----------------------------------------------------------


@register_op
class DeltaReader(TableOp):
    """Reads data from a Delta Lake table.

    Args:
        fpath: File path to the Delta Lake table.
        batch_split: Whether to read the table in batches. Defaults to False.
        
    """

    fpath: str
    batch_split: bool = False
    _dataset: t.Any  # pyarrow dataset
    _batch_generator: t.Optional[t.Iterator[t.Any]]  # record batch generator

    def setup(self, settings: Settings | None = None):
        self._dataset = dl.DeltaTable(self.fpath).to_pyarrow_dataset()
        if self.is_incremental:
            self._batch_generator = iter(self._dataset.to_batches())
        return self

    @property
    def is_incremental(self) -> bool:
        return self.batch_split is True

    def run(self) -> TYPE_TABLE_OUTPUT:
        if not self.is_incremental:
            data = pl.from_arrow(self._dataset.to_table())
        else:
            try:
                data = pl.from_arrow(next(self._batch_generator))  # type: ignore
            except StopIteration:
                data = None

        if data is not None:
            assert isinstance(data, pl.DataFrame)
        return {"output": data}


# -----------------------------------------------------------
# Read from Uptrain's object storage
# -----------------------------------------------------------


class UptrainReader(TableOp):
    dataset_id: str

    def setup(self, _: t.Optional[Settings] = None):
        return self

    def run(self) -> TYPE_TABLE_OUTPUT:
        raise NotImplementedError(
            "UptrainReader is not implemented yet in the library."
        )
