from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = ''
    rabbitmq_url: str = ''
    redis_url: str = ''
    celery_broker: str = ''
    celery_backend: str = ''
    env: str = "dev"

    class Config:
        env_file = ".env"

settings = Settings()
