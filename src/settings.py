from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    database_url: str
    massive_api_key: str
    massive_web_socket: str

    model_config = SettingsConfigDict(env_file=".env.compose")

settings = Settings()