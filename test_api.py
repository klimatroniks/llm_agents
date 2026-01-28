import os
from openai import OpenAI

import pytest
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    pytest.skip(
        "OPENAI_API_KEY not set — skipping OpenAI integration tests",
        allow_module_level=True,
    )


def test_openai_client_init():
    client = OpenAI()
    assert client is not None
