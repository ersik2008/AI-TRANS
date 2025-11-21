from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LANG_MAP = {
    "ru": "Russian",
    "en": "English",
    "kk": "Kazakh"
}

async def translate_text(text: str, target_language: str) -> str:
    if not text.strip():
        return ""
    
    lang = LANG_MAP.get(target_language, "English")
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate accurately without adding comments."},
                {"role": "user", "content": f"Translate to {lang}:\n{text}"}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")