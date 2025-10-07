from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config import settings

#---------------------------------------------
# SYNC ENGINE
#---------------------------------------------


engine = create_engine(
    url=settings.database_url,
    echo=True,
    pool_size=5,
    max_overflow=10
)

session = sessionmaker(engine)

#---------------------------------------------
# ASYNC ENGINE
#---------------------------------------------

async_engine = create_async_engine(
    url=settings.database_url,
    echo=True,
    pool_size=5,
    max_overflow=10
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
