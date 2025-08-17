from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Settings(BaseSettings):
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DB: str

    @property
    def url(self):
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}'
    
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
engine = create_async_engine(url=settings.url)
async_session = async_sessionmaker(engine)


