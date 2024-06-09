import re
import json

def extract(message: str):
    """
    com.systemone.lc2.manualloadplanning.dto.LoadDTO [ id = 2978157  flightId = 667743 legId = 687554  deleted = false  fragmentId = LoadFragment ]

    BULK
    Item Id   Number       Status    Weight         Pieces    Volume    Origin    Onl.Sta.  Dest.     Category  Position  Confirmed  Remarks  
    37125629  NULL         ESTIMATE  65.00     KG   5         0.00      DUB       DUB       CDG       BT        NULL      false     NULL 
    37125630  NULL         ESTIMATE  13.00     KG   1         0.00      DUB       DUB       CDG       B         NULL      false     NULL 

    ULD
    Item Id   ULD       Number    Airline   Special   Status    Weight         Pieces    Volume    Origin    Onl.Sta.  Dest.     Category  Position  Confirmed  Remarks  
    37125626  AKH       NULL      MN                  ESTIMATE  455.00    KG   35        0.00      DUB       DUB       CDG       B         NULL      false     NULL 
    37125628  AKH       NULL      MN                  ESTIMATE  455.00    KG   35        0.00      DUB       DUB       CDG       B         NULL      false     NULL 
    37146875  AKH       44747     BA        NULL      ACTUAL    104.00    KG   0         0.00      DUB       DUB       CDG       C         NULL      false     VAL 
    37125625  AKH       NULL      MN                  ESTIMATE  455.00    KG   35        0.00      DUB       DUB       CDG       B         NULL      false     NULL 
    37125627  AKH       NULL      MN                  ESTIMATE  455.00    KG   35        0.00      DUB       DUB       CDG       B         NULL      false     NULL 
    37146876  AKH       67103     MN        NULL      ACTUAL    200.00    KG   0         0.00      DUB       DUB       CDG       C         NULL      false     NULL 

    Total baggage      : 1898.00  KG               
    Total cargo        : 304.00   KG               
    Total MNC          : 0.00     KG               
    Total mail         : 0.00     KG
    """
    data = {
        "LoadDTO": {
            "id": None,
            "flightId": None,
            "legId": None,
            "deleted": None,
            "fragmentId": None
        },
        "BULK": [],
        "ULD": [],
        "Totals": {
            "Total baggage": None,
            "Total cargo": None,
            "Total EIC": None,
            "Total mail": None
        }
    }

    # Extract LoadDTO basic information
    dto_pattern = re.compile(r'LoadDTO \[ id = (.*)  flightId = (.*) legId = (.*)  deleted = (.*)  fragmentId = (.*) \]')
    dto_match = dto_pattern.search(message)
    if dto_match:
        data["LoadDTO"]["id"] = int(dto_match.group(1)) if dto_match.group(1) != "NULL" else None
        data["LoadDTO"]["flightId"] = int(dto_match.group(2)) if dto_match.group(2) != "NULL" else None
        data["LoadDTO"]["legId"] = int(dto_match.group(3)) if dto_match.group(3) != "NULL" else None
        data["LoadDTO"]["deleted"] = dto_match.group(4).lower() == 'true'
        data["LoadDTO"]["fragmentId"] = dto_match.group(5)

    # Extract BULK information
    bulk_pattern = re.compile(r'(\d+)\s+NULL\s+(\w+)\s+(\d+\.\d+)\s+KG\s+(\d+)\s+(\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(NULL|\w+)\s+(true|false)\s+(NULL|\w+)', re.MULTILINE)
    for match in bulk_pattern.finditer(message):
        data["BULK"].append({
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
            "Confirmed": match.group(11).lower() == 'true',
            "Remarks": None if match.group(12) == "NULL" else match.group(12)
        })

    # Extract ULD information
    uld_pattern = re.compile(r'(\d+)\s+(\w+)\s+(NULL|\w+)\s+(\w+)\s+NULL\s+(\w+)\s+(\d+\.\d+)\s+KG\s+(\d+)\s+(\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(NULL|\w+)\s+(true|false)\s+(NULL|\w+)', re.MULTILINE)
    for match in uld_pattern.finditer(message):
        data["ULD"].append({
            "Item Id": int(match.group(1)),
            "ULD": match.group(2),
            "Number": None if match.group(3) == "NULL" else int(match.group(3)),
            "Airline": match.group(4),
            "Special": None,
            "Status": match.group(5),
            "Weight": float(match.group(6)),
            "Weight unit": "KG",
            "Pieces": int(match.group(7)),
            "Volume": float(match.group(8)),
            "Origin": match.group(9),
            "Onl.Sta.": match.group(10),
            "Dest.": match.group(11),
            "Category": match.group(12),
            "Position": None if match.group(13) == "NULL" else match.group(13),
            "Confirmed": match.group(14).lower() == 'true',
            "Remarks": None if match.group(15) == "NULL" else match.group(15)
        })

    # Extract totals
    total_baggage_pattern = re.compile(r'Total baggage\s*:\s*(\d+\.\d+)\s*KG')
    total_cargo_pattern = re.compile(r'Total cargo\s*:\s*(\d+\.\d+)\s*KG')
    total_EIC_pattern = re.compile(r'Total EIC\s*:\s*(\d+\.\d+)\s*KG')
    total_mail_pattern = re.compile(r'Total mail\s*:\s*(\d+\.\d+)\s*KG')

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


    return json.dumps(data)