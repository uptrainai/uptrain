"""
Implement operators over text data.

This module provides several operators for processing and analyzing text data, including:
- `DocsLinkVersion`: Extracts version numbers from URLs in text data, optionally filtered by domain name.
- `TextLength`: Calculates the length of each text entry in a column.
- `TextComparison`: Compares each text entry in a column with a reference text.

"""

from __future__ import annotations
import re
import typing as t
from urllib.parse import urlparse

from loguru import logger
import polars as pl
from uptrain.framework import Settings

if t.TYPE_CHECKING:
    from uptrain.framework import Settings
from uptrain.operators.base import *


# TODO: Add support for versions without a minor version number (e.g., "v1") or without a patch version number (e.g., "v1.2")
@register_op
class DocsLinkVersion(ColumnOp):
    """
    Operator to extract version numbers from URLs in text data.

    Args:
        domain_name (str, optional): Filter down to links from this domain. Defaults to None.
        col_in_text (str): The name of the input column containing the text data.

    Returns:
        dict: A dictionary containing the extracted version numbers.

    Example:
        import polars as pl
        from uptrain.operators.language import DocsLinkVersion

        # Create a DataFrame
        df = pl.DataFrame({
            "text": ["https://docs.streamlit.io/1.9.0/library/api-reference/charts/st.plotly_chart#stplotly_chart", "This is an example: v1.2.3", 
            "Another example: https://example.com/v2.0"]
        })

        # Create an instance of the DocsLinkVersion class
        link_op = DocsLinkVersion(col_in_text="text")

        # Extract the version numbers
        versions = link_op.run(df)["output"]

        # Print the extracted version numbers
        print(versions)

    Output:
        shape: (3,)
        Series: '_col_0' [str]
        [
                "1.9.0"
                null
                null
        ]

    """

    domain_name: t.Optional[str] = None  # filter down to links from this domain
    col_in_text: str

    def setup(self, settings: Settings | None = None):
        return self

    def run(self, data: pl.DataFrame) -> TYPE_COLUMN_OUTPUT:
        def fetch_version(text):
            for link in extract_links(text, self.domain_name):
                v = extract_version(link)
                if v is not None:
                    return v
            return None

        return {
            "output": data.get_column(self.col_in_text)
            .apply(fetch_version)
            .alias(get_output_col_name_at(0))
        }


@register_op
class TextLength(ColumnOp):
    """
    Operator to calculate the length of each text entry in a column.

    Args:
        col_in_text (str): The name of the input column containing the text data.

    Returns:
        dict: A dictionary containing the calculated text lengths.

    Example:
        import polars as pl
        from uptrain.operators.language import TextLength

        # Create a DataFrame
        df = pl.DataFrame({
            "text": ["This is a sample text.", "Another example sentence.", "Yet another sentence."]
        })

        # Create an instance of the TextLength class
        length_op = TextLength(col_in_text="text")

        # Calculate the length of each text entry
        lengths = length_op.run(df)["output"]

        # Print the text lengths
        print(lengths)

    Output:
        shape: (3,)
        Series: '_col_0' [i64]
        [
                22
                25
                21
        ]

    """

    col_in_text: str

    def setup(self, settings: Settings | None = None):
        return self

    def run(self, data: pl.DataFrame) -> TYPE_COLUMN_OUTPUT:
        return {
            "output": data.get_column(self.col_in_text)
            .apply(len)
            .alias(get_output_col_name_at(0))
        }


@register_op
class TextComparison(ColumnOp):
    """
    Operator to compare each text entry in a column with a reference text.

    Args:
        reference_text (str): The reference text for comparison.
        col_in_text (str): The name of the input column containing the text data.

    Returns:
        dict: A dictionary containing the comparison results (1 if equal, 0 otherwise).

    Example:
        import polars as pl
        from uptrain.operators.language import TextComparison

        # Create a DataFrame
        df = pl.DataFrame({
            "text": ["This is a sample text.", "Another example sentence.", "Yet another sentence."]
        })

        # Set the reference text for comparison
        ref_text = "This is a sample text."

        # Create an instance of the TextComparison class
        comp_op = TextComparison(reference_text=ref_text, col_in_text="text")

        # Compare each text entry with the reference text
        comparison = comp_op.run(df)["output"]
        
        # Print the comparison results
        print(comparison)

    Output:
        shape: (3,)
        Series: '_col_0' [i64]
        [
                1
                0
                0
        ]
    
    """

    reference_text: str
    col_in_text: str

    def setup(self, settings: Settings | None = None):
        return self

    def run(self, data: pl.DataFrame) -> TYPE_COLUMN_OUTPUT:
        return {
            "output": data.get_column(self.col_in_text)
            .apply(lambda x: int(x == self.reference_text))
            .alias(get_output_col_name_at(0))
        }


# -----------------------------------------------------------
# Utility routines (for above operators)
# -----------------------------------------------------------


def extract_links(text, base_domain=None):
    """
    Extracts links from the given text.

    Args:
        text (str): The text from which links are to be extracted.
        base_domain (str, optional): If provided, only links containing this base domain will be returned. Defaults to None.

    Returns:
        list: A list of extracted links from the text, optionally filtered by the base domain.
    
    """
    pattern = r"\bhttps?://\S+\b"
    matches = re.findall(pattern, text)
    if base_domain is not None:
        return [m for m in matches if base_domain in m]
    else:
        return matches


def extract_version(url):
    """
    Extracts version information from the given URL.

    Args:
        url (str): The URL from which version information is to be extracted.

    Returns:
        str or None: The extracted version information, or None if no version information is found.
    
    """
    patterns = [
        r"v\d+\.\d+\.\d+",
        r"v\d+",
        r"\d+\.\d+\.\d+",
        r"\d+\.\d+",
        r"\d+",
    ]
    pattern = r"|".join([r"^" + s + r"$" for s in patterns])

    path_strings = urlparse(url).path.split("/")
    for s in path_strings:
        match = re.search(pattern, s)
        if match:
            return match.group()
    return None
