import re
import pandas as pd
import os
from tqdm import tqdm
from utils import random_sample, add_to_df  # assuming these are defined elsewhere

ACTION = "CreateLoadingInstructionAction"

def extract_abcd(df):
    action_df = df[df.action_name == ACTION]
    random_sample(action_df)

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        # Check if it is the relevant format (format 3)
        if "Message type        :   LOADING_INSTRUCTION" in current_row:
            pattern_edno = r"EDNO (\d+)"
            pattern_all_weights = r'ALL WEIGHTS IN KILOGRAM'
            pattern_planned_load = r'PLANNED JOINING LOAD\s+BLR\s+Y\s+(\d+)\s+C\s+(\d+)\s+M\s+(\d+)\s+B\s+(\d+)'
            pattern_actual_weight = r'LOADING INSTRUCTION\s+ACTUAL\s+WEIGHT'
            pattern_weight_cpt = r'CPT (\d+)\s+MAX\s+(\d+).*?ONLOAD:\s+\w+\s+.*?/(\d+)'

            edno_match = re.search(pattern_edno, current_row)
            all_weights_match = re.search(pattern_all_weights, current_row)
            planned_load_match = re.search(pattern_planned_load, current_row)
            weight_cpt_matches = re.findall(pattern_weight_cpt, current_row)

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

            add_to_df(action_df, extracted_data, idx)

    # Ensure the directory exists
    # output_dir = "pipeline/actions/actions_data"
    # os.makedirs(output_dir, exist_ok=True)
    # output_path = os.path.join(output_dir, f"abcd_{ACTION}.csv")

    # Drop the entry_details column before saving to CSV
    action_df = action_df.drop(columns=['entry_details'])
    # action_df.to_csv(output_path, index=False)
    action_df.to_csv(f"pipeline/actions/actions_data/abcd_{ACTION}.csv")
    return action_df
