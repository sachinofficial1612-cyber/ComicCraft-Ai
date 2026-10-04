import os
import json
import time
import re
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel
from ..config import settings
from ..utils.logger import get_logger

logger = get_logger("gemini_client")

T = TypeVar("T", bound=BaseModel)

class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        self.text_model = settings.GEMINI_TEXT_MODEL
        self.image_model = settings.GEMINI_IMAGE_MODEL
        self._client = None
        
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
                logger.info(f"Initialized Gemini Client with text model {self.text_model}")
            except Exception as e:
                logger.warning(f"Failed to initialize google-genai client: {e}")
        else:
            logger.info("No GEMINI_API_KEY found. AI services will use intelligent fallbacks.")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self._client)

    def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        """Generate text using Gemini text model with retry logic."""
        if not self.is_configured:
            raise ValueError("GEMINI_API_KEY is not configured.")

        max_retries = 3
        backoff = 2
        for attempt in range(max_retries):
            try:
                from google.genai import types
                config = types.GenerateContentConfig()
                if system_instruction:
                    config.system_instruction = system_instruction
                
                response = self._client.models.generate_content(
                    model=self.text_model,
                    contents=prompt,
                    config=config
                )
                return response.text
            except Exception as e:
                logger.warning(f"Gemini generate_text attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(backoff ** attempt)
        return ""

    def generate_structured(self, prompt: str, schema: Type[T], system_instruction: str = "") -> T:
        """Generate structured response matching Pydantic schema."""
        if not self.is_configured:
            raise ValueError("GEMINI_API_KEY is not configured.")

        max_retries = 3
        backoff = 2
        for attempt in range(max_retries):
            try:
                from google.genai import types
                
                # Attempt structured JSON output via API config if available
                config = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema
                )
                if system_instruction:
                    config.system_instruction = system_instruction

                response = self._client.models.generate_content(
                    model=self.text_model,
                    contents=prompt,
                    config=config
                )
                
                # Parse JSON
                raw_text = response.text.strip()
                raw_json = self._extract_json(raw_text)
                return schema.model_validate_json(raw_json)

            except Exception as e:
                logger.warning(f"Structured generation attempt {attempt + 1} failed: {e}. Trying raw JSON prompt format.")
                # Fallback to standard prompt requesting raw JSON
                try:
                    fallback_prompt = (
                        f"{prompt}\n\nProvide response in valid JSON matching schema:\n"
                        f"{json.dumps(schema.model_json_schema(), indent=2)}"
                    )
                    from google.genai import types
                    raw_resp = self._client.models.generate_content(
                        model=self.text_model,
                        contents=fallback_prompt
                    )
                    extracted = self._extract_json(raw_resp.text)
                    return schema.model_validate_json(extracted)
                except Exception as inner_e:
                    logger.error(f"Fallback structured retry failed: {inner_e}")
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(backoff ** attempt)

        raise RuntimeError("Failed to generate structured data after retries.")

    def _extract_json(self, text: str) -> str:
        """Extract clean JSON string from code blocks or raw text."""
        text = text.strip()
        # Remove ```json ... ``` wrapper
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            return match.group(1).strip()
        # Find first { and last }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start:end+1]
        return text

gemini_client = GeminiClient()
