from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Legal Consultation Platform"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./legal_platform.db"

    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"


settings = Settings()
