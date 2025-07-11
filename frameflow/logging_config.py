#!/usr/bin/env python3

import logging
from datetime import datetime
import os

def setup_logging(level=logging.INFO, log_dir="logs"):
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Generate datestamped log filename
    log_filename = datetime.now().strftime("frameflow_%Y%m%d_%H%M%S.log")
    log_path = os.path.join(log_dir, log_filename)

    # Create formatter
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    # Root logger setup
    logging.basicConfig(level=level, handlers=[console_handler, file_handler])

    # Silence noisy third-party libraries
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)

    logging.info(f"Logging initialized. Log file: {log_path}")
