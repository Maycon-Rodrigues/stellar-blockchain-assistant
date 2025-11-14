from agno.models.openai import OpenAIChat
from agno.models.google import Gemini

MODEL_CONFIG = {
    "model": OpenAIChat("gpt-4o-mini"),
    # "model": Gemini("gemini-2.5-flash"),
}
