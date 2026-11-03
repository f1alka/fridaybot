import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from arq import create_pool
from arq.connections import RedisSettings
from loguru import logger

from config import settings

bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Пул Redis
redis = None

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    if message.chat.id != settings.owner_chat_id:
        return
    await message.answer("👋 Бот готов. Отправьте голосовое сообщение.")

@dp.message(F.voice)
async def handle_voice(message: Message):
    if message.chat.id != settings.owner_chat_id:
        return
        
    await message.answer("🎧 Получено. Отправляю в очередь...")
    
    # Скачиваем файл
    file = await bot.get_file(message.voice.file_id)
    ogg_path = f"/tmp/{message.voice.file_id}.ogg"
    await bot.download_file(file.file_path, ogg_path)
    
    # Отправляем задачу в Redis
    await redis.enqueue_job('process_voice_task', ogg_path, message.chat.id)

async def main():
    global redis
    redis = await create_pool(RedisSettings(host=settings.redis_host, port=settings.redis_port))
    logger.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())