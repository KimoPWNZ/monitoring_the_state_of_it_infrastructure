from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    db_path: str = "monitoring.db"

    default_check_interval: int = 60
    request_timeout: int = 5
    warning_response_time: int = 1000
    critical_response_time: int = 3000
    warning_cpu_load: float = 75.0
    critical_cpu_load: float = 90.0
    warning_ram_usage: float = 80.0
    critical_ram_usage: float = 95.0
    warning_disk_usage: float = 85.0
    critical_disk_usage: float = 95.0

    icmp_timeout: float = 2.0
    default_tcp_port: int = 80

    snmp_community: str = "public"
    snmp_version: str = "2c"
    snmp_port: int = 161
    snmp_timeout: int = 2
    snmp_retries: int = 1
    snmp_uptime_oid: str = "1.3.6.1.2.1.1.3.0"
    snmp_cpu_oid: str | None = None
    snmp_ram_oid: str | None = None
    snmp_disk_oid: str | None = None

    local_agent_enabled: bool = True
    local_agent_disk_path: str = "/"
    local_agent_cpu_interval: float = 0.1

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
