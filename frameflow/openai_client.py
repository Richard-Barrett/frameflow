#!/usr/bin/env python3

import logging
import time
from openai import OpenAI
from openai import APIError, RateLimitError

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key=None, model="gpt-4o"):
        logger.info("Initializing OpenAI client")
        if api_key:
            self.client = OpenAI(api_key=api_key)
            logger.debug("OpenAI client configured with provided API key.")
        else:
            self.client = OpenAI()
            logger.debug("OpenAI client configured using environment variable.")
        self.model = model
        logger.info(f"Using OpenAI model: {model}")

    def summarize_chunk(self, chunk_text, retries=5, initial_wait=2, max_wait=60):
        prompt = f"Summarize this chunk:\n\n{chunk_text}"
        attempt = 0

        while attempt < retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                summary = response.choices[0].message.content
                logger.debug(f"Received summary from OpenAI: {summary}")
                return summary

            except RateLimitError:
                wait_time = min(initial_wait * (2 ** attempt), max_wait)
                logger.warning(f"⚠️ Rate limit exceeded. Retry {attempt + 1}/{retries} in {wait_time}s.")
                time.sleep(wait_time)
                attempt += 1

            except APIError as e:
                logger.error(f"OpenAI API error: {e}. Retry {attempt + 1}/{retries}.")
                wait_time = min(initial_wait * (2 ** attempt), max_wait)
                time.sleep(wait_time)
                attempt += 1

            except Exception as e:
                logger.error(f"Unexpected error summarizing chunk: {e}")
                break

        logger.error("❌ Exceeded maximum retries due to rate limits or persistent errors.")
        return "Rate limit exceeded or error occurred repeatedly."

    def list_models(self):
        logger.info("✅ Available OpenAI models:")
        models = self.client.models.list()
        for model in models.data:
            logger.info(f" - {model.id}")

    @staticmethod
    def verify_models():
        client = OpenAI()
        logger.info("✅ Available OpenAI models:")
        models = client.models.list()
        for model in models.data:
            logger.info(f" - {model.id}")
