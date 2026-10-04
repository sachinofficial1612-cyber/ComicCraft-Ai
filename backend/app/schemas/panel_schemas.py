from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict

class PanelBase(BaseModel):
    panel_number: int
    title: Optional[str] = None
    scene_description: Optional[str] = None
    narration: Optional[str] = None
    dialogue: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    speaker: Optional[str] = None
    sound_effect: Optional[str] = None
    image_prompt: Optional[str] = None

class PanelCreate(PanelBase):
    pass

class PanelUpdate(BaseModel):
    title: Optional[str] = None
    scene_description: Optional[str] = None
    narration: Optional[str] = None
    dialogue: Optional[List[Dict[str, Any]]] = None
    speaker: Optional[str] = None
    sound_effect: Optional[str] = None
    image_prompt: Optional[str] = None
    panel_number: Optional[int] = None

class PanelResponse(PanelBase):
    id: str
    project_id: str
    image_path: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
