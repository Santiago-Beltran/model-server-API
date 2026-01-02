import time
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
import hiro
from datetime import timedelta

from modelserverAPI.config import config
from modelserverAPI.main import app  # Required for testing rate limits\

from fastapi.testclient import TestClient
from typing import Generator

from modelserverAPI.conftest import client


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
    response = await async_client.post(
        "/predict", json=good_info, headers={config.API_KEY_NAME: config.API_KEY}
    )
    assert response.status_code == 200


@pytest.mark.anyio
async def test_predict_none(async_client: AsyncClient):
    response = await async_client.post(
        "/predict", headers={config.API_KEY_NAME: config.API_KEY}
    )

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
    response = await async_client.post(
        "/predict", json=bad_info, headers={config.API_KEY_NAME: config.API_KEY}
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_prediction_unauthorized_bad_key(
    async_client: AsyncClient, good_info: dict
):
    response = await async_client.post(
        "/predict", json=good_info, headers={config.API_KEY_NAME: "mumbojumbo"}
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_prediction_unauthorized_bad_key_name(
    async_client: AsyncClient, good_info: dict
):
    response = await async_client.post(
        "/predict", json=good_info, headers={"mumbojumbo": config.API_KEY}
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_prediction_unauthorized_no_headers(
    async_client: AsyncClient, good_info: dict
):
    response = await async_client.post("/predict", json=good_info)
    assert response.status_code == 401


# Meant only as a local benchmark
@pytest.mark.anyio
async def test_predict_performance(async_client: AsyncClient, good_info: dict):
    """Meant only as a local benchmark"""

    num_requests = 500
    max_response_time = 1

    async def send_request():
        app.state.limiter.reset()

        start_time = time.time()

        request = await async_client.post(
            "/predict", json=good_info, headers={config.API_KEY_NAME: config.API_KEY}
        )

        assert request.status_code == 200

        return time.time() - start_time

    elapsed_times = [await send_request() for _ in range(num_requests)]

    assert sum(elapsed_times) <= max_response_time


# Test limits
@pytest.mark.anyio
def test_second_request_limit(client: client, good_info: dict):
    request_sent_counter = 0

    request_limit_per_second = int(config.REQUEST_LIMIT_PER_SECOND.split("/")[0])
    request_limit_per_minute = int(config.REQUEST_LIMIT_PER_MINUTE.split("/")[0])

    # Test limits make sense.
    assert request_limit_per_minute <= (request_limit_per_second * 60)

    with hiro.Timeline() as timeline:
        timeline.freeze()

        while request_sent_counter < request_limit_per_minute:
            for _ in range(request_limit_per_second):
                request = client.post(
                    "/predict",
                    json=good_info,
                    headers={config.API_KEY_NAME: config.API_KEY},
                )

                assert request.status_code == 200

                request_sent_counter += 1

            timeline.forward(1)

    request = client.post(
        "/predict", json=good_info, headers={config.API_KEY_NAME: config.API_KEY}
    )

    assert request.status_code == 429
