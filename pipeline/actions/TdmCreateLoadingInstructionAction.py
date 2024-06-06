import json
import re


def extract(message: str):
    typos = {
        "BAG_LOZY_ITEMS_GEN": "BAG_LOAD_ITEMS_GEN",
        "LOZYING_INSTRUCTION": "LOADING_INSTRUCTION",
        "LOZYSHEET": "LOADSHEET",
    }  # Fix typos in the messages from zyxw
    for key, value in typos.items():
        message = message.replace(key, value)

    if "com.systemone.lc2.common.dto.SingleAttributeDTO" in message:
        return None
    if "STATUS LOADING_INSTRUCTION" in message:
        """ 
        Example Message: 'STATUS LOADING_INSTRUCTION 1 FUEL 2 AIRCRAFT_CONFIG 1 EZFW 1 
        CARGO_FINAL 1 CARGO_TRANSFER 1 OFP 2 CABIN_CONFIG 1 AUTO_MODE_ACTIVE 1 AUTOMATION_STARTED 0 
        BAG_LOAD_ITEMS_GEN 1 EZFW_COUNTER 1 REGISTRATION 1 REGISTRATION_CHANGE 1 FUEL_ORDER 2'
        
        All the keys are separated by a space and the values are the next element in the list.
        """
        keys = [
            "LOADING_INSTRUCTION",
            "FUEL",
            "AIRCRAFT_CONFIG",
            "EZFW",
            "CARGO_FINAL",
            "CARGO_TRANSFER",
            "OFP",
            "CABIN_CONFIG",
            "AUTO_MODE_ACTIVE",
            "AUTOMATION_STARTED",
            "BAG_LOAD_ITEMS_GEN",
            "EZFW_COUNTER",
            "REGISTRATION",
            "REGISTRATION_CHANGE",
            "FUEL_ORDER",
            "DGR_ITEMS",
            "CHECK_IN_FINAL",
            "OFFBLOCK",
            "AIRBORNE",
            "BAG_ULD_ORD",
            "CALC_HIST_DATA",
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

    if "Telex receivers" in message or "Email receivers" in message:
        return None  # not relevant enough
    raise NotImplementedError("This message is not supported yet")
