#!/usr/bin/env python3

import logging
import requests
from frameflow.client import BaseClient

logger = logging.getLogger(__name__)

class LocalLLMClient(BaseClient):
    def __init__(self, endpoint="http://localhost:8000/v1/chat/completions", api_key=None):
        logger.info("Initializing Local LLM client")
        self.endpoint = endpoint
        self.api_key = api_key
        logger.debug(f"Local LLM endpoint: {self.endpoint}")

    def summarize_chunk(self, chunk_text):
        logger.debug("Summarizing chunk with Local LLM.")
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = {
            "model": "mistral",
            "messages": [{"role": "user", "content": chunk_text}],
        }
        response = requests.post(self.endpoint, json=data, headers=headers)
        summary = response.json()['choices'][0]['message']['content']
        logger.debug(f"Received summary from Local LLM: {summary}")
        return summary
