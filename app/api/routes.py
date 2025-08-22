# app/api/routes.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
async def test_endpoint():
    return {"message": "API is working!"}


@router.post("/upload-pdf")
async def upload_pdf():
    return {"message": "PDF uploaded successfully!"}
