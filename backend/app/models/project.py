import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    original_prompt = Column(Text, nullable=False)
    character_name = Column(String(255), nullable=False, default="Protagonist")
    setting = Column(String(255), nullable=False, default="Enchanted Forest")
    tone = Column(String(100), nullable=False, default="Dramatic")
    art_style = Column(String(100), nullable=False, default="Comic Book")
    panel_count = Column(Integer, nullable=False, default=6)
    status = Column(String(50), nullable=False, default="draft")  # draft, generating, completed, failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    characters = relationship("Character", back_populates="project", cascade="all, delete-orphan")
    panels = relationship("Panel", back_populates="project", order_by="Panel.panel_number", cascade="all, delete-orphan")
    exports = relationship("ComicExport", back_populates="project", cascade="all, delete-orphan")
