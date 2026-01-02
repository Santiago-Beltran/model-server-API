import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

os.environ["ENV_STATE"] = "test"

from modelserverAPI.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app)


@pytest.fixture()
async def async_client(client) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=client.base_url
    ) as ac:
        yield ac


@pytest.fixture(autouse=True)
def reset_limiter() -> None:
    app.state.limiter.reset()
