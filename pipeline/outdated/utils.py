import numpy as np
import random

def write_to_file(text: str, fileneame: str):
    with open(fileneame, "w") as file:
        file.write(text)

def add_to_df(df, extracted_data, idx):
    for key, value in extracted_data.items():
            # add columns from entry_details keys if not exist
            if key not in df.columns:
                df[str(key)] = np.nan
            # write data in entry_details key columns
            df.at[idx, key] = value

def random_sample(df):
    random_index = random.randint(0, len(df) - 1)
    random_sample = str(df.iloc[random_index].entry_details)
    print(random_sample)
    write_to_file(random_sample, "random_sampel.txt")