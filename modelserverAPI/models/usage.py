from enum import Enum
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveFloat,
    PositiveInt,
)


class CityEnum(str, Enum):
    MEDELLIN = "medellin"
    ENVIGADO = "envigado"
    BELLO = "bello"
    ITAGUI = "itagui"
    LA_ESTRELLA = "la_estrella"
    SABANETA = "sabaneta"


class PropertyTypeEnum(str, Enum):
    HOUSE = "house"
    APARTMENT = "apartment"


# Adapt the expected input to your case.
class RawInput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: CityEnum
    property_type: PropertyTypeEnum
    strata: Annotated[int, Field(ge=1, le=6)]
    area: Annotated[float, Field(ge=30, le=10_000)]
    built_area: Annotated[float, Field(ge=30, le=5_000)]
    rooms: Annotated[int, Field(gt=0, lt=10)]
    bathrooms: Annotated[int, Field(gt=0, lt=10)]
    parking_spots: Annotated[int, Field(ge=0, lt=10)]

    has_sauna_jacuzzi_or_turkish_bath: bool
    has_pool: bool

    antiquity: Annotated[int, Field(ge=1, le=5)]

    latitude: Annotated[float, Field(ge=6, le=6.5)]
    longitude: Annotated[float, Field(ge=-75.6, le=-75.3)]


# What the model will be fed with...
# Variables must match column names.
class ProcessedData(BaseModel):
    """This is what the model will be fed with..."""

    model_config = ConfigDict(from_attributes=True)

    zone_mean_price_per_sqm: PositiveFloat
    area_sqm: PositiveFloat
    built_area_sqm: PositiveFloat
    age: Literal[1, 2, 3, 4, 5]
    bedrooms: PositiveInt
    bathrooms: PositiveInt
    parking_spots: int
    strata: Literal[1, 2, 3, 4, 5, 6]
    latitude: float
    longitude: float
    sauna_turkish_bath_jacuzzi: bool
    pool: bool
    property_type_Apartamento: bool
    property_type_Casa: bool
    city_Bello: bool
    city_Envigado: bool
    city_Itaguí: bool
    city_La_estrella: bool
    city_Medellín: bool
    city_Sabaneta: bool

