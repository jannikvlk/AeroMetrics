import re
import json


def extract(message: str):
    data = {}

    if "com.systemone.lc2.legaircraftconfiguration.dto.AircraftDataDTO" in message:
        data = {
            "start_weight": None,
            "start_index": None,
            "crew": None,
            "water(%)": None,
            "Galley_Codes": [],
            "Corrections": [],
            "Weight_Tables": [],
        }

        # Extract start weight, start index, crew, and water
        start_info_pattern = re.compile(
            r"Start Weight\s*:\s*(\d+\.\d+)\s*KG\s*Start Index\s*:\s*(\d+\.\d+)"
        )
        start_info_match = start_info_pattern.search(message)
        if start_info_match:
            data["start_weight"] = float(start_info_match.group(1))
            data["start_index"] = float(start_info_match.group(2))

        crew_pattern = re.compile(r"Crew\s*:\s*([^\n]+)")
        crew_match = crew_pattern.search(message)
        if crew_match:
            data["crew"] = crew_match.group(1).strip()

        water_pattern = re.compile(r"Water\(%\)\s*:\s*([^\n]+)")
        water_match = water_pattern.search(message)
        if water_match:
            data["water(%)"] = water_match.group(1).strip()

        # Extract galley codes
        galley_pattern = re.compile(r"T\s*\|\s*(\d+\.\d+)\s*KG\s*\|\s*(-?\d+\.\d+)")
        for match in galley_pattern.finditer(message):
            data["Galley_Codes"].append(
                {
                    "TTL": "T",
                    "Weight": float(match.group(1)),
                    "unit": "KG",
                    "Index": float(match.group(2)),
                }
            )

        # Extract corrections
        corrections_pattern = re.compile(
            r"(\d+\.\d+)\s*KG\s*\|\s*(-?\d+\.\d+)\s*\|\s*(\S*)\s*\|\s*(.*)"
        )
        for match in corrections_pattern.finditer(message):
            data["Corrections"].append(
                {
                    "DOW": float(match.group(1)),
                    "Unit": "KG",
                    "DOI": float(match.group(2)),
                    "Pos": (
                        match.group(3).strip()
                        if match.group(3).strip() != "NULL"
                        else None
                    ),
                    "Remark": match.group(4).strip(),
                }
            )

        # Extract weight tables
        weight_table_pattern = re.compile(
            r"(Pax|Special Pax|Bag)\s*\|\s*([A-Z]*)\s*\|\s*(.*?)(?:\s*KG)?\s*$"
        )
        weight_table_matches = weight_table_pattern.findall(message)

        for match in weight_table_matches:
            table_name = match[0].strip()
            airline = match[1].strip()
            weight = match[2].strip()
            unit = None

            if weight != "NULL":
                if weight.endswith("KG"):
                    weight = weight.replace(" KG", "").strip()
                    unit = "KG"

            weight_value = None if weight == "NULL" else weight

            data["Weight_Tables"].append(
                {
                    "Weight_Tables": table_name,
                    "Airline": airline,
                    "Weight": weight_value,
                    "Unit": unit,
                }
            )

    else:
        data = {"Categories": [], "Total_Weight": None, "Index": None, "Status": {}}

        # Extract categories and weights
        lines = message.strip().split("\n")
        for line in lines[1:]:
            category = {}
            if line.startswith("Total Weight:"):
                break
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 4:
                category = {
                    "Category": parts[0],
                    "Weight": float(parts[1].replace(" KG", "")),
                    "Index": float(parts[2]),
                    "Description": parts[3],
                }
            elif len(parts) == 3:
                category = {
                    "Category": "Galley",
                    "Weight": float(parts[1].replace(" KG", "")),
                    "Index": float(parts[2]),
                }
            data["Categories"].append(category)

        # Extract total weight and index
        total_line = lines[-2]
        total_weight_match = re.search(r"Total Weight:\s*([\d\.]+)\s*KG", total_line)
        index_match = re.search(r"Index:\s*([\d\.]+)", total_line)

        if total_weight_match and index_match:
            data["Total_Weight"] = float(total_weight_match.group(1))
            data["Index"] = float(index_match.group(1))

        # Extract status
        status_line = lines[-1]
        status_pattern = re.compile(r"(\S+)\s+(\d+)")
        status_matches = status_pattern.findall(status_line)
        for key, value in status_matches:
            data["Status"][key] = int(value)

    with open("test.json", "w") as f:
        json.dump(data, f, indent=4)
    with open("test.txt", "w") as f:
        f.write(message)
    return json.dumps(data, indent=4)
