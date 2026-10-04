from sqlalchemy.orm import Session
from ..models.project import Project
from ..models.character import Character
from ..models.panel import Panel
from ..ai import (
    analyze_story,
    generate_comic_outline,
    build_visual_prompt,
    build_continuity_context,
    get_image_provider,
    regenerate_panel_story
)
from ..services.storage_service import storage_service
from ..utils.logger import get_logger

logger = get_logger("generation_orchestrator")

class GenerationOrchestrator:
    def run_full_pipeline(self, db: Session, project: Project) -> Project:
        """Executes full end-to-end comic generation pipeline."""
        try:
            logger.info(f"Starting pipeline for project {project.id}: '{project.title}'")
            project.status = "generating"
            project.error_message = None
            db.commit()

            # Stage A: Story Analysis
            analysis = analyze_story(
                original_prompt=project.original_prompt,
                character_name=project.character_name,
                setting=project.setting,
                tone=project.tone,
                art_style=project.art_style
            )
            project.title = analysis["title"]
            db.commit()

            # Stage B: Outline & Character Bible
            panel_count_setting = str(project.panel_count)
            outline = generate_comic_outline(
                title=project.title,
                story_prompt=project.original_prompt,
                character_name=project.character_name,
                setting=project.setting,
                tone=project.tone,
                art_style=project.art_style,
                panel_count_setting=panel_count_setting
            )

            # Save Characters
            # Clear existing characters if re-running
            db.query(Character).filter(Character.project_id == project.id).delete()
            for char_prof in outline.characters:
                char_entry = Character(
                    project_id=project.id,
                    name=char_prof.name,
                    description=char_prof.description,
                    appearance=char_prof.appearance,
                    personality=char_prof.personality,
                    clothing=char_prof.clothing,
                    colors=char_prof.colors
                )
                db.add(char_entry)
            db.commit()

            # Save & Generate Panels
            db.query(Panel).filter(Panel.project_id == project.id).delete()
            
            image_provider = get_image_provider()
            
            panels_created = []
            for p_outline in outline.panels:
                img_path = storage_service.get_panel_image_path(project.id, p_outline.panel)
                
                # Dialogue formatting
                dialogue_data = [d.model_dump() for d in p_outline.dialogue]

                panel_entry = Panel(
                    project_id=project.id,
                    panel_number=p_outline.panel,
                    title=p_outline.title,
                    scene_description=p_outline.scene_description,
                    narration=p_outline.narration or "",
                    dialogue=dialogue_data,
                    speaker=p_outline.dialogue[0].speaker if p_outline.dialogue else project.character_name,
                    sound_effect=p_outline.sound_effect or "",
                    image_prompt=p_outline.image_prompt,
                    image_path=f"/api/projects/{project.id}/panels/{p_outline.panel}/image",
                    status="pending"
                )
                db.add(panel_entry)
                panels_created.append((panel_entry, img_path, p_outline.image_prompt, p_outline.title))

            db.commit()

            # Generate artwork for each panel using image provider
            for panel_entry, img_path, prompt, panel_title in panels_created:
                try:
                    image_provider.generate_image(
                        prompt=prompt,
                        output_path=img_path,
                        panel_number=panel_entry.panel_number,
                        title=panel_title,
                        art_style=project.art_style
                    )
                    panel_entry.status = "completed"
                except Exception as img_err:
                    logger.error(f"Image generation failed for panel {panel_entry.panel_number}: {img_err}")
                    panel_entry.status = "failed"
                db.commit()

            project.status = "completed"
            db.commit()
            db.refresh(project)
            logger.info(f"Pipeline completed successfully for project {project.id}")
            return project

        except Exception as pipeline_err:
            logger.error(f"Pipeline failed for project {project.id}: {pipeline_err}")
            project.status = "failed"
            project.error_message = str(pipeline_err)
            db.commit()
            return project

    def regenerate_single_panel_image(self, db: Session, panel: Panel) -> Panel:
        """Regenerate artwork for an individual panel."""
        project = panel.project
        img_path = storage_service.get_panel_image_path(project.id, panel.panel_number)
        image_provider = get_image_provider()

        prompt = panel.image_prompt or f"Comic artwork panel for {project.title}, panel {panel.panel_number}"
        image_provider.generate_image(
            prompt=prompt,
            output_path=img_path,
            panel_number=panel.panel_number,
            title=panel.title or f"Panel {panel.panel_number}",
            art_style=project.art_style
        )
        panel.status = "completed"
        db.commit()
        db.refresh(panel)
        return panel

    def regenerate_single_panel_story(self, db: Session, panel: Panel) -> Panel:
        """Regenerate dialogue and narration for an individual panel."""
        project = panel.project
        all_panels = db.query(Panel).filter(Panel.project_id == project.id).order_by(Panel.panel_number).all()

        prev_panel = next((p for p in all_panels if p.panel_number == panel.panel_number - 1), None)
        next_panel = next((p for p in all_panels if p.panel_number == panel.panel_number + 1), None)

        story_data = regenerate_panel_story(
            project_title=project.title,
            panel_number=panel.panel_number,
            total_panels=len(all_panels),
            scene_description=panel.scene_description or "",
            characters_present=[project.character_name],
            prev_summary=prev_panel.scene_description if prev_panel else "",
            next_summary=next_panel.scene_description if next_panel else ""
        )

        panel.narration = story_data["narration"]
        panel.dialogue = story_data["dialogue"]
        panel.sound_effect = story_data["sound_effect"]
        db.commit()
        db.refresh(panel)
        return panel

orchestrator = GenerationOrchestrator()
