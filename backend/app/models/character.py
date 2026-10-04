import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    appearance = Column(Text, nullable=True)
    personality = Column(Text, nullable=True)
    clothing = Column(Text, nullable=True)
    colors = Column(Text, nullable=True)
    reference_image_path = Column(String(500), nullable=True)

    project = relationship("Project", back_populates="characters")
