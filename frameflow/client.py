#!/usr/bin/env python3

class BaseClient:
    def summarize_chunk(self, chunk_text):
        raise NotImplementedError("summarize_chunk must be implemented in client subclasses.")
