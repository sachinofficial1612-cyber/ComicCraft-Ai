from typing import Dict, Any, List
from ..schemas.ai_schemas import CharacterProfile

def build_visual_prompt(
    art_style: str,
    character_bibles: List[CharacterProfile],
    scene_description: str,
    action: str,
    emotion: str,
    camera_angle: str,
    background: str,
    lighting: str,
    continuity_context: str = ""
) -> str:
    """Build a detailed visual prompt for Gemini image generation without text overlays."""
    char_descriptions = []
    for char in character_bibles:
        char_descriptions.append(
            f"Character '{char.name}': {char.appearance}. Clothing: {char.clothing}. Color palette: {char.colors}."
        )
    combined_chars = " ".join(char_descriptions)

    prompt = (
        f"Comic book panel illustration in {art_style} style. "
        f"{combined_chars} "
        f"Scene action: {action}. Emotion/Expression: {emotion}. "
        f"Environment & Background: {background}. {scene_description}. "
        f"Camera framing: {camera_angle}. Lighting: {lighting}. "
        f"{continuity_context} "
        f"Visual style: High detail, crisp lines, rich colors, professional comic publishing quality. "
        f"DO NOT render speech bubbles, dialogue text, sound effects, or captions into the image artwork."
    )
    return prompt.strip()
