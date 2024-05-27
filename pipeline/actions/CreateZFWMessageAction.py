import re
from tqdm import tqdm

from utils import random_sample
from utils import add_to_df

ACTION = "CreateZFWMessageAction"

def extract_data_from_xml(xml_string):
    # Use regular expressions to find key-value pairs
    keys = ['airline', 'arrivalStation', 'departureStation', 'flightDateLocal', 'revisionNumber',
            'dryOperatingWeight', 'actualZFW', 'cargoWeight', 'baggageWeight', 'paxWeight', 'basicWeight']

    data_dict = {}
    for key in keys:
        match = re.search(r'<{}>(.*?)</{}>'.format(key, key), xml_string)
        if match:
            data_dict[key] = match.group(1)
        else:
            data_dict[key] = None
    return data_dict

def extract_abcd(df):

    action_df = df[df.action_name == ACTION]
    random_sample(action_df)

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        try:
            # skip system row because of lacking information
            if "Receiver queue" in current_row:
                extracted_data = extract_data_from_xml(current_row)
                add_to_df(action_df, extracted_data, idx)
            else: pass
        except Exception as e:
            print(e)
            break

    print(action_df.columns)
    return action_df
