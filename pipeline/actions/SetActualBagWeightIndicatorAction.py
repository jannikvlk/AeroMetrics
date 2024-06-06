import re
import json

ACTION = "SetActualBagWeightIndicatorAction"

def extract(message):

    if message != None: 
        pattern = re.compile(r'(\w+):\s*([^ ]+)')
        matches = pattern.findall(message)

        extracted_data = {key: value for key, value in matches}

        return json.dumps(extracted_data)

    elif message == None:
        pass
    else:
        print(message)
        pass

