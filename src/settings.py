from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "analytics-api"
    admin_email: str
    database_url: str
    massive_api_key: str
    massive_web_socket: str
    celery_broker_url: str
    celery_backend_url: str

    model_config = SettingsConfigDict(env_file=".env.compose")

settings = Settings()