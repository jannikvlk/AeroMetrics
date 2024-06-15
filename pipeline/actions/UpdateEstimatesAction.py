import json, re


def extract(message: str):




    if "Pax Weight =" in message:
        """Pax Weight = 11850.0 KG Bag Weight = 1920.0 KG Cargo = 56.1 KG Mail = 0.0 KG DOW = 44584.0 KG ZFW = 56434.0 KG\r\n
            STATUS FUEL 2 AIRCRAFT_CONFIG 1 EZFW 2 CARGO_TRANSFER 1 CABIN_CONFIG 1 CALC_HIST_DATA 1 AUTO_MODE_ACTIVE 1 AUTOMATION_STARTED 0 BAG_LOAD_ITEMS_GEN 1 EZFW_COUNTER 2 REGISTRATION 1 REGISTRATION_CHANGE 2',"""

        # Initialize an empty dictionary to store key-value pairs
        all_keys = {
            "AIRCRAFT_CONFIG",
            "AUTOMATION_STARTED",
            "AUTO_MODE_ACTIVE",
            "BAG_LOAD_ITEMS_GEN",
            "Bag Weight",
            "CABIN_CONFIG",
            "CALC_HIST_DATA",
            "CARGO_FINAL",
            "CARGO_TRANSFER",
            "CHECK_IN_OPEN",
            "Cargo",
            "DGR_ITEMS",
            "DOW",
            "EZFW",
            "EZFW_COUNTER",
            "FUEL",
            "FUEL_ORDER",
            "Mail",
            "OFP",
            "Pax Weight",
            "REGISTRATION",
            "REGISTRATION_CHANGE",
            "TRANSIT_ACCEPTANCE",
            "TRANSIT_PAX",
            "Weight Unit",
            "ZFW",
        }

        # Initialize the dictionary with None for all keys
        key_value_pairs = {key: None for key in all_keys}

        # Split the message into two parts
        parts = message.split("\r\n")
        main_part = parts[0]
        status_part = parts[1]

        # Define the expected keywords and units for weights
        weight_keywords = ["Pax Weight", "Bag Weight", "Cargo", "Mail", "DOW", "ZFW"]

        # Process the weight-related part
        for keyword in weight_keywords:
            pattern = rf"{keyword}\s*=\s*([-+]?[0-9]*\.?[0-9]+)\s*([a-zA-Z]+)"
            match = re.search(pattern, main_part)
            if match:
                value, unit = match.groups()
                key_value_pairs[keyword] = (
                    float(value.strip()) if "." in value.strip() else int(value.strip())
                )
                key_value_pairs["Weight Unit"] = (
                    unit.strip()
                )  # Assuming only one unit is present in the message

        # Process the status-related part
        status_pairs = status_part.split()
        status_pairs.pop(0)  # Remove the 'STATUS' keyword

        for i in range(0, len(status_pairs), 2):
            if i + 1 < len(status_pairs):
                key = status_pairs[i]
                value = status_pairs[i + 1]
                # Convert value to int or float if it is a number
                if value.isdigit():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                key_value_pairs[key] = value

        return json.dumps(key_value_pairs)
    if (
        "com.onesystem.lc2.estimateshandling.dto.EstimateWeightsDTO" in message
        or "com.systemone.lc2.estimateshandling.dto.EstimateWeightsDTO" in message
    ):
        
        """com.onesystem.lc2.estimateshandling.dto.EstimateWeightsDTO [ id = 543038  flightId = 517633 legId = 543038  deleted = false  fragmentId = EstimatesFragment ]\r\n\r\n 
        Pax                 : 160                       Pax Weight          : 11850.0    KG \r\n 
        Bag                 : 120                       Bag Weight          : 1800.0     KG \r\n
        Cargo                                                               : 700.0      KG \r\n
        Mail                                                                : 66.0       KG \r\n 
        Tare                : 0                                             : 0.0        KG \r\n
        ------------------------------------------------------------------------------------------------------------------------\r\n 
        Traffic Load                                                        : 14416.0    KG \r\n 
        DOW                                                                 : 44584.0    KG \r\n
        ------------------------------------------------------------------------------------------------------------------------\r\n 
        EZFW                                                                : 59000.0    KG\r\n 
        Remark              :',



        """

        """Explanation EstimateWeightsDTO Object:

        id: 543038
        flightId: 517633
        legId: 543038
        deleted: false
        fragmentId: EstimatesFragment
        Weights:

        Pax (Passengers): 160
        Pax Weight: 11850.0 KG
        Bag (Baggage): 120
        Bag Weight: 1800.0 KG
        Cargo: 700.0 KG
        Mail: 66.0 KG
        Tare: 0
        Tare Weight: 0.0 KG
        Traffic Load: 14416.0 KG

        DOW (Dry Operating Weight): 44584.0 KG

        EZFW (Estimated Zero Fuel Weight): 59000.0 KG

        Remark: (Empty in this case)"""
        # Initialize an empty dictionary to store key-value pairs
        key_value_pairs = {}

        # Define a function to convert values to int or float
        def convert_to_number(value):
            try:
                if "." in value:
                    return float(value)
                return int(value)
            except ValueError:
                return value

        # Extract the DTO section
        dto_part = re.search(
            r"com\.(?:onesystem|systemone)\.lc2\.estimateshandling\.dto\.EstimateWeightsDTO \[ ([^\]]+)\]",
            message,
        )
        if dto_part:
            dto_pairs = re.findall(r"(\w+)\s*=\s*([\w.]+)", dto_part.group(1))
            for key, value in dto_pairs:
                key_value_pairs[key] = convert_to_number(value)

        # Extract weights and other details
        weights_part = message.split("\r\n\r\n", 2)[-1]
        weight_lines = weights_part.split("\r\n")

        weight_keywords = [
            "Pax",
            "Pax Weight",
            "Bag",
            "Bag Weight",
            "Cargo",
            "Mail",
            "Tare",
            "Traffic Load",
            "DOW",
            "EZFW",
        ]
        for line in weight_lines:
            for keyword in weight_keywords:
                pattern = rf"{keyword}\s*:\s*([-+]?[0-9]*\.?[0-9]+)\s*([a-zA-Z]*)"
                match = re.search(pattern, line)
                if match:
                    value, unit = match.groups()
                    key_value_pairs[keyword] = convert_to_number(value.strip())
                    if unit:
                        key_value_pairs["Weight Unit"] = unit.strip()

        # Extract Remark (if any)
        remark_pattern = re.search(r"Remark\s*:\s*(.*)", weights_part)
        if remark_pattern:
            key_value_pairs["Remark"] = remark_pattern.group(1).strip()

        return json.dumps(key_value_pairs)
    raise NotImplementedError("This message is not supported yet")
