# frameflow
Transcribe technical videos into structured How-To documents with visual frame context.

# 🖼️ FrameFlow

**FrameFlow** is a CLI tool to extract **technical documentation from video recordings** using:

- Frame extraction and OCR
- Whisper transcription
- LLM summarization (OpenAI, Gemini, Claude, or local)
- Markdown documentation generation with embedded frames

---

## 🚀 **Features**

✅ Frame-by-frame extraction with OCR  
✅ Whisper-based audio transcription  
✅ LLM summarization via OpenAI, Gemini, Claude  
✅ Smart FPS mode detection  
✅ CLI with configurable parameters  
✅ Logging with timestamps and runtime logs  
✅ Docker support

---

## ⚠️ **Prerequisites**

- **Python 3.10 or 3.11** (Python 3.13 not fully supported for Whisper)
- **macOS or Linux**
- **System dependencies:**

### **macOS**

```bash
brew install ffmpeg tesseract
```

### Ubuntu

```bash
sudo apt update
sudo apt install ffmpeg tesseract-ocr python3-venv
```

### 🐍 **Virtual environment setup**

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
make install
```

### 🔧 **CLI Usage**

```bash
frameflow --input-file /path/to/video.mp4 --client openai
```

```bash
> frameflow --help
usage: frameflow [-h] [--input-file INPUT_FILE] [--output OUTPUT] [--fps FPS] [--fps-smart-mode] [--whisper-model WHISPER_MODEL]
                 [--client {openai,local,gemini,claude}] [--client-model CLIENT_MODEL] [--client-token CLIENT_TOKEN] [--transcribe]
                 [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--list-available-models]

FrameFlow: Transcribe technical videos into visual How-To documents.

options:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
                        Path to input video file
  --output OUTPUT       Output Markdown file
  --fps FPS             Frame extraction FPS. If not set, uses scene change.
  --fps-smart-mode      Enable smart FPS extraction based on video length.
  --whisper-model WHISPER_MODEL
                        Whisper model size (tiny, base, small, medium, large)
  --client {openai,local,gemini,claude}
                        AI client to use for summarization
  --client-model CLIENT_MODEL
                        AI model name for the selected client
  --client-token CLIENT_TOKEN
                        API token for the AI client (overrides environment variable if provided)
  --transcribe          If set, generate transcript only.
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set log verbosity level (default: INFO)
  --list-available-models
                        List available models for the selected client
```

---

## 🔑 **API Key setup**

### OpenAI
```bash
export OPENAI_API_KEY="sk-xxxx"
```

Or use `--client-token` argument.

## 🧪 **Testing**

Run tests with:

```bash
make test
```

## 🐳 **Docker usage**

Build image:

```bash
make docker-build
```

Run container:

```bash
make docker-run
```

---

## ✨ **Makefile commands**

```bash
> make help

📝 FrameFlow Makefile Commands:

  make venv           Create Python virtual environment
  make install        Install FrameFlow locally in editable mode
  make reinstall      Reinstall FrameFlow (uninstall + editable install)
  make build          Build distribution packages
  make publish        Publish package to PyPI
  make test           Run unit tests with pytest
  make lint           Run pylint for static code analysis
  make format         Format code with black
  make docker-build   Build the FrameFlow Docker image
  make docker-run     Run FrameFlow container with --help
  make clean          Remove __pycache__ and .pytest_cache
```

---

## 📂 **Output files**

- frames/ – extracted frames
- howto.md – generated documentation
- logs/ – runtime logs with timestamps

## 🛠️ **Troubleshooting**

- ModuleNotFoundError: cv2 – install OpenCV:

```bash
pip install opencv-python
```

- AttributeError: module 'whisper' has no attribute 'load_model' – install correct whisper:

```bash
pip uninstall whisper
pip install openai-whisper
```

- OCR errors – ensure tesseract is installed and in your PATH.

---

## 📄 **License**
MIT License

