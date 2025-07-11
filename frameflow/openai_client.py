#!/usr/bin/env python3

import logging
from openai import OpenAI
from frameflow.client import BaseClient

logger = logging.getLogger(__name__)

class OpenAIClient(BaseClient):
    def __init__(self, api_key=None):
        logger.info("Initializing OpenAI client")
        if api_key:
            self.client = OpenAI(api_key=api_key)
            logger.debug("OpenAI client initialized with provided API key.")
        else:
            self.client = OpenAI()
            logger.debug("OpenAI client initialized using environment variable.")

    def summarize_chunk(self, chunk_text):
        logger.debug("Summarizing chunk with OpenAI.")
        prompt = f"Summarize this chunk:\n\n{chunk_text}"
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content
        logger.debug(f"Received summary from OpenAI: {summary}")
        return summary
