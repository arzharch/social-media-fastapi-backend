from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_PASSWORD: str 
    POSTGRES_HOST: str 
    POSTGRES_DATABASE: str
    POSTGRES_USER: str

    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file=".env"

settings = Settings()