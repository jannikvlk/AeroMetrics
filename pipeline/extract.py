import pandas as pd
import os
from actions import CalculateWeightAndTrimAction
from actions import StorePaxDataAction
from actions import CreateZFWMessageAction
from actions import CreatLoadSheetAction
from actions import SendLoadsheetAction
from actions import CheckinMsgProcessor
from actions import SendFuelOrderAction
from actions import SetActualBagWeightIndicatorAction
from actions import StoreRegistrationAndConfigurationAc
from actions import UpdateFuelDataAction
from actions import EstimateStorePaxDataAction

# Read the parquet files
abc_file_path = os.path.join(os.path.dirname(__file__), '../data', 'ABCD_tripfiles.parquet')
df_abcd = pd.read_parquet(abc_file_path, engine="pyarrow")

df = pd.DataFrame()
CalculateWeightAndTrimAction.extract_abcd(df_abcd)
StorePaxDataAction.extract_abcd(df_abcd)
CreateZFWMessageAction.extract_abcd(df_abcd)
CreatLoadSheetAction.extract_abcd(df_abcd)
SendLoadsheetAction.extract_abcd(df_abcd)
CheckinMsgProcessor.extract_abcd(df_abcd)
SendFuelOrderAction.extract_abcd(df_abcd)
SetActualBagWeightIndicatorAction.extract_abcd(df_abcd)
StoreRegistrationAndConfigurationAc.extract_abcd(df_abcd)
UpdateFuelDataAction.extract_abcd(df_abcd)
#EstimateStorePaxDataAction.extract_abcd(df_abcd)