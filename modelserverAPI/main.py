import logging
import xgboost as xgb

from contextlib import asynccontextmanager

import numpy as np
from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware


from modelserverAPI.logging_conf import configure_logging
from modelserverAPI.models.usage import RawInput, ProcessedData, PredictionOut
from modelserverAPI.machine_learning.load_model import load_model
from modelserverAPI.machine_learning.preprocess import transform_data

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)

app.state.ml_model = load_model()


@app.post("/predict", response_model=float)
async def get_prediction(info: RawInput):
    transformed_data: ProcessedData = transform_data(info)
    data = transformed_data.model_dump()
    model: xgb.sklearn.XGBModel = app.state.ml_model

    logger.debug("Generating Prediction...")

    X = np.array([list(data.values())])  # wrap in list to make it 2D

    prediction = model.predict(X)

    return float(prediction[0])
