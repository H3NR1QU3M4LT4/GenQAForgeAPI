# Author: Henrique Malta
FROM python:3.10.12-slim-buster

# Metadata
LABEL maintainer="Henrique Malta <Silvinohenrique.Malta@merkle.com>"
LABEL version="0.0.1"
LABEL name="FastAPI app"

# Install code python dependencies
RUN pip install --upgrade pip \
    && pip install 'farm-haystack[inference,faiss]' --no-cache-dir \
    && pip install sentence_transformers --no-cache-dir --no-deps \
    && pip install openai --no-cache-dir --no-deps

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get install -y libfontconfig && \
    wget --no-check-certificate https://dl.xpdfreader.com/xpdf-tools-linux-4.04.tar.gz && \
    tar -xvf xpdf-tools-linux-4.04.tar.gz && \
    cp xpdf-tools-linux-4.04/bin64/pdftotext /usr/local/bin && \
    rm xpdf-tools-linux-4.04.tar.gz && \
    apt-get remove -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# FastAPI app
WORKDIR /code
COPY ./app /code/app

# Install Python dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--log-level=debug"]
