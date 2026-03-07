from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configures backend using variables found in .env file."""

    # NOTE: ALLOWED_ORIGINS will be converted to Sequence[str] via field
    # validator though type hints will still show str.
    # Is there a way to fix this?

    ALLOWED_ORIGINS: str = ""
    API_PREFIX: str = "/api"
    DEBUG: bool = False

    DATABASE_URL: str = ""
    OPEN_AI_KEY: str = ""

    # NOTE: Prviously in Pydantic v1, a nested Config class was needed.
    # Using model_config: SettingsConfigDict is new in Pydantic v2.

    model_config = SettingsConfigDict(
        env=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> list[str]:
        return v.split(",") if v else []


settings = Settings()
