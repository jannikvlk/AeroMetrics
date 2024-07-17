# Define the file paths
from pathlib import Path

DATA = Path("../data")
AB_DIR = Path("abcd")
MN_DIR = Path("mnop")
ZY_DIR = Path("zyxw")


CSV_AB = DATA.joinpath(AB_DIR, "ABCD_tripfiles.csv")
CSV_MN = DATA.joinpath(MN_DIR, "MNOP_tripfiles.csv")
CSV_ZY = DATA.joinpath(ZY_DIR, "ZYXW_tripfiles.csv")

CSV_AB_FIXED = DATA.joinpath(AB_DIR, "ABCD_tripfiles_fixed.csv")
CSV_MN_FIXED = DATA.joinpath(MN_DIR, "MNOP_tripfiles_fixed.csv")
CSV_ZY_FIXED = DATA.joinpath(ZY_DIR, "ZYXW_tripfiles_fixed.csv")

PARQUET_AB = DATA.joinpath(AB_DIR, "ABCD_tripfiles.parquet")
PARQUET_MN = DATA.joinpath(MN_DIR, "MNOP_tripfiles.parquet")
PARQUET_ZY = DATA.joinpath(ZY_DIR, "ZYXW_tripfiles.parquet")

PARQUET_AB_TEST = DATA.joinpath(AB_DIR, "ABCD_tripfiles_test.parquet")
PARQUET_MN_TEST = DATA.joinpath(MN_DIR, "MNOP_tripfiles_test.parquet")
PARQUET_ZY_TEST = DATA.joinpath(ZY_DIR, "ZYXW_tripfiles_test.parquet")

PARQUET_AB_CONV = DATA.joinpath(AB_DIR, "ABCD_tripfiles_conv.parquet")
PARQUET_MN_CONV = DATA.joinpath(MN_DIR, "MNOP_tripfiles_conv.parquet")
PARQUET_ZY_CONV = DATA.joinpath(ZY_DIR, "ZYXW_tripfiles_conv.parquet")

PARQUET_AB_WEIGHTS = DATA.joinpath(
    AB_DIR,
    "ABCD_tripfiles_weights.parquet",
)
PARQUET_MN_WEIGHTS = DATA.joinpath(
    MN_DIR,
    "MNOP_tripfiles_weights.parquet",
)
PARQUET_ZY_WEIGHTS = DATA.joinpath(
    ZY_DIR,
    "ZYXW_tripfiles_weights.parquet",
)
PARQUET_WEIGHTS = DATA.joinpath(
    "tripfiles_weights.parquet",
)

CSV_AB_WEIGHTS = DATA.joinpath(
    AB_DIR,
    "ABCD_tripfiles_weights.csv",
)
CSV_MN_WEIGHTS = DATA.joinpath(
    MN_DIR,
    "MNOP_tripfiles_weights.csv",
)
CSV_ZY_WEIGHTS = DATA.joinpath(
    ZY_DIR,
    "ZYXW_tripfiles_weights.csv",
)
CSV_WEIGHTS = DATA.joinpath(
    "tripfiles_weights.csv",
)

PARQUET_AB_FLIGHTTABLE = DATA.joinpath(
    AB_DIR,
    "ABCD_flighttable.parquet",
)
PARQUET_MN_FLIGHTTABLE = DATA.joinpath(
    MN_DIR,
    "MNOP_flighttable.parquet",
)
PARQUET_ZY_FLIGHTTABLE = DATA.joinpath(
    ZY_DIR,
    "ZYXW_flighttable.parquet",
)
PARQUET_FLIGHTTABLE = DATA.joinpath(
    "flighttable.parquet",
)

CSV_AB_FLIGHTTABLE = DATA.joinpath(
    AB_DIR,
    "ABCD_flighttable.csv",
)
CSV_MN_FLIGHTTABLE = DATA.joinpath(
    MN_DIR,
    "MNOP_flighttable.csv",
)
CSV_ZY_FLIGHTTABLE = DATA.joinpath(
    ZY_DIR,
    "ZYXW_flighttable.csv",
)
CSV_FLIGHTTABLE = DATA.joinpath(
    "flighttable.csv",
)

PARQUET_AB_AUTOMATIONTABLE = DATA.joinpath(
    AB_DIR,
    "ABCD_tableau_automation.parquet",
)
PARQUET_MN_AUTOMATIONTABLE = DATA.joinpath(
    MN_DIR,
    "MNOP_tableau_automation.parquet",
)
PARQUET_ZY_AUTOMATIONTABLE = DATA.joinpath(
    ZY_DIR,
    "ZYXW_tableau_automation.parquet",
)
PARQUET_AUTOMATIONTABLE = DATA.joinpath(
    "tableau_automation.parquet",
)

CSV_AB_AUTOMATIONTABLE = DATA.joinpath(
    AB_DIR,
    "ABCD_tableau_automation.csv",
)
CSV_MN_AUTOMATIONTABLE = DATA.joinpath(
    MN_DIR,
    "MNOP_tableau_automation.csv",
)
CSV_ZY_AUTOMATIONTABLE = DATA.joinpath(
    ZY_DIR,
    "ZYXW_tableau_automation.csv",
)
CSV_AUTOMATIONTABLE = DATA.joinpath(
    "tableau_automation.csv",
)