#!/usr/bin/env python3

import frameflow.openai_client as oclient
import frameflow.gemini_client as gclient
import frameflow.claude_client as cclient
import frameflow.local_llm_client as lclient
import logging
logging.getLogger().setLevel(logging.CRITICAL)


def test_openai_client_init(monkeypatch):
    class MockCreate:
        def create(self, **kwargs):
            return type("obj", (object,), {
                "choices": [type("o", (object,), {
                    "message": type("m", (object,), {"content": "test summary"})()
                })()]
            })()

    class MockChat:
        def __init__(self):
            self.completions = MockCreate()

    class MockOpenAI:
        def __init__(self):
            self.chat = MockChat()

    monkeypatch.setattr(oclient, "OpenAI", MockOpenAI)
    client = oclient.OpenAIClient()
    summary = client.summarize_chunk("test chunk")
    assert "test summary" in summary

def test_gemini_client(monkeypatch):
    class MockResponse:
        text = "gemini summary"

    class MockGenerativeModel:
        def __init__(self, model_name): pass
        def generate_content(self, prompt): return MockResponse()

    class MockGenAI:
        @staticmethod
        def configure(api_key=None): pass
        GenerativeModel = MockGenerativeModel

    monkeypatch.setattr(gclient, "genai", MockGenAI)

    client = gclient.GeminiClient()
    result = client.summarize_chunk("test chunk")
    assert "gemini summary" in result


def test_claude_client(monkeypatch):
    class MockContent:
        text = "claude summary"

    class MockMessage:
        content = [MockContent()]

    class MockMessages:
        def create(self, **kwargs): return MockMessage()

    class MockAnthropic:
        def __init__(self):
            self.messages = MockMessages()

    monkeypatch.setattr(cclient, "Anthropic", MockAnthropic)
    client = cclient.ClaudeClient()
    result = client.summarize_chunk("test chunk")
    assert "claude summary" in result

def test_local_llm_client(monkeypatch):
    class MockResponse:
        def json(self):
            return {'choices': [{'message': {'content': 'local summary'}}]}

    monkeypatch.setattr(lclient.requests, "post", lambda *a, **k: MockResponse())
    client = lclient.LocalLLMClient()
    result = client.summarize_chunk("test chunk")
    assert "local summary" in result
