# GenQAForgeAPI

## Introduction
This API it is a Python FastAPI for interacting with a FAISS database of documents, retrieving the most similar documents 
to a given query, and answering questions about the documents.
It is using a retriever `vblagoje/dpr-question_encoder-single-lfqa-wiki` from the HuggingFace model hub. Also for the 
question answering it is using the `gtp-35-turbo` model from Azure OpenAI service, however if you don't have the proper 
keys and endpoints for the OpenAI service it will use the `google/flan-t5-large`.

## Installation
1. Clone the repository
2. Install the requirements.txt file
3. Install the other python packages listed in ./scripts/installation.sh
4. Or run the installation.sh script
5. Finally, execute the FastAPI: `uvicorn main:app --reload`

## Usage
The API has 3 different services:

### Health Check
#### /
This endpoint returns a simple message to welcome you and check if the API is running.

#### /health
This endpoint returns a simple message to check if the API is running with a status code of 200 and Healthy.

### FAISS

#### /upload
This endpoint accepts a pdf file and uploads it to the FAISS database. It returns a message with the sucess or failure of the upload.

#### /files
This endpoint returns a list of all the files in the FAISS database.

#### /len_files
This endpoint returns the number of files in the FAISS database.

#### /delete
This endpoint accepts a filename and deletes it from the FAISS database. It returns a message with the sucess or failure of the deletion.

### LFQA

#### /simple_lfqa
This endpoint takes a query or question and returns the answer in a simple string format. `{"answer": "generator_answer"}`

#### /detailed_lfqa
This endpoint takes a query or question and returns the answer in a detailed JSON format. 
```json
{
  "answer": "answer",
  "context": "context",
  "score": "score",
  "type": "type",
  "meta": "meta"
}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
