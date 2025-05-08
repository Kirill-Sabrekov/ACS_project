from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Система мониторинга для промышленных датчиков"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost/postgres"

    class Config:
        env_file = ".env"

settings = Settings() 