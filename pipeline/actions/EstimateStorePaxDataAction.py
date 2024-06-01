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
            pattern = (
                    r"Booked\s+"                      # Match the word 'Booked'
                    r"(\d+)\s+"                       # Match Y value (digits)
                    r"(NULL|\d+)\s+"                  # Match Jump value (NULL or digits)
                    r"(NULL|\d+)\s+"                  # Match Standby value (NULL or digits)
                    r"(NULL|\d+)\s+"                  # Match Male value (NULL or digits)
                    r"(NULL|\d+)\s+"                  # Match Female value (NULL or digits)
                    r"(NULL|\d+)\s+"                  # Match Child value (NULL or digits)
                    r"(NULL|\d+)\s+"                  # Match Infant value (NULL or digits)
                    r"(NULL|\d+)\s+"                  # Match Bags value (NULL or digits)
                    r"(NULL|[\d.]+)\s+KG\s+"          # Match BWgt value (NULL or digits with decimal point)
                    r"(NULL|[\d.]+)\s+"               # Match Average value (NULL or digits with decimal point)
                )
            matches = re.findall(pattern, current_row, re.DOTALL)
            keys = [
                "estimated_Y", "estimated_Jump", "estimated_Standby", "estimated_Male", "estimated_Female", "estimated_Child", "estimated_Infant", "estimated_Bags", "estimated_BWgt", "estimated_Average_BWgt"
            ]

            if matches:
                values = matches[0]
                extracted_data = dict(zip(keys, values))

                add_to_df(output_df, extracted_data, idx)

            else:
                print("No matches found.")
                print(current_row)
                break

        
        elif "STATUS AIRCRAFT_CONFIG" or "STATUS FUEL" in current_row:
            pass
        else:
            print(current_row)
            break



    output_df.to_csv(f"pipeline/actions/actions_data/abcd_{ACTION}.csv")
    return output_df