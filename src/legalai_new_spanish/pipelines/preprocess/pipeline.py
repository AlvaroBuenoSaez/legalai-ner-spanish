"""
This is a boilerplate pipeline 'preprocess'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import process_tc

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
            node(
                func=process_tc,
                inputs=["params:raw_tc"],
                outputs="tc_sentences",
                name="process_tc",
            ),
        
    ])
