import re
import json


def parse_first_line(first_line):
    """
    MEssage:
    'TOTAL Pax: 6    Y: 6  Jump: 0    StandBy: NULL  Male: 2  Female: 2  Child: 2  Infant: 0  Total bag: 6  Total bag weight: 72.0 KG  Baggage weight type: HISTORIC
    Distribution        : CKI_DISTRIBUTION         
    Section             : 0A                       0C                       
    Capacity            : Y72                      Y102                     
    Distribution        : Y0                       Y0'

    Data
    '{'TOTAL Pax': 6,
        'Y': 6,
        'Jump': 0,
        'StandBy': None,
        'Male': 2,
        'Female': 2,
        'Child': 2,
        'Infant': 0,
        'Total bag': 6,
        'Total bag weight': 72.0,
        'Baggage weight type': 'HISTORIC',
        'Weight unit': 'KG',
        'Sections': {'0A': {'Capacity': 'Y72', 'Distribution': 'Y0'},
        '0C': {'Capacity': 'Y102', 'Distribution': 'Y0'}},
       'Distribution': 'CKI_DISTRIBUTION'
    }'
    """


    # Fixed keys in the first line
    keys = [
        "TOTAL Pax",
        "Y",
        "Jump",
        "StandBy",
        "Male",
        "Female",
        "Child",
        "Infant",
        "Total bag",
        "Total bag weight",
        "Baggage weight type",
    ]

    # Initialize an empty dictionary
    flight_data = {}

    # Split the first line into parts based on multiple spaces
    parts = re.split(r"\s{2,}", first_line)

    # Function to convert string to integer, float or leave as is
    def convert_value(value):
        try:
            if value == "NULL":
                return None, None
            if "KG" in value:
                return float(value.replace("KG", "").strip()), "KG"
            elif value.isdigit():
                return int(value), None
            else:
                return value, None
        except ValueError:
            raise ValueError(f"Could not convert value {value}")
            # return value, None

    # Variable to store weight unit
    weight_unit = None

    # Map each part to the corresponding key and convert values
    for key, part in zip(keys, parts):
        raw_value = part.split(": ")[1].strip()
        value, unit = convert_value(raw_value)
        flight_data[key] = value
        if unit:
            weight_unit = unit

    # Add the weight unit to the dictionary if it was found
    if weight_unit:
        flight_data["Weight unit"] = weight_unit

    return flight_data


def parse_remaining_lines(lines):
    # Initialize an empty dictionary for the resulting structure
    remaining_data = {"Sections": {}}

    # Define a function to parse a line with a key and multiple values
    def parse_line(line):
        parts = re.split(r"\s{2,}", line.strip())
        key = parts[0].split(":")[0].strip()
        values = [part.strip().lstrip(":").strip() for part in parts[1:]]
        return key, values

    # Process the first 'Distribution' line separately
    distribution_key, distribution_values = parse_line(lines[0])
    remaining_data[distribution_key] = distribution_values[0]

    # Process the 'Section', 'Capacity', and 'Distribution' lines
    _, sections_values = parse_line(lines[1])
    _, capacities_values = parse_line(lines[2])
    _, distributions_values = parse_line(lines[3])

    # Populate the Sections dictionary
    for section, capacity, distribution in zip(
        sections_values, capacities_values, distributions_values
    ):
        section = section.lstrip(":").strip()  # Remove any leading colons and spaces
        remaining_data["Sections"][section] = {
            "Capacity": capacity.lstrip(":").strip(),
            "Distribution": distribution.lstrip(":").strip(),
        }

    return remaining_data


def extract(message):
    if message is None:
        return None
    if "TOTAL Pax" in message:
        lines = message.split("\r\n")
        data = parse_first_line(lines[0])
        if "Distribution" in message:
            data.update(parse_remaining_lines(lines[1:]))
        return json.dumps(data)

    raise NotImplementedError("This message is not supported yet", message)
