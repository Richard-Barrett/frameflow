#!/usr/bin/env python3

import subprocess
import logging
logging.getLogger().setLevel(logging.CRITICAL)


def test_cli_help():
    result = subprocess.run(["python", "-m", "frameflow.cli", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "FrameFlow" in result.stdout
