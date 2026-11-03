import ollama
import json
from loguru import logger
from config import settings
from schemas import ExtractedData

SYSTEM_PROMPT = """
Ты — AI-ассистент, который структурирует сырые голосовые заметки в Markdown.
Твоя задача — проанализировать текст, определить его категорию (diary, task, event, person, project) 
и извлечь сущности. Верни ТОЛЬКО валидный JSON, соответствующий схеме.
"""

def extract_knowledge(text: str) -> ExtractedData:
    """Отправка текста в Ollama с требованием JSON на выходе."""
    try:
        response = ollama.chat(
            model=settings.ollama_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Текст заметки: {text}"}
            ],
            format="json", # Ollama заставит модель выдать JSON
            options={"temperature": 0.1}
        )
        
        raw_json = response['message']['content']
        logger.debug(f"LLM raw output: {raw_json}")
        
        # Валидация через Pydantic V2
        data = ExtractedData.model_validate_json(raw_json)
        return data
        
    except Exception as e:
        logger.error(f"LLM validation error: {e}")
        # Fallback, если LLM сошла с ума
        return ExtractedData(
            category="diary",
            title="Необработанная заметка",
            summary=text,
            tags=["fallback"]
        )