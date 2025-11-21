from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LANG_MAP = {
    "ru": "Russian",
    "en": "English",
    "kk": "Kazakh"
}

async def translate_text(text: str, target_language: str) -> str:
    lang = LANG_MAP.get(target_language, "English")

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"Translate this text to {lang}:\n{text}"
    )

    return response.output_text
