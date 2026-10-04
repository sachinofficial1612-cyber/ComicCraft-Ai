from backend.app.schemas.ai_schemas import ComicOutline, PanelOutline, DialogueItem, CharacterProfile

def test_comic_outline_schema_validation():
    char = CharacterProfile(
        name="Free",
        description="A red fox",
        appearance="Auburn fur, bright eyes",
        personality="Brave",
        clothing="Green cloak",
        colors="Auburn, emerald green"
    )
    dialogue = DialogueItem(speaker="Free", text="Hello world!", emotion="happy", bubble_type="speech")
    panel = PanelOutline(
        panel=1,
        title="Beginning",
        scene_description="Forest entrance",
        characters_present=["Free"],
        action="Walks in",
        emotion="curious",
        camera_angle="Wide Shot",
        background="Forest",
        lighting="Sunlight",
        narration="The adventure begins.",
        dialogue=[dialogue],
        image_prompt="Comic panel of a red fox in an enchanted forest."
    )
    outline = ComicOutline(
        title="Test Comic",
        story_concept="A test story concept",
        characters=[char],
        panels=[panel]
    )
    assert outline.title == "Test Comic"
    assert len(outline.panels) == 1
    assert outline.panels[0].dialogue[0].speaker == "Free"
