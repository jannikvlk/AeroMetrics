import pandas as pd
import os
from actions import CalculateWeightAndTrimAction
from actions import StorePaxDataAction
from actions import CreateZFWMessageAction
from actions import CreatLoadSheetAction

abc_file_path = os.path.join(os.path.dirname(__file__), '../data', 'ABCD_tripfiles.parquet')

# Read the parquet file
df_abcd = pd.read_parquet(abc_file_path, engine="pyarrow")

df = pd.DataFrame()
#CalculateWeightAndTrimAction.extract_abc(df_abcd)
#StorePaxDataAction.extract_abc(df_abcd)
#CreateZFWMessageAction.extract_abc(df_abcd)
CreatLoadSheetAction.extract_abc(df_abcd)