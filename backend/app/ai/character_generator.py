from typing import Dict, Any
from .gemini_client import gemini_client
from ..schemas.ai_schemas import CharacterProfile
from ..utils.logger import get_logger

logger = get_logger("character_generator")

def generate_character_bible(name: str, story_prompt: str, setting: str, art_style: str) -> CharacterProfile:
    """Generate a detailed visual and personality character bible."""
    if gemini_client.is_configured:
        prompt = (
            f"Create a detailed character bible for character '{name}'.\n"
            f"Story context: {story_prompt}\n"
            f"Setting: {setting}\n"
            f"Art Style: {art_style}\n\n"
            "Provide specific species/body, facial traits, hair/fur, clothing style, exact color palette, and personality."
        )
        try:
            return gemini_client.generate_structured(prompt, CharacterProfile)
        except Exception as e:
            logger.warning(f"Gemini character generation failed: {e}. Using fallback generator.")

    # Fallback Character Bible Generator
    desc = f"{name} is the main protagonist of the story."
    appearance = f"{name} has expressive features, distinctive visual style suitable for {art_style} art, with vibrant, iconic design."
    personality = "Brave, curious, resilient, and resourceful."
    clothing = "Traveler gear with signature cape/jacket and functional boots."
    colors = "Primary colors with contrasting accents."

    if "fox" in (name + story_prompt).lower():
        appearance = "A vibrant red fox with bright amber eyes, sleek auburn fur, bushy white-tipped tail, and sharp inquisitive ears."
        clothing = "A weathered leather adventurer satchel and a warm emerald green travel cloak."
        colors = "Auburn orange, white, emerald green, and warm amber."
        personality = "Clever, quick-witted, adventurous, and protective of friends."

    return CharacterProfile(
        name=name,
        description=desc,
        appearance=appearance,
        personality=personality,
        clothing=clothing,
        colors=colors
    )
