import re
import json

ACTION = "UpdateFuelDataAction"

"""
The UpdateFuelDataAction includes Final Zero Fuel Weight

ATOW = FZFW + Total Fuel (trip fuel + take off fuel + taxi fuel)

"""

def extract(message):
    if "com.onesystem.lc2.fuelhandling.dto.FuelDTO" in message:
        keys_to_extract = ['FZFW', 'Trip Fuel', 'Take Off Fuel', 'Taxi Fuel']
        dict_keys = ["final_zfw", "trip_fuel", "taxi_fuel", "take_off_fuel"]
        extracted_data = {}

        atow = 0
        for i in range(0, len(keys_to_extract)):
            match = re.search(rf'{keys_to_extract[i]}\s*:\s*([\d.]+)\s*KG', message)
            if match:
                value = float(match.group(1))
                extracted_data[dict_keys[i]] = value
                
                atow += float(value)

        extracted_data["ATOW"] = atow

        return json.dumps(extracted_data)

    elif "STATUS LOADING_INSTRUCTION" or "STATUS LOADSHEET 1" in message:
        keys_to_extract = ['trip', 'takeoff', 'taxi']
        dict_keys = ["trip_fuel", "taxi_fuel", "take_off_fuel"]
        extracted_data = {}

        for i in range(0, len(keys_to_extract)):
            match = re.search(rf'{keys_to_extract[i]}=(\d+\.\d+)\s*KG', message)
            if match:
                value = float(match.group(1))
                extracted_data[dict_keys[i]] = value

        return json.dumps(extracted_data)
    else:
        pass

