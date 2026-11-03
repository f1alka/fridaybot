import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from loguru import logger
from schemas import ExtractedData
from config import settings

env = Environment(loader=FileSystemLoader("templates"))

def save_to_vault(data: ExtractedData) -> str:
    """Рендеринг Markdown через Jinja2 и сохранение в папку."""
    # Определяем папку на основе категории
    folder_map = {
        "diary": "Notes",
        "task": "Tasks",
        "event": "Events",
        "person": "People",
        "project": "Projects"
    }
    target_dir = os.path.join(settings.vault_path, folder_map.get(data.category, "Inbox"))
    os.makedirs(target_dir, exist_ok=True)
    
    # Формируем имя файла
    safe_title = "".join([c if c.isalnum() else "_" for c in data.title])[:50]
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{safe_title}.md"
    filepath = os.path.join(target_dir, filename)

    # Рендерим шаблон
    template = env.get_template("note.md.j2")
    content = template.render(
        data=data,
        date=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    logger.info(f"Saved to vault: {filepath}")
    return filepath