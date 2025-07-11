#!/usr/bin/env python3

import pytest # type: ignore
import logging
logging.getLogger().setLevel(logging.CRITICAL)


@pytest.fixture
def sample_chunk():
    return [{"start": 0.0, "end": 10.0, "text": "Install build tools using apt-get."}]
