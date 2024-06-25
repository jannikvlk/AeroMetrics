import re
import json

from actions.remove_typos import remove_typos


def extract(message: str) -> str | None:
    message = remove_typos(message)
    """
    com.systemone.lc2.paxactuals.dto.PaxDataWrapperDTO [ id = NULL ]
    paxDataDTO     : com.systemone.lc2.paxactuals.dto.PaxDataDTO [ id = 2872743 ]
    Baggage weight type: STANDARD       
    MUC            
                    Y              J              Jump           Standby        Male           Female         Child          Infant         Bags           BWgt           Average        
    Loadsheet       136            1              NULL           0              70             64             3              0              100            1300.00 KG     13.00 KG       

    Distribution   : CKI_DISTRIBUTION 
    Section        : 0A             0B             0C             
    Capacity       : J4Y54          Y60            Y54            
    Distribution   : J1Y26          Y46            Y48            
    Special pax    : NULL
    Cki average weight : NULL
    """

    """
    TOTAL Pax: 254    Y: 233  J: 21  Jump: 0    StandBy: NULL  Male: 121  Female: 129  Child: 4  Infant: 0  Total bag: 248  Total bag weight: 3720.0 KG  Baggage weight type: STANDARD
    Distribution        : CKI_DISTRIBUTION         
    Section             : 0A                       0B                       0C                       
    Capacity            : J23                      Y142                     Y106                     
    Distribution        : J14                      Y111                     Y73                      
    Undistributed pax   : 56                       
    STATUS AIRCRAFT_CONFIG 1 EZFW 1 CARGO_TRANSFER 1 CABIN_CONFIG 1 AUTO_MODE_ACTIVE 1 AUTOMATION_STARTED 0 BAG_LOAD_ITEMS_GEN 1 EZFW_COUNTER 1 REGISTRATION 1 REGISTRATION_CHANGE 1
    """
    data = {
        "paxDataDTO": None,
        "Baggage_weight_type": None,
        "Loadsheet": {},
        "Distribution": None,
        "Section": [],
        "Capacity": [],
        "Distribution_Details": [],
        "Special_pax": None,
        "Cki_average_weight": None,
        "Total_Pax": None,
        "Total_Bag": None,
        "Total_Bag_Weight": None,
        "Status": {},
    }

    # Extract paxDataDTO ID
    pax_data_dto_pattern = re.compile(
        r"paxDataDTO\s*:\s*com\.systemone\.lc2\.paxactuals\.dto\.PaxDataDTO\s*\[ id\s*=\s*(\d+) \]"
    )
    pax_data_dto_match = pax_data_dto_pattern.search(message)
    if pax_data_dto_match:
        data["paxDataDTO"] = int(pax_data_dto_match.group(1))

    # Extract Baggage weight type
    baggage_weight_type_pattern = re.compile(r"Baggage weight type:\s*(\S+)")
    baggage_weight_type_match = baggage_weight_type_pattern.search(message)
    if baggage_weight_type_match:
        data["Baggage_weight_type"] = baggage_weight_type_match.group(1).strip()

    # Extract Loadsheet details
    loadsheet_pattern = re.compile(
        r"Loadsheet\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)\s+KG\s+(\d+\.\d+)\s+KG"
    )
    loadsheet_match = loadsheet_pattern.search(message)
    if loadsheet_match:
        data["Loadsheet"] = {
            "Y": int(loadsheet_match.group(1)),
            "J": int(loadsheet_match.group(2)),
            "Jump": (
                None
                if loadsheet_match.group(3) == "NULL"
                else int(loadsheet_match.group(3))
            ),
            "Standby": int(loadsheet_match.group(4)),
            "Male": int(loadsheet_match.group(5)),
            "Female": int(loadsheet_match.group(6)),
            "Child": int(loadsheet_match.group(7)),
            "Infant": int(loadsheet_match.group(8)),
            "Bags": int(loadsheet_match.group(9)),
            "BWgt": float(loadsheet_match.group(10)),
            "Average": float(loadsheet_match.group(11)),
        }

    # Extract Distribution type
    distribution_pattern = re.compile(r"Distribution\s*:\s*(\S+)")
    distribution_match = distribution_pattern.search(message)
    if distribution_match:
        data["Distribution"] = distribution_match.group(1).strip()

    # Extract Sections
    section_pattern = re.compile(r"Section\s*:\s*(\S+)\s+(\S+)\s+(\S+)")
    section_match = section_pattern.search(message)
    if section_match:
        data["Section"] = [
            section_match.group(1),
            section_match.group(2),
            section_match.group(3),
        ]

    # Extract Capacity
    capacity_pattern = re.compile(r"Capacity\s*:\s*(\S+)\s+(\S+)\s+(\S+)")
    capacity_match = capacity_pattern.search(message)
    if capacity_match:
        data["Capacity"] = [
            capacity_match.group(1),
            capacity_match.group(2),
            capacity_match.group(3),
        ]

    # Extract Distribution details
    distribution_details_pattern = re.compile(
        r"Distribution\s*:\s*(\S+)\s+(\S+)\s+(\S+)"
    )
    distribution_details_match = distribution_details_pattern.search(message)
    if distribution_details_match:
        data["Distribution_Details"] = [
            distribution_details_match.group(1),
            distribution_details_match.group(2),
            distribution_details_match.group(3),
        ]

    # Extract Special pax
    special_pax_pattern = re.compile(r"Special pax\s*:\s*(\S+)")
    special_pax_match = special_pax_pattern.search(message)
    if special_pax_match:
        data["Special_pax"] = (
            None
            if special_pax_match.group(1) == "NULL"
            else special_pax_match.group(1).strip()
        )

    # Extract Cki average weight
    cki_avg_weight_pattern = re.compile(r"Cki average weight\s*:\s*(\S+)")
    cki_avg_weight_match = cki_avg_weight_pattern.search(message)
    if cki_avg_weight_match:
        data["Cki_average_weight"] = (
            None
            if cki_avg_weight_match.group(1) == "NULL"
            else cki_avg_weight_match.group(1).strip()
        )

    # Extract total pax information
    total_pax_pattern = re.compile(
        r"TOTAL Pax:\s*(\d+)\s+Y:\s*(\d+)\s+J:\s*(\d+)\s+Jump:\s*(\d+|NULL)\s+StandBy:\s*(\d+|NULL)\s+Male:\s*(\d+)\s+Female:\s*(\d+)\s+Child:\s*(\d+)\s+Infant:\s*(\d+)\s+Total bag:\s*(\d+)\s+Total bag weight:\s*(\d+\.\d+)\s*KG"
    )
    total_pax_match = total_pax_pattern.search(message)
    if total_pax_match:
        data["Total_Pax"] = {
            "Total": int(total_pax_match.group(1)),
            "Y": int(total_pax_match.group(2)),
            "J": int(total_pax_match.group(3)),
            "Jump": (
                None
                if total_pax_match.group(4) == "NULL"
                else int(total_pax_match.group(4))
            ),
            "StandBy": (
                None
                if total_pax_match.group(5) == "NULL"
                else int(total_pax_match.group(5))
            ),
            "Male": int(total_pax_match.group(6)),
            "Female": int(total_pax_match.group(7)),
            "Child": int(total_pax_match.group(8)),
            "Infant": int(total_pax_match.group(9)),
            "Total_bag": int(total_pax_match.group(10)),
            "Total_bag_weight": float(total_pax_match.group(11)),
        }

    # Extract undistributed pax
    undistributed_pax_pattern = re.compile(r"Undistributed pax\s*:\s*(\d+)")
    undistributed_pax_match = undistributed_pax_pattern.search(message)
    if undistributed_pax_match:
        data["Undistributed_pax"] = int(undistributed_pax_match.group(1))

    # Extract status information
    status_pattern = re.compile(r"STATUS\s+(\S+\s+\d+\s*)+")
    status_match = status_pattern.search(message)
    if status_match:
        status_elements = status_match.group().replace("STATUS", "").strip().split()
        for i in range(0, len(status_elements), 2):
            data["Status"][status_elements[i]] = int(status_elements[i + 1])

    return json.dumps(data)
