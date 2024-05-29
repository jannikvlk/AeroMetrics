import re
from tqdm import tqdm
import pandas as pd

from utils import random_sample
from utils import add_to_df

ACTION = "UpdateFuelDataAction"

def extract_abcd(df):
    action_df = df[df.action_name == ACTION]

    for idx, row in tqdm(action_df.iterrows(), total=action_df.shape[0], desc="Processing rows"):
        current_row = row["entry_details"]

        if 

def extract_mnop(df):
    pass
