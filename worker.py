import asyncio
import os
from arq import create_pool
from arq.connections import RedisSettings
from loguru import logger

from config import settings
from services.audio import process_audio
from services.llm import extract_knowledge
from services.obsidian import save_to_vault
from services.git_sync import sync_vault

async def process_voice_task(ctx, ogg_path: str, chat_id: int):
    """Пайплайн: Audio -> LLM -> Obsidian -> Git."""
    logger.info(f"Started processing {ogg_path}")
    
    # 1. Worker 1: Audio Pipeline
    transcript = await asyncio.to_thread(process_audio, ogg_path)
    if not transcript:
        await ctx['bot'].send_message(chat_id, "❌ Не удалось распознать речь.")
        return

    # 2. Worker 2: Knowledge Pipeline
    await ctx['bot'].send_message(chat_id, f"📝 <b>Расшифровка:</b>\n{transcript}\n\n🧠 <i>Анализирую...</i>", parse_mode="HTML")
    
    extracted_data = await asyncio.to_thread(extract_knowledge, transcript)
    
    # 3. Obsidian Vault
    filepath = await asyncio.to_thread(save_to_vault, extracted_data)
    
    # 4. Git Sync
    commit_msg = f"Add {extracted_data.category}: {extracted_data.title}"
    await asyncio.to_thread(sync_vault, commit_msg)

    # Уведомляем пользователя
    await ctx['bot'].send_message(
        chat_id, 
        f"✅ Сохранено в <code>{os.path.basename(filepath)}</code>\n"
        f"Категория: <b>{extracted_data.category}</b>\n"
        f"Теги: {', '.join(extracted_data.tags)}",
        parse_mode="HTML"
    )

class WorkerSettings:
    functions = [process_voice_task]
    redis_settings = RedisSettings(host=settings.redis_host, port=settings.redis_port)
    # Можно добавить cron для проверки дедлайнов (напоминания)