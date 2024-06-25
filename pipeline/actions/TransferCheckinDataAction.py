import re
import pandas as pd
import os
from tqdm import tqdm
import json

from actions.remove_typos import remove_typos


def extract(message: str) -> str | None:
    message = remove_typos(message)
    # Define the regular expressions to extract the information
    pattern1 = r"TOTAL\s+Pax:\s+(\d+)\s+Y:\s+(\d+)\s+Jump:\s+(\d+)\s+StandBy:\s+(NULL|\d+)\s+Male:\s+(\d+)\s+Female:\s+(\d+)\s+Child:\s+(\d+)\s+Infant:\s+(\d+)\s+Total\s+bag:\s+(\d+)\s+Total\s+bag\s+weight:\s+([\d.]+)\s+KG\s+Baggage\s+weight\s+type:\s+(\w+)\s+Distribution\s+:\s+(\w+)\s+Section\s+:\s+([\w\s]+)\s+Capacity\s+:\s+([\w\s]+)\s+Distribution\s+:\s+([\w\s]+)"
    pattern2 = r"(?:([A-Z]+))\s+Y\s+(\d+)\s+Jump\s+(NULL|\d+)\s+Standby\s+(NULL|\d+)\s+Male\s+(\d+)\s+Female\s+(\d+)\s+Child\s+(\d+)\s+Infant\s+(\d+)\s+Bags\s+(\d+)\s+BWgt\s+([\d.]+)\s+KG\s+Average\s+([\d.]+)\s+KG"
    pattern_loadsheet = r"Loadsheet\s+(\d+)"

    match1 = re.search(pattern1, message)
    match2 = re.search(pattern2, message)
    match_loadsheet = re.search(pattern_loadsheet, message)

    loadsheet_number = match_loadsheet.group(1) if match_loadsheet else None

    if match1:
        total_pax = match1.group(1)
        y_pax = match1.group(2)
        jump_pax = match1.group(3)
        standby_pax = match1.group(4)
        male_pax = match1.group(5)
        female_pax = match1.group(6)
        child_pax = match1.group(7)
        infant_pax = match1.group(8)
        total_bags = match1.group(9)
        total_bag_weight = match1.group(10)
        bag_weight_type = match1.group(11)
        distribution_type = match1.group(12)
        sections = match1.group(13).split()
        capacities = match1.group(14).split()
        distributions = match1.group(15).split()

        extracted_data_list = []

        for section, capacity, distribution in zip(sections, capacities, distributions):
            extracted_data = {
                "Loadsheet_Number": loadsheet_number,
                "Total_Pax": total_pax,
                "Y_Pax": y_pax,
                "Jump_Pax": jump_pax,
                "Standby_Pax": standby_pax,
                "Male_Pax": male_pax,
                "Female_Pax": female_pax,
                "Child_Pax": child_pax,
                "Infant_Pax": infant_pax,
                "Total_Bags": total_bags,
                "Total_Bag_Weight_KG": total_bag_weight,
                "Baggage_Weight_Type": bag_weight_type,
                "Distribution_Type": distribution_type,
                "Section": section,
                "Capacity": capacity,
                "Distribution": distribution,
            }
            extracted_data_list.append(extracted_data)

        return json.dumps(extracted_data_list)

    elif match2:
        (
            station,
            y_pax,
            jump_pax,
            standby_pax,
            male_pax,
            female_pax,
            child_pax,
            infant_pax,
            total_bags,
            bag_weight,
            average_weight,
        ) = match2.groups()

        extracted_data = {
            "Loadsheet_Number": loadsheet_number,
            "Station": station,
            "Y_Pax": y_pax,
            "Jump_Pax": jump_pax,
            "Standby_Pax": standby_pax,
            "Male_Pax": male_pax,
            "Female_Pax": female_pax,
            "Child_Pax": child_pax,
            "Infant_Pax": infant_pax,
            "Total_Bags": total_bags,
            "Total_Bag_Weight_KG": bag_weight,
            "Average_Weight_KG": average_weight,
        }

        return json.dumps(extracted_data)

    return json.dumps({})
