from pydantic_settings import BaseSettings, SettingsConfigDict


class KaizillaSettings(BaseSettings):
    # TODO: Do not provide default value here, now it is only for testing purposes until i add .env file with dummy key
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    THUMBNAIL_MAX_SIZE_X: int = 1024
    THUMBNAIL_MAX_SIZE_Y: int = 1024

    model_config = SettingsConfigDict(case_sensitive=True)


settings = KaizillaSettings()
