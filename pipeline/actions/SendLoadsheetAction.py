import re
import json
from actions.remove_typos import remove_typos


def extract(message: str) -> str | None:
    message = remove_typos(message)
  

    if (
        "Message type        :   LOADSHEET" in message
        or "Message type        :   LOADING_INSTRUCTION" in message
    ):
        """{
                'TOTAL TRAFFIC LOAD'
                'DRY OPERATING WEIGHT'
                'ZERO FUEL WEIGHT ACTUAL'
                'TAKE OFF FUEL'
                'TAKE OFF WEIGHT ACTUAL'
                'TRIP'
                'LANDING WEIGHT ACTUAL'
                },"""
        
        
        patterns = {}
        if "TRIP FUEL" in message:
            # This identifies zyxw messages because they are the only ones with TRIP followed by FUEL
            patterns = {
                "TOTAL TRAFFIC LOAD": r"TOTAL\s+TRAFFIC\s+LOAD\s+(\d+)",
                "DRY OPERATING WEIGHT": r"DRY\s+OPERATING\s+WEIGHT\s+(\d+)",
                "ZERO FUEL WEIGHT ACTUAL": r"ZERO\s+FUEL\s+WEIGHT\s+ACTUAL\s+(\d+)",
                "TAKE OFF FUEL": r"TAKE\s+OFF\s+FUEL\s+(\d+)",
                "TAKE OFF WEIGHT ACTUAL": r"TAKE\s+OFF\s+WEIGHT\s+ACTUAL\s+(\d+)",
                "TRIP FUEL": r"TRIP\s+FUEL\s+(\d+)",
                "LANDING WEIGHT ACTUAL": r"LANDING\s+WEIGHT\s+ACTUAL\s+(\d+)",
            }

        elif "ZERO FUEL WEIGHT ACTUAL" in message: # This identifies abcd messages
          
            patterns = {
                "TOTAL TRAFFIC LOAD": r"TOTAL TRAFFIC LOAD\s+(\d+)",
                "DRY OPERATING WEIGHT": r"DRY OPERATING WEIGHT\s+(\d+)",
                "ZERO FUEL WEIGHT ACTUAL": r"ZERO FUEL WEIGHT ACTUAL\s+(\d+)",
                "TAKE OFF FUEL": r"TAKE OFF FUEL\s+(\d+)",
                "TAKE OFF WEIGHT ACTUAL": r"TAKE OFF WEIGHT ACTUAL\s+(\d+)",
                "TRIP FUEL": r"TRIP\s+(\d+)",
                "LANDING WEIGHT ACTUAL": r"LANDING WEIGHT ACTUAL\s+(\d+)",
            }
        elif "ZFW" in message:
            # This identifies mnop messages because they are the only ones with abbreviations like ZFW
            patterns = {
            "DRY OPERATING WEIGHT": r"DOW\s+(\d+)", # DOW
            "TOTAL TRAFFIC LOAD": r"PAY\s+(\d+)", # PAY
            "ZERO FUEL WEIGHT ACTUAL": r"ZFW\s+(\d+)", # ZFW
            "TAKE OFF FUEL": r"TOF\s+(\d+)", # TOF
            "TAKE OFF WEIGHT ACTUAL": r"TOW\s+(\d+)", # TOW
            "TRIP FUEL": r"TIF\s+(\d+)", # TIF
            "LANDING WEIGHT ACTUAL": r"LAW\s+(\d+)" # LAW
            }
        
        extracted_weights = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, message)
            if match:
                extracted_weights[key] = int(match.group(1))
            else:
                extracted_weights[key] = None  # Assign None if the value is not found
        
        return json.dumps(extracted_weights)
    

    if "STATUS LOADSHEET" in message or "STATUS LOADING_INSTRUCTION" in message:
        return None
    if "lc2.common.dto.SendDocumentDTO" in message:
        return None
    raise NotImplementedError("This message is not supported yet")
