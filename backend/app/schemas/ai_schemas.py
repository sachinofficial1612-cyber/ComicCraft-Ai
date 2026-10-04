from typing import List, Optional
from pydantic import BaseModel, Field

class DialogueItem(BaseModel):
    speaker: str = Field(description="Character speaking")
    text: str = Field(description="Dialogue text (concise, fit for speech bubble)")
    emotion: str = Field(default="neutral", description="Emotion/expression of speaker")
    bubble_type: str = Field(default="speech", description="Bubble type: speech, thought, shout, whisper")

class PanelOutline(BaseModel):
    panel: int = Field(description="Panel sequence number")
    title: str = Field(description="Short panel title")
    scene_description: str = Field(description="Detailed visual environment and scene description")
    characters_present: List[str] = Field(default_factory=list, description="Names of characters in panel")
    action: str = Field(description="Action happening in panel")
    emotion: str = Field(description="Dominant mood/emotion")
    camera_angle: str = Field(default="Medium Shot", description="Camera framing (Wide Shot, Close Up, Low Angle, etc.)")
    background: str = Field(default="Detailed background", description="Background elements")
    lighting: str = Field(default="Cinematic lighting", description="Lighting style")
    narration: Optional[str] = Field(default="", description="Narrative caption text")
    dialogue: List[DialogueItem] = Field(default_factory=list, description="Dialogue lines for speech bubbles")
    sound_effect: Optional[str] = Field(default="", description="Sound effect text e.g. WHOOSH, BOOM")
    image_prompt: str = Field(description="Complete standalone visual prompt for image generation model")

class CharacterProfile(BaseModel):
    name: str
    description: str
    appearance: str
    personality: str
    clothing: str
    colors: str

class ComicOutline(BaseModel):
    title: str = Field(description="Title of the comic")
    story_concept: str = Field(description="Overview of the story")
    characters: List[CharacterProfile] = Field(default_factory=list, description="Character bibles")
    panels: List[PanelOutline] = Field(description="List of planned comic panels")
