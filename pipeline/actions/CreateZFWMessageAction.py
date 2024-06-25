import re
import json

from actions.remove_typos import remove_typos


def extract_data_from_xml(xml_string):
    # Use regular expressions to find key-value pairs
    keys = [
        "airline",
        "arrivalStation",
        "departureStation",
        "flightDateLocal",
        "revisionNumber",
        "dryOperatingWeight",
        "actualZFW",
        "cargoWeight",
        "baggageWeight",
        "paxWeight",
        "basicWeight",
    ]

    data_dict = {}
    for key in keys:
        match = re.search(r"<{}>(.*?)</{}>".format(key, key), xml_string)
        if match:
            data_dict[key] = match.group(1)
        else:
            data_dict[key] = None
    return data_dict


def extract(message: str) -> str | None:
    message = remove_typos(message)

    if "Receiver queue" in message:
        extracted_data = extract_data_from_xml(message)
        return json.dumps(extracted_data)

    elif "EmptyDTO - no input expected" in message or "STATUS " in message:
        return None
    raise NotImplementedError("This message is not supported yet:", message)
