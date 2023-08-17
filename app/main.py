""" FastAPI to predict latitudes, longitudes and areas for solar panels
"""
from fastapi import FastAPI
import logging

from app.routes import health_router, faiss_router, lfqa_router


log_format = "%(levelname)s:     %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

description = """
FastAPI helps you create a full API. 🚀
"""

app = FastAPI(
    title="FastAPI",
    description=description,
    version="0.0.1",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "Silvino Henrique Malta",
        "email": "Silvinohenrique.Malta@merkle.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(health_router)
app.include_router(faiss_router)
app.include_router(lfqa_router)
