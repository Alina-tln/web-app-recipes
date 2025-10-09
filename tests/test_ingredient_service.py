import pytest
from recipe_service.models import ingredients_models as models
from recipe_service.services.ingredient_service import (
    IngredientService,
    IngredientAlreadyExists,
    IngredientNotFound,
)


@pytest.mark.asyncio
async def test_create_ingredient_success(setup_async_session, session):
    """Creating an ingredient with a real database"""
    session = setup_async_session
    service = IngredientService(session)

    # Creating categories
    cat1 = models.Category(name="Spices")
    cat2 = models.Category(name="Vegetables")
    session.add_all([cat1, cat2])
    await session.commit()
    await session.refresh(cat1)
    await session.refresh(cat2)

    # Creating ingredient
    ingredient = await service.create_ingredient("Pepper", [cat1.id, cat2.id])

    assert ingredient.id is not None
    assert ingredient.name == "Pepper"
    assert len(ingredient.categories) == 2


@pytest.mark.asyncio
async def test_create_ingredient_duplicate_name(setup_async_session, session):
    session = setup_async_session
    service = IngredientService(session)

    cat = models.Category(name="Fruits")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    await service.create_ingredient("Apple", [cat.id])

    with pytest.raises(IngredientAlreadyExists):
        await service.create_ingredient("Apple", [cat.id])


@pytest.mark.asyncio
async def test_create_ingredient_missing_categories(setup_async_session, session):
    """Error if categories not found"""
    session = setup_async_session
    service = IngredientService(session)

    with pytest.raises(ValueError, match="Some categories not found"):
        await service.create_ingredient("Nonexistent", [999])


@pytest.mark.asyncio
async def test_get_all_ingredients(setup_async_session, session):
    session = setup_async_session
    service = IngredientService(session)

    cat = models.Category(name="Oils")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    ing1 = await service.create_ingredient("Olive oil", [cat.id])
    ing2 = await service.create_ingredient("Sunflower oil", [cat.id])

    result = await service.get_all_ingredients()

    assert len(result) >= 2
    assert {i.name for i in result} >= {"Olive oil", "Sunflower oil"}


@pytest.mark.asyncio
async def test_get_ingredient_by_id_success(setup_async_session, session):
    session = setup_async_session
    service = IngredientService(session)

    cat = models.Category(name="Dairy")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    ing = await service.create_ingredient("Milk", [cat.id])
    found = await service.get_ingredient_by_id(ing.id)

    assert found.id == ing.id
    assert found.name == "Milk"


@pytest.mark.asyncio
async def test_get_ingredient_by_id_not_found(setup_async_session, session):
    session = setup_async_session
    service = IngredientService(session)

    with pytest.raises(IngredientNotFound):
        await service.get_ingredient_by_id(999)


@pytest.mark.asyncio
async def test_update_ingredient_name_and_categories(setup_async_session, session):
    session = setup_async_session
    service = IngredientService(session)

    cat1 = models.Category(name="Sweeteners")
    cat2 = models.Category(name="Natural")
    session.add_all([cat1, cat2])
    await session.commit()
    await session.refresh(cat1)
    await session.refresh(cat2)

    ing = await service.create_ingredient("Sugar", [cat1.id])

    updated = await service.update_ingredient(ing.id, new_name="Cane sugar", categories=[cat1.id, cat2.id])

    assert updated.name == "Cane sugar"
    assert len(updated.categories) == 2


@pytest.mark.asyncio
async def test_update_ingredient_duplicate_name(setup_async_session, session):
    session = setup_async_session
    service = IngredientService(session)

    cat = models.Category(name="Grains")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    ing1 = await service.create_ingredient("Rice", [cat.id])
    ing2 = await service.create_ingredient("Wheat", [cat.id])

    with pytest.raises(IngredientAlreadyExists):
        await service.update_ingredient(ing2.id, new_name="Rice")


@pytest.mark.asyncio
async def test_update_ingredient_invalid_category(setup_async_session, session):
    session = setup_async_session
    service = IngredientService(session)

    cat = models.Category(name="Seafood")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    ing = await service.create_ingredient("Shrimp", [cat.id])

    with pytest.raises(ValueError, match="at least one valid category"):
        await service.update_ingredient(ing.id, categories=[999])


@pytest.mark.asyncio
async def test_delete_ingredient_success(setup_async_session, session):
    session = setup_async_session
    service = IngredientService(session)

    cat = models.Category(name="Beverages")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    ing = await service.create_ingredient("Tea", [cat.id])
    deleted_name = await service.delete_ingredient(ing.id)

    assert deleted_name == "Tea"

    # Checking that it is no longer in the database.
    result = await session.get(models.Ingredient, ing.id)
    assert result is None


@pytest.mark.asyncio
async def test_delete_ingredient_not_found(setup_async_session, session):
    session = setup_async_session
    service = IngredientService(session)

    with pytest.raises(IngredientNotFound):
        await service.delete_ingredient(999)
