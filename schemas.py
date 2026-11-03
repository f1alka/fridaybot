from pydantic import BaseModel, Field
from typing import Literal, List, Optional
from datetime import datetime

class ExtractedData(BaseModel):
    category: Literal["diary", "task", "event", "person", "project"] = Field(
        description="Категория заметки"
    )
    title: str = Field(description="Краткий заголовок на основе текста")
    summary: str = Field(description="Само содержание, очищенное от слов-паразитов")
    tags: List[str] = Field(default_factory=list, description="Теги для Obsidian")
    tasks: List[str] = Field(default_factory=list, description="Извлеченные задачи, если есть")
    due_date: Optional[str] = Field(None, description="Дедлайн в формате YYYY-MM-DD, если есть")
    entities: List[str] = Field(default_factory=list, description="Упомянутые люди, компании")