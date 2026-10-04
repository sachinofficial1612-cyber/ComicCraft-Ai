import os
from typing import List
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ..models.project import Project
from ..models.panel import Panel
from ..exporters.png_exporter import png_exporter
from ..services.storage_service import storage_service
from ..utils.logger import get_logger

logger = get_logger("pdf_exporter")

class PDFExporter:
    def export_comic_pdf(self, project: Project, panels: List[Panel]) -> str:
        """Generates a professional PDF comic book export with cover title page and composite comic pages."""
        # First generate composite PNG pages
        png_pages = png_exporter.export_comic_pngs(project, panels)
        
        pdf_filename = f"{project.title.replace(' ', '_')}_Comic.pdf"
        pdf_path = storage_service.get_export_path(project.id, pdf_filename)

        c = canvas.Canvas(pdf_path, pagesize=letter)
        pdf_w, pdf_h = letter  # 612 x 792 points

        # Draw Cover Page
        c.setFillColorRGB(0.06, 0.09, 0.16)  # Dark sleek cover
        c.rect(0, 0, pdf_w, pdf_h, fill=1, stroke=0)

        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(pdf_w / 2, pdf_h - 180, project.title.upper())

        c.setFont("Helvetica", 16)
        c.setFillColorRGB(0.8, 0.85, 0.95)
        c.drawCentredString(pdf_w / 2, pdf_h - 220, f"A COMICCRAFT ORIGINAL STORY")

        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(0.9, 0.7, 0.2)
        c.drawCentredString(pdf_w / 2, pdf_h - 260, f"ART STYLE: {project.art_style.upper()}")

        # Display first panel thumbnail on cover
        first_panel_path = storage_service.get_panel_image_path(project.id, 1)
        if os.path.exists(first_panel_path):
            try:
                c.drawImage(first_panel_path, (pdf_w - 320)/2, pdf_h - 600, width=320, height=240, preserveAspectRatio=True)
            except Exception as e:
                logger.warning(f"Failed to embed thumbnail on cover: {e}")

        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0.7, 0.7, 0.7)
        c.drawCentredString(pdf_w / 2, 50, f"Created with ComicCraft AI Story Creator")
        c.showPage()

        # Add Comic Pages
        for page_img_path in png_pages:
            c.drawImage(page_img_path, 0, 0, width=pdf_w, height=pdf_h, preserveAspectRatio=False)
            c.showPage()

        c.save()
        logger.info(f"Generated PDF export saved to {pdf_path}")
        return pdf_path

pdf_exporter = PDFExporter()
