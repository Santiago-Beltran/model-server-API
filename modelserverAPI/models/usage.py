from pydantic import BaseModel, ConfigDict, model_validator, PositiveInt, PositiveFloat
from typing import Literal


VALID_PROPERTY_TYPES = ('house', 'apartment')
VALID_CITIES = ("bello", "envigado", "itagui", "la estrella", "medellin", "sabaneta")
VALID_STRATA = (1, 2, 3, 4, 5, 6)
VALID_ANTIQUITY = (1, 2, 3, 4, 5)

# Adapt the expected input to your case.
class RawInput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str
    property_type: str
    strata: PositiveInt
    area: PositiveFloat
    built_area: PositiveFloat
    rooms: PositiveInt
    bathrooms: PositiveInt
    parking_spots: int

    bool_sauna_turkishbath_pool: bool
    bool_pool: bool

    antiquity: PositiveInt

    latitude: float
    longitude: float

    # Validate accordingly
    @model_validator(mode="after")
    def validate_property_type(self):
        if self.property_type not in VALID_PROPERTY_TYPES:
            raise ValueError(f"property type must be one of the following: {VALID_PROPERTY_TYPES}")
        return self

    @model_validator(mode="after")
    def validate_city(self):
        if self.city not in VALID_CITIES:
            raise ValueError(f"city must be one of the following: {VALID_CITIES}")
        return self


    @model_validator(mode="after")
    def validate_strata(self):
        if self.strata not in VALID_STRATA:
            raise ValueError(f"strata must be one of the following: {VALID_STRATA}")
        return self
        

    @model_validator(mode="after")
    def validate_antiquity(self):
        if self.antiquity not in VALID_ANTIQUITY:
            raise ValueError(f"antiquity must be one of the following: {VALID_ANTIQUITY}")
        return self

    @model_validator(mode="after")
    def validate_areas(self):
        if self.built_area > self.area:
            raise ValueError("built_area must be smaller than area")
        return self

    @model_validator(mode="after")
    def validate_location(self):
        if not (6.1 <= self.latitude <= 6.4):
            raise ValueError("location provided is outside of Aburra's Valley")
        if not (-75.65 <= self.longitude <= -75.50):
            raise ValueError("location provided is outside of Aburra's Valley")
        return self
        
    @model_validator(mode="after")
    def validate_parking_spots(self):
        if not (0 <= self.parking_spots):
            raise ValueError("parking spots must be greater than or equal to zero")
        return self
        
# What should be the result of processing the data...
class ProcessedData(BaseModel):
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

# Output of the prediction, return the given data for traceability purposes
class PredictionOut(RawInput):
    prediction: PositiveFloat


