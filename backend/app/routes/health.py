import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db
from ..config import settings
from ..ai import gemini_client

router = APIRouter(prefix="/api/health", tags=["health"])

@router.get("")
def health_check(db: Session = Depends(get_db)):
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    storage_writable = os.access(settings.STORAGE_DIR, os.W_OK)

    return {
        "status": "healthy" if (db_ok and storage_writable) else "unhealthy",
        "backend": True,
        "database": db_ok,
        "storage_writable": storage_writable,
        "gemini_configured": gemini_client.is_configured,
        "version": "1.0.0"
    }

@router.get("/ai")
def ai_health_check():
    return {
        "configured": gemini_client.is_configured,
        "text_model": settings.GEMINI_TEXT_MODEL,
        "image_model": settings.GEMINI_IMAGE_MODEL,
        "provider": settings.IMAGE_PROVIDER,
        "api_key_set": bool(settings.GEMINI_API_KEY)
    }
