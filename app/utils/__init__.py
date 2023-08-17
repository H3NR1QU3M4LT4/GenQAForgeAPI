from app.utils.initialize_components import check_faiss, create_retriever, create_prompt_model, create_pipe

# Initialize the FAISSDocumentStore
document_store = check_faiss()
retriever = create_retriever(document_store)
prompt_node = create_prompt_model()
pipe = create_pipe(retriever, prompt_node)
