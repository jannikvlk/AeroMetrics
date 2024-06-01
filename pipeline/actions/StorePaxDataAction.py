import re
from tqdm import tqdm

from utils import random_sample
from utils import add_to_df

ACTION = "StorePaxDataAction"

def extract_abcd(df):
    action_df = df[df.action_name == ACTION]
    output_df = action_df[["id"]].copy()

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        # skip system row because of lacking information
        if "com.onesystem.lc2.paxactuals.dto.PaxDataDTO" in current_row:
            # pattern to extract infos from string
            pattern = re.compile(
            r'(?P<type>Checkin|Loadsheet)\s+'
            r'(?P<Y>\d+|\w+)\s+'
            r'(?P<Jump>\d+|\w+)\s+'
            r'(?P<Standby>\d+|\w+)\s+'
            r'(?P<Male>\d+|\w+)\s+'
            r'(?P<Female>\d+|\w+)\s+'
            r'(?P<Child>\d+|\w+)\s+'
            r'(?P<Infant>\d+|\w+)\s+'
            r'(?P<Bags>\d+|\w+)\s+'
            r'(?P<BWgt>[0-9.]+|\w+)\s+'
            #r'(?P<Average>[0-9.]+|\w+)'
        )
            # find match from pattern
            match = pattern.search(current_row)
            

            # add to teh data frame if match
            if match:
                extracted_data = match.groupdict()
                add_to_df(output_df, extracted_data, idx)

            else:
                print("No match found")
                print(current_row)
                break

        elif "TOTAL Pax" in current_row:
            pattern = re.compile(
                r'TOTAL Pax:\s*(?P<TOTAL_Pax>\d+)\s*'
                r'Y:\s*(?P<Y>\d+)\s*'
                r'Jump:\s*(?P<Jump>\d+|NULL)\s*'
                r'StandBy:\s*(?P<Standby>\d+|NULL)\s*'
                r'Male:\s*(?P<Male>\d+|NULL)\s*'
                r'Female:\s*(?P<Female>\d+|NULL)\s*'
                r'Child:\s*(?P<Child>\d+|NULL)\s*'
                r'Infant:\s*(?P<Infant>\d+|NULL)\s*'
                r'Total bag:\s*(?P<Bags>\d+)\s*'
                r'Total bag weight:\s*(?P<BWgt>[\d.]+ KG)\s*'
                r'Baggage weight type:\s*(?P<Baggage_weight_type>\w+)'
            )

            # Extracting matches
            match = pattern.search(current_row)

            # Extracted key-value pairs
            if match:
                extracted_data = match.groupdict()
                #print(extracted_data)
                add_to_df(output_df, extracted_data, idx)
            else:
                print("----")
                print("No match found")
                print(current_row)
                break
                    
        else:
            print("unexpected format")
            print(current_row)
            break


    output_df.to_csv(f"pipeline/actions/actions_data/abcd_{ACTION}.csv")
    return output_df
