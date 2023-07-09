import os
from uptrain.framework import Settings

SETTINGS = Settings()
SELF_DIR = os.path.dirname(os.path.abspath(__file__))


# uptrain.operators.drift
def test_concept_drift():
    import polars as pl
    from uptrain.operators import ParamsDDM, ConceptDrift
    from uptrain.operators import CsvReader

    # Create an instance of the ParamsDDM class with the parameters
    params_ddm = ParamsDDM(warm_start=500, warning_threshold=2.0, drift_threshold=3.0)

    # Create an instance of the ConceptDrift operator
    op = ConceptDrift(algorithm="DDM", params=params_ddm, col_in_measure="prediction")

    # Run the operator on the input data
    input_data = (
        CsvReader(fpath=os.path.join(SELF_DIR, "data/predictions.csv"))
        .setup(SETTINGS)
        .run()["output"]
    )
    output = op.setup(SETTINGS).run(input_data)["extra"]

    # Check the detected concept drift information
    if output["alert_info"] is not None:
        print("Counter:", output["alert_info"]["counter"])


# uptrain.operators.language.embedding
def test_embedding():
    import polars as pl
    from uptrain.operators import Embedding

    # Create a DataFrame
    df = pl.DataFrame(
        {"text": ["This is the first sentence.", "Here is another sentence."]}
    )

    # Create an instance of the Embedding class
    embedding_op = Embedding(model="MiniLM-L6-v2", col_in_text="text")

    # Generate embeddings for the text column
    embeddings = embedding_op.setup(SETTINGS).run(df)["output"]

    # Print the embeddings
    print(embeddings)


# uptrain.operators.embs
def test_embs_cosine_distribution():
    import polars as pl
    from uptrain.operators import Distribution
    from uptrain.operators import JsonReader

    # Create an instance of the Distribution operator
    op = Distribution(
        kind="cosine_similarity",
        col_in_embs=["context_embeddings", "response_embeddings"],
        col_in_groupby=["question_idx", "experiment_id"],
        col_out=["similarity-context", "similarity-response"],
    )

    # Run the operator on the input data
    input_data = (
        JsonReader(fpath=os.path.join(SELF_DIR, "data/qna_on_docs_samples.jsonl"))
        .setup(SETTINGS)
        .run()["output"]
    )
    output = op.setup(SETTINGS).run(input_data)["output"]

    # Print the output
    print(output)


# uptrain.operators.embs
def test_embs_rouge_score():
    import polars as pl
    from uptrain.operators import Distribution
    from uptrain.operators import JsonReader

    # Create an instance of the Distribution operator
    op = Distribution(
        kind="rouge",
        col_in_embs=["document_text"],
        col_in_groupby=["question_idx", "experiment_id"],
        col_out=["rogue_f1"],
    )
    # Run the operator on the input data
    input_data = (
        JsonReader(fpath=os.path.join(SELF_DIR, "data/qna_on_docs_samples.jsonl"))
        .setup(SETTINGS)
        .run()["output"]
    )
    output = op.setup(SETTINGS).run(input_data)["output"]

    # Print the output
    print(output)


# uptrain.operators.embs
def test_embs_umap_operator():
    import polars as pl
    from uptrain.operators import UMAP
    from uptrain.operators import JsonReader

    # Create an instance of the UMAP operator
    op = UMAP(col_in_embs_1="context_embeddings", col_in_embs_2="response_embeddings")

    # Run the operator on the input data
    input_data = (
        JsonReader(fpath=os.path.join(SELF_DIR, "data/qna_on_docs_samples.jsonl"))
        .setup(SETTINGS)
        .run()["output"]
    )
    output = op.setup(SETTINGS).run(input_data)["output"]

    # Print the output
    print(output)


# uptrain.operators.similarity
def test_cosine_similarity_operator():
    import polars as pl
    import numpy as np
    from uptrain.operators import CosineSimilarity

    # Create a DataFrame
    df = pl.DataFrame(
        {
            "vector1": [np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.5, 0.6])],
            "vector2": [np.array([0.7, 0.8, 0.9]), np.array([0.2, 0.3, 0.4])],
        }
    )

    # Create an instance of the CosineSimilarity class
    similarity_op = CosineSimilarity(
        col_in_vector_1="vector1", col_in_vector_2="vector2"
    )

    # Calculate the cosine similarity between the two vectors
    result = similarity_op.run(df)
    similarity_scores = result["output"]

    # Print the similarity scores
    print(similarity_scores)


# uptrain.operators.metrics
def test_accuracy_operator():
    from uptrain.operators import Accuracy
    from uptrain.operators import CsvReader

    # Create an instance of the Accuracy operator
    op = Accuracy(
        kind="NOT_EQUAL",
        col_in_prediction="prediction",
        col_in_ground_truth="ground_truth",
    )

    # Run the operator on the input data
    input_data = (
        CsvReader(fpath=os.path.join(SELF_DIR, "data/predictions.csv"))
        .setup(SETTINGS)
        .run()["output"]
    )
    accuracy_scores = op.setup(SETTINGS).run(input_data)["output"]

    # Print the accuracy scores
    print(accuracy_scores)


# uptrain.operators.table
def test_table_operator():
    import polars as pl
    from uptrain.operators import ColumnExpand

    # Create a DataFrame
    df = pl.DataFrame({"column1": [1, 2, 3], "column2": ["A", "B", "C"]})

    # Create an instance of the ColumnExpand class
    expand_op = ColumnExpand(
        col_out_names=["column1", "column2"], col_vals=[df["column1"], df["column2"]]
    )

    # Return the input DataFrame as it is
    output_df = expand_op.run(df)["output"]

    # Print the output DataFrame
    print(output_df)


# uptrain.operators.vis
def test_vis_plot_operators():
    import polars as pl
    from uptrain.operators import LineChart, ScatterPlot, BarChart, Histogram, MultiPlot

    # Create a DataFrame
    df = pl.DataFrame({"x": [1, 2, 3, 4, 5], "y": [10, 20, 15, 25, 30]})

    # LINE CHART
    # Create a line chart using the LineChart class
    line_chart = LineChart(props={"x": "x", "y": "y"}, title="Line Chart")

    # Generate the line chart
    line_chart = line_chart.run(df)["extra"]["chart"]

    # Show the chart
    # line_chart.show()

    # SCATTER CHART
    # Create a scatter chart using the ScatterPlot class
    scatter_chart = ScatterPlot(
        props={"x": "x", "y": "y"}, title="Scatter Chart"
    )

    # Generate the scatter chart
    scatter_chart = scatter_chart.run(df)["extra"]["chart"]

    # Show the chart
    # scatter_chart.show()

    # BAR CHART
    # Create a bar chart using the BarChart class
    bar_chart = BarChart(props={"x": "x", "y": "y"}, title="Bar Chart")

    # Generate the bar chart
    bar_chart = bar_chart.run(df)["extra"]["chart"]

    # Show the chart
    # bar_chart.show()

    # HISTOGRAM
    # Create a histogram using the Histogram class
    histogram = Histogram(props={"x": "x"}, title="Histogram")

    # Generate the histogram
    histogram = histogram.run(df)["extra"]["chart"]

    # Show the chart
    # histogram.show()

    # SUBPLOT
    # Create a subplot using the MultiPlot class
    subplot = MultiPlot(
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

    # Generate the subplot
    subplot = subplot.run(df)["extra"]["chart"]

    # Show the chart
    subplot.show()


# uptrain.operators.language.rouge
def test_rouge_operator():
    import polars as pl
    from uptrain.operators import RougeScore

    # Create a DataFrame
    df = pl.DataFrame(
        {
            "text_generated": [
                "This is the generated text.",
                "Another generated sentence.",
            ],
            "text_source": [
                "This is the original source text.",
                "This is a different source text.",
            ],
        }
    )

    # Create an instance of the RougeScore class
    rouge_op = RougeScore(score_type="f1")

    # Calculate the Rouge-L scores
    scores = rouge_op.run(df)["output"]

    # Print the Rouge-L scores
    print(scores)


# uptrain.operators.language.text
def test_docs_link_version_operator():
    import polars as pl
    from uptrain.operators import DocsLinkVersion

    # Create a DataFrame
    df = pl.DataFrame(
        {
            "text": [
                "https://docs.streamlit.io/1.9.0/library/api-reference/charts/st.plotly_chart#stplotly_chart",
                "No version here",
            ]
        }
    )

    # Create an instance of the DocsLinkVersion class
    link_op = DocsLinkVersion(col_in_text="text")

    # Extract the version numbers
    versions = link_op.run(df)["output"]

    # Print the extracted version numbers
    print(versions)


# uptrain.operators.language.text
def test_text_length_operator():
    import polars as pl
    from uptrain.operators import TextLength

    # Create a DataFrame
    df = pl.DataFrame(
        {
            "text": [
                "This is a sample text.",
                "Another example sentence.",
                "Yet another sentence.",
            ]
        }
    )

    # Create an instance of the TextLength class
    length_op = TextLength(col_in_text="text")

    # Calculate the length of each text entry
    lengths = length_op.run(df)["output"]

    # Print the text lengths
    print(lengths)


# uptrain.operators.language.text
def test_text_comparison_operator():
    import polars as pl
    from uptrain.operators import TextComparison

    # Create a DataFrame
    df = pl.DataFrame(
        {
            "text": [
                "This is a sample text.",
                "Another example sentence.",
                "Yet another sentence.",
            ]
        }
    )

    # Set the reference text for comparison
    ref_text = "This is a sample text."

    # Create an instance of the TextComparison class
    comp_op = TextComparison(reference_texts=ref_text, col_in_text="text")

    # Compare each text entry with the reference text
    comparison = comp_op.run(df)["output"]

    # Print the comparison results
    print(comparison)
