from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path
from typing import Protocol

from PIL import Image, ImageDraw, ImageFont

from app.config import settings
from app.ai.gemini_client import gemini_client

logger = logging.getLogger(__name__)


class ImageProvider(Protocol):
    def generate_image(
        self,
        prompt: str,
        output_path: str | Path,
        panel_number: int = 1,
        title: str = "",
        art_style: str = "Comic Book",
    ) -> str:
        ...


def _safe_name(prompt: str, panel_number: int = 1) -> str:
    """Create a safe deterministic filename."""

    slug = re.sub(
        r"[^a-zA-Z0-9]+",
        "-",
        prompt.lower(),
    ).strip("-")

    slug = slug[:55] or "panel"

    digest = hashlib.sha1(
        prompt.encode("utf-8")
    ).hexdigest()[:10]

    return f"panel-{panel_number}-{slug}-{digest}.png"


def _ensure_output_directory(
    output_path: str | Path,
) -> Path:
    """Make sure the output directory exists."""

    path = Path(output_path)

    if path.suffix.lower() != ".png":
        path = path.with_suffix(".png")

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def _load_font(size: int = 28):
    """Load a reasonable font on Windows/Linux/macOS."""

    candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibri.ttf"),
        Path(
            "/usr/share/fonts/truetype/dejavu/"
            "DejaVuSans.ttf"
        ),
        Path(
            "/usr/share/fonts/truetype/liberation2/"
            "LiberationSans-Regular.ttf"
        ),
    ]

    for font_path in candidates:
        try:
            if font_path.exists():
                return ImageFont.truetype(
                    str(font_path),
                    size=size,
                )
        except Exception:
            continue

    return ImageFont.load_default()


def _placeholder(
    prompt: str,
    output_path: str | Path,
    panel_number: int = 1,
    title: str = "",
) -> str:
    """
    Generate a local fallback image.

    This is only used when an external image provider fails.
    """

    output = _ensure_output_directory(output_path)

    width = 1024
    height = 768

    image = Image.new(
        "RGB",
        (width, height),
        (18, 32, 58),
    )

    draw = ImageDraw.Draw(image)

    # Sky
    draw.rectangle(
        [0, 0, width, height // 2],
        fill=(22, 52, 92),
    )

    # Sun
    draw.ellipse(
        [820, 80, 920, 180],
        fill=(255, 70, 70),
    )

    # Mountains
    draw.polygon(
        [
            (0, 500),
            (180, 420),
            (300, 470),
            (470, 350),
            (620, 470),
            (760, 390),
            (900, 470),
            (1024, 410),
            (1024, 768),
            (0, 768),
        ],
        fill=(8, 17, 30),
    )

    # Character silhouette
    draw.ellipse(
        [465, 245, 535, 315],
        fill=(5, 15, 27),
    )

    draw.polygon(
        [
            (475, 310),
            (525, 310),
            (555, 520),
            (445, 520),
        ],
        fill=(5, 15, 27),
    )

    # Border
    draw.rectangle(
        [8, 8, width - 8, height - 8],
        outline=(245, 245, 245),
        width=5,
    )

    font = _load_font(24)

    draw.text(
        (30, 30),
        "FALLBACK ARTWORK",
        fill=(255, 255, 255),
        font=font,
    )

    draw.text(
        (30, 65),
        f"PANEL {panel_number}",
        fill=(255, 255, 255),
        font=font,
    )

    small_font = _load_font(18)

    draw.text(
        (25, height - 40),
        "AI IMAGE PROVIDER UNAVAILABLE",
        fill=(220, 220, 220),
        font=small_font,
    )

    image.save(
        output,
        format="PNG",
        optimize=True,
    )

    logger.warning(
        "Fallback artwork created at %s",
        output,
    )

    return str(output)


class HuggingFaceImageProvider:
    """
    Image generation provider using Hugging Face
    Inference Providers.

    Default model:

        black-forest-labs/FLUX.1-schnell
    """

    def __init__(
        self,
        token: str | None = None,
        model: str | None = None,
        provider: str | None = None,
    ):
        try:
            from huggingface_hub import InferenceClient
        except ImportError as exc:
            raise RuntimeError(
                "huggingface_hub is not installed. "
                "Run: pip install huggingface_hub"
            ) from exc

        self.token = (
            token
            or getattr(settings, "HF_TOKEN", "")
        )

        self.model = (
            model
            or getattr(
                settings,
                "HF_IMAGE_MODEL",
                "black-forest-labs/FLUX.1-schnell",
            )
        )

        self.provider = (
            provider
            or getattr(
                settings,
                "HF_IMAGE_PROVIDER",
                "auto",
            )
        )

        if not self.token:
            raise RuntimeError(
                "HF_TOKEN is not configured."
            )

        logger.info(
            "Initializing Hugging Face image provider: "
            "model=%s provider=%s",
            self.model,
            self.provider,
        )

        self.client = InferenceClient(
            provider=self.provider,
            api_key=self.token,
        )

    def generate_image(
        self,
        prompt: str,
        output_path: str | Path,
        panel_number: int = 1,
        title: str = "",
        art_style: str = "Comic Book",
    ) -> str:
        """
        Generate a real AI image using Hugging Face FLUX.
        """

        output = _ensure_output_directory(
            output_path
        )

        style = (
            str(art_style).strip()
            if art_style
            else "Comic Book"
        )

        panel_title = (
            str(title).strip()
            if title
            else f"Panel {panel_number}"
        )

        final_prompt = (
            "Create a high-quality illustrated comic "
            "book panel.\n\n"
            f"ART STYLE: {style}\n"
            f"PANEL: {panel_number}\n"
            f"TITLE: {panel_title}\n\n"
            "IMPORTANT VISUAL REQUIREMENTS:\n"
            "- Show the actual story scene described below.\n"
            "- Use clearly visible characters.\n"
            "- Use expressive facial expressions and poses.\n"
            "- Use detailed environments.\n"
            "- Use cinematic composition.\n"
            "- Use professional digital comic artwork.\n"
            "- Use coherent anatomy.\n"
            "- Make the main action visually obvious.\n"
            "- Do not create a generic landscape.\n"
            "- Do not create an empty scene.\n"
            "- Do not add captions.\n"
            "- Do not add speech bubbles.\n"
            "- Do not add written dialogue.\n"
            "- Do not add watermarks.\n"
            "- Do not add logos.\n"
            "- Do not add random text.\n\n"
            "STORY SCENE:\n"
            f"{prompt}"
        )

        logger.info(
            "Generating AI artwork with Hugging Face "
            "for panel %s: %s",
            panel_number,
            output,
        )

        try:
            image = self.client.text_to_image(
                prompt=final_prompt,
                model=self.model,
                width=1024,
                height=768,
            )
        except Exception as exc:
            logger.exception(
                "Hugging Face image generation failed "
                "for panel %s: %s",
                panel_number,
                exc,
            )
            raise

        if image is None:
            raise RuntimeError(
                "Hugging Face returned no image."
            )

        if not isinstance(image, Image.Image):
            raise RuntimeError(
                "Hugging Face returned an unexpected "
                f"image type: {type(image)}"
            )

        image = image.convert("RGB")

        image.save(
            output,
            format="PNG",
            optimize=True,
        )

        logger.info(
            "Hugging Face AI artwork saved: %s",
            output,
        )

        return str(output)


class GeminiImageProvider:
    """
    Optional Gemini image-generation provider.
    """

    def __init__(
        self,
        client=None,
        model: str | None = None,
    ):
        self.gemini_client = (
            client or gemini_client
        )

        self.model = (
            model
            or getattr(
                settings,
                "GEMINI_IMAGE_MODEL",
                "gemini-3.1-flash-image",
            )
        )

        if not getattr(
            self.gemini_client,
            "is_configured",
            False,
        ):
            raise RuntimeError(
                "Gemini client is not configured."
            )

    def generate_image(
        self,
        prompt: str,
        output_path: str | Path,
        panel_number: int = 1,
        title: str = "",
        art_style: str = "Comic Book",
    ) -> str:
        """Generate artwork using Gemini."""

        output = _ensure_output_directory(
            output_path
        )

        try:
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError(
                "google-genai is not installed."
            ) from exc

        style = (
            str(art_style).strip()
            if art_style
            else "Comic Book"
        )

        final_prompt = (
            "Create a professional comic book panel.\n\n"
            f"ART STYLE: {style}\n"
            f"PANEL: {panel_number}\n"
            f"TITLE: {title}\n\n"
            "Show the story scene clearly with "
            "expressive characters, detailed environment, "
            "cinematic composition and polished digital "
            "comic artwork.\n\n"
            "Do not add captions, speech bubbles, "
            "watermarks, logos or random text.\n\n"
            f"SCENE:\n{prompt}"
        )

        logger.info(
            "Generating Gemini artwork for panel %s: %s",
            panel_number,
            output,
        )

        response = (
            self.gemini_client
            ._client
            .models
            .generate_content(
                model=self.model,
                contents=[final_prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                ),
            )
        )

        parts = getattr(
            response,
            "parts",
            None,
        ) or []

        for part in parts:
            inline_data = getattr(
                part,
                "inline_data",
                None,
            )

            if inline_data:
                image = part.as_image()

                if image is None:
                    continue

                image.save(
                    output,
                    format="PNG",
                )

                logger.info(
                    "Gemini AI artwork saved: %s",
                    output,
                )

                return str(output)

        raise RuntimeError(
            "Gemini did not return an image."
        )


class FallbackImageProvider:
    """
    Local fallback provider.

    Used only when an AI image provider fails and
    ALLOW_IMAGE_FALLBACK is enabled.
    """

    def generate_image(
        self,
        prompt: str,
        output_path: str | Path,
        panel_number: int = 1,
        title: str = "",
        art_style: str = "Comic Book",
    ) -> str:
        return _placeholder(
            prompt=prompt,
            output_path=output_path,
            panel_number=panel_number,
            title=title,
        )


def _create_huggingface_provider() -> HuggingFaceImageProvider:
    """Create the Hugging Face provider."""

    return HuggingFaceImageProvider(
        token=getattr(
            settings,
            "HF_TOKEN",
            "",
        ),
        model=getattr(
            settings,
            "HF_IMAGE_MODEL",
            "black-forest-labs/FLUX.1-schnell",
        ),
        provider=getattr(
            settings,
            "HF_IMAGE_PROVIDER",
            "auto",
        ),
    )


def _create_gemini_provider() -> GeminiImageProvider:
    """Create the Gemini provider."""

    return GeminiImageProvider(
        client=gemini_client,
        model=getattr(
            settings,
            "GEMINI_IMAGE_MODEL",
            "gemini-3.1-flash-image",
        ),
    )


def get_image_provider() -> ImageProvider:
    """
    Select the configured image provider.

    IMAGE_PROVIDER values:

        huggingface
        hugging_face
        hf
        flux
        gemini
        google
        fallback
        local
        auto
    """

    provider_name = str(
        getattr(
            settings,
            "IMAGE_PROVIDER",
            "huggingface",
        )
    ).strip().lower()

    allow_fallback = bool(
        getattr(
            settings,
            "ALLOW_IMAGE_FALLBACK",
            True,
        )
    )

    logger.info(
        "Requested image provider: %s",
        provider_name,
    )

    # ---------------------------------------------------------
    # EXPLICIT HUGGING FACE
    # ---------------------------------------------------------

    if provider_name in {
        "huggingface",
        "hugging_face",
        "hf",
        "flux",
    }:
        try:
            provider = _create_huggingface_provider()

            logger.info(
                "Using Hugging Face image provider: %s",
                provider.model,
            )

            return provider

        except Exception as exc:
            logger.exception(
                "Hugging Face initialization failed: %s",
                exc,
            )

    # ---------------------------------------------------------
    # GEMINI
    # ---------------------------------------------------------

    if provider_name in {
        "gemini",
        "google",
        "auto",
        "huggingface",
        "hugging_face",
        "hf",
        "flux",
    }:
        try:
            provider = _create_gemini_provider()

            logger.info(
                "Using Gemini image provider: %s",
                provider.model,
            )

            return provider

        except Exception as exc:
            logger.exception(
                "Gemini initialization failed: %s",
                exc,
            )

    # ---------------------------------------------------------
    # FALLBACK
    # ---------------------------------------------------------

    if allow_fallback:
        logger.warning(
            "Using local fallback image provider."
        )

        return FallbackImageProvider()

    raise RuntimeError(
        "No image provider is available and "
        "ALLOW_IMAGE_FALLBACK is disabled."
    )


def generate_image(
    prompt: str,
    output_path: str | Path,
    panel_number: int = 1,
    title: str = "",
    art_style: str = "Comic Book",
) -> str:
    """
    Generate an image using the configured provider.

    This public helper is compatible with the existing
    ComicCraft generation pipeline.
    """

    provider = get_image_provider()

    try:
        return provider.generate_image(
            prompt=prompt,
            output_path=output_path,
            panel_number=panel_number,
            title=title,
            art_style=art_style,
        )

    except Exception as exc:
        logger.exception(
            "Primary image generation failed: %s",
            exc,
        )

        allow_fallback = bool(
            getattr(
                settings,
                "ALLOW_IMAGE_FALLBACK",
                True,
            )
        )

        if not allow_fallback:
            raise

        logger.warning(
            "Primary provider failed. "
            "Creating fallback artwork instead."
        )

        return FallbackImageProvider().generate_image(
            prompt=prompt,
            output_path=output_path,
            panel_number=panel_number,
            title=title,
            art_style=art_style,
        )


__all__ = [
    "ImageProvider",
    "HuggingFaceImageProvider",
    "GeminiImageProvider",
    "FallbackImageProvider",
    "get_image_provider",
    "generate_image",
]