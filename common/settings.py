from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: str = "postgresql://postgres:postgres@localhost:5432/"
    APOSTGRES_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/"
    REDIS_URL: str = "redis://localhost:6379"


settings = Settings()
