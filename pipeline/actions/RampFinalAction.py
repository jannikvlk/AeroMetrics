import re
import json


def extract(message: str):
    typos = {
        "BAG_LOZY_ITEMS_GEN": "BAG_LOAD_ITEMS_GEN",
        "LOZYING_INSTRUCTION": "LOADING_INSTRUCTION",
        "LOZYSHEET": "LOADSHEET",
    }  # Fix typos in the messages from zyxw
    for key, value in typos.items():
        message = message.replace(key, value)

    if "STATUS" in message:
        """ 
        Example Message: 'STATUS LOADING_INSTRUCTION 1 FUEL 4 AIRCRAFT_CONFIG 1 EZFW 3 CARGO_FINAL 1 
        RAMP_FINAL 1 CARGO_TRANSFER 1 CABIN_CONFIG 1 CALC_HIST_DATA 1 CHECK_IN_OPEN 1 AUTO_MODE_ACTIVE 1 AUTOMATION_STARTED 0 BAG_LOAD_ITEMS_GEN 1 EZFW_COUNTER 3 REGISTRATION 1 REGISTRATION_CHANGE 5'
        
        All the keys are separated by a space and the values are the next element in the list.
        """

        keys = [
            "AIRBORNE",
            "AIRCRAFT_CONFIG",
            "ALLOWANCE_CHECK_PERFORMED",
            "AUTOMATION_STARTED",
            "AUTO_MODE_ACTIVE",
            "BAG_LOAD_ITEMS_GEN",
            "BAG_LOZY_ITEMS_GEN",
            "BAG_ULD_ORD",
            "CABIN_CONFIG",
            "CALC_HIST_DATA",
            "CARGO_FINAL",
            "CARGO_TRANSFER",
            "CHECK_IN_FINAL",
            "CHECK_IN_OPEN",
            "DGR_ITEMS",
            "EZFW",
            "EZFW_COUNTER",
            "FINAL_RELEASE",
            "FUEL",
            "FUEL_ORDER",
            "LDM",
            "LOADING_INSTRUCTION",
            "LOADSHEET",
            "LOZYING_INSTRUCTION",
            "LOZYSHEET",
            "OFFBLOCK",
            "OFP",
            "PDM",
            "RAMP_FINAL",
            "REGISTRATION",
            "REGISTRATION_CHANGE",
            "TRANSIT_ACCEPTANCE",
            "TRANSIT_PAX",
        ]

        # Initialize dictionary with None for all keys
        data = {key: None for key in keys}

        # Split the message into parts
        parts = message.split()

        # Iterate through parts and extract key-value pairs
        i = 0
        while i < len(parts):
            if parts[i] in keys:
                key = parts[i]
                if i + 1 < len(parts) and re.match(r"^-?\d+(\.\d+)?$", parts[i + 1]):
                    value = parts[i + 1]
                    data[key] = int(value)
                    i += 2
                else:
                    i += 1
            else:
                i += 1

        return json.dumps(data)
    if "Discrepancy check result" in message:
        """ Example Message: 'Discrepancy check result\r\n
        Discrepancy happend: true\r\n
        Discrepancies\r\n 
        Type                      Destination               Bag pieces                Bag 
        weight               \r\nLOZYTABLE                  REC                       
        170                       3400.00 KG                \r\nCKI                        
        REC                       0                         0.00    KG                
        \r\nSUM                        REC                       170                       3400.00 KG'

        The message is formatted like a table with some information in a header.
        Data is extracted into a dictionary with the following structure:
        {'Discrepancy check result': 
            {
                'Discrepancy happened': True
            },
        'Discrepancies': 
            [
                {
                    'Type': 'LOADTABLE',
                    'Destination': 'REC',
                    'Bag pieces': 298,
                    'Bag weight': 5960.0
                },
                {   
                    'Type': 'CKI', 
                    'Destination': 'REC', 
                    'Bag pieces': 0, 
                    'Bag weight': 0.0
                },
                {
                    'Type': 'SUM',
                    'Destination': 'REC',
                    'Bag pieces': 298,
                    'Bag weight': 5960.0
                }
            ]
        }
    
        
        LOADTABLE: This might refer to the planned or documented load of baggage for a specific flight or destination.
        CKI: This could stand for "Check-In," referring to the actual bags checked in for the flight.
        SUM: This represents the summary or difference between the planned/documented load and the actual checked-in load.
        """
        # Initialize an empty dictionary
        result = {"Discrepancy check result": {}, "Discrepancies": []}

        # Split the report into lines
        lines = message.split("\n")


        # Parse the first part of the report
        result["Discrepancy check result"]["Discrepancy happened"] = (
            lines[1].split(": ")[1].strip() == "true"
        )

        # Parse the discrepancies
        for line in lines[
            4:7
        ]:  # One error in the data where the loadtable is repeated twice
            
            if line.strip():
                columns = line.split()
                discrepancy = {
                    "Type": columns[0],
                    "Destination": columns[1],
                    "Bag pieces": int(columns[2]),
                    "Bag weight": float(columns[3].replace("KG", "").strip()),
                }
                result["Discrepancies"].append(discrepancy)

        return json.dumps(result)
    if "Caller user" in message:
        """ This does not include weight data. e.g.:
        'Caller user             : human\r\n
        Close ramp              : true\r\n
        Check discrepancy       : false\r\n
        User name               : Louis Lupoyo\r\n
        Confirmation message    : This aircraft has been loaded in accordance with mnop air loading 
        instructions. I have instructed the high loader driver to engage all restraining locks and nets.'
        """
        return None
    raise NotImplementedError("This message is not supported yet")
