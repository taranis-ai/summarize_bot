from summarize_bot.config import Config
from taranis_base_bot import create_app
from taranis_base_bot.log import logger
from typing import Any

def request_parser(data: dict) -> dict[str, Any]:
    if unexpected_keys := set(data) - set(Config.PAYLOAD_SCHEMA):
        logger.warning(f"The payload contains unexpected keys: {unexpected_keys}")

    accepted_data = {}
    for key, key_schema in Config.PAYLOAD_SCHEMA.items():
        if not key_schema.get("required", True) and key not in data:
            continue

        if key not in data:
            raise ValueError(f"Payload does not contain '{key}' key!")

        val = data.get(key)
        if val is None or (isinstance(val, (tuple, list, str)) and not val):
            raise ValueError(f"No data provided for '{key}' key!")

        data_type = key_schema.get("type")

        if data_type and not isinstance(val, (list, str)): 
            raise ValueError(f"Data for '{key}' is not of type '{data_type}'")
        accepted_data[key] = data[key]
    return accepted_data

app = create_app(Config.PACKAGE_NAME, Config, request_parser=request_parser)
