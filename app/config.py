from pydantic import BaseSettings

class Settings(BaseSettings):
    api_key: str
    ollama_url: str
    max_parallel_requests: int = 5

    class Config:
        env_file = ".env"

settings = Settings()

