import re
from tqdm import tqdm

from utils import random_sample
from utils import add_to_df

ACTION = "CalculateWeightAndTrimAction"

def extract_abc(df):

    action_df = df[df.action_name == ACTION]
    random_sample(action_df)

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        # skip system row because of lacking information
        if "onesystem" in current_row:
            pass
        else:
            # pattern to extract infos from string
            pattern = re.compile(r'(\w+(\s\w+)*)\s*:\s*([^\s]+)')
            matches = pattern.findall(current_row)
            extracted_data = {match[0].strip(): match[2] for match in matches}
            
            # iterate all rows
            add_to_df(action_df, extracted_data, idx)

            return action_df