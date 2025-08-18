from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.models import Base


class Settings(BaseSettings):
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DB: str

    @property
    def url(self):
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}'
    
    model_config = SettingsConfigDict(env_file='db.env')


settings = Settings()
engine = create_async_engine(url=settings.url, echo=True)
async_session = async_sessionmaker(engine)


async def start_db_engine():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()