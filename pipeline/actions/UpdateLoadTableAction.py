import re
import json


def extract(message: str):
    """
    com.onesystem.lc2.manualloadplanning.dto.LoadDTO [ id = 2259193  flightId = 517500 legId = 542905  deleted = false  fragmentId = LoadFragment ]
    BULK

    Item Id   Number       Status    Weight         Pieces    Volume    Origin    Onl.Sta.  Dest.     Category  Position  Confirmed  Remarks
    7374773   NULL         ESTIMATE  688.00    KG   80        0.00      DEL       DEL       AYJ       B         3         false     NULL
    7374774   NULL         ESTIMATE  172.00    KG   20        0.00      DEL       DEL       AYJ       B         4         false     NULL
    7374775   NULL         ESTIMATE  29.00     KG   0         0.00      DEL       DEL       AYJ       C         3         false     NULL

    Total baggage      : 860.00   KG
    Total cargo        : 29.00    KG
    Total EIC          : 0.00     KG
    Total mail         : 0.00     KG

    STATUS LOADING_INSTRUCTION 1 FUEL 1 AIRCRAFT_CONFIG 1 EZFW 2 CARGO_TRANSFER 1 CABIN_CONFIG 1 TRANSIT_ACCEPTANCE 1 TRANSIT_PAX 1 CALC_HIST_DATA 1 CHECK_IN_OPEN 1 AUTO_MODE_ACTIVE 1 AUTOMATION_STARTED 0 BAG_LOAD_ITEMS_GEN 1 EZFW_COUNTER 2 REGISTRATION 1 REGISTRATION_CHANGE 5
    """

    data = {
        "LoadDTO": {
            "id": None,
            "flightId": None,
            "legId": None,
            "deleted": None,
            "fragmentId": None,
        },
        "BULK": [],
        "ULD": [],
        "Totals": {
            "Total baggage": None,
            "Total cargo": None,
            "Total EIC": None,
            "Total mail": None,
        },
        "Status": {},
    }

    # Extract LoadDTO basic information
    dto_pattern = re.compile(
        r"LoadDTO \[ id = (.*)  flightId = (.*) legId = (.*)  deleted = (.*)  fragmentId = (.*) \]"
    )
    dto_match = dto_pattern.search(message)
    if dto_match:
        data["LoadDTO"]["id"] = (
            int(dto_match.group(1)) if dto_match.group(1) != "NULL" else None
        )
        data["LoadDTO"]["flightId"] = (
            int(dto_match.group(2)) if dto_match.group(2) != "NULL" else None
        )
        data["LoadDTO"]["legId"] = (
            int(dto_match.group(3)) if dto_match.group(3) != "NULL" else None
        )
        data["LoadDTO"]["deleted"] = dto_match.group(4).lower() == "true"
        data["LoadDTO"]["fragmentId"] = dto_match.group(5)

    # Extract BULK information
    bulk_pattern = re.compile(
        r"(\d+)\s+NULL\s+(\w+)\s+(\d+\.\d+)\s+KG\s+(\d+)\s+(\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(NULL|\w+)\s+(true|false)\s+(NULL|\w+)",
        re.MULTILINE,
    )
    for match in bulk_pattern.finditer(message):
        data["BULK"].append(
            {
                "Item Id": int(match.group(1)),
                "Status": match.group(2),
                "Weight": float(match.group(3)),
                "Weight unit": "KG",
                "Pieces": int(match.group(4)),
                "Volume": float(match.group(5)),
                "Origin": match.group(6),
                "Onl.Sta.": match.group(7),
                "Dest.": match.group(8),
                "Category": match.group(9),
                "Position": None if match.group(10) == "NULL" else match.group(10),
                "Confirmed": match.group(11).lower() == "true",
                "Remarks": None if match.group(12) == "NULL" else match.group(12),
            }
        )

    # Extract BULK information
    bulk_pattern = re.compile(
        r"(\d+)\s+(NULL|\w+)\s+(\w+)\s+(\d+\.\d+)\s+KG\s+(\d+)\s+(\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(NULL|\w+)\s+(true|false)\s+(NULL|\w+)",
        re.MULTILINE,
    )
    for match in bulk_pattern.finditer(message):
        data["BULK"].append(
            {
                "Item Id": int(match.group(1)),
                "Number": match.group(2) if match.group(2) != "NULL" else None,
                "Status": match.group(3),
                "Weight": float(match.group(4)),
                "Weight unit": "KG",
                "Pieces": int(match.group(5)),
                "Volume": float(match.group(6)),
                "Origin": match.group(7),
                "Onl.Sta.": match.group(8),
                "Dest.": match.group(9),
                "Category": match.group(10),
                "Position": None if match.group(11) == "NULL" else match.group(11),
                "Confirmed": match.group(12).lower() == "true",
                "Remarks": match.group(13) if match.group(13) != "NULL" else None,
            }
        )

    # Extract totals
    total_baggage_pattern = re.compile(r"Total baggage\s*:\s*(\d+\.\d+)\s*KG")
    total_cargo_pattern = re.compile(r"Total cargo\s*:\s*(\d+\.\d+)\s*KG")
    total_EIC_pattern = re.compile(r"Total EIC\s*:\s*(\d+\.\d+)\s*KG")
    total_mail_pattern = re.compile(r"Total mail\s*:\s*(\d+\.\d+)\s*KG")

    total_baggage_match = total_baggage_pattern.search(message)
    total_cargo_match = total_cargo_pattern.search(message)
    total_EIC_match = total_EIC_pattern.search(message)
    total_mail_match = total_mail_pattern.search(message)

    if total_baggage_match:
        data["Totals"]["Total baggage"] = float(total_baggage_match.group(1))
    if total_cargo_match:
        data["Totals"]["Total cargo"] = float(total_cargo_match.group(1))
    if total_EIC_match:
        data["Totals"]["Total EIC"] = float(total_EIC_match.group(1))
    if total_mail_match:
        data["Totals"]["Total mail"] = float(total_mail_match.group(1))

    # Extract status information
    status_pattern = re.compile(r"STATUS\s+(\S+\s+\d+\s*)+")
    status_match = status_pattern.search(message)
    if status_match:
        status_elements = status_match.group().replace("STATUS", "").strip().split()
        for i in range(0, len(status_elements), 2):
            data["Status"][status_elements[i]] = int(status_elements[i + 1])

    return json.dumps(data)
