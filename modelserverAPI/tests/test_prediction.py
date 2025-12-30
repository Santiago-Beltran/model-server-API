import pytest
from httpx import AsyncClient

from modelserverAPI.models.usage import RawInput
from modelserverAPI.config.error_messages import ERROR_MESSAGES


@pytest.fixture
def good_info() -> dict:
    return {
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
        "longitude": -75.5722,
    }


@pytest.mark.anyio
async def test_predict(async_client: AsyncClient, good_info: dict):
    response = await async_client.post("/predict", json=good_info)
    assert response.status_code == 200

@pytest.mark.anyio
async def test_predict_none(async_client: AsyncClient):
    response = await async_client.post("/predict")

    assert response.status_code == 422

@pytest.mark.parametrize(
    "field, bad_value, error_message",
    [
        ("city", "abc", ERROR_MESSAGES['validity']['city']),
        ("property_type", "abc",  ERROR_MESSAGES['validity']['property_type']),
        ("strata", 7,  ERROR_MESSAGES['validity']['strata']),
        #("strata", -1,  ERROR_MESSAGES['validity']['strata']),
        ("area", 5,  ERROR_MESSAGES['validity']['area']),
        ("area", 50_000,  ERROR_MESSAGES['validity']['area']),
        #("area", -1,  ERROR_MESSAGES['validity']['area']),
        ("built_area", 10,  ERROR_MESSAGES['validity']['built_area']),
        ("built_area", 6_000,  ERROR_MESSAGES['validity']['built_area']),
        ("rooms", 50,  ERROR_MESSAGES['validity']['rooms']),
        #("rooms", -5,  ERROR_MESSAGES['validity']['rooms']),
        ("bathrooms", 50, ERROR_MESSAGES['validity']['bathrooms']),
        #("bathrooms", -5, ERROR_MESSAGES['validity']['bathrooms']),
    ],
)
@pytest.mark.anyio
async def test_invalid_fields(
    async_client: AsyncClient,
    good_info: dict,
    field: str,
    bad_value: str | float,
    error_message: str,
):
    bad_info = good_info
    bad_info[field] = bad_value
    response = await async_client.post("/predict", json=bad_info)

    assert response.status_code == 422
    assert error_message in response.text
