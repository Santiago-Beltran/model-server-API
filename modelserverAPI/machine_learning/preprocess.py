import json
import numpy as np
from pydantic import PositiveFloat
from modelserverAPI.models.usage import (
    RawInput,
    ProcessedData,
    CityEnum,
    PropertyTypeEnum,
)

NUMBER_OF_PROPERTIES_PER_ZONE = 80

with open("location_and_prices.json") as f:
    data = json.load(f)

DATA_LAT = np.array([row["latitude"] for row in data], dtype=np.float32)
DATA_LON = np.array([row["longitude"] for row in data], dtype=np.float32)
DATA_PRICE = np.array([row["price_per_sqm"] for row in data], dtype=np.float32)

PROPERTY_TYPES = set(PropertyTypeEnum.__members__.values())
CITY_TYPES = set(CityEnum.__members__.values())


def get_mean_price_per_sqm_in_zone(
    latitude: float, longitude: float
) -> PositiveFloat | None:
    dx = DATA_LAT - latitude
    dy = DATA_LON - longitude
    dists = dx * dx + dy * dy
    idx = np.argpartition(dists, NUMBER_OF_PROPERTIES_PER_ZONE)[
        :NUMBER_OF_PROPERTIES_PER_ZONE
    ]
    return float(np.mean(DATA_PRICE[idx])) if idx.size else None


def get_property_type_booleans(property_type: str) -> dict | None:
    if property_type not in PROPERTY_TYPES:
        return None
    return {ptype: int(property_type == ptype) for ptype in PROPERTY_TYPES}


def get_city_booleans(city: str) -> dict | None:
    if city not in CITY_TYPES:
        return None
    return {ctype: int(city == ctype) for ctype in CITY_TYPES}


def transform_data(raw_input: RawInput) -> ProcessedData:
    property_booleans_dict = get_property_type_booleans(raw_input.property_type)
    city_booleans_dict = get_city_booleans(raw_input.city)

    return ProcessedData(
        zone_mean_price_per_sqm=get_mean_price_per_sqm_in_zone(
            raw_input.latitude, raw_input.longitude
        ),
        area_sqm=raw_input.area,
        built_area_sqm=raw_input.built_area,
        age=raw_input.antiquity,
        bedrooms=raw_input.rooms,
        bathrooms=raw_input.bathrooms,
        parking_spots=raw_input.parking_spots,
        strata=raw_input.strata,
        latitude=raw_input.latitude,
        longitude=raw_input.longitude,
        sauna_turkish_bath_jacuzzi=raw_input.has_sauna_jacuzzi_or_turkish_bath,
        pool=raw_input.has_pool,
        property_type_Apartamento=property_booleans_dict["apartment"],
        property_type_Casa=property_booleans_dict["house"],
        city_Bello=city_booleans_dict["bello"],
        city_Envigado=city_booleans_dict["envigado"],
        city_Itaguí=city_booleans_dict["itagui"],
        city_La_estrella=city_booleans_dict["la_estrella"],
        city_Medellín=city_booleans_dict["medellin"],
        city_Sabaneta=city_booleans_dict["sabaneta"],
    )
