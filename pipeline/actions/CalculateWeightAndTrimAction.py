import re
import json
ACTION = "CalculateWeightAndTrimAction"


def extract(message):

    # skip system row because of lacking information
    if "onesystem" in message:
        pass
    else:
        # pattern to extract infos from string
        pattern = re.compile(r"(\w+(\s\w+)*)\s*:\s*([^\s]+)")
        matches = pattern.findall(message)
        extracted_data = {match[0].strip(): match[2] for match in matches}

        return json.dumps(extracted_data)

