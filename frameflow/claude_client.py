#!/usr/bin/env python3

import logging
from anthropic import Anthropic
from frameflow.client import BaseClient

logger = logging.getLogger(__name__)

class ClaudeClient(BaseClient):
    def __init__(self, api_key=None):
        logger.info("Initializing Claude client")
        if api_key:
            self.client = Anthropic(api_key=api_key)
            logger.debug("Claude client initialized with provided API key.")
        else:
            self.client = Anthropic()
            logger.debug("Claude client initialized using environment variable.")

    def summarize_chunk(self, chunk_text):
        logger.debug("Summarizing chunk with Claude.")
        prompt = f"Summarize this chunk:\n\n{chunk_text}"
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.content[0].text
        logger.debug(f"Received summary from Claude: {summary}")
        return summary

