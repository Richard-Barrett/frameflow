#!/usr/bin/env python3

import logging
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from frameflow.client import BaseClient

logger = logging.getLogger(__name__)

class GeminiClient(BaseClient):
    def __init__(self, api_key=None, model="gemini-pro"):
        logger.info("Initializing Gemini client")
        if api_key:
            genai.configure(api_key=api_key)
            logger.debug("Gemini client configured with provided API key.")
        else:
            genai.configure()
            logger.debug("Gemini client configured using environment variable.")
        self.model_name = model
        self.model = genai.GenerativeModel(self.model_name)

    def summarize_chunk(self, chunk_text, retries=5, initial_wait=2, max_wait=60):
        attempt = 0
        while attempt < retries:
            try:
                prompt = f"Summarize this chunk:\n\n{chunk_text}"
                response = self.model.generate_content(prompt)
                return response.text
            except ResourceExhausted as e:
                wait_time = min(initial_wait * (2 ** attempt), max_wait)
                logger.warning(f"⚠️ Gemini rate limit exceeded. Retry {attempt+1}/{retries} in {wait_time}s.")
                time.sleep(wait_time)
                attempt += 1
            except Exception as e:
                logger.error(f"Unexpected Gemini error: {e}")
                break
        logger.error("❌ Exceeded maximum retries for Gemini.")
        return "Rate limit exceeded or persistent error."

    def list_models(self):
        models = genai.list_models()
        logger.info("✅ Available Gemini models:")
        for model in models:
            methods = getattr(model, "supported_generation_methods", [])
            logger.info(f" - {model.name} | methods: {methods}")
