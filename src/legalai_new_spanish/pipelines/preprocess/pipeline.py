"""
This is a boilerplate pipeline 'preprocess'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import plot_results, process_tc,get_results,extract_relevant_data,to_csv

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
            # node(
            #     func=process_tc,
            #     inputs=["params:raw_tc"],
            #     outputs=["tc_sentences","tc_reports"],
            #     name="process_tc",
            # ),
            node(
                func=get_results,
                inputs=["tc_reports"],
                outputs="tc_results",
                name="tc_reports",
            ),
            node(
                func=extract_relevant_data,
                inputs=["tc_sentences"],
                outputs="tc_relevant_data",
                name="extract_relevant_data",
            ),   
            node(
                func=plot_results,
                inputs=["tc_results","tc_relevant_data"],
                outputs=["bar_results","bar_relevant_data"],
                name="plot_results"
            ),
             node(
                func=to_csv,
                inputs="tc_sentences",
                outputs="tc_sentences_text",
                name="to_CSV"
            )
    ]
)
