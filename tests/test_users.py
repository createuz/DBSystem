import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from database import Base
from main import app
from settings import settings

DATABASE_URL_TEST = settings.DB_URL + "_test"


@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    # Test DB yaratish
    engine = create_async_engine(DATABASE_URL_TEST, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest.mark.anyio
async def test_create_and_get_user(client):
    # Yaratish
    resp = await client.post("/users/", json={
        "username": "testuser",
        "first_name": "Test",
        "language": "en"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "testuser"
    user_id = data["id"]

    # O‘qish
    resp2 = await client.get(f"/users/{user_id}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["first_name"] == "Test"

    # Yangilash
    resp3 = await client.patch(f"/users/{user_id}", json={"first_name": "Updated"})
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["first_name"] == "Updated"
