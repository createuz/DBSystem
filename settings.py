from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    REDIS_URL: str

    PG_POOL_MIN_SIZE: int = 5
    PG_POOL_MAX_SIZE: int = 20
    REDIS_POOL_MAX_CONNECTIONS: int = 20

    class Config:
        env_file = ".env"


settings = Settings()
