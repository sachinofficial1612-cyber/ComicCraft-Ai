from .gemini_client import gemini_client
from ..utils.logger import get_logger

logger = get_logger("story_analyzer")

def analyze_story(original_prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> dict:
    """Analyze story prompt to extract title, concept, theme, and key beats."""
    if gemini_client.is_configured:
        prompt = (
            f"Analyze comic story prompt:\n"
            f"Prompt: {original_prompt}\n"
            f"Character: {character_name}\n"
            f"Setting: {setting}\n"
            f"Tone: {tone}\n"
            f"Art Style: {art_style}\n\n"
            "Generate a JSON object with keys: title, concept, genre, key_beats (list of strings)."
        )
        try:
            resp_text = gemini_client.generate_text(prompt)
            import json
            clean_json = gemini_client._extract_json(resp_text)
            parsed = json.loads(clean_json)
            return {
                "title": parsed.get("title", f"The Tale of {character_name}"),
                "concept": parsed.get("concept", original_prompt),
                "genre": parsed.get("genre", "Adventure"),
                "key_beats": parsed.get("key_beats", [])
            }
        except Exception as e:
            logger.warning(f"Story analyzer Gemini call failed: {e}. Using intelligent fallback.")

    # Fallback title & concept formatting
    clean_title = original_prompt.strip().split(".")[0].title()
    if len(clean_title) > 40:
        clean_title = f"The Quest of {character_name}"
    return {
        "title": clean_title if clean_title else f"The Legend of {character_name}",
        "concept": original_prompt,
        "genre": "Adventure",
        "key_beats": ["Beginning introduction", "Rising action discovery", "Climax challenge", "Resolution outcome"]
    }
