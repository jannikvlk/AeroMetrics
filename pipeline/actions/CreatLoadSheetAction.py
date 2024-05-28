import re
from tqdm import tqdm
import pandas as pd

from utils import random_sample
from utils import add_to_df

ACTION = "CreateLoadsheetAction"

def extract_abcd(df):
    action_df = df[df.action_name == ACTION]
    random_sample(action_df)

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        if "Message type        :   LOADSHEET" or "Message type        :   LOADING_INSTRUCTION" in current_row:
            pattern_edno = r"EDNO (\d+)"
            pattern_takeoff_weight_actual = r'TAKE OFF WEIGHT ACTUAL\s+(\d+)'  # Match one or more digits for takeoff weight
            pattern_all_weights = r'ALL WEIGHTS IN KILOGRAM'  # Exact match for weights unit

            # Extract information using regular expressions
            edno_match = re.search(pattern_edno, current_row)
            takeoff_weight_actual_match = re.search(pattern_takeoff_weight_actual, current_row)
            all_weights_match = re.search(pattern_all_weights, current_row)

            extracted_data = {}
            extracted_data['Loadsheet_Version_Number'] = edno_match.group(1) if edno_match else None
            extracted_data['TAKE_OFF_WEIGHT_ACTUAL'] = takeoff_weight_actual_match.group(1) if takeoff_weight_actual_match else None
            extracted_data['Weights_unit'] = 'KILOGRAM' if all_weights_match else None

            add_to_df(action_df, extracted_data, idx)
        elif "STATUS LOADSHEET" in current_row:
            pass
        elif "STATUS LOADING_INSTRUCTION" in current_row:
            pass
        elif "om.onesystem.lc2.common.dto.SingleAttributeDTO" in current_row:
            pass
        else:
            print(current_row)

    action_df.to_csv(f"pipeline/actions/actions_data/abcd_{ACTION}.csv")
    return action_df