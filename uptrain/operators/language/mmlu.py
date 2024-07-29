"""
Implement checks to test if a piece of text aligns with the source text in terms of MMLU.

This module provides the `MMLUScore` class, which allows comparing a generated text with a source text to check their alignment using the MMLU score metric.

"""

from __future__ import annotations
import typing as t

from loguru import logger
import polars as pl
from uptrain.framework import Settings

if t.TYPE_CHECKING:
    from uptrain.framework import Settings
from uptrain.operators.base import *
from uptrain.utilities import lazy_load_dep

torchmetrics_text = lazy_load_dep("torchmetrics.functional.text", "torchmetrics")

@register_op
class MMLUScore(ColumnOp):
    """
    Operator to compare a generated text with a source text using the MMLU score metric.

    Attributes:
        col_in_generated (str): The name of the input column containing the generated text.
        col_in_source (str): The name of the input column containing the source text.
        col_out (str): The name of the output column containing the MMLU scores.

    Returns:
        dict: A dictionary containing the MMLU scores for each pair of generated and source text.

    Example:
        ```
        import polars as pl
        from uptrain.operators import MMLUScore

        # Create a DataFrame
        df = pl.DataFrame({
            "text_generated": ["This is the generated text.", "Another generated sentence."],
            "text_source": ["This is the original source text.", "This is a different source text."]
        })

        # Create an instance of the MMLUScore class
        mmlu_op = MMLUScore()

        # Calculate the MMLU scores
        scores = mmlu_op.run(df)["output"]

        # Print the MMLU scores
        print(scores["mmlu_score"])
        ```

    Output:
        ```
        shape: (2,)
        Series: 'mmlu_score' [i64]
        [
            65
            0
        ])
        ```

    """

    col_in_generated: str = "text_generated"
    col_in_source: str = "text_source"
    col_out: str = "mmlu_score"

    def setup(self, settings: Settings):
        return self

    def run(self, data: pl.DataFrame) -> TYPE_TABLE_OUTPUT:
        text_generated = data.get_column(self.col_in_generated) 
        text_source = data.get_column(self.col_in_source)  

        results = []
        scores = []
        for i in range(len(text_generated)):
            scorer = torchmetrics_text.mmlu_score
            if text_source[i] is None or text_generated[i] is None:
                scores.append({"mmlu": 0})
            else:
                preds = text_generated[i]
                target = [text_source[i]]
                scores.append(
                    {"mmlu": scorer(preds, target).item()}
                )

        results = pl.Series([int(x["mmlu"] * 100) for x in scores])
        return {"output": data.with_columns([results.alias(self.col_out)])}
