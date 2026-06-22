from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    DB_PATH: str = "./monitoring.db"

    DEFAULT_CHECK_INTERVAL: int = 60
    REQUEST_TIMEOUT: int = 5
    WARNING_RESPONSE_TIME: int = 1000
    CRITICAL_RESPONSE_TIME: int = 3000

    EMAIL_NOTIFICATIONS_ENABLED: bool = False
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

    REPORT_EXPORT_FORMAT: str = "csv"
    MONITORING_LOOP_INTERVAL: int = 30

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
