from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configures backend using variables found in .env file."""

    # NOTE: ALLOWED_ORIGINS will be converted to Sequence[str] via field
    # validator though type hints will still show str.
    # Is there a way to fix this?

    ALLOWED_ORIGINS: str
    API_PREFIX: str
    DEBUG: bool

    DATABASE_URL: str
    # OPEN_AI_KEY: str

    # NOTE: Previously in Pydantic v1, a nested Config class was needed.
    # Using model_config: SettingsConfigDict is new in Pydantic v2.

    # NOTE: There must exist the same vars in .env as the specified fields here.
    # Furthermore, make sure that rather than `env=".env"` we are rather using
    # `env_file=".env"`.

    # NOTE: Must run via `uv run src/main.py`.

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> list[str]:
        return v.split(",") if v else []


settings = Settings()
