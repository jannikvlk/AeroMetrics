TYPOS = {
    # "BAG_LOZY_ITEMS_GEN": "BAG_LOAD_ITEMS_GEN",
    # "LOZYING_INSTRUCTION": "LOADING_INSTRUCTION",
    # "LOZYSHEET": "LOADSHEET",
    "DEZY": "DEAD",
    "ZYDITIONAL": "ADDITIONAL",
    "LOZY": "LOAD",
}  # Fix typos in the messages from zyxw


def remove_typos(message: str) -> str | None:
    if type(message) is not str:
        return None

    for key, value in TYPOS.items():
        message = message.replace(key, value)
    return message


def test():
    return 1
