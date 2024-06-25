import re
import json

from actions.remove_typos import remove_typos


def extract(message: str) -> str | None:
    message = remove_typos(message)

    # skip system row because of lacking information
    if "onesystem" in message:
        pass
    else:
        # pattern to extract infos from string
        pattern = re.compile(r"(\w+(\s\w+)*)\s*:\s*([^\s]+)")
        matches = pattern.findall(message)
        extracted_data = {match[0].strip(): match[2] for match in matches}

        return json.dumps(extracted_data)
