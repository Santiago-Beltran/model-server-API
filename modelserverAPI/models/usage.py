from pydantic import BaseModel, ConfigDict, model_validator, PositiveInt, PositiveFloat
from typing import Literal

from modelserverAPI.config.error_messages import ERROR_MESSAGES
from modelserverAPI.config.valid_fields import VALID_FIELDS


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

    # Validate multiple option fields
    @model_validator(mode="after")
    def validate_multipleoption_fields(self):
        if not self.city in VALID_FIELDS["city"]:
            raise ValueError(ERROR_MESSAGES["validity"]["city"])

        if not self.property_type in VALID_FIELDS["property_type"]:
            raise ValueError(ERROR_MESSAGES["validity"]["property_type"])

        if not self.strata in VALID_FIELDS["strata"]:
            raise ValueError(ERROR_MESSAGES["validity"]["strata"])

        if not self.antiquity in VALID_FIELDS["antiquity"]:
            raise ValueError(ERROR_MESSAGES["validity"]["antiquity"])
        
        return self
    
    @model_validator(mode="after")
    def validate_ranges_of_fields(self):
        if not (30 <= self.area <= 10_000):
            raise ValueError(ERROR_MESSAGES['validity']['area'])
        if not(30 <= self.built_area <= 5_000):
            raise ValueError(ERROR_MESSAGES['validity']['built_area'])
        if not(0 < self.rooms < 10):
            raise ValueError(ERROR_MESSAGES['validity']['rooms'])
        if not(0 < self.bathrooms < 10):
            raise ValueError(ERROR_MESSAGES['validity']['bathrooms'])
        if not(6 <= self.latitude <= 6.5):
            raise ValueError(ERROR_MESSAGES['validity']['latitude'])
        if not(-75.6 <= self.longitude <= -75.3):
            raise ValueError(ERROR_MESSAGES['validity']['longitude'])
        
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