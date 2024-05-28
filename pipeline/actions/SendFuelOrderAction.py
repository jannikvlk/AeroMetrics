import re
from tqdm import tqdm
import pandas as pd

from utils import random_sample
from utils import add_to_df

ACTION = "SendFuelOrderAction"

def extract_abcd(df):
    pass
    # for abcd no data for this action

def extract_mnop(df):
    action_df = df[df.action_name == ACTION]

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        if "PRELIMINARY FUEL ORDER" in current_row:
            pattern = re.compile(r"\b(\d{3})\b.*?BLOCK FUEL:\s+(\d+)\s+(\w+)", re.DOTALL)

            # Search for matches in the text
            match = pattern.search(current_row)

            # Initialize the dictionary
            extracted_data = {}

            # If a match is found, extract the data and store it in the dictionary
            if match:
                extracted_data['AircraftType'] = match.group(1)
                extracted_data['BlockFuel'] = match.group(2)
                extracted_data['Metric'] = match.group(3)
                extracted_data['FuelOrderState'] = "PRELIMINARY"

            add_to_df(action_df, extracted_data, idx)


        elif "FINAL FUEL ORDER" in current_row:
            pattern = re.compile(r"\b(\d{3})\b.*?BLOCK FUEL:\s+(\d+)\s+(\w+)", re.DOTALL)

            # Search for matches in the text
            match = pattern.search(current_row)

            # Initialize the dictionary
            extracted_data = {}

            # If a match is found, extract the data and store it in the dictionary
            if match:
                extracted_data['AircraftType'] = match.group(1)
                extracted_data['BlockFuel'] = match.group(2)
                extracted_data['Metric'] = match.group(3)
                extracted_data['FuelOrderState'] = "FINAL"

            add_to_df(action_df, extracted_data, idx)

        elif "com.systemone.lc2.common.dto.SendDocumentDTO" in current_row:
            pass

        else:
            print("x")
            print(current_row)
            break
    
    action_df.to_csv(f"pipeline/actions/actions_data/mnop_{ACTION}.csv")
    return action_df