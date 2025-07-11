#!/usr/bin/env python3

import frameflow.processor as processor
import logging
logging.getLogger().setLevel(logging.CRITICAL)


def test_process_video_runs():
    processor.process_video("demo.mp4", "out.md", None, "large", False, False, "openai", None)

