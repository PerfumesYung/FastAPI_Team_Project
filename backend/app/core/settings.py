"""환경설정: backend/.env 파일의 값을 읽습니다."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    database_url: str = "sqlite:///./study.db"
    secret_key: str = ""  # JWT 구현 시 .env에 안전한 값을 입력하고 검증하세요.
    access_token_expire_minutes: int = 30

settings = Settings()
