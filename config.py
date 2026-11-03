from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token: str
    owner_chat_id: int
    redis_host: str = "localhost"
    redis_port: int = 6379
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"
    vault_path: str = "./vault"
    git_repo_url: str = ""
    git_user_name: str = "AI Assistant"
    git_user_email: str = "ai@assistant.local"
    whisper_model: str = "large-v3"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()