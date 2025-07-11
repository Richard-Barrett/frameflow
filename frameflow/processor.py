#!/usr/bin/env python3

import logging
import os
import cv2
import whisper
import pytesseract

from frameflow.openai_client import OpenAIClient
from frameflow.claude_client import ClaudeClient
from frameflow.gemini_client import GeminiClient
from frameflow.local_llm_client import LocalLLMClient

logger = logging.getLogger(__name__)

def extract_frames(video_path, output_dir, fps=None, smart_mode=False):
    logger.info("Extracting frames...")
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if smart_mode:
        logger.info("Smart mode enabled: extracting all frames for analysis")
        frame_interval = 1
    elif fps:
        frame_interval = int(video_fps / fps)
    else:
        frame_interval = int(video_fps)  # default to 1 fps

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            filename = os.path.join(output_dir, f"frame_{saved_count:05d}.jpg")
            cv2.imwrite(filename, frame)
            saved_count += 1
        frame_count += 1

    cap.release()
    logger.info(f"Extracted {saved_count} frames to {output_dir}")

def analyze_frame(frame_path):
    image_text = ""
    try:
        image_text = pytesseract.image_to_string(frame_path)
    except Exception as e:
        logger.warning(f"OCR failed for {frame_path}: {e}")
    return image_text.strip()

def transcribe_audio(video_path, model_name="large"):
    logger.info("Transcribing audio with Whisper...")
    model = whisper.load_model(model_name)
    result = model.transcribe(video_path)
    transcript = result['text']
    logger.info("Transcription complete.")
    return transcript

def get_client(client_name, client_token, client_model):
    if client_name == "openai":
        return OpenAIClient(api_key=client_token, model=client_model)
    elif client_name == "claude":
        return ClaudeClient(api_key=client_token, model=client_model)
    elif client_name == "gemini":
        return GeminiClient(api_key=client_token, model=client_model)
    elif client_name == "local":
        return LocalLLMClient(model=client_model)
    else:
        raise ValueError(f"Unknown client: {client_name}")


def process_video(input_file, output, fps, whisper_model, fps_smart_mode, transcribe, client_name, client_token, client_model):
    logger.info(f"Processing: {input_file}")
    logger.info(f"Output: {output}")
    logger.info(f"Whisper Model: {whisper_model}")
    logger.info(f"Transcribe only: {transcribe}")
    logger.info(f"Client: {client_name}")
    logger.info(f"Client Model: {client_model}")

    # Initialize AI client
    client = get_client(client_name, client_token, client_model)

    # Step 1: Extract frames
    frames_dir = "frames"
    extract_frames(input_file, frames_dir, fps, fps_smart_mode)

    # Step 2: Analyze frames with OCR
    logger.info("Analyzing frames with OCR...")
    frame_texts = {}
    for frame_file in sorted(os.listdir(frames_dir)):
        frame_path = os.path.join(frames_dir, frame_file)
        ocr_text = analyze_frame(frame_path)
        frame_texts[frame_file] = ocr_text

    # Step 3: Transcribe audio
    transcript = transcribe_audio(input_file, whisper_model)

    if transcribe:
        with open(output, "w") as f:
            f.write("# FrameFlow Transcript Output\n\n")
            f.write(transcript)
        logger.info(f"Transcript saved to {output}")
        return

    # Step 4: Summarize each frame + transcript chunk
    logger.info("Summarizing frames and transcription...")
    with open(output, "w") as f:
        f.write("# FrameFlow How-To Documentation\n\n")
        for idx, (frame_file, ocr_text) in enumerate(frame_texts.items(), start=1):
            combined_input = f"OCR Text:\n{ocr_text}\n\nTranscript:\n{transcript}\n\n"
            summary = client.summarize_chunk(combined_input)
            f.write(f"## Step {idx}\n")
            f.write(f"![{frame_file}](frames/{frame_file})\n\n")
            f.write(summary + "\n\n")

    logger.info(f"How-To Markdown file generated at: {output}")

