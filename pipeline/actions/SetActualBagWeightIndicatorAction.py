import re
import json

from actions.remove_typos import remove_typos


def extract(message: str) -> str | None:
    message = remove_typos(message)

    if message is not None:
        pattern = re.compile(r"(\w+):\s*([^ ]+)")
        matches = pattern.findall(message)

        extracted_data = {key: value for key, value in matches}

        return json.dumps(extracted_data)

    elif message is None:
        pass
    else:
        print(message)
        pass
