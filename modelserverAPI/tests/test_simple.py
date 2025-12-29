import pytest
from httpx import AsyncClient

from modelserverAPI.models.usage import RawInput


@pytest.mark.anyio
async def test_predict(async_client: AsyncClient):
    info = {
        "city": "medellin",
        "property_type": "apartment",
        "strata": 6,
        "area": 120,
        "built_area": 120,
        "rooms": 3,
        "bathrooms": 2,
        "parking_spots": 1,
        "bool_sauna_turkishbath_pool": True,
        "bool_pool": True,
        "antiquity": 2,
        "latitude": 6.1948,
        "longitude": -75.5722
    }

    response = await async_client.post("/predict", json=info)

    assert response.json() == 1
