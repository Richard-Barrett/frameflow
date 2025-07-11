#!/usr/bin/env python3

import logging

# Gemini
import google.generativeai as genai

# OpenAI
from openai import OpenAI

# Anthropic Claude
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class GeminiModelVerifier:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.client = genai

    def list_models(self):
        try:
            models = self.client.list_models()
            logger.info("✅ Available Gemini models:")
            for m in models:
                logger.info(f" - {m.name} | methods: {m.supported_generation_methods}")
        except Exception as e:
            logger.error(f"❌ Failed to list Gemini models: {e}")


class OpenAIModelVerifier:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def list_models(self):
        try:
            models = self.client.models.list()
            logger.info("✅ Available OpenAI models:")
            for m in models.data:
                logger.info(f" - {m.id}")
        except Exception as e:
            logger.error(f"❌ Failed to list OpenAI models: {e}")


class ClaudeModelVerifier:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def list_models(self):
        try:
            # Claude API may not support listing all models dynamically; list known models
            known_models = ["claude-3-opus-20240229", "claude-3-sonnet-20240229"]
            logger.info("✅ Available Claude models (known):")
            for m in known_models:
                logger.info(f" - {m}")
        except Exception as e:
            logger.error(f"❌ Failed to list Claude models: {e}")


def list_models_for_client(client_name, client_token=None):
    if client_name == "openai":
        verifier = OpenAIModelVerifier(api_key=client_token)
    elif client_name == "gemini":
        verifier = GeminiModelVerifier(api_key=client_token)
    elif client_name == "claude":
        verifier = ClaudeModelVerifier(api_key=client_token)
    else:
        logger.error(f"Unknown client for model listing: {client_name}")
        return

    verifier.list_models()
