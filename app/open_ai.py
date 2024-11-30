import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def open_ai_client() -> OpenAI:
    api_key = os.getenv("OPEN_AI_KEY")
    if not api_key:
        raise ValueError("The OpenAI API key is not set in the environment variables.")
    return OpenAI(api_key=api_key)
