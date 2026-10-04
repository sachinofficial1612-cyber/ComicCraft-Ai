import os
from typing import List
from PIL import Image, ImageDraw, ImageFont
from ..models.project import Project
from ..models.panel import Panel
from ..generators.comic_composer import composer
from ..services.storage_service import storage_service
from ..utils.logger import get_logger

logger = get_logger("png_exporter")

class PNGExporter:
    def export_comic_pngs(self, project: Project, panels: List[Panel]) -> List[str]:
        """Generates rendered composite PNG comic pages complete with narration boxes and speech bubbles."""
        page_layouts = composer.calculate_page_layout(len(panels))
        output_files = []

        for p_info in page_layouts:
            page_num = p_info["page"]
            cols, rows = p_info["grid"]
            start_p = p_info["panels_start"]
            end_p = p_info["panels_end"]
            page_panels = [p for p in panels if start_p <= p.panel_number <= end_p]

            page_img = self._composite_page(project, page_panels, cols, rows, page_num, len(page_layouts))
            
            out_path = storage_service.get_export_path(project.id, f"{project.title}_page_{page_num}.png")
            page_img.save(out_path, "PNG")
            output_files.append(out_path)

        return output_files

    def _composite_page(self, project: Project, page_panels: List[Panel], cols: int, rows: int, page_num: int, total_pages: int) -> Image.Image:
        page_w, page_h = 1600, 2200
        margin = 60
        header_h = 140
        footer_h = 60

        page = Image.new("RGB", (page_w, page_h), color=(255, 255, 255))
        draw = ImageDraw.Draw(page)

        # Draw Header
        draw.rectangle([0, 0, page_w, header_h], fill=(15, 23, 42))
        try:
            title_font = ImageFont.truetype("arial.ttf", 44)
            sub_font = ImageFont.truetype("arial.ttf", 22)
            body_font = ImageFont.truetype("arial.ttf", 18)
            bold_font = ImageFont.truetype("arialbd.ttf", 20)
        except Exception:
            title_font = small_font = body_font = bold_font = ImageFont.load_default()

        draw.text((margin, 35), project.title.upper(), fill=(255, 255, 255), font=title_font)
        draw.text((margin, 90), f"ART STYLE: {project.art_style.upper()}  |  CHARACTER: {project.character_name.upper()}", fill=(203, 213, 225), font=sub_font)

        # Calculate grid cell dimensions
        avail_w = page_w - (2 * margin) - ((cols - 1) * 30)
        avail_h = page_h - header_h - footer_h - (2 * margin) - ((rows - 1) * 30)
        cell_w = avail_w // cols
        cell_h = avail_h // rows

        for idx, panel in enumerate(page_panels):
            r = idx // cols
            c = idx % cols
            x = margin + c * (cell_w + 30)
            y = header_h + margin + r * (cell_h + 30)

            # Load panel image if exists
            panel_img_disk_path = storage_service.get_panel_image_path(project.id, panel.panel_number)
            if os.path.exists(panel_img_disk_path):
                try:
                    p_img = Image.open(panel_img_disk_path).convert("RGB")
                    p_img = p_img.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
                    page.paste(p_img, (x, y))
                except Exception as e:
                    logger.warning(f"Could not render panel image for panel {panel.panel_number}: {e}")
                    draw.rectangle([x, y, x + cell_w, y + cell_h], fill=(220, 220, 230))
            else:
                draw.rectangle([x, y, x + cell_w, y + cell_h], fill=(240, 240, 245))

            # Draw outer comic border
            draw.rectangle([x, y, x + cell_w, y + cell_h], outline=(0, 0, 0), width=5)

            # Panel Badge
            draw.rectangle([x + 10, y + 10, x + 110, y + 40], fill=(0, 0, 0), outline=(255, 255, 255), width=2)
            draw.text((x + 20, y + 15), f"PANEL {panel.panel_number}", fill=(255, 255, 255), font=bold_font)

            # Draw Narration Box at top
            if panel.narration:
                narr_text = panel.narration[:120] + ("..." if len(panel.narration) > 120 else "")
                narr_h = 55
                draw.rectangle([x + 10, y + cell_h - narr_h - 10, x + cell_w - 10, y + cell_h - 10], fill=(254, 240, 138), outline=(0, 0, 0), width=3)
                draw.text((x + 20, y + cell_h - narr_h), f"NARRATION: {narr_text}", fill=(0, 0, 0), font=body_font)

            # Draw Speech Bubbles
            if panel.dialogue and isinstance(panel.dialogue, list):
                bub_y = y + 55
                for d in panel.dialogue[:2]:  # render up to 2 bubbles per panel
                    if isinstance(d, dict) and d.get("text"):
                        spk = d.get("speaker", "Hero")
                        txt = d.get("text", "")
                        bub_type = d.get("bubble_type", "speech")

                        bub_w = min(cell_w - 40, 340)
                        bub_h = 60
                        bx = x + 20
                        by = bub_y

                        # Draw bubble box / oval
                        if bub_type == "thought":
                            draw.ellipse([bx, by, bx + bub_w, by + bub_h], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
                        elif bub_type == "shout":
                            draw.rectangle([bx, by, bx + bub_w, by + bub_h], fill=(254, 202, 202), outline=(220, 38, 38), width=4)
                        else: # speech
                            draw.rounded_rectangle([bx, by, bx + bub_w, by + bub_h], radius=15, fill=(255, 255, 255), outline=(0, 0, 0), width=3)

                        draw.text((bx + 15, by + 10), f"{spk}: \"{txt}\"", fill=(0, 0, 0), font=body_font)
                        bub_y += bub_h + 15

        # Draw Footer
        draw.rectangle([0, page_h - footer_h, page_w, page_h], fill=(15, 23, 42))
        draw.text((margin, page_h - 42), f"COMICCRAFT AI STORY CREATOR  |  PAGE {page_num} OF {total_pages}", fill=(255, 255, 255), font=sub_font)

        return page

png_exporter = PNGExporter()
