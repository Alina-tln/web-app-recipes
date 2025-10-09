import pytest
from sqlalchemy import select
from recipe_service.models import ingredients_models as models
from recipe_service.services.ingredient_service import IngredientService, IngredientAlreadyExists, IngredientNotFound

@pytest.mark.asyncio
async def test_create_ingredient_ok(session):
    cat = models.Category(name="Vegetables")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    service = IngredientService(session)
    ingredient = await service.create_ingredient("Tomato", [cat.id])

    assert ingredient.name == "Tomato"
    assert ingredient.categories[0].name == "Vegetables"


@pytest.mark.asyncio
async def test_create_ingredient_duplicate_name(session):
    cat = models.Category(name="Spices")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    service = IngredientService(session)
    await service.create_ingredient("Salt", [cat.id])

    with pytest.raises(IngredientAlreadyExists):
        await service.create_ingredient("Salt", [cat.id])


@pytest.mark.asyncio
async def test_create_ingredient_invalid_categories(session):
    service = IngredientService(session)
    with pytest.raises(ValueError, match="Some categories not found"):
        await service.create_ingredient("Cheese", [999])


@pytest.mark.asyncio
async def test_update_ingredient_name(session):
    cat = models.Category(name="Fruits")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    service = IngredientService(session)
    ing = await service.create_ingredient("Apple", [cat.id])
    updated = await service.update_ingredient(ing.id, new_name="Green Apple")

    assert updated.name == "Green Apple"


@pytest.mark.asyncio
async def test_update_ingredient_name_conflict(session):
    cat = models.Category(name="Dairy")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    service = IngredientService(session)
    await service.create_ingredient("Milk", [cat.id])
    ing2 = await service.create_ingredient("Cream", [cat.id])

    with pytest.raises(IngredientAlreadyExists):
        await service.update_ingredient(ing2.id, new_name="Milk")


@pytest.mark.asyncio
async def test_update_ingredient_categories_only(session):
    cat1 = models.Category(name="Protein")
    cat2 = models.Category(name="Vegan")
    session.add_all([cat1, cat2])
    await session.commit()
    await session.refresh(cat1)
    await session.refresh(cat2)

    service = IngredientService(session)
    ing = await service.create_ingredient("Tofu", [cat1.id])
    updated = await service.update_ingredient(ing.id, categories=[cat2.id])

    assert updated.categories[0].name == "Vegan"


@pytest.mark.asyncio
async def test_update_ingredient_not_found(session):
    service = IngredientService(session)
    with pytest.raises(IngredientNotFound):
        await service.update_ingredient(999, new_name="Fake")


@pytest.mark.asyncio
async def test_delete_ingredient_ok(session):
    cat = models.Category(name="Herbs")
    session.add(cat)
    await session.commit()
    await session.refresh(cat)

    service = IngredientService(session)
    ing = await service.create_ingredient("Basil", [cat.id])
    deleted_name = await service.delete_ingredient(ing.id)

    assert deleted_name == "Basil"


@pytest.mark.asyncio
async def test_delete_ingredient_not_found(session):
    service = IngredientService(session)
    with pytest.raises(IngredientNotFound):
        await service.delete_ingredient(999)
