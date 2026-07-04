from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str
    app_version: str
    debug: bool

    # Database
    database_url: str
    database_echo: bool
    database_pool_size: int
    database_max_overflow: int
    database_pool_pre_ping: bool
    database_pool_recycle: int

    # Authentication
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
