import re
import json
import utils

ACTION = "SendLoadsheetAction"

def extract(message):
    if "Message type        :   LOADSHEET" or "Message type        :   LOADING_INSTRUCTION" in message:
        pattern_edno = r"(EDNO|Edition number) (\d+)"
        pattern_takeoff_weight_actual = r'(TAKE OFF WEIGHT ACTUAL|TAKE OFF WEIGHT  ACTUAL)\s+(\d+)'  # Match one or more digits for takeoff weight
        pattern_tow = r'\bTOW\b\s+(\d+)'
        pattern_all_weights = r'ALL WEIGHTS IN KILOGRAM'  # Exact match for weights unit

        # Extract information using regular expressions
        edno_match = re.search(pattern_edno, message)
        takeoff_weight_actual_match = re.search(pattern_takeoff_weight_actual, message)
        tow_match = re.search(pattern_tow, message)
        all_weights_match = re.search(pattern_all_weights, message)

        extracted_data = {}
        extracted_data['EDNO'] = edno_match.group(1) if edno_match else None
        extracted_data['TAKE_OFF_WEIGHT_ACTUAL'] = tow_match.group(1) if tow_match else (takeoff_weight_actual_match.group(1) if takeoff_weight_actual_match else None)
        extracted_data['Weights_unit'] = 'KILOGRAM' if all_weights_match else None

        if extracted_data["TAKE_OFF_WEIGHT_ACTUAL"] == None:
            pass

        json.dumps(extracted_data)
    elif "STATUS LOADSHEET" or "STATUS LOADING_INSTRUCTION" or "Email receivers     :" in message:
        pass
    elif "com.systemone.lc2.common.dto.SendDocumentDTO" or "com.onesystem.lc2.common.dto.SendDocumentDTO"  in  message:
        pass
    else:
        print(message)
        pass