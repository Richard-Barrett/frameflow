#!/usr/bin/env python3

import logging
import google.generativeai as genai
from frameflow.client import BaseClient

logger = logging.getLogger(__name__)

class GeminiClient(BaseClient):
    def __init__(self, api_key=None):
        logger.info("Initializing Gemini client")
        if api_key:
            genai.configure(api_key=api_key)
            logger.debug("Gemini client configured with provided API key.")
        else:
            genai.configure()
            logger.debug("Gemini client configured using environment variable.")
        self.model = genai.GenerativeModel("gemini-pro")

    def summarize_chunk(self, chunk_text):
        logger.debug("Summarizing chunk with Gemini.")
        prompt = f"Summarize this chunk:\n\n{chunk_text}"
        response = self.model.generate_content(prompt)
        summary = response.text
        logger.debug(f"Received summary from Gemini: {summary}")
        return summary
