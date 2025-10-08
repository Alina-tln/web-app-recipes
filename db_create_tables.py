import asyncio
from db_base import Base
from database import async_session, async_engine
from sqlalchemy import text
import recipe_service.models.recipes_models
import recipe_service.models.ingredients_models
import user_service.models.users
import user_service.models.groups
import translation_service.models.translations


async def setup_database(drop: bool = False):

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(setup_database(drop=True))  # drop=True for dev
    print("Creating tables is complete ✅")