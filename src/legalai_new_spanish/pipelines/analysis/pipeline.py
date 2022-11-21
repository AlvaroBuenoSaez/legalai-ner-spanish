"""
This is a boilerplate pipeline 'analysis'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from . nodes import print_data

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
                func=print_data,
                inputs=["tc_sentences","tc_relevant_data"],
                outputs="tc_info",
                name="print_data",
            )
    ])
