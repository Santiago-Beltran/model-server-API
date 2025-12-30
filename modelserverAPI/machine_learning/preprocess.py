import json
from pydantic import PositiveFloat
from haversine import haversine


from modelserverAPI.models.usage import RawInput, ProcessedData, VALID_FIELDS

NUMBER_OF_PROPERTIES_PER_ZONE = 80

with open("location_and_prices.json") as f:
    data = json.load(f)


def get_mean_price_per_sqm_in_zone(latitude: float, longitude: float) -> PositiveFloat:
    closest = sorted(
        data,
        key=lambda property: haversine(
            (latitude, longitude), (property["latitude"], property["longitude"])
        ),
    )
    closest = closest[:NUMBER_OF_PROPERTIES_PER_ZONE]

    prices = [row["price_per_sqm"] for row in closest]

    mean_sqm_price = sum(prices) / len(prices) if prices else None

    return mean_sqm_price


def get_property_type_booleans(property_type: str) -> tuple:
    if property_type not in VALID_FIELDS["property_type"]:
        return None

    return {
        valid_property_type: (1 if property_type == valid_property_type else 0)
        for valid_property_type in VALID_FIELDS["property_type"]
    }


def get_city_booleans(city: str) -> dict:
    if city not in VALID_FIELDS["city"]:
        return None
    return {
        valid_city: (1 if valid_city == city else 0)
        for valid_city in VALID_FIELDS["city"]
    }


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
        sauna_turkish_bath_jacuzzi=raw_input.bool_sauna_turkishbath_pool,
        pool=raw_input.bool_pool,
        property_type_Apartamento=property_booleans_dict["apartment"],
        property_type_Casa=property_booleans_dict["house"],
        city_Bello=city_booleans_dict["bello"],
        city_Envigado=city_booleans_dict["envigado"],
        city_Itaguí=city_booleans_dict["itagui"],
        city_La_estrella=city_booleans_dict["la estrella"],
        city_Medellín=city_booleans_dict["medellin"],
        city_Sabaneta=city_booleans_dict["sabaneta"],
    )
