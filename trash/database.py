from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config import settings

engine = create_engine(
    url=settings.database_url,
    echo=True,
    pool_size=5,
    max_overflow=10
)

async_engine = create_async_engine(
    url=settings.database_url_async,
    echo=True,
    pool_size=5,
    max_overflow=10
)

Base = declarative_base()

#To create a table in Postgres
#Base.metadata.create_all(engine)