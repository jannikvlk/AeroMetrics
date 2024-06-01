import re
from tqdm import tqdm
import pandas as pd

from utils import add_to_df

ACTION = "UpdateFuelDataAction"

"""
The UpdateFuelDataAction includes Final Zero Fuel Weight

ATOW = FZFW + Total Fuel (trip fuel + take off fuel + taxi fuel)

"""

def extract_abcd(df):
    action_df = df[df.action_name == ACTION]
    output_df = action_df[["id"]].copy()

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        if "com.onesystem.lc2.fuelhandling.dto.FuelDTO" in current_row:
            keys_to_extract = ['FZFW', 'Trip Fuel', 'Take Off Fuel', 'Taxi Fuel']
            dict_keys = ["final_zfw", "trip_fuel", "taxi_fuel", "take_off_fuel"]
            extracted_data = {}

            atow = 0
            for i in range(0, len(keys_to_extract)):
                match = re.search(rf'{keys_to_extract[i]}\s*:\s*([\d.]+)\s*KG', current_row)
                if match:
                    value = float(match.group(1))
                    extracted_data[dict_keys[i]] = value
                    
                    atow += float(value)

            extracted_data["ATOW"] = atow

            add_to_df(output_df, extracted_data, idx)

        elif "STATUS LOADING_INSTRUCTION" or "STATUS LOADSHEET 1" in current_row:
            keys_to_extract = ['trip', 'takeoff', 'taxi']
            dict_keys = ["trip_fuel", "taxi_fuel", "take_off_fuel"]
            extracted_data = {}

            for i in range(0, len(keys_to_extract)):
                match = re.search(rf'{keys_to_extract[i]}=(\d+\.\d+)\s*KG', current_row)
                if match:
                    value = float(match.group(1))
                    extracted_data[dict_keys[i]] = value

            add_to_df(output_df, extracted_data, idx)

        else:
            print(current_row)
            break

    output_df.to_csv(f"pipeline/actions/actions_data/abcd_{ACTION}.csv")
    return output_df
 
def extract_mnop(df):
    pass
