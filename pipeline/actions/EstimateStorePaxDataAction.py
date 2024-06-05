import re
import json

ACTION = "EstimateStorePaxDataAction"
def extract(message):
    if "com.onesystem.lc2.paxactuals.dto.PaxDataDTO" in message:
        pattern = (
                r"Booked\s+"                      # Match the word 'Booked'
                r"(\d+)\s+"                       # Match Y value (digits)
                r"(NULL|\d+)\s+"                  # Match Jump value (NULL or digits)
                r"(NULL|\d+)\s+"                  # Match Standby value (NULL or digits)
                r"(NULL|\d+)\s+"                  # Match Male value (NULL or digits)
                r"(NULL|\d+)\s+"                  # Match Female value (NULL or digits)
                r"(NULL|\d+)\s+"                  # Match Child value (NULL or digits)
                r"(NULL|\d+)\s+"                  # Match Infant value (NULL or digits)
                r"(NULL|\d+)\s+"                  # Match Bags value (NULL or digits)
                r"(NULL|[\d.]+)\s+KG\s+"          # Match BWgt value (NULL or digits with decimal point)
                r"(NULL|[\d.]+)\s+"               # Match Average value (NULL or digits with decimal point)
            )
        matches = re.findall(pattern, message, re.DOTALL)
        keys = [
            "estimated_Y", "estimated_Jump", "estimated_Standby", "estimated_Male", "estimated_Female", "estimated_Child", "estimated_Infant", "estimated_Bags", "estimated_BWgt", "estimated_Average_BWgt"
        ]

        if matches:
            values = matches[0]
            extracted_data = dict(zip(keys, values))

            return json.dumps(extracted_data)

    
    elif "STATUS AIRCRAFT_CONFIG" or "STATUS FUEL" in message:
        pass