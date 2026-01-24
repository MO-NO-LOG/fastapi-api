from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str = "5432"
    DB_NAME: str

    SECRET_KEY: str = "supersecretkey"  # Default for dev, change in prod
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    TMDB_API_KEY: str = ""  # TMDB API key for fetching movie data

    class Config:
        env_file = ".env"


settings = Settings()  # ty:ignore[missing-argument]
