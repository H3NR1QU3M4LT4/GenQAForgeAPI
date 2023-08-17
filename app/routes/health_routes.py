""" Health routes module
"""
from fastapi import APIRouter, status


router = APIRouter()


@router.get("/", tags=["Health"], summary="Root info", response_description="Message string")
async def root():
    """
    Root endpoint
    - **message**: message (string) welcome message
    """
    return {"message": "Welcome to the API!"}


@router.get("/health", tags=["Health"], summary="Check API health", response_description="API status",
            status_code=status.HTTP_200_OK)
async def perform_healthcheck():
    """
    Health endpoint
    - **status**: status (string) healthy status
    """
    return "Healthy"
