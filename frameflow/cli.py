#!/usr/bin/env python3

import argparse
from frameflow.processor import process_video
from frameflow.logging_config import setup_logging
import logging

def main():
    parser = argparse.ArgumentParser(description="FrameFlow: Transcribe technical videos into visual How-To documents.")
    parser.add_argument("--input-file", required=False, help="Path to input video file")
    parser.add_argument("--output", default="howto.md", help="Output Markdown file")
    parser.add_argument("--fps", type=float, default=None, help="Frame extraction FPS. If not set, uses scene change.")
    parser.add_argument("--fps-smart-mode", action="store_true", help="Enable smart FPS extraction based on video length.")
    parser.add_argument("--whisper-model", default="large", help="Whisper model size (tiny, base, small, medium, large)")
    parser.add_argument("--client", default="openai", choices=["openai", "local", "gemini", "claude"], help="AI client to use for summarization")
    parser.add_argument("--client-model", default=None, help="AI model name for the selected client")
    parser.add_argument("--client-token", default=None, help="API token for the AI client (overrides environment variable if provided)")
    parser.add_argument("--transcribe", action="store_true", help="If set, generate transcript only.")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set log verbosity level (default: INFO)")
    parser.add_argument("--list-available-models", action="store_true", help="List available models for the selected client")

    args = parser.parse_args()

    # Initialize logging with selected level
    setup_logging(level=getattr(logging, args.log_level.upper(), logging.INFO))

    if args.list_available_models:
        from frameflow.verify_models import list_models_for_client
        list_models_for_client(args.client, args.client_token)
        return

    process_video(
        args.input_file,
        args.output,
        args.fps,
        args.whisper_model,
        args.fps_smart_mode,
        args.transcribe,
        args.client,
        args.client_token,
        args.client_model
    )

if __name__ == "__main__":
    main()
