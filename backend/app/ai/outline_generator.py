from typing import List
from .gemini_client import gemini_client
from .character_generator import generate_character_bible
from ..schemas.ai_schemas import ComicOutline, PanelOutline, DialogueItem, CharacterProfile
from ..utils.logger import get_logger

logger = get_logger("outline_generator")

def determine_panel_count(count_input: str, story_prompt: str) -> int:
    """Parse or resolve AUTO panel count between 4 and 10."""
    if count_input.upper() == "AUTO":
        length = len(story_prompt.split())
        if length < 15:
            return 4
        elif length < 35:
            return 6
        elif length < 60:
            return 8
        else:
            return 10
    try:
        val = int(count_input)
        if val in [4, 6, 8, 10]:
            return val
        return max(4, min(10, val))
    except ValueError:
        return 6

def generate_comic_outline(
    title: str,
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
    panel_count_setting: str
) -> ComicOutline:
    """Generate structured comic outline containing panel scripts and visual prompts."""
    panel_count = determine_panel_count(panel_count_setting, story_prompt)
    logger.info(f"Generating outline for '{title}' with {panel_count} panels.")

    char_bible = generate_character_bible(character_name, story_prompt, setting, art_style)

    if gemini_client.is_configured:
        prompt = (
            f"Generate a complete structured comic outline with exactly {panel_count} panels.\n"
            f"Title: {title}\n"
            f"Story Prompt: {story_prompt}\n"
            f"Main Character: {char_bible.name} - {char_bible.appearance}\n"
            f"Setting: {setting}\n"
            f"Tone: {tone}\n"
            f"Art Style: {art_style}\n\n"
            f"Requirements:\n"
            f"- Create exactly {panel_count} sequential panels.\n"
            f"- Each panel MUST include title, scene_description, action, emotion, camera_angle, background, lighting, narration, dialogue, and a standalone image_prompt.\n"
            f"- Keep dialogue short and punchy so it fits in speech bubbles.\n"
            f"- Make sure the image_prompt describes the visual scene without requesting speech bubbles or text overlay inside the image."
        )
        try:
            outline = gemini_client.generate_structured(prompt, ComicOutline)
            if len(outline.panels) == panel_count:
                return outline
            logger.warning(f"Generated panel count ({len(outline.panels)}) mismatch with requested ({panel_count}). Adjusting.")
        except Exception as e:
            logger.warning(f"Gemini outline generation failed: {e}. Utilizing fallback outline generator.")

    # Intelligent Fallback Outline Generator for robust offline / mock / fallback execution
    fallback_panels: List[PanelOutline] = []
    
    story_beats = _build_story_beats(panel_count, character_name, story_prompt, setting, tone)

    for i, beat in enumerate(story_beats, start=1):
        dialogue_items = []
        if beat["dialogue_text"]:
            dialogue_items.append(DialogueItem(
                speaker=character_name,
                text=beat["dialogue_text"],
                emotion=beat["emotion"],
                bubble_type=beat.get("bubble_type", "speech")
            ))

        img_prompt = (
            f"Comic art in {art_style} style. {char_bible.appearance}, wearing {char_bible.clothing}. "
            f"Scene: {beat['scene']}. Background: {setting}, {beat['lighting']}. "
            f"Camera angle: {beat['camera']}. Mood: {tone}. High visual detail, clean layout, no text."
        )

        fallback_panels.append(PanelOutline(
            panel=i,
            title=beat["title"],
            scene_description=beat["scene"],
            characters_present=[character_name],
            action=beat["action"],
            emotion=beat["emotion"],
            camera_angle=beat["camera"],
            background=setting,
            lighting=beat["lighting"],
            narration=beat["narration"],
            dialogue=dialogue_items,
            sound_effect=beat.get("sound_effect", ""),
            image_prompt=img_prompt
        ))

    return ComicOutline(
        title=title,
        story_concept=story_prompt,
        characters=[char_bible],
        panels=fallback_panels
    )

def _build_story_beats(count: int, name: str, story: str, setting: str, tone: str) -> List[dict]:
    """Generates rich sequential story beats tailored to requested panel count."""
    templates = {
        4: [
            {"title": "The Awakening", "scene": f"{name} stands at the boundary of {setting}, gazing at the unknown horizon.", "action": f"{name} steps forward curiously.", "emotion": "hopeful", "camera": "Wide Shot", "lighting": "Golden sunrise light", "narration": f"Deep within {setting}, a new adventure begins for {name}.", "dialogue_text": "The wind whispers of ancient secrets...", "bubble_type": "thought"},
            {"title": "The Discovery", "scene": f"{name} discovers a glowing magical artifact embedded in a stone altar.", "action": f"{name} reaches out towards the artifact.", "emotion": "astonished", "camera": "Medium Close Up", "lighting": "Mystical blue glow", "narration": "A sudden discovery changes everything.", "dialogue_text": "What is this power?", "bubble_type": "speech"},
            {"title": "The Conflict", "scene": f"The ground trembles as a shadow guardian looms over {name}.", "action": f"{name} braces for action, standing firm.", "emotion": "determined", "camera": "Low Angle Shot", "lighting": "Dramatic dark shadows with orange sparks", "narration": "Danger strikes without warning!", "dialogue_text": "I won't back down!", "bubble_type": "shout", "sound_effect": "ROAR!"},
            {"title": "Triumph & Beyond", "scene": f"{name} unleashes the light from the artifact, banishing the shadows.", "action": f"{name} stands victorious under bright clear skies.", "emotion": "triumphant", "camera": "Heroic Eye Level Shot", "lighting": "Radiant sunbeams", "narration": "With courage and determination, light restores the realm.", "dialogue_text": "The story has only just begun.", "bubble_type": "speech"}
        ],
        6: [
            {"title": "Into the Unknown", "scene": f"{name} enters the heart of {setting}.", "action": f"{name} walks carefully along an ancient path.", "emotion": "curious", "camera": "Establishing Wide Shot", "lighting": "Dappled forest sunlight", "narration": f"It started on a quiet morning in {setting}.", "dialogue_text": "Every path leads to a story.", "bubble_type": "thought"},
            {"title": "Unexpected Sign", "scene": f"{name} notices glowing footprints leading deeper into the sanctuary.", "action": f"{name} kneels down to examine the marks.", "emotion": "intrigued", "camera": "Close Up", "lighting": "Soft luminescent green", "narration": "A subtle clue appears on the mossy ground.", "dialogue_text": "Fresh tracks... I'm not alone here.", "bubble_type": "whisper"},
            {"title": "The Hidden Chamber", "scene": f"{name} pushes past heavy vines into a majestic ruined temple.", "action": f"{name} gasps at the vast glowing chamber.", "emotion": "awed", "camera": "Wide High Angle", "lighting": "Ethereal crystal light", "narration": "Beneath the canopy lies a forgotten relic of power.", "dialogue_text": "Incredible... it's really real!", "bubble_type": "speech"},
            {"title": "Shadow Intrusion", "scene": f"Dark swirling tendrils emerge from the shadows, blocking the exit.", "action": f"{name} leaps back defensively.", "emotion": "alert", "camera": "Dynamic Dutch Angle", "lighting": "Harsh purple neon rim light", "narration": "Suddenly, dark shadows close in!", "dialogue_text": "Who goes there?!", "bubble_type": "shout", "sound_effect": "WHOOSH!"},
            {"title": "Clash of Will", "scene": f"{name} channels energy from the central crystal to form a glowing barrier.", "action": f"{name} raises hands, shielding the realm.", "emotion": "fierce", "camera": "Medium Action Shot", "lighting": "Blinding golden surge", "narration": "Surging courage ignites the dormant magic.", "dialogue_text": "Light banishes the darkness!", "bubble_type": "shout", "sound_effect": "KABOOM!"},
            {"title": "A New Dawn", "scene": f"{name} stands atop the temple steps as peace settles over {setting}.", "action": f"{name} smiles warmly into the distance.", "emotion": "serene", "camera": "Heroic Medium Shot", "lighting": "Golden twilight glow", "narration": f"The realm is safe, and {name}'s legacy is carved in legend.", "dialogue_text": "Onto the next horizon.", "bubble_type": "speech"}
        ]
    }

    if count in templates:
        return templates[count]

    # Dynamically expand for 8 or 10 panels
    base = templates[6]
    extra_count = count - 6
    beats = list(base)
    for k in range(extra_count):
        beats.insert(3 + k, {
            "title": f"Chapter Step {k+1}",
            "scene": f"{name} encounters a secondary obstacle in {setting}.",
            "action": f"{name} solves a puzzling dilemma.",
            "emotion": "focused",
            "camera": "Medium Shot",
            "lighting": "Atmospheric twilight",
            "narration": f"Every challenge tests {name}'s resolve.",
            "dialogue_text": "I have to stay sharp!",
            "bubble_type": "speech"
        })
    return beats
