from typing import Optional
from pydantic import BaseModel, ConfigDict

class CharacterBase(BaseModel):
    name: str
    description: Optional[str] = None
    appearance: Optional[str] = None
    personality: Optional[str] = None
    clothing: Optional[str] = None
    colors: Optional[str] = None
    reference_image_path: Optional[str] = None

class CharacterCreate(CharacterBase):
    pass

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    appearance: Optional[str] = None
    personality: Optional[str] = None
    clothing: Optional[str] = None
    colors: Optional[str] = None
    reference_image_path: Optional[str] = None

class CharacterResponse(CharacterBase):
    id: str
    project_id: str

    model_config = ConfigDict(from_attributes=True)
