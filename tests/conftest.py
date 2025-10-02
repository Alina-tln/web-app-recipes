import pytest

from database import engine, settings
from db_base import Base
from sqlalchemy.orm import  Session


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


