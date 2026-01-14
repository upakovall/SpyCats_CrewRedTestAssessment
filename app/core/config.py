from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./db.sqlite3"
    THECATAPI_KEY: str | None = None
    ENV: str = "local"

    class Config:
        env_file = ".env"


settings = Settings()
