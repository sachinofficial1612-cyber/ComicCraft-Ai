import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.export import ComicExport
from ..services.project_service import project_service
from ..services.storage_service import storage_service
from ..exporters import pdf_exporter, png_exporter
from ..utils.logger import get_logger

logger = get_logger("routes_export")

router = APIRouter(prefix="/api/projects/{project_id}/export", tags=["export"])

@router.post("/pdf")
def export_pdf(project_id: str, db: Session = Depends(get_db)):
    """Export comic project as PDF file."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project.panels:
        raise HTTPException(status_code=400, detail="Cannot export project with no panels")

    pdf_path = pdf_exporter.export_comic_pdf(project, project.panels)
    
    export_entry = ComicExport(
        project_id=project.id,
        export_type="pdf",
        file_path=pdf_path
    )
    db.add(export_entry)
    db.commit()

    filename = os.path.basename(pdf_path)
    return {
        "id": export_entry.id,
        "project_id": project.id,
        "export_type": "pdf",
        "filename": filename,
        "download_url": f"/api/projects/{project.id}/export/download/{filename}"
    }

@router.post("/png")
def export_png(project_id: str, db: Session = Depends(get_db)):
    """Export comic project as PNG page files."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project.panels:
        raise HTTPException(status_code=400, detail="Cannot export project with no panels")

    png_paths = png_exporter.export_comic_pngs(project, project.panels)
    
    exports = []
    for p_path in png_paths:
        export_entry = ComicExport(
            project_id=project.id,
            export_type="png",
            file_path=p_path
        )
        db.add(export_entry)
        filename = os.path.basename(p_path)
        exports.append({
            "id": export_entry.id,
            "filename": filename,
            "download_url": f"/api/projects/{project.id}/export/download/{filename}"
        })
    db.commit()

    return {"project_id": project.id, "export_type": "png", "pages": exports}

@router.get("/download/{filename}")
def download_export(project_id: str, filename: str):
    """Download exported comic file (PDF or PNG)."""
    file_path = storage_service.get_export_path(project_id, filename)
    if os.path.exists(file_path):
        media_type = "application/pdf" if filename.endswith(".pdf") else "image/png"
        return FileResponse(file_path, media_type=media_type, filename=filename)
    logger.error(f"Download export file not found at: {file_path}")
    raise HTTPException(status_code=404, detail=f"Export file '{filename}' not found")
