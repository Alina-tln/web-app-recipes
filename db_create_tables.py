import asyncio
from db_base import Base
from database import async_engine


async def setup_database(drop: bool = False):

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(setup_database(drop=True))  # drop=True for dev
    print("Creating tables is complete ✅")
