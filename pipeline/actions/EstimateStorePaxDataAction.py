import re
from tqdm import tqdm
import pandas as pd
import numpy as np

from utils import add_to_df

ACTION = "EstimateStorePaxDataAction"
def extract_abcd(df):
    action_df = df[df.action_name == ACTION]
    output_df = action_df[["id"]].copy()

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        if "com.onesystem.lc2.paxactuals.dto.PaxDataDTO" in current_row:

            keys_to_extract = ['Baggage weight type', 'Standby', 'Male', 'Female', 'Child', 'Infant', 'Bags', 'BWgt', 'Average']
            extracted_values = {}

            # Use regular expressions to extract the values
            for key in keys_to_extract:
                match = re.search(rf'{key}:\s*\'([\w\s\r\n]+)\'', current_row)
                if match:
                    value = match.group(1).strip()
                    extracted_values[key] = value

            # Print the extracted values
            print("Extracted Values:")
            print(extracted_values)



    output_df.to_csv(f"pipeline/actions/actions_data/abcd_{ACTION}.csv")
    return output_df