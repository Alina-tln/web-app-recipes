import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Any, Generator

from recipe_service.main import app
from recipe_service.pydantic_schemas.ingredients import CategoryReadSchema

# The setup_async_session fixture from conftest.py will provide us with a transactional AsyncSession

# ----------------------------------------------------------------------
# Fixture for overriding the session dependency
# ----------------------------------------------------------------------

# In tests, we need the ability to "inject" a test session into FastAPI.
# To do this, we override the get_session dependency.
@pytest.fixture
def override_get_session(setup_async_session: AsyncSession) -> Generator[None, Any, None]:
    """
    Creates an override function for the FastAPI get_session dependency,
    which always returns a test session with a transaction rollback.
    """
    async def _get_session_override():
        yield setup_async_session

    # Apply the override for the duration of the tests
    app.dependency_overrides[app.dependency_overrides.get("get_session", object())] = _get_session_override
    # In SQLAlchemy 2.0 with AsyncSession, you must use an explicit import
    # from the module where the get_session function is defined
    from recipe_service.main import get_session
    app.dependency_overrides[get_session] = _get_session_override

    yield

    # Clear the override after the tests are complete
    app.dependency_overrides.clear()


# ----------------------------------------------------------------------
# Fixture for an asynchronous client
# ----------------------------------------------------------------------

@pytest.fixture
async def client(override_get_session):
    """
    An asynchronous HTTP client for calling FastAPI endpoints.
    Depends on override_get_session to use the test database.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# ----------------------------------------------------------------------
# 3. CRUD FOR CATEGORIES
# ----------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_category_success(client: AsyncClient):
    """Testing successful category creation."""
    response = await client.post(
        "/ingredient_category",
        json={"name": "Dairy"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Dairy"
    assert "id" in data
    assert isinstance(data["id"], int) and data["id"] > 0

@pytest.mark.asyncio
async def test_create_category_already_exists(client: AsyncClient):
    """Testing creation of existing category (HTTP 409)."""
    category_name = "Vegetables"
    await client.post(
        "/ingredient_category",
        json={"name": category_name}
    )
    response = await client.post(
        "/ingredient_category",
        json={"name": category_name}
    )

    assert response.status_code == 409
    assert "Category 'Vegetables' already exists." in response.json()["detail"]


@pytest.mark.asyncio
async def test_read_all_categories_empty(client: AsyncClient):
    """Testing getting all categories when the database is empty."""
    response = await client.get("/ingredient_category")

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_read_all_categories_populated(client: AsyncClient):
    """Testing getting all categories when the database is full."""
    await client.post("/ingredient_category", json={"name": "Meat"})
    await client.post("/ingredient_category", json={"name": "Fruits"})

    response = await client.get("/ingredient_category")

    assert response.status_code == 200
    categories = response.json()
    assert len(categories) == 2
    CategoryReadSchema.model_validate(categories[0])


@pytest.mark.asyncio
async def test_read_category_by_id_success(client: AsyncClient):
    """Testing successful acquisition of category by ID."""
    # Создаем категорию и получаем ее ID
    create_resp = await client.post("/ingredient_category", json={"name": "Nuts"})
    category_id = create_resp.json()["id"]

    response = await client.get(f"/ingredient_category/{category_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "Nuts"

@pytest.mark.asyncio
async def test_read_category_by_id_not_found(client: AsyncClient):
    """Testing getting a non-existent category (HTTP 404)."""
    response = await client.get("/ingredient_category/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"

@pytest.mark.asyncio
async def test_update_category_success(client: AsyncClient):
    """Testing a successful category update."""
    create_resp = await client.post("/ingredient_category", json={"name": "Bread"})
    category_id = create_resp.json()["id"]

    update_resp = await client.put(
        f"/ingredient_category/{category_id}",
        json={"name": "Bakery"}
    )

    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["id"] == category_id
    assert data["name"] == "Bakery"

    get_resp = await client.get(f"/ingredient_category/{category_id}")
    assert get_resp.json()["name"] == "Bakery"

@pytest.mark.asyncio
async def test_update_category_not_found(client: AsyncClient):
    """Testing updating a non-existent category (HTTP 404)."""
    response = await client.put(
        "/ingredient_category/999",
        json={"name": "New name"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"

@pytest.mark.asyncio
async def test_delete_category_success(client: AsyncClient):
    """Testing successful deletion of a category."""
    create_resp = await client.post("/ingredient_category", json={"name": "Spices"})
    category_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/ingredient_category/{category_id}")

    assert delete_resp.status_code == 200
    data = delete_resp.json()
    assert data["Result"] is True
    assert data["id"] == category_id
    assert data["name"] == "Spices"

    get_resp = await client.get(f"/ingredient_category/{category_id}")
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_delete_category_not_found(client: AsyncClient):
    """Testing deletion of non-existent category (HTTP 404)."""
    response = await client.delete("/ingredient_category/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"