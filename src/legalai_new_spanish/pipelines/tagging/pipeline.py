"""
This is a boilerplate pipeline 'tagging'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import join_entities,infer_ancora,infer_conll,infer_capitel,fix_entities,tag_sentences,format_sentences_to_BIO
def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
            node(
                func=infer_ancora,
                inputs=["tc_sentences_text","params:config"],
                outputs="tc_entities_ancora",
                name="infer_data_ancora",
            ),
            node(
                func=infer_capitel,
                inputs=["tc_sentences_text","params:config"],
                outputs="tc_entities_capitel",
                name="infer_data_capitell",
            ),
            node(
                func=infer_conll,
                inputs=["tc_sentences_text","params:config"],
                outputs="tc_entities_conll",
                name="infer_data_conll",
            ),
            # node(
            #     func=join_entities,
            #     inputs=["tc_entities_conll","tc_entities_capitel","tc_entities_ancora"],
            #     outputs="tc_entities",
            #     name="join_entities",
            # ),
            # node(
            #     func=fix_entities,
            #     inputs="tc_entities",
            #     outputs="tc_entities_fixed",
            #     name="fiz_entitites",
            # ),
            # node(
            #     func=format_sentences_to_BIO,
            #     inputs="tc_sentences_text",
            #     outputs="tc_NER",
            #     name="format_sentences_word_by_word",
            # )
            # node(
            #     func=tag_sentences,
            #     inputs=["tc_entities_fixed","tc_sentences"],
            #     outputs="tc_tagged",
            #     name="fiz_entitites",
            # ) 
    ]
    )
