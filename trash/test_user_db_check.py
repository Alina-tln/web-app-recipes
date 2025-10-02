import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.models.users import User

@pytest.mark.asyncio # 👈 Шаг 2: Делаем тест асинхронным
async def test_user_is_persisted_in_db(
        async_session: AsyncSession, # 👈 Шаг 2: Запрашиваем асинхронную сессию
        test_user_fixture: User       # 👈 Шаг 2: Запрашиваем сохраненного пользователя
):
    """
    Проверяет, что объект User, созданный фикстурой, действительно существует в базе данных
    и может быть извлечен.
    """

    # User уже создан и сохранен в сессии благодаря test_user_fixture.
    user_id_to_check = test_user_fixture.id

    # 1. Сбросим сессию, чтобы гарантировать, что данные берутся из БД, а не из кэша сессии.
    await async_session.expunge_all()

    # 2. Выполняем SELECT запрос, чтобы проверить существование
    stmt = select(User).where(User.id == user_id_to_check)
    result = await async_session.execute(stmt)

    user_from_db = result.scalar_one_or_none()

    # 3. Проверка
    assert user_from_db is not None, "Пользователь не найден в БД."
    assert user_from_db.email == "test_user_for_check@example.com"
