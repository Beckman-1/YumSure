import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import engine, AsyncSessionLocal
from app.services.seeder import seed_database
from app.core.security import create_access_token

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session", autouse=True)
async def seed_test_database():
    async with AsyncSessionLocal() as session:
        await seed_database(session)
    yield
    await engine.dispose()

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_headers():
    def _make_headers(user_id: str = "default", email: str = "demo@yumsure.app"):
        token = create_access_token({"sub": user_id, "email": email})
        return {"Authorization": f"Bearer {token}"}
    return _make_headers
