from fastapi import APIRouter, File, UploadFile, Depends
from haystack.nodes import PDFToTextConverter, PreProcessor
from pathlib import Path
import shutil
import tempfile

from app.utils import document_store, retriever
from app.utils.check_inputs import check_inputs


router = APIRouter()


@router.post("/upload/", tags=["Faiss Database"], summary="Upload file", response_description="Message string",
             dependencies=[Depends(check_inputs)])
async def upload_file(file: UploadFile = File(...)):
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = Path(temp_dir) / file.filename

            # Save the uploaded file to the temporary directory
            with temp_file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Convert, preprocess, and index the document parts
            converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
            docs = converter.convert(file_path=temp_file_path, meta={"file_name": file.filename})

            preprocessor = PreProcessor(
                clean_empty_lines=True,
                clean_whitespace=True,
                clean_header_footer=False,
                split_by="word",
                split_length=128,
                split_respect_sentence_boundary=True,
            )

            # Preprocess the documents
            docs = preprocessor.process(docs)

            # Index the documents
            document_store.write_documents(docs)

            document_store.update_embeddings(retriever)
            document_store.save("document_store")

            return {"message": "File uploaded and database created"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/files/", tags=["Faiss Database"], summary="List uploaded files", response_description="List of files")
async def list_uploaded_files():
    # Get a list of unique original document paths from the FAISS store
    try:
        all_documents = document_store.get_all_documents()
        uploaded_files_dict = {}
        for doc in all_documents:
            if not uploaded_files_dict.get(f'{doc.meta["file_name"]}'):
                uploaded_files_dict[f'{doc.meta["file_name"]}'] = doc.meta["file_name"]

        uploaded_files = [{"file_name": file_name} for file_name in uploaded_files_dict]

        return {"uploaded_files": list(uploaded_files)}
    except Exception as e:
        return {"error": str(e), "message": "No files in database"}


@router.get("/len_files/", tags=["Faiss Database"], summary="Number of uploaded files",
            response_description="Number of files")
async def len_uploaded_files():
    try:
        all_documents = document_store.get_all_documents()
        uploaded_files_dict = {}
        for doc in all_documents:
            if not uploaded_files_dict.get(f'{doc.meta["file_name"]}'):
                uploaded_files_dict[f'{doc.meta["file_name"]}'] = doc.meta["file_name"]

        return {"len_uploaded_files": len(uploaded_files_dict)}
    except Exception as e:
        return {"error": str(e), "message": "No files in database"}


@router.delete("/files/{file_name}", tags=["Faiss Database"], summary="Delete file",
               response_description="Message string")
async def delete_file(file_name: str):
    try:
        all_documents = document_store.get_all_documents()

        for doc in all_documents:
            if doc.meta.get("file_name"):
                if doc.meta["file_name"] == file_name:
                    document_store.delete_documents(ids=[doc.id])

        document_store.update_embeddings(retriever)
        document_store.save("document_store")
        return {"message": f"File {file_name} deleted"}
    except Exception as e:
        return {"error": str(e), "message": "No files in database"}
