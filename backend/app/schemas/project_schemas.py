from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from .character_schemas import CharacterResponse
from .panel_schemas import PanelResponse

class ProjectCreate(BaseModel):
    original_prompt: str = Field(..., description="User story prompt")
    character_name: str = Field(default="Free", description="Main character name")
    setting: str = Field(default="Enchanted Forest", description="Setting")
    tone: str = Field(default="Dramatic", description="Story tone")
    art_style: str = Field(default="Realistic", description="Art style")
    panel_count: str = Field(default="6", description="Panel count: 4, 6, 8, 10, or AUTO")

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    original_prompt: Optional[str] = None
    character_name: Optional[str] = None
    setting: Optional[str] = None
    tone: Optional[str] = None
    art_style: Optional[str] = None
    panel_count: Optional[int] = None
    status: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    title: str
    original_prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str
    panel_count: int
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    characters: List[CharacterResponse] = Field(default_factory=list)
    panels: List[PanelResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
