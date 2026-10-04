import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class Panel(Base):
    __tablename__ = "panels"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    panel_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)
    scene_description = Column(Text, nullable=True)
    narration = Column(Text, nullable=True)
    dialogue = Column(JSON, nullable=True, default=list)  # List of dicts: [{speaker, text, emotion, type, x, y}]
    speaker = Column(String(255), nullable=True)
    sound_effect = Column(String(100), nullable=True)
    image_prompt = Column(Text, nullable=True)
    image_path = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="panels")
