import sys

from pydantic_settings import BaseSettings, SettingsConfigDict


class KaizillaSettings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    THUMBNAIL_MAX_SIZE_X: int = 1024
    THUMBNAIL_MAX_SIZE_Y: int = 1024

    model_config = SettingsConfigDict(case_sensitive=True)


def validate_settings() -> KaizillaSettings:
    settings = KaizillaSettings()

    # It is hard to convert from ValidationError to user-friendly messages, thus do it hard way
    errors: list[str] = []

    if not settings.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is not set, please check your settings")

    if errors:
        print("\n".join(errors), file=sys.stderr)  # noqa:T201
        sys.exit(-1)

    return settings


settings = validate_settings()
