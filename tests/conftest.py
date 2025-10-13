import asyncio

import pytest
import pytest_asyncio

from database import engine, settings, async_engine, async_session
from db_base import Base
from sqlalchemy.orm import Session


# ---------------------------------------------
# FIXTURES FOR ORM MODELS TESTING (SYNC)
# ---------------------------------------------
@pytest.fixture(scope="session")
def setup_db():
    print(f"{settings.DB_NAME}")
    assert settings.MODE == "TEST"
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(setup_db):
    with engine.connect() as connection:
        transaction = connection.begin()
        test_session = Session(bind=connection)
        yield test_session
        test_session.close()
        transaction.rollback()


# ---------------------------------------------
# FIXTURES FOR FAST API TESTING (ASYNC)
# ---------------------------------------------
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_setup_db():
    print(f"{settings.DB_NAME}")
    assert settings.MODE == "TEST"
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_engine.dispose()


@pytest_asyncio.fixture
async def setup_async_session(async_setup_db):
    async with async_engine.connect() as connection:
        async with connection.begin() as transaction:
            test_async_session = async_session(
                bind=connection,
                join_transaction_mode="create_savepoint")
            try:
                yield test_async_session
            finally:
                await transaction.rollback()
                await test_async_session.close()
