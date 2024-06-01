import re
from tqdm import tqdm
import pandas as pd

from utils import random_sample
from utils import add_to_df

ACTION = "SetActualBagWeightIndicatorAction"

def extract_abcd(df):
    action_df = df[df.action_name == ACTION]
    output_df = action_df[["id"]].copy()
    	
    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        if current_row != None: 
            # Define the regular expression patterns
            pax_pattern = re.compile(r"TOTAL Pax:\s*(\d+)")
            baggage_weight_pattern = re.compile(r"Total bag weight:\s*([\d.]+)\s*KG")

            # Search for matches in the text
            pax_match = pax_pattern.search(current_row)
            baggage_weight_match = baggage_weight_pattern.search(current_row)

            extracted_data = {}

            if pax_match:
                extracted_data['actual_total_passangers'] = int(pax_match.group(1))

            if baggage_weight_match:
                extracted_data['actual_total_bags_weight'] = float(baggage_weight_match.group(1))

            add_to_df(output_df, extracted_data, idx)

        elif current_row == None:
            pass
        else:
            print(current_row)
            break

    output_df.to_csv(f"pipeline/actions/actions_data/mnop_{ACTION}.csv")
    return output_df


def extract_mnop(df):
    pass  
    #no data for mnop