import re
import json


def extract(message):

    
    if "lc2.manualloadplanning.dto.LoadDTO" in message:
        # Normalize line breaks to just '\n' for easier processing
        normalized_text = message.replace("\r\n", "\n").strip()

        def parse_header(header):
            header_dict = {}
            matches = re.findall(r"(\w+)\s*=\s*(\S+)", header)
            for key, value in matches:
                header_dict[key] = value.strip("[]")
            return header_dict

        def parse_bulk(bulk_section):
            bulk_data = []
            lines = bulk_section.strip().split("\n")[
                2:
            ]  # Skip the first two lines (headers)
            for line in lines:
                columns = re.split(
                    r"\s{2,}", line.strip()
                )  # Split by two or more spaces
                if len(columns) < 13:
                    continue  # Skip lines that don't have enough columns

                item_dict = {
                    "Item Id": columns[0] if columns[0] != "NULL" else None,
                    "Number": columns[1] if columns[1] != "NULL" else None,
                    "Status": columns[2],
                    "Weight": float(columns[3]) if is_float(columns[3]) else None,
                    "Weight Unit": columns[4],
                    "Pieces": int(columns[5]) if is_int(columns[5]) else None,
                    "Volume": float(columns[6]) if is_float(columns[6]) else None,
                    "Origin": columns[7],
                    "Onl.Sta.": columns[8],
                    "Dest.": columns[9],
                    "Category": columns[10],
                    "Position": columns[11],
                    "Confirmed": (
                        columns[12].lower() == "true" if len(columns) > 12 else None
                    ),
                    "Remarks": (
                        columns[13]
                        if len(columns) > 13 and columns[13] != "NULL"
                        else None
                    ),
                }
                bulk_data.append(item_dict)
            return bulk_data

        def parse_uld(uld_section):
            uld_data = []
            lines = uld_section.strip().split("\n")[
                2:
            ]  # Skip the first two lines (headers)
            for line in lines:
                columns = re.split(
                    r"\s{2,}", line.strip()
                )  # Split by two or more spaces
                if len(columns) < 14:
                    continue  # Skip lines that don't have enough columns

                item_dict = {
                    "Item Id": columns[0] if columns[0] != "NULL" else None,
                    "ULD": columns[1] if columns[1] != "NULL" else None,
                    "Number": columns[2] if columns[2] != "NULL" else None,
                    "Airline": columns[3] if columns[3] != "NULL" else None,
                    "Special": columns[4] if columns[4] != "NULL" else None,
                    "Status": columns[5],
                    "Weight": float(columns[6]) if is_float(columns[6]) else None,
                    "Weight Unit": columns[7] if len(columns) > 7 else None,
                    "Pieces": int(columns[8]) if is_int(columns[8]) else None,
                    "Volume": float(columns[9]) if is_float(columns[9]) else None,
                    "Origin": columns[10] if len(columns) > 10 else None,
                    "Onl.Sta.": columns[11] if len(columns) > 11 else None,
                    "Dest.": columns[12] if len(columns) > 12 else None,
                    "Category": columns[13] if len(columns) > 13 else None,
                    "Position": columns[14] if len(columns) > 14 else None,
                    "Confirmed": (
                        columns[15].lower() == "true" if len(columns) > 15 else None
                    ),
                    "Remarks": (
                        columns[16]
                        if len(columns) > 16 and columns[16] != "NULL"
                        else None
                    ),
                }
                uld_data.append(item_dict)
            return uld_data

        def parse_totals(totals_section):
            totals = {}
            for line in totals_section.strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":")
                    key = key.strip()
                    # Only split on the first space after the numeric value to get the value as a float
                    value = float(value.strip().split()[0])
                    totals[key] = value
            return totals

        def parse_status(status_section):
            status_dict = {}
            # Remove the initial "STATUS" keyword and split the rest
            status_items = status_section.replace("STATUS ", "").split()

            # Use an iterator to go through the items
            it = iter(status_items)
            for key in it:
                value = next(it, None)
                if value and is_int(value):
                    value = int(value)
                status_dict[key] = value
            return status_dict

        def is_int(value):
            try:
                return int(value)
            except (ValueError, TypeError):
                return False

        def is_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return False

        # Use a regular expression to find the sections
        sections = re.split(
            r"(?=\nBULK|\nULD|\nTotal baggage|\nSTATUS)", normalized_text
        )

        header_section = sections[0] if len(sections) > 0 else ""
        header_info = parse_header(header_section)

        bulk_section = next((s for s in sections if s.startswith("\nBULK")), None)
        bulk_info = parse_bulk(bulk_section) if bulk_section else []

        uld_section = next((s for s in sections if s.startswith("\nULD")), None)
        uld_info = parse_uld(uld_section) if uld_section else []

        totals_section = next((s for s in sections if s.startswith("\nTotal")), None)
        # print(sections)
        # for i, item in enumerate(sections):
        #     print(i, item)
        # print(totals_section)
        totals_info = parse_totals(totals_section) if totals_section else {}

        status_section = next((s for s in sections if s.startswith("\nSTATUS")), None)
        status_info = parse_status(status_section) if status_section else {}

        load_info = {
            "Header": header_info,
            "Bulk": bulk_info,
            "ULD": uld_info,
            "Totals": totals_info,
            "Status": status_info,
        }

        return json.dumps(load_info)
    raise NotImplementedError("This message is not supported yet", message)
