import re
import pandas as pd
import os
from tqdm import tqdm
from utils import random_sample, add_to_df  # assuming these are defined elsewhere
import json

ACTION = "CreateLoadingInstructionAction"

def extract(message):
        # Check if it is the relevant format (format 3)
        if "Message type        :   LOADING_INSTRUCTION" in message:
            pattern_edno = r"EDNO (\d+)"
            pattern_all_weights = r'ALL WEIGHTS IN KILOGRAM'
            pattern_planned_load = r'PLANNED JOINING LOAD\s+BLR\s+Y\s+(\d+)\s+C\s+(\d+)\s+M\s+(\d+)\s+B\s+(\d+)'
            pattern_actual_weight = r'LOADING INSTRUCTION\s+ACTUAL\s+WEIGHT'
            pattern_weight_cpt = r'CPT (\d+)\s+MAX\s+(\d+).*?ONLOAD:\s+\w+\s+.*?/(\d+)'

            edno_match = re.search(pattern_edno, message)
            all_weights_match = re.search(pattern_all_weights, message)
            planned_load_match = re.search(pattern_planned_load, message)
            weight_cpt_matches = re.findall(pattern_weight_cpt, message)

            extracted_data = {
                'Loadsheet_Version_Number': edno_match.group(1) if edno_match else None,
                'Weights_unit': 'KILOGRAM' if all_weights_match else None,
                'Planned_Y': planned_load_match.group(1) if planned_load_match else None,
                'Planned_C': planned_load_match.group(2) if planned_load_match else None,
                'Planned_M': planned_load_match.group(3) if planned_load_match else None,
                'Planned_B': planned_load_match.group(4) if planned_load_match else None,
            }

            for i, (cpt_number, max_weight, onload_weight) in enumerate(weight_cpt_matches, start=1):
                extracted_data[f'CPT_{cpt_number}_MAX'] = max_weight
                extracted_data[f'CPT_{cpt_number}_ONLOAD'] = onload_weight

            return json.dumps(extracted_data)

