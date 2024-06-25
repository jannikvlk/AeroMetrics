import re
import json

from actions.remove_typos import remove_typos

"""
The UpdateFuelDataAction includes Final Zero Fuel Weight

ATOW = FZFW + Total Fuel (trip fuel + take off fuel + taxi fuel)

"""


def extract(message: str) -> str | None:
    message = remove_typos(message)
    if "fuelhandling.dto.FuelDTO" in message:
        keys_to_extract = ["FZFW", "Trip Fuel", "Take Off Fuel", "Taxi Fuel"]
        dict_keys = ["final_zfw", "trip_fuel", "taxi_fuel", "take_off_fuel"]
        extracted_data = {}

        atow = 0
        for i in range(0, len(keys_to_extract)):
            match = re.search(rf"{keys_to_extract[i]}\s*:\s*([\d.]+)\s*KG", message)
            if match:
                value = float(match.group(1))
                extracted_data[dict_keys[i]] = value

                atow += float(value)

        extracted_data["ATOW"] = atow

        return json.dumps(extracted_data)

    elif "STATUS LOADING_INSTRUCTION" in message or "STATUS LOADSHEET" in message:
        keys_to_extract = ["trip", "takeoff", "taxi"]
        dict_keys = ["trip_fuel", "taxi_fuel", "take_off_fuel"]
        extracted_data = {}

        for i in range(0, len(keys_to_extract)):
            match = re.search(rf"{keys_to_extract[i]}=(\d+\.\d+)\s*KG", message)
            if match:
                value = float(match.group(1))
                extracted_data[dict_keys[i]] = value

        return json.dumps(extracted_data)

    if "STATUS AIRCRAFT_CONFIG" in message or "STATUS FUEL" in message:
        # TODO
        return None
    raise NotImplementedError("This message is not supported yet:", message)
