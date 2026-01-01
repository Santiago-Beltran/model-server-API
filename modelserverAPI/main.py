import logging
import xgboost as xgb
from requests import Request

from contextlib import asynccontextmanager

import requests

import numpy as np
from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from asgi_correlation_id import CorrelationIdMiddleware

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from modelserverAPI.logging_conf import configure_logging
from modelserverAPI.models.usage import RawInput, ProcessedData, PredictionOut
from modelserverAPI.machine_learning.load_model import load_model
from modelserverAPI.machine_learning.preprocess import transform_data

from modelserverAPI.config import config

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address, default_limits=[config.REQUEST_LIMIT_PER_MINUTE])

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(CorrelationIdMiddleware)

# Global rate limit
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

api_key_header = APIKeyHeader(name=config.API_KEY_NAME)
app.state.ml_model = load_model()


# Auth dependency
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == config.API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate API KEY",
        )


@app.post("/predict", response_model=float)
async def get_prediction(info: RawInput, api_key: str = Security(get_api_key)):
    transformed_data: ProcessedData = transform_data(info)
    data = transformed_data.model_dump()
    model: xgb.sklearn.XGBModel = app.state.ml_model

    logger.debug("Generating Prediction...")
    X = np.array([list(data.values())])

    prediction = model.predict(X)[0]

    return float(1)
