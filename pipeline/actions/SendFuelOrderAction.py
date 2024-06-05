import re
import json

ACTION = "SendFuelOrderAction"

"""
No Data for abcd and jsut 4 for zyxw
"""

def extract(message):
        if "PRELIMINARY FUEL ORDER" in message:
            pattern = re.compile(r"\b(\d{3})\b.*?BLOCK FUEL:\s+(\d+)\s+(\w+)", re.DOTALL)

            # Search for matches in the text
            match = pattern.search(message)

            # Initialize the dictionary
            extracted_data = {}

            # If a match is found, extract the data and store it in the dictionary
            if match:
                extracted_data['AircraftType'] = match.group(1)
                extracted_data['BlockFuel'] = match.group(2)
                extracted_data['Metric'] = match.group(3)
                extracted_data['FuelOrderState'] = "PRELIMINARY"

            return json.dumps(extracted_data)


        elif "FINAL FUEL ORDER" in message:
            pattern = re.compile(r"\b(\d{3})\b.*?BLOCK FUEL:\s+(\d+)\s+(\w+)", re.DOTALL)

            # Search for matches in the text
            match = pattern.search(message)

            # Initialize the dictionary
            extracted_data = {}

            # If a match is found, extract the data and store it in the dictionary
            if match:
                extracted_data['AircraftType'] = match.group(1)
                extracted_data['BlockFuel'] = match.group(2)
                extracted_data['Metric'] = match.group(3)
                extracted_data['FuelOrderState'] = "FINAL"

            return json.dumps(extracted_data)

        elif "com.systemone.lc2.common.dto.SendDocumentDTO" in message:
            pass

        else:
            print(message)
            pass
    