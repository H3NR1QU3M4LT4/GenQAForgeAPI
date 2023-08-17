import os
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.pipelines import Pipeline
from haystack.nodes import PromptModel
from haystack.nodes import PromptNode, PromptTemplate, AnswerParser
from dotenv import load_dotenv


load_dotenv()


def check_faiss():
    if "faiss_document_store.db" in os.listdir("."):
        print("faiss already installed")
        try:
            loaded_document_store = FAISSDocumentStore.load(
                index_path="document_store",
                config_path="document_store.json"
            )
            return loaded_document_store
        except Exception as e:
            print(e)
            os.remove("faiss_document_store.db")
    else:
        print("faiss not installed")
        new_document_store = FAISSDocumentStore(embedding_dim=128, faiss_index_factory_str="Flat")
        return new_document_store


def create_retriever(document_store):
    retriever = DensePassageRetriever(
        document_store=document_store,
        # query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
        # passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
        query_embedding_model="vblagoje/dpr-question_encoder-single-lfqa-wiki",
        passage_embedding_model="vblagoje/dpr-ctx_encoder-single-lfqa-wiki",
        top_k=3,
    )
    return retriever


def create_prompt_model():
    rag_prompt = PromptTemplate(
        prompt="""Synthesize a comprehensive answer from the following text for the given question.
        Provide a clear response that reference the key points and information presented in the 
        text. Your answer should be in your own words and be no longer than 50 words.
        \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""",
        output_parser=AnswerParser(),
    )

    try:
        azure_chat = PromptModel(
            model_name_or_path=os.getenv('OPENAI_API_TYPE'),
            api_key=os.getenv('OPENAI_API_KEY'),
            model_kwargs={
                "azure_deployment_name": os.getenv('OPENAI_API_DEPLOYMENT'),
                "azure_base_url": os.getenv('OPENAI_API_BASE'),
            },
        )
        prompt_node = PromptNode(azure_chat, default_prompt_template=rag_prompt)
        return prompt_node

    except Exception as e:
        print(e)
        print("Error creating prompt model")
        prompt_node = PromptNode(model_name_or_path="google/flan-t5-large", default_prompt_template=rag_prompt)
        return prompt_node


def create_pipe(retriever, prompt_node):
    pipe = Pipeline()
    pipe.add_node(component=retriever, name="retriever", inputs=["Query"])
    pipe.add_node(component=prompt_node, name="prompt_node", inputs=["retriever"])
    return pipe
