import pytest
from httpx import AsyncClient

from modelserverAPI.config import config

@pytest.fixture
def good_info() -> dict:
    return {
        "city": "itagui",
        "property_type": "apartment",
        "strata": 6,
        "area": 120,
        "built_area": 120,
        "rooms": 3,
        "bathrooms": 2,
        "parking_spots": 1,
        "has_sauna_jacuzzi_or_turkish_bath": True,
        "has_pool": True,
        "antiquity": 2,
        "latitude": 6.1948,
        "longitude": -75.5722,
    }


@pytest.mark.anyio
async def test_predict(async_client: AsyncClient, good_info: dict):
    response = await async_client.post("/predict", json=good_info, headers={config.API_KEY_NAME: config.API_KEY})
    assert response.status_code == 200


@pytest.mark.anyio
async def test_predict_none(async_client: AsyncClient):
    response = await async_client.post("/predict",  headers={config.API_KEY_NAME: config.API_KEY})

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("city", "abc"),
        ("property_type", "abc"),
        ("strata", 7),
        ("strata", -1),
        ("area", 5),
        ("area", 50_000),
        ("area", -1),
        ("built_area", 10),
        ("built_area", 6_000),
        ("rooms", 50),
        ("rooms", -5),
        ("bathrooms", 50),
        ("bathrooms", -5),
        ("bathrooms", "hi"),
        ("property_type", None),
    ],
)
@pytest.mark.anyio
async def test_invalid_fields(
    async_client: AsyncClient,
    good_info: dict,
    field: str,
    bad_value: str | float,
):
    bad_info = good_info
    bad_info[field] = bad_value
    response = await async_client.post("/predict", json=bad_info,  headers={config.API_KEY_NAME: config.API_KEY})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_prediction_unauthorized_bad_key(
    async_client: AsyncClient,
    good_info: dict
):
    response = await async_client.post("/predict", json=good_info, headers={config.API_KEY_NAME: "mumbojumbo"})
    assert response.status_code == 401

@pytest.mark.anyio
async def test_prediction_unauthorized_bad_key_name(
    async_client: AsyncClient,
    good_info: dict
):
    response = await async_client.post("/predict", json=good_info, headers={"mumbojumbo": config.API_KEY})
    assert response.status_code == 401

@pytest.mark.anyio
async def test_prediction_unauthorized_no_headers(
    async_client: AsyncClient,
    good_info: dict
):
    response = await async_client.post("/predict", json=good_info)
    assert response.status_code == 401

