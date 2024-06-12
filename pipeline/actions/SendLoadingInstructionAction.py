import re
import pandas as pd
import os
from tqdm import tqdm
from utils import random_sample, add_to_df  # assuming these are defined elsewhere
import json

def extract(message):
    if "Message type        :   LOADING_INSTRUCTION" in message:
        pattern_subject = r"Subject\s+:\s+([A-Z0-9/]+);\s*Loading Instruction Edition (\d+)"
        pattern_edno = r"EDNO\s*(\d+)"
        pattern_all_weights = r"ALL WEIGHTS IN KILOGRAM"
        pattern_human_clc = r"HUMAN-CLC\s*(\d+)"
        pattern_flight_info = r"FROM/TO FLIGHT\s+.*?\s+([A-Z]{3})\s+([A-Z]{3})\s+([A-Z0-9\s/]+)\s+([A-Z0-9]+)\s+Y(\d+)\s+(\d{2}[A-Z]{3}\d{2})\s+(\d{4})"
        pattern_planned_load = r"PLANNED JOINING LOAD\s+([A-Z]{3})\s+Y\s+(\d+)\s+C\s+(\d+)\s+M\s+(\d+)\s+B\s+(\d+)"
        pattern_cpt = r"CPT (\d+)\s+MAX\s+(\d+).*?ONLOAD:\s+\w+\s+.*?/(\d+).*?CPT (\d+) TOTAL:"

        subject_match = re.search(pattern_subject, message)
        edno_match = re.search(pattern_edno, message)
        all_weights_match = re.search(pattern_all_weights, message)
        human_clc_match = re.search(pattern_human_clc, message)
        flight_info_match = re.search(pattern_flight_info, message)
        planned_load_match = re.search(pattern_planned_load, message)
        cpt_matches = re.findall(pattern_cpt, message, re.DOTALL)

        extracted_data = {
            'Flight_Number': subject_match.group(1) if subject_match else None,
            'Flight_Date': subject_match.group(2) if subject_match else None,
            'Flight_Route': {
                'From': flight_info_match.group(1) if flight_info_match else None,
                'To': flight_info_match.group(2) if flight_info_match else None
            },
            'Instruction_Version': subject_match.group(2) if subject_match else None,
            'Edition_Number': edno_match.group(1) if edno_match else None,
            'Weights_Unit': 'KILOGRAM' if all_weights_match else None,
            'Human_CLC': human_clc_match.group(1) if human_clc_match else None,
            'Version': flight_info_match.group(5) if flight_info_match else None,
            'Date': flight_info_match.group(6) if flight_info_match else None,
            'Time': flight_info_match.group(7) if flight_info_match else None,
            'Planned_Load': {
                'Y': planned_load_match.group(2) if planned_load_match else None,
                'C': planned_load_match.group(3) if planned_load_match else None,
                'M': planned_load_match.group(4) if planned_load_match else None,
                'B': planned_load_match.group(5) if planned_load_match else None
            },
            'Compartments': {}
        }

        for cpt_number, max_weight, onload_weight, cpt_total_number in cpt_matches:
            extracted_data['Compartments'][f'CPT_{cpt_number}'] = {
                'MAX': max_weight,
                'ONLOAD': onload_weight,
                'CPT_TOTAL': onload_weight  # Assuming CPT TOTAL is the same as ONLOAD weight for simplicity
            }

        return json.dumps(extracted_data, indent=4)

