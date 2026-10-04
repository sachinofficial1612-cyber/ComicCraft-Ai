from sqlalchemy.orm import Session
from ..models.project import Project
from ..schemas.project_schemas import ProjectCreate
from ..services.project_service import project_service
from ..services.generation_orchestrator import orchestrator
from ..utils.logger import get_logger

logger = get_logger("demo_service")

DEMO_PROMPT = "A brave red fox named Free explores an enchanted forest, discovering glowing ancient ruins and unlocking mystical secrets."

def seed_demo_project(db: Session) -> Project:
    """Check if demo project exists or seed it using the real generation pipeline."""
    existing = db.query(Project).filter(Project.character_name == "Free", Project.title.contains("Enchanted Forest")).first()
    if existing:
        return existing

    logger.info("Seeding built-in demo project 'Free the Fox in Enchanted Forest'...")
    demo_req = ProjectCreate(
        original_prompt=DEMO_PROMPT,
        character_name="Free",
        setting="Enchanted Forest",
        tone="Dramatic",
        art_style="Realistic",
        panel_count="6"
    )
    
    project = project_service.create_project(db, demo_req)
    project = orchestrator.run_full_pipeline(db, project)
    return project
