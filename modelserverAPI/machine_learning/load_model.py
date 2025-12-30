import pickle
import xgboost as xgb
from functools import lru_cache
# Load your model


@lru_cache
def load_model() -> xgb.sklearn.XGBRegressor:
    with open("model.pickle", "rb") as f:
        return pickle.load(f)["model"]
