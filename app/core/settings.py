from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "dev"
    jwt_secret_key: str = ""
    jwt_algorithm: str = ""
    jwt_issuer: str = ""
    jwt_audience: str = ""
    database_url: str = ""
    database_pool_min_size: int = 0
    database_pool_max_size: int = 0
    rabbitmq_url: str = ""
    redis_url: str = ""


    class Config:
        env_file = ".env"

settings = Settings()


