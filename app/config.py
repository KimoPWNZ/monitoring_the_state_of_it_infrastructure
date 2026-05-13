from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    db_path: str = "monitoring.db"

    default_check_interval: int = 60
    request_timeout: int = 5
    warning_response_time: int = 1000
    critical_response_time: int = 3000

    auth_enabled: bool = False
    auth_username: str | None = None
    auth_password: str | None = None

    email_notifications: bool = False
    smtp_server: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None
    smtp_to: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
