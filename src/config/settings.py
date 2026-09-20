# configurações (Pydantic BaseSettings)

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cep_api_timeout: int = 5


settings = Settings()