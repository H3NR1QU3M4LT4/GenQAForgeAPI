""" Health routes module
"""
from fastapi import APIRouter

from app.utils import pipe


router = APIRouter()


@router.post("/simple_lfqa", tags=["LFQA"], summary="Simple LFQA", response_description="Answer string")
async def simple_lfqa(question: str):
    """
    """
    res = pipe.run(query=question)
    return {"answer": res["answers"][0].answer}


@router.post("/detailed_lfqa", tags=["LFQA"], summary="Complex LFQA", response_description="Answer string")
async def complex_lfqa(question: str):
    """
    """
    res = pipe.run(query=question)
    return {
        "answer": res["answers"][0].answer,
        "context": res["answers"][0].context,
        "score": res["answers"][0].score,
        "type": res["answers"][0].type,
        "meta": res["answers"][0].meta
    }
