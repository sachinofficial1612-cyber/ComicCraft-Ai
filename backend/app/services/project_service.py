from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.project import Project
from ..models.character import Character
from ..models.panel import Panel
from ..models.export import ComicExport
from ..schemas.project_schemas import ProjectCreate, ProjectUpdate
from ..services.storage_service import storage_service

class ProjectService:
    def create_project(self, db: Session, req: ProjectCreate) -> Project:
        # Resolve panel count string
        panel_cnt = 6
        if req.panel_count != "AUTO":
            try:
                panel_cnt = int(req.panel_count)
            except ValueError:
                panel_cnt = 6

        project = Project(
            title=f"Comic: {req.character_name}'s Adventure",
            original_prompt=req.original_prompt,
            character_name=req.character_name,
            setting=req.setting,
            tone=req.tone,
            art_style=req.art_style,
            panel_count=panel_cnt,
            status="draft"
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    def get_project(self, db: Session, project_id: str) -> Optional[Project]:
        return db.query(Project).filter(Project.id == project_id).first()

    def list_projects(self, db: Session) -> List[Project]:
        return db.query(Project).order_by(Project.created_at.desc()).all()

    def update_project(self, db: Session, project_id: str, updates: ProjectUpdate) -> Optional[Project]:
        project = self.get_project(db, project_id)
        if not project:
            return None
        data = updates.model_dump(exclude_unset=True)
        for field, val in data.items():
            setattr(project, field, val)
        db.commit()
        db.refresh(project)
        return project

    def delete_project(self, db: Session, project_id: str) -> bool:
        project = self.get_project(db, project_id)
        if not project:
            return False
        storage_service.delete_project_storage(project_id)
        db.delete(project)
        db.commit()
        return True

project_service = ProjectService()
