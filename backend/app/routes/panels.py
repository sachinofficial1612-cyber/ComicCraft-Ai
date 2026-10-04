import os
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.panel import Panel
from ..models.project import Project
from ..schemas.panel_schemas import PanelUpdate, PanelResponse
from ..services.project_service import project_service
from ..services.storage_service import storage_service
from ..services.generation_orchestrator import orchestrator
from ..utils.logger import get_logger

logger = get_logger("routes_panels")

router = APIRouter(prefix="/api/projects/{project_id}/panels", tags=["panels"])

@router.get("/{panel_number}/image")
def get_panel_image(project_id: str, panel_number: int):
    """Serve panel artwork PNG file."""
    img_path = storage_service.get_panel_image_path(project_id, panel_number)
    if os.path.exists(img_path):
        return FileResponse(img_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Panel artwork not found")

@router.put("/{panel_id}", response_model=PanelResponse)
def update_panel(project_id: str, panel_id: str, updates: PanelUpdate, db: Session = Depends(get_db)):
    """Update panel properties (dialogue, narration, image prompt, etc.)."""
    panel = db.query(Panel).filter(Panel.id == panel_id, Panel.project_id == project_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    data = updates.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(panel, k, v)

    db.commit()
    db.refresh(panel)
    return panel

@router.post("/{panel_id}/regenerate-image", response_model=PanelResponse)
def regenerate_panel_image(project_id: str, panel_id: str, db: Session = Depends(get_db)):
    """Regenerate panel artwork without changing dialogue/narration."""
    panel = db.query(Panel).filter(Panel.id == panel_id, Panel.project_id == project_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    panel = orchestrator.regenerate_single_panel_image(db, panel)
    return panel

@router.post("/{panel_id}/regenerate-story", response_model=PanelResponse)
def regenerate_panel_story_route(project_id: str, panel_id: str, db: Session = Depends(get_db)):
    """Regenerate dialogue and narration for panel without re-generating artwork."""
    panel = db.query(Panel).filter(Panel.id == panel_id, Panel.project_id == project_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    panel = orchestrator.regenerate_single_panel_story(db, panel)
    return panel

@router.post("/{panel_id}/regenerate-both", response_model=PanelResponse)
def regenerate_panel_both(project_id: str, panel_id: str, db: Session = Depends(get_db)):
    """Regenerate both artwork and dialogue/narration for panel."""
    panel = db.query(Panel).filter(Panel.id == panel_id, Panel.project_id == project_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    panel = orchestrator.regenerate_single_panel_story(db, panel)
    panel = orchestrator.regenerate_single_panel_image(db, panel)
    return panel

@router.delete("/{panel_id}")
def delete_panel(project_id: str, panel_id: str, db: Session = Depends(get_db)):
    """Delete a single panel and re-index remaining panel numbers."""
    panel = db.query(Panel).filter(Panel.id == panel_id, Panel.project_id == project_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    db.delete(panel)
    db.commit()

    # Re-index remaining panels
    panels = db.query(Panel).filter(Panel.project_id == project_id).order_by(Panel.panel_number).all()
    for idx, p in enumerate(panels, start=1):
        p.panel_number = idx
    db.commit()

    # Update project panel_count
    project = project_service.get_project(db, project_id)
    if project:
        project.panel_count = len(panels)
        db.commit()

    return {"message": "Panel deleted successfully", "remaining_panels": len(panels)}

@router.post("", response_model=PanelResponse)
def add_panel(project_id: str, db: Session = Depends(get_db)):
    """Add a new empty panel to the project."""
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    current_count = db.query(Panel).filter(Panel.project_id == project_id).count()
    new_num = current_count + 1

    new_panel = Panel(
        project_id=project_id,
        panel_number=new_num,
        title=f"Panel {new_num}",
        scene_description=f"New scene in {project.setting}",
        narration="A new chapter unfolds...",
        dialogue=[{
            "speaker": project.character_name,
            "text": "What awaits us next?",
            "emotion": "curious",
            "bubble_type": "speech"
        }],
        speaker=project.character_name,
        sound_effect="",
        image_prompt=f"Comic panel artwork for {project.character_name} in {project.setting}, {project.art_style} style.",
        image_path=f"/api/projects/{project_id}/panels/{new_num}/image",
        status="pending"
    )
    db.add(new_panel)
    project.panel_count = new_num
    db.commit()
    db.refresh(new_panel)

    # Generate artwork for the new panel
    orchestrator.regenerate_single_panel_image(db, new_panel)
    return new_panel
