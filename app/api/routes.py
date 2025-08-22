# app/api/routes.py
from fastapi import APIRouter, File, UploadFile

from app.services.upload_service import handle_pdf_upload

router = APIRouter()


@router.get("/test")
async def test_endpoint():
    return {"message": "API is working!"}


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    return await handle_pdf_upload(file)
