import re
from tqdm import tqdm
import pandas as pd
import numpy as np

from utils import random_sample
from utils import add_to_df

ACTION = "CheckinMsgProcessor"
def extract_abcd(df):
    action_df = df[df.action_name == ACTION]
    random_sample(action_df)

    patterns = {
        'aircraft_regTailNbr': r'<(?:n:)?regTailNbr>\s*(.*?)\s*<\/(?:n:)?regTailNbr>',
        'aircraftType': r'<(?:n:)?aircraftType>\s*(.*?)\s*<\/(?:n:)?aircraftType>',
        'aircraft_configuration': r'<(?:n:)?configuration>\s*(.*?)\s*<\/(?:n:)?configuration>'
    }
    
    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        if '<?xml version="1.0" encoding="UTF-8"?>' in current_row:
            # Dictionary to store the extracted values
            extracted_data = {}

            # Extract data using re
            for key, pattern in patterns.items():
                match = re.search(pattern, current_row)
                if match:
                    extracted_data[key] = match.group(1)
                else:
                    extracted_data[key] = np.nan

            add_to_df(action_df, extracted_data, idx)

        elif "The message was processed successfully" in current_row:
            pass
        else:
            print(current_row)
            break

    action_df.to_csv(f"pipeline/actions/actions_data/{ACTION}.csv")
    return action_df