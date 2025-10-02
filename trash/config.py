from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    TEST_HOST: str
    TEST_PORT: int
    TEST_USER: str
    TEST_PASSWORD: str
    TEST_NAME: str


    @property
    def test_db_url_async(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_USER}:{self.TEST_PASSWORD}@{self.TEST_HOST}:{self.TEST_PORT}/{self.TEST_NAME}"

    @property
    def test_db_url(self) -> str:
        return f"postgresql+psycopg://{self.TEST_USER}:{self.TEST_PASSWORD}@{self.TEST_HOST}:{self.TEST_PORT}/{self.TEST_NAME}"

    model_config = SettingsConfigDict(env_file='recipes-web-app/.env.test')


settings = Settings()
