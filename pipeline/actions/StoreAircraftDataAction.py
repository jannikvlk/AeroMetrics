import re
import json

def extract(message: str):
    data = {}

    # if "com.onesystem.lc2.legaircraftconfiguration.dto.AircraftDataDTO" in message:
    data = {
        "start_weight": None,
        "start_index": None,
        "crew": None,
        "water(%)": None,
        "Galley_Codes": [],
        "Corrections": [],
        "Weight_Tables": [],
        "Max_Weights": [],
        "Status": {}
    }

    # Extract start weight, start index, crew, and water
    start_info_pattern = re.compile(r'Start Weight\s*:\s*(\d+\.\d+)\s*KG\s*Start Index\s*:\s*(\d+\.\d+)')
    start_info_match = start_info_pattern.search(message)
    if start_info_match:
        data["start_weight"] = float(start_info_match.group(1))
        data["start_index"] = float(start_info_match.group(2))

    crew_pattern = re.compile(r'Crew\s*:\s*([^\n]+)')
    crew_match = crew_pattern.search(message)
    if crew_match:
        data["crew"] = crew_match.group(1).strip()

    water_pattern = re.compile(r'Water\(%\)\s*:\s*([^\n]+)')
    water_match = water_pattern.search(message)
    if water_match:
        data["water(%)"] = water_match.group(1).strip()

    # Extract galley codes
    galley_pattern = re.compile(r'(\w+)\s*\|\s*(\d+\.\d+)\s*(KG)\s*\|\s*(-?\d+\.\d+)')
    for match in galley_pattern.finditer(message):
        data["Galley_Codes"].append({
            "TTL": match.group(1),
            "Weight": float(match.group(2)),
            "unit": match.group(3),
            "Index": float(match.group(4))
        })

    # Extract corrections
    corrections_pattern = re.compile(r'(\d+\.\d+)\s*(KG)\s*\|\s*(-?\d+\.\d+)\s*\|\s*(\S*)\s*\|\s*(.*)')
    for match in corrections_pattern.finditer(message):
        data["Corrections"].append({
            "DOW": float(match.group(1)),
            "Unit": match.group(2),
            "DOI": float(match.group(3)),
            "Pos": match.group(4).strip() if match.group(4).strip() != "NULL" else None,
            "Remark": match.group(5).strip()
        })


    # Extract weight tables
    weight_table_pattern = re.compile(r'(Pax|Special Pax|Bag)\s*\|\s*([A-Z]*)\s*\|\s*(.*?)(?:\s*KG|NULL)')
    for match in weight_table_pattern.finditer(message):
        table_name = match.group(1).strip()
        airline = match.group(2).strip()
        weight = match.group(3).strip()

        # Validate weight value
        if weight and weight != "NULL":
            weight_value = weight.replace(" KG", "").strip()
            try:
                weight_value = float(weight_value)
            except ValueError:
                weight_value = None
        else:
            weight_value = None

        data["Weight_Tables"].append({
            "Table": table_name,
            "Airline": airline,
            "Weight": weight_value,
            "Unit": "KG" if weight_value is not None else None
        })

    # Extract max weights
    max_weights_pattern = re.compile(r'(\w+ Adj\.)\s*:\s*(NULL|\d+\.\d+\s*KG)?\s*\|\s*(NULL|\d+\.\d+\s*KG)?')
    for match in max_weights_pattern.finditer(message):
        left_value = match.group(2)
        right_value = match.group(3)
        
        if left_value and left_value != "NULL":
            left_value_cleaned = left_value.replace(" KG", "").strip()
            try:
                left_value_cleaned = float(left_value_cleaned)
            except ValueError:
                left_value_cleaned = None
            left_unit = "KG"
        else:
            left_value_cleaned = None
            left_unit = None

        if right_value and right_value != "NULL":
            right_value_cleaned = right_value.replace(" KG", "").strip()
            try:
                right_value_cleaned = float(right_value_cleaned)
            except ValueError:
                right_value_cleaned = None
            right_unit = "KG"
        else:
            right_value_cleaned = None
            right_unit = None

        data["Max_Weights"].append({
            "Type": match.group(1),
            "Left_Value": left_value_cleaned,
            "Left_Unit": left_unit,
            "Right_Value": right_value_cleaned,
            "Right_Unit": right_unit
        })

    # Extract status
    lines = message.strip().split("\n")
    status_line = lines[-1]
    status_pattern = re.compile(r'(\S+)\s+(\d+)')
    status_matches = status_pattern.findall(status_line)
    for key, value in status_matches:
        data["Status"][key] = int(value)

    return json.dumps(data)