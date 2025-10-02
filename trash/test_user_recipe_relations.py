import pytest
from sqlalchemy import select
from recipe_service.models.recipes import Recipe, UserRecipe
from user_service.models.users import User

@pytest.mark.asyncio
async def test_user_deletion_sets_recipe_author_to_null(
        async_session, setup_base_dependencies, recipe_data
):
    """
    Проверка межсхемной связи: User (users) -> Recipe (recipes) с ondelete="SET NULL"
    на колонке author_id.
    """
    deps = setup_base_dependencies

    # 1. Создание Recipe, связанного с User
    user_id = deps['user_id']
    recipe = Recipe(author_id=user_id, **recipe_data)
    async_session.add(recipe)
    await async_session.flush()
    recipe_id = recipe.id

    # 2. Удаление User (объект User берем из фикстуры)
    user = deps['user']
    await async_session.delete(user)
    await async_session.commit()

    # 3. Проверка: автор в Recipe должен быть NULL
    # Обновляем состояние объекта из БД
    await async_session.refresh(recipe)

    assert recipe.author_id is None, "author_id не был установлен в NULL после удаления User."

# --------------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_user_recipe_m2m_linkage(
        async_session, setup_base_dependencies, recipe_data
):
    """
    Проверка связи User -> UserRecipe (пользовательская версия рецепта).
    Проверка ON DELETE CASCADE при удалении User.
    """
    deps = setup_base_dependencies

    # 1. Создание Recipe и UserRecipe
    base_recipe = Recipe(author_id=deps['user_id'], **recipe_data)
    async_session.add(base_recipe)
    await async_session.flush()

    user_recipe = UserRecipe(
        base_recipe_id=base_recipe.id,
        user_id=deps['user_id'],
        language_id=deps['language_id'],
        title="My Custom Pasta",
        instructions="Cook it."
    )
    async_session.add(user_recipe)
    await async_session.commit()
    user_recipe_id = user_recipe.id

    # 2. Удаление User
    user = deps['user']
    await async_session.delete(user)
    await async_session.commit()

    # 3. Проверка: UserRecipe должен быть удален (CASCADE)
    stmt_ur = select(UserRecipe).where(UserRecipe.id == user_recipe_id)
    deleted_ur = (await async_session.execute(stmt_ur)).scalar_one_or_none()

    assert deleted_ur is None, "UserRecipe не был удален каскадно после удаления User."