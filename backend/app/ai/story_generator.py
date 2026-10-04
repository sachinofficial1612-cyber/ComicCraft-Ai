from typing import Dict, Any, List
from .gemini_client import gemini_client
from ..utils.logger import get_logger

logger = get_logger("story_generator")

def regenerate_panel_story(
    project_title: str,
    panel_number: int,
    total_panels: int,
    scene_description: str,
    characters_present: List[str],
    prev_summary: str = "",
    next_summary: str = ""
) -> Dict[str, Any]:
    """Regenerate dialogue and narration for a single panel while keeping story continuity."""
    if gemini_client.is_configured:
        prompt = (
            f"Regenerate dialogue and narration for Panel {panel_number} of {total_panels} in '{project_title}'.\n"
            f"Scene: {scene_description}\n"
            f"Characters: {', '.join(characters_present)}\n"
            f"Previous scene: {prev_summary}\n"
            f"Next scene: {next_summary}\n\n"
            "Return JSON with keys:\n"
            "- narration (string)\n"
            "- dialogue (list of dicts with speaker, text, emotion, bubble_type)\n"
            "- sound_effect (string)"
        )
        try:
            resp = gemini_client.generate_text(prompt)
            import json
            clean = gemini_client._extract_json(resp)
            parsed = json.loads(clean)
            return {
                "narration": parsed.get("narration", "The adventure continues..."),
                "dialogue": parsed.get("dialogue", []),
                "sound_effect": parsed.get("sound_effect", "")
            }
        except Exception as e:
            logger.warning(f"Regenerate story via Gemini failed: {e}. Using fallback.")

    speaker = characters_present[0] if characters_present else "Hero"
    return {
        "narration": f"In panel {panel_number}, the scene unfolds dramatically.",
        "dialogue": [{
            "speaker": speaker,
            "text": "We must press forward, whatever comes!",
            "emotion": "determined",
            "bubble_type": "speech"
        }],
        "sound_effect": "WHOOSH"
    }
