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
Additional arguments
Flag	Description
--fps	Set frames per second for extraction
--fps-smart-mode	Enable smart FPS detection
--transcribe	Generate only audio transcription
--client-token	API token for selected client
--log-level	Set log verbosity (DEBUG, INFO, WARNING, ERROR)
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

