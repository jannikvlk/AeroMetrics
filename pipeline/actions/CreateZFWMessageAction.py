import re
import json

ACTION = "CreateZFWMessageAction"

def extract_data_from_xml(xml_string):
    # Use regular expressions to find key-value pairs
    keys = ['airline', 'arrivalStation', 'departureStation', 'flightDateLocal', 'revisionNumber',
            'dryOperatingWeight', 'actualZFW', 'cargoWeight', 'baggageWeight', 'paxWeight', 'basicWeight']

    data_dict = {}
    for key in keys:
        match = re.search(r'<{}>(.*?)</{}>'.format(key, key), xml_string)
        if match:
            data_dict[key] = match.group(1)
        else:
            data_dict[key] = None
    return data_dict

def extract(message):

    if "Receiver queue" in message:
        extracted_data = extract_data_from_xml(message)
        return json.dumps(extracted_data)
    
    elif "EmptyDTO - no input expected" or "STATUS " in message:
        pass
    else: 
        print(message)
        pass
