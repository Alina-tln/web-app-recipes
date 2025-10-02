from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MODE: str

    DB_CONNECT_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str


    @property
    def database_url_async(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_CONNECT_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_CONNECT_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()





