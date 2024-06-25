import re
import json
import utils

from actions.remove_typos import remove_typos


def extract(message: str) -> str | None:
    message = remove_typos(message)

    # skip system row because of lacking information
    if (
        "Y              Jump           Standby        Male           Female         Child          Infant         Bags           BWgt           Average"
        in message
        or "                Y              J              Jump           Standby        Male           Female         Child          Infant         Bags           BWgt           Average        "
        in message
    ):
        pattern = re.compile(
            r"(?P<type>\w+)\s+"
            r"(?P<Y>\d+|NULL)\s+"
            r"(?P<Jump>\d+|NULL)\s+"
            r"(?P<Standby>\d+|NULL)\s+"
            r"(?P<Male>\d+|NULL)\s+"
            r"(?P<Female>\d+|NULL)\s+"
            r"(?P<Child>\d+|NULL)\s+"
            r"(?P<Infant>\d+|NULL)\s+"
            r"(?P<Bags>\d+|NULL)\s+"
            r"(?P<BWgt>[0-9.]+|NULL)\s*KG\s+"
            r"(?P<Average>[0-9.]+|NULL)\s*"
        )

        match = pattern.search(message)

        if match:
            extracted_data = match.groupdict()
            return json.dumps(extracted_data)
        else:
            return None

    elif "lc2.paxactuals.dto.PaxDataDTO" in message:

        # pattern to extract infos from string
        pattern = re.compile(
            r"(?P<type>Checkin|Loadsheet)\s+"
            r"(?P<Y>\d+|\w+)\s+"
            r"(?P<Jump>\d+|\w+)\s+"
            r"(?P<Standby>\d+|\w+)\s+"
            r"(?P<Male>\d+|\w+)\s+"
            r"(?P<Female>\d+|\w+)\s+"
            r"(?P<Child>\d+|\w+)\s+"
            r"(?P<Infant>\d+|\w+)\s+"
            r"(?P<Bags>\d+|\w+)\s+"
            r"(?P<BWgt>[0-9.]+|\w+)\s+"
            # r'(?P<Average>[0-9.]+|\w+)'
        )
        # find match from pattern
        match = pattern.search(message)

        # add to teh data frame if match
        if match:
            extracted_data = match.groupdict()

            return json.dumps(extracted_data)

        else:
            return None

    elif "TOTAL Pax" in message:
        pattern = re.compile(
            r"(?:TOTAL Pax:\s*(?P<TOTAL_Pax>\w+)\s*)?"
            r"(?:Y:\s*(?P<Y>\w+)\s*)?"
            r"(?:Jump:\s*(?P<Jump>\w+|NULL)\s*)?"
            r"(?:StandBy:\s*(?P<Standby>\w+|NULL)\s*)?"
            r"(?:Male:\s*(?P<Male>\w+|NULL)\s*)?"
            r"(?:Female:\s*(?P<Female>\w+|NULL)\s*)?"
            r"(?:Child:\s*(?P<Child>\w+|NULL)\s*)?"
            r"(?:Infant:\s*(?P<Infant>\w+|NULL)\s*)?"
            r"(?:Total bag:\s*(?P<Bags>\w+)\s*)?"
            r"(?:Total bag weight:\s*(?P<BWgt>[\d.]+ KG)\s*)?"
            r"(?:Baggage weight type:\s*(?P<Baggage_weight_type>\w+))?.*"
        )
        match = pattern.search(message)

        if match:
            extracted_data = match.groupdict()
            return json.dumps(extracted_data)
        else:
            return None

    raise NotImplementedError("This message is not supported yet:", message)
