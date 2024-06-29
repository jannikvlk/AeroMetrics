# Define the file paths
from pathlib import Path

DATA_DIR = Path("../data")
AB_DIR = Path("")
MN_DIR = Path("")
ZY_DIR = Path("")

CSV_FILE_AB = DATA_DIR.joinpath(AB_DIR, "ABCD_tripfiles.csv")
CSV_FILE_MN = DATA_DIR.joinpath(MN_DIR, "MNOP_tripfiles.csv")
CSV_FILE_ZY = DATA_DIR.joinpath(ZY_DIR, "ZYXW_tripfiles.csv")

PARQUET_FILE_AB = DATA_DIR.joinpath(AB_DIR, "ABCD_tripfiles.parquet")
PARQUET_FILE_MN = DATA_DIR.joinpath(MN_DIR, "MNOP_tripfiles.parquet")
PARQUET_FILE_ZY = DATA_DIR.joinpath(ZY_DIR, "ZYXW_tripfiles.parquet")

PARQUET_FILE_AB_CONV = DATA_DIR.joinpath(AB_DIR, "ABCD_tripfiles_conv.parquet")
PARQUET_FILE_MN_CONV = DATA_DIR.joinpath(MN_DIR, "MNOP_tripfiles_conv.parquet")
PARQUET_FILE_ZY_CONV = DATA_DIR.joinpath(ZY_DIR, "ZYXW_tripfiles_conv.parquet")

PARQUET_FILE_AB_WEIGHTS = DATA_DIR.joinpath(AB_DIR, "ABCD_tripfiles_weights.parquet")
PARQUET_FILE_MN_WEIGHTS = DATA_DIR.joinpath(MN_DIR, "MNOP_tripfiles_weights.parquet")
PARQUET_FILE_ZY_WEIGHTS = DATA_DIR.joinpath(ZY_DIR, "ZYXW_tripfiles_weights.parquet")

PARQUET_FILE_AB_FLIGHTTABLE = DATA_DIR.joinpath(AB_DIR, "ABCD_flighttable.parquet")
PARQUET_FILE_MN_FLIGHTTABLE = DATA_DIR.joinpath(MN_DIR, "MNOP_flighttable.parquet")
PARQUET_FILE_ZY_FLIGHTTABLE = DATA_DIR.joinpath(ZY_DIR, "ZYXW_flighttable.parquet")
