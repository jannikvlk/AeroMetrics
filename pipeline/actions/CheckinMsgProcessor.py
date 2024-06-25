import re
import json
import numpy as np

from actions.remove_typos import remove_typos


def extract(message: str) -> str | None:
    message = remove_typos(message)
    patterns = {
        "aircraft_regTailNbr": r"<(?:n:)?regTailNbr>\s*(.*?)\s*<\/(?:n:)?regTailNbr>",
        "aircraftType": r"<(?:n:)?aircraftType>\s*(.*?)\s*<\/(?:n:)?aircraftType>",
        "aircraft_configuration": r"<(?:n:)?configuration>\s*(.*?)\s*<\/(?:n:)?configuration>",
    }

    if '<?xml version="1.0" encoding="UTF-8"?>' in message:
        # Dictionary to store the extracted values
        extracted_data = {}

        # Extract data using re
        for key, pattern in patterns.items():
            match = re.search(pattern, message)
            if match:
                extracted_data[key] = match.group(1)
            else:
                extracted_data[key] = np.nan

        return json.dumps(extracted_data)

    elif "The message was processed successfully" in message:
        pass
    else:
        print(message)
        pass
