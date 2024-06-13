import re
import json

def extract(message):
    if "Message type        :   LOADSHEET" in message or "Message type        :   LOADING_INSTRUCTION" in message or "Message type        :   LOZYSHEET" in message:
        # Define regex patterns
        pattern_edno = r'EDNO\s*\n(?:.*\n){2}\s*(\d+)'     
        pattern_takeoff_weight_actual = r'TAKE OFF WEIGHT ACTUAL\s+(\d+)'
        pattern_tow = r'\bTOW\b\s+(\d+)'
        pattern_all_weights = r'ALL WEIGHTS IN KILOGRAM' 

        # Extract information using regular expressions
        edno_match = re.search(pattern_edno, message)
        takeoff_weight_actual_match = re.search(pattern_takeoff_weight_actual, message)
        tow_match = re.search(pattern_tow, message)
        all_weights_match = re.search(pattern_all_weights, message)

        extracted_data = {}
        extracted_data['EDNO'] = edno_match.group(1) if edno_match else None
        extracted_data['TAKE_OFF_WEIGHT_ACTUAL'] = tow_match.group(1) if tow_match else (takeoff_weight_actual_match.group(1) if takeoff_weight_actual_match else None)
        extracted_data['Weights_unit'] = 'KILOGRAM' if all_weights_match else None
        
        return json.dumps(extracted_data)
    elif "STATUS LOADSHEET" in message:
        pass
    elif "STATUS LOADING_INSTRUCTION" in message:
        pass
    elif "om.onesystem.lc2.common.dto.SingleAttributeDTO" in message:
        pass
    else:
        pass

