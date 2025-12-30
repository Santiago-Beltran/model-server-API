from modelserverAPI.config.valid_fields import VALID_FIELDS

ERROR_MESSAGES = {
    "validity": {
        "city": f"city must be one of the following: {VALID_FIELDS['city']}",
        "property_type": f"property type must be one of the following: {VALID_FIELDS['property_type']}",
        "strata": f"strata must be one of the following: {VALID_FIELDS['strata']}",
        "area": "area must be between 30 m2 to 10_000 m2",
        "built_area": "built area must be between 30 m2 to 5_000 m2",
        "rooms": "room number must be bigger than 0 and smaller than 10",
        "bathrooms": "bathroom number must be bigger than 0 and smaller than 10",
        "parking_spots": "parking spots number must be bigger or equal than 0 and smaller than 10",
        "has_pool": "has_pool must be a boolean",
        "has_sauna_jacuzzi_or_turkish_bath": "has_sauna_jacuzzi_or_turkish_bath must be boolean",
        "antiquity": f"antiquity must be one of the following: {VALID_FIELDS['antiquity']}",
        "latitude": f"latitude doesn't match Aburra's Valley",
        "longitude": f"longitude doesn't match Aburra's Valley",
    }
}
