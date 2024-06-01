import re
from tqdm import tqdm
import pandas as pd
import numpy as np

from utils import random_sample
from utils import add_to_df

ACTION = "StoreRegistrationAndConfigurationAc"
def extract_abcd(df):
    action_df = df[df.action_name == ACTION]
    output_df = action_df[["id"]].copy()

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        if "Water(%)" in current_row:
            pattern = re.compile(r"Start Weight\s*:\s*([\d.]+)\s*(\w+)\s*.*?Total Weight:\s*([\d.]+)\s*(\w+)", re.DOTALL)

            # Search for matches in the text
            match = pattern.search(current_row)

            # Initialize the dictionary
            extracted_data = {}

            # If a match is found, extract the data and store it in the dictionary
            if match:
                extracted_data['start_weight'] = float(match.group(1))
                extracted_data['start_weight_metric'] = match.group(2)
                extracted_data['basic_empty_weight'] = float(match.group(3))
                extracted_data['basic_empty_weight_metric'] = match.group(4)

            add_to_df(output_df, extracted_data, idx)
        elif "systemone" or "onesystem" in current_row:
            pass
        else:
            print(current_row)
            break

    output_df.to_csv(f"pipeline/actions/actions_data/abcd_{ACTION}.csv")
    return output_df