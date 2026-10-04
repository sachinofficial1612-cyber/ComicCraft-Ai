import os
import io
import math
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont
from .gemini_client import gemini_client
from ..config import settings
from ..utils.logger import get_logger

logger = get_logger("image_generator")

class ImageProvider(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, output_path: str, panel_number: int, title: str = "", art_style: str = "Comic Book") -> str:
        pass

class GeminiImageProvider(ImageProvider):
    def generate_image(self, prompt: str, output_path: str, panel_number: int, title: str = "", art_style: str = "Comic Book") -> str:
        if not gemini_client.is_configured:
            raise ValueError("Gemini API key is not configured.")

        try:
            # Use google-genai SDK models.generate_images if available
            from google.genai import types
            logger.info(f"Generating image with Gemini model {gemini_client.image_model} for panel {panel_number}")
            
            result = gemini_client._client.models.generate_images(
                model=gemini_client.image_model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="4:3",
                    output_mime_type="image/png"
                )
            )
            if result.generated_images:
                image_bytes = result.generated_images[0].image.image_bytes
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(image_bytes)
                logger.info(f"Saved generated image to {output_path}")
                return output_path
        except Exception as e:
            logger.warning(f"Gemini image generation failed: {e}. Falling back to canvas artwork generator.")
            fallback = FallbackImageProvider()
            return fallback.generate_image(prompt, output_path, panel_number, title, art_style)

        raise RuntimeError("No image returned from Gemini.")

class FallbackImageProvider(ImageProvider):
    """Generates rich, stylized comic artwork placeholders when AI image generation API is offline or unconfigured."""
    def generate_image(self, prompt: str, output_path: str, panel_number: int, title: str = "", art_style: str = "Comic Book") -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        width, height = 800, 600
        image = Image.new("RGB", (width, height), color=(20, 24, 33))
        draw = ImageDraw.Draw(image)

        # Style palette mapping
        style_palettes = {
            "realistic": ((15, 23, 42), (30, 58, 138), (239, 68, 68)),
            "cartoon": ((254, 240, 138), (249, 115, 22), (236, 72, 153)),
            "anime": ((192, 132, 252), (99, 102, 241), (244, 114, 182)),
            "manga": ((245, 245, 245), (100, 100, 100), (20, 20, 20)),
            "watercolor": ((207, 250, 254), (165, 243, 252), (14, 165, 233)),
            "cinematic": ((10, 15, 26), (30, 41, 59), (245, 158, 11)),
            "3d": ((30, 27, 75), (67, 56, 202), (99, 102, 241)),
            "comic book": ((23, 37, 84), (29, 78, 216), (234, 179, 8)),
            "noir": ((10, 10, 10), (50, 50, 50), (200, 200, 200)),
            "children's illustration": ((254, 226, 226), (251, 146, 60), (74, 222, 128))
        }

        bg_col, mid_col, accent_col = style_palettes.get(art_style.lower(), style_palettes["comic book"])

        # Draw gradient sky / background
        for y in range(height):
            r = int(bg_col[0] + (mid_col[0] - bg_col[0]) * (y / height))
            g = int(bg_col[1] + (mid_col[1] - bg_col[1]) * (y / height))
            b = int(bg_col[2] + (mid_col[2] - bg_col[2]) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Draw distant horizon / mountain silhouettes
        points = [(0, height)]
        step = 40
        for x in range(0, width + step, step):
            h_y = int(height * 0.55 + math.sin(x * 0.015 + panel_number) * 40)
            points.append((x, h_y))
        points.append((width, height))
        draw.polygon(points, fill=(int(bg_col[0]*0.5), int(bg_col[1]*0.5), int(bg_col[2]*0.5)))

        # Draw sun / moon glow
        sun_x, sun_y = width - 180, 140
        draw.ellipse([sun_x - 60, sun_y - 60, sun_x + 60, sun_y + 60], fill=accent_col)

        # Draw foreground character silhouette
        char_x = int(width * 0.35)
        char_y = int(height * 0.5)
        draw.ellipse([char_x - 45, char_y - 80, char_x + 45, char_y + 10], fill=(15, 23, 42))  # Torso/Head
        draw.polygon([(char_x - 35, char_y - 40), (char_x + 35, char_y - 40), (char_x + 55, char_y + 120), (char_x - 55, char_y + 120)], fill=(15, 23, 42)) # Cloak

        # Draw comic border frame
        draw.rectangle([10, 10, width - 10, height - 10], outline=(255, 255, 255), width=6)
        draw.rectangle([16, 16, width - 16, height - 16], outline=(0, 0, 0), width=3)

        # Panel number badge
        badge_box = [30, 30, 160, 75]
        draw.rectangle(badge_box, fill=(0, 0, 0, 200), outline=(255, 255, 255), width=2)
        
        try:
            font = ImageFont.truetype("arial.ttf", 22)
            small_font = ImageFont.truetype("arial.ttf", 14)
        except Exception:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        draw.text((45, 42), f"PANEL {panel_number}", fill=(255, 255, 255), font=font)

        # Watermark/Style Tag at bottom
        draw.text((30, height - 45), f"ART STYLE: {art_style.upper()} | AI GENERATED ARTWORK", fill=(255, 255, 255), font=small_font)

        image.save(output_path, "PNG")
        logger.info(f"Generated fallback comic artwork saved to {output_path}")
        return output_path

def get_image_provider() -> ImageProvider:
    provider_name = settings.IMAGE_PROVIDER.lower()
    if provider_name == "gemini" and gemini_client.is_configured:
        return GeminiImageProvider()
    return FallbackImageProvider()
