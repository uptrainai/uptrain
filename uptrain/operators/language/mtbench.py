"""
Implement checks to evaluate multi-turn dialogues using MT-Bench.

This module provides the `MTBenchScore` class, which allows comparing generated multi-turn dialogues with source dialogues to evaluate their alignment using the MT-Bench score metric.

"""

from __future__ import annotations
import typing as t

import polars as pl
from uptrain.framework import Settings

if t.TYPE_CHECKING:
    from uptrain.framework import Settings
from uptrain.operators.base import *
from uptrain.utilities import lazy_load_dep

# Hypothetical function to compute MT-Bench score
def compute_mtbench_score(generated_dialogue: list[str], source_dialogue: list[str]) -> float:
    # Example logic for MT-Bench score calculation
    # Replace this with the actual MT-Bench scoring logic
    score = sum(1 for gen, src in zip(generated_dialogue, source_dialogue) if gen == src) / len(source_dialogue)
    return score

@register_op
class MTBenchScore(ColumnOp):
    """
    Operator to compare generated multi-turn dialogues with source dialogues using the MT-Bench score metric.

    Attributes:
        col_in_generated (str): The name of the input column containing the generated dialogues.
        col_in_source (str): The name of the input column containing the source dialogues.
        col_out (str): The name of the output column containing the MT-Bench scores.

    Returns:
        dict: A dictionary containing the MT-Bench scores for each pair of generated and source dialogues.

    Example:
        ```
        import polars as pl
        from uptrain.operators import MTBenchScore

        # Create a DataFrame
        df = pl.DataFrame({
            "dialogue_generated": [["Hi", "Hello"], ["How are you?", "I'm fine, thanks."]],
            "dialogue_source": [["Hello", "Hi"], ["How do you do?", "I'm good, thank you."]]
        })

        # Create an instance of the MTBenchScore class
        mtbench_op = MTBenchScore()

        # Calculate the MT-Bench scores
        scores = mtbench_op.run(df)["output"]

        # Print the MT-Bench scores
        print(scores["mtbench_score"])
        ```

    Output:
        ```
        shape: (2,)
        Series: 'mtbench_score' [f64]
        [
            0.5
            0.0
        ])
        ```

    """

    col_in_generated: str = "dialogue_generated"
    col_in_source: str = "dialogue_source"
    col_out: str = "mtbench_score"

    def setup(self, settings: Settings):
        return self

    def run(self, data: pl.DataFrame) -> TYPE_TABLE_OUTPUT:
        dialogues_generated = data.get_column(self.col_in_generated).to_list()  # candidate/preds
        dialogues_source = data.get_column(self.col_in_source).to_list()  # reference/target

        scores = []
        for generated, source in zip(dialogues_generated, dialogues_source):
            if source is None or generated is None:
                scores.append(0.0)
            else:
                score = compute_mtbench_score(generated, source)
                scores.append(score)

        results = pl.Series(scores, name=self.col_out)
        return {"output": data.with_columns([results])}
