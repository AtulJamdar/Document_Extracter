from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str

    DATABASE_URL: str

    OCR_ENGINE: str

    GROQ_API_KEY: str

    LLM_MODEL: str

    ENABLE_PREPROCESSING: bool = True

    class Config:

        env_file = ".env"


settings = Settings()
