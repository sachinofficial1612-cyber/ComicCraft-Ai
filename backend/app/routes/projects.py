from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.project_schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from ..services.project_service import project_service
from ..services.generation_orchestrator import orchestrator
from ..services.demo_service import seed_demo_project
from ..utils.logger import get_logger

logger = get_logger("routes_projects")

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(req: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new comic project draft."""
    project = project_service.create_project(db, req)
    return project

@router.get("", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    """List all comic projects."""
    return project_service.list_projects(db)

@router.post("/demo", response_model=ProjectResponse)
def get_or_create_demo(db: Session = Depends(get_db)):
    """Get or seed built-in demo comic project."""
    return seed_demo_project(db)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    """Get project details with panels and characters."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, updates: ProjectUpdate, db: Session = Depends(get_db)):
    """Update project details."""
    updated = project_service.update_project(db, project_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    """Delete project and associated files."""
    deleted = project_service.delete_project(db, project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return None

@router.post("/{project_id}/generate", response_model=ProjectResponse)
def generate_comic(project_id: str, db: Session = Depends(get_db)):
    """Trigger complete AI comic generation pipeline."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Run generation
    project = orchestrator.run_full_pipeline(db, project)
    return project

@router.get("/{project_id}/status")
def get_project_status(project_id: str, db: Session = Depends(get_db)):
    """Get current project status and panel generation progress."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    completed_panels = sum(1 for p in project.panels if p.status == "completed")
    total_panels = len(project.panels) or project.panel_count

    return {
        "project_id": project.id,
        "status": project.status,
        "error_message": project.error_message,
        "completed_panels": completed_panels,
        "total_panels": total_panels,
        "progress_percentage": int((completed_panels / total_panels) * 100) if total_panels > 0 else 0
    }
