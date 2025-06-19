import os

def set_groq_api_key(key: str):
    os.environ["GROQ_API_KEY"] = key

def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "")