"""
This module implements visualization operators for simple-checks in uptrain.

The module provides the `BarChart`, `LineChart`, `ScatterPlot`, `Table`, `Histogram`, and `MultiPlot` classes, 
which allow generating various types of visualizations. The charts are created based on 
the input DataFrame.

"""

from __future__ import annotations
import typing as t

from loguru import logger
from pydantic import Field
import polars as pl

if t.TYPE_CHECKING:
    from uptrain.framework import Settings
from uptrain.operators.base import *
from uptrain.utilities import lazy_load_dep

px = lazy_load_dep("plotly.express", "plotly")
ps = lazy_load_dep("plotly.subplots", "plotly")

__all__ = ["BarChart", "LineChart", "ScatterPlot", "Table", "Histogram", "MultiPlot"]


# Not to be used as an operator, only as a base class
class Chart(OpBaseModel):
    props: dict = Field(default_factory=dict)
    title: str = ""
    filter_on: list[str] = Field(default_factory=list)

    def setup(self, settings: Settings):
        return self
    
    def run(self, data: pl.DataFrame) -> TYPE_TABLE_OUTPUT:
        chart = getattr(px, self.kind)(data.to_pandas(), **self.props)
        return {"output": None, "extra": {"chart": chart}}

@register_op
class BarChart(Chart):
    """
    Operator to generate a bar chart.

    Attributes:
        props (dict): Additional properties to pass to the BarChart constructor.
        title (str): The title of the chart.

    Returns:
        dict: A dictionary containing the chart object.

    Example:
        ```
        import polars as pl
        from uptrain.operators import BarChart

        # Create a DataFrame
        df = pl.DataFrame({
            "x": [1, 2, 3, 4, 5],
            "y": [10, 20, 15, 25, 30]
        })

        # Create a bar chart using the BarChart class
        bar_chart = BarChart(props={"x": "x", "y": "y"}, title="Bar Chart")

        # Generate the bar chart
        chart = bar_chart.run(df)["extra"]["chart"]

        # Show the chart
        chart.show()
        ```

    """


    props: dict = Field(default_factory=dict)
    title: str = ""

    kind = "bar"


@register_op
class LineChart(Chart):
    """
    Operator to generate a line chart.

    Attributes:
        props (dict): Additional properties to pass to the LineChart constructor.
        title (str): The title of the chart.

    Returns:
        dict: A dictionary containing the chart object.

    Example:
        ```
        import polars as pl
        from uptrain.operators import LineChart

        # Create a DataFrame
        df = pl.DataFrame({
            "x": [1, 2, 3, 4, 5],
            "y": [10, 20, 15, 25, 30]
        })

        # Create a line chart using the LineChart class
        line_chart = LineChart(props={"x": "x", "y": "y"}, title="Line Chart")

        # Generate the line chart
        chart = line_chart.run(df)["extra"]["chart"]

        # Show the chart
        chart.show()
        ```

    """


    props: dict = Field(default_factory=dict)
    title: str = ""

    kind = "line"


@register_op
class ScatterPlot(Chart):
    """
    Operator to generate a scatter chart.

    Attributes:
        props (dict): Additional properties to pass to the ScatterPlot constructor.
        title (str): The title of the chart.

    Returns:
        dict: A dictionary containing the chart object.

    Example:
        ```
        import polars as pl
        from uptrain.operators import ScatterPlot

        # Create a DataFrame
        df = pl.DataFrame({
            "x": [1, 2, 3, 4, 5],
            "y": [10, 20, 15, 25, 30]
        })

        # Create a scatter chart using the ScatterPlot class
        scatter_plot = ScatterPlot(props={"x": "x", "y": "y"}, title="Scatter Plot")

        # Generate the scatter plot
        chart = scatter_plot.run(df)["extra"]["chart"]

        # Show the chart
        chart.show()
        ```

    """


    props: dict = Field(default_factory=dict)
    title: str = ""

    kind = "scatter"


@register_op
class Histogram(Chart):
    """
    Operator to generate a histogram.

    Attributes:
        props (dict): Additional properties to pass to the Histogram chart constructor.
        title (str): The title of the chart.

    Returns:
        dict: A dictionary containing the chart object.

    Example:
        ```
        import polars as pl
        from uptrain.operators import Histogram

        # Create a DataFrame
        df = pl.DataFrame({
            "x": [1, 2, 3, 4, 5],
            "y": [10, 20, 15, 25, 30]
        })

        # Create a histogram chart using the Histogram class
        histogram_chart = Histogram(props={"x": "x", "y": "y"}, title="Histogram Chart")

        # Generate the histogram chart
        chart = histogram_chart.run(df)["extra"]["chart"]

        # Show the chart
        chart.show()
        ```

    """


    props: dict = Field(default_factory=dict)
    title: str = ""

    kind = "histogram"


@register_op
class MultiPlot(Chart):
    """
    Operator to generate a subplot that can display multiple charts side-by-side.

    Attributes:
        props (dict): Additional properties to pass to the MultiPlot constructor.
        title (str): The title of the chart.

    Returns:
        dict: A dictionary containing the chart object.

    Example:
        ```
        import polars as pl
        from uptrain.operators import MultiPlot, LineChart, ScatterPlot, BarChart, Histogram

        # Create a DataFrame
        df = pl.DataFrame({
            "x": [1, 2, 3, 4, 5],
            "y": [10, 20, 15, 25, 30]
        })

        # Create a multiplot using the MultiPlot class
        multiplot = MultiPlot(
            props={},
            charts=[
                LineChart(
                    props={"x": "x", "y": "y"}, 
                    title="Line Chart"
                ),
                ScatterPlot(
                    props={"x": "x", "y": "y"},
                    title="Scatter Plot"
                ),
                BarChart(
                    props={"x": "x", "y": "y"},
                    title="Bar Chart"
                ),
                Histogram(
                    props={"x": "x"},
                    title="Histogram"
                )
            ],
            title="MultiPlot",
        )

        # Generate the multiplot
        chart = multiplot.run(df)["extra"]["chart"]

        # Show the chart
        chart.show()
        ```

    """

    props: dict = Field(default_factory=dict)
    title: str = ""
    charts: list

    kind = "multiplot"

    def run(self, data: pl.DataFrame) -> TYPE_TABLE_OUTPUT:
        subplot = ps.make_subplots(
            rows=1,
            cols=len(self.charts),
            subplot_titles=[chart.title for chart in self.charts],
        )

        for chart in self.charts:
            plot = getattr(px, chart.kind)(data.to_pandas(), **chart.props)
            subplot.add_trace(plot.to_dict()["data"][0], row=1, col=self.charts.index(chart) + 1)

        return {"output": None, "extra": {"chart": subplot}}

