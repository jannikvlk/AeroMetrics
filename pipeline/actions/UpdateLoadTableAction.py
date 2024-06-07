import re
import json

def extract(message: str):
    if "com.systemone.lc2.legaircraftconfiguration.dto.AircraftDataDTO" in message:
        """
        com.systemone.lc2.legaircraftconfiguration.dto.AircraftDataDTO [ id = NULL ]
        Configuration
        Start Weight : 123533.0 KG Start Index: 38.10
        Crew         : 2/8
        Water(%)     : $ac.water
        Galley Codes
        TTL     | Weight          | Index  
        T       | 855.00   KG     | -8.2935 
        T       | 842.00   KG     | -4.19316 
        T       | 1150.00  KG     | 10.3845 
        Corrections
        DOW             | DOI      | Pos   | Remark
        770.00   KG     | -2.35    |       | REASON_CREW
        100.00   KG     | 0.00     | NULL  | Crew Bags 
        Weigth Tables | Airline  | Weight
        Pax           | MN       | M88.0F70.0C35.0I0.0 KG
        Special Pax   |          | NULL           
        Bag           | MN       | 15.00    KG    
        Max Weights  Selected         | Manual
        MZFW Adj.:   NULL             | NULL           
        MTOW Adj.:   NULL             | NULL           
        MLAW Adj.:   NULL             | NULL           
        MTXW Adj.:   NULL
        """
        
        data = {
            "start_weight": None,
            "star_index": None,
            "crew": None,
            "water(%)": None,
            "Galley_Codes": [],
            "Corrections": [],
            "ka": []
        }
        
        # Extract start weight, start index, crew, and water
        start_info_pattern = re.compile(r'Start Weight\s*:\s*(\d+\.\d+)\s*KG\s*Start Index\s*:\s*(\d+\.\d+)')
        start_info_match = start_info_pattern.search(message)
        if start_info_match:
            data["start_weight"] = float(start_info_match.group(1))
            data["star_index"] = float(start_info_match.group(2))
        
        crew_pattern = re.compile(r'Crew\s*:\s*([^\n]+)')
        crew_match = crew_pattern.search(message)
        if crew_match:
            data["crew"] = crew_match.group(1).strip()
        
        water_pattern = re.compile(r'Water\(%\)\s*:\s*([^\n]+)')
        water_match = water_pattern.search(message)
        if water_match:
            data["water(%)"] = water_match.group(1).strip()
        
        # Extract galley codes
        galley_pattern = re.compile(r'T\s*\|\s*(\d+\.\d+)\s*KG\s*\|\s*(-?\d+\.\d+)')
        for match in galley_pattern.finditer(message):
            data["Galley_Codes"].append({
                "TTL": "T",
                "Weight": float(match.group(1)),
                "unit": "KG",
                "Index": float(match.group(2))
            })
        
        # Extract corrections
        corrections_pattern = re.compile(r'(\d+\.\d+)\s*KG\s*\|\s*(-?\d+\.\d+)\s*\|\s*([\d]*)\s*\|\s*(.*)')
        for match in corrections_pattern.finditer(message):
            data["Corrections"].append({
                "DOW": float(match.group(1)),
                "Unit": "KG",
                "DOI": float(match.group(2)),
                "Pos": match.group(3).strip(),
                "Remark": match.group(4).strip()
            })
        
        # Extract weight tables
        weight_table_pattern = re.compile(r'(Pax|Special Pax|Bag)\s*\|\s*([A-Z]*)\s*\|\s*(.*)')
        for match in weight_table_pattern.finditer(message):
            weight = match.group(3).strip()
            weight = None if weight == "NULL" else weight
            weight = float(weight) if weight and weight.replace('.', '', 1).isdigit() else weight
            data["ka"].append({
                "Weigth_Tables": match.group(1).strip(),
                "Airline": match.group(2).strip(),
                "Weight": weight,
                "Unit": "KG" if weight and isinstance(weight, float) else ""
            })
        with open("test.json", "w") as f:
            json.dump(data, f, indent=4)
        with open("test.txt", "w") as f:
            f.write(message)
        return json.dumps(data)

    raise NotImplementedError("This message is not supported yet")