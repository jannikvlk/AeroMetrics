import re
import json

ACTION = "StoreRegistrationAndConfigurationAc"


def extract(message):
    if "Water(%)" in message:
        pattern = re.compile(r"Start Weight\s*:\s*([\d.]+)\s*(\w+)\s*.*?Total Weight:\s*([\d.]+)\s*(\w+)", re.DOTALL)

        # Search for matches in the text
        match = pattern.search(message)

        # Initialize the dictionary
        extracted_data = {}

        # If a match is found, extract the data and store it in the dictionary
        if match:
            extracted_data['start_weight'] = float(match.group(1))
            extracted_data['start_weight_metric'] = match.group(2)
            extracted_data['basic_empty_weight'] = float(match.group(3))
            extracted_data['basic_empty_weight_metric'] = match.group(4)

        return json.dumps(extracted_data)
    elif "systemone" or "onesystem" in message:
        pass
    else:
        print(message)
        pass