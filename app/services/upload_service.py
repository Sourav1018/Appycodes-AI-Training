import os

from fastapi import HTTPException, UploadFile

from app.config.app_config import settings
from app.db.supabase_conn import get_supabase_client
from app.validators.file_validator import validate_pdf


async def handle_pdf_upload(file: UploadFile):
    # Validate PDF
    validate_pdf(file)

    # Read into memory
    file_bytes = await file.read()

    if settings.USE_SUPABASE:
        supabase = get_supabase_client()
        try:
            response = supabase.storage.from_("pdfs").upload(
                file.filename, file_bytes, {"content-type": "application/pdf"}
            )
            return {"message": "Upload successful (Supabase)", "response": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        os.makedirs("uploads", exist_ok=True)
        with open(f"uploads/{file.filename}", "wb") as f:
            f.write(file_bytes)
        return {"message": "Saved locally"}
