import re

"""
+------+-------+------------------------+
| Item | Price | Special offers         |
+------+-------+------------------------+
| A    | 50    | 3A for 130, 5A for 200 |
| B    | 30    | 2B for 45              |
| C    | 20    |                        |
| D    | 15    |                        |
| E    | 40    | 2E get one B free      |
| F    | 10    | 2F get one F free      |
| G    | 20    |                        |
| H    | 10    | 5H for 45, 10H for 80  |
| I    | 35    |                        |
| J    | 60    |                        |
| K    | 80    | 2K for 150             |
| L    | 90    |                        |
| M    | 15    |                        |
| N    | 40    | 3N get one M free      |
| O    | 10    |                        |
| P    | 50    | 5P for 200             |
| Q    | 30    | 3Q for 80              |
| R    | 50    | 3R get one Q free      |
| S    | 30    |                        |
| T    | 20    |                        |
| U    | 40    | 3U get one U free      |
| V    | 50    | 2V for 90, 3V for 130  |
| W    | 20    |                        |
| X    | 90    |                        |
| Y    | 10    |                        |
| Z    | 50    |                        |
+------+-------+------------------------+
"""


def parse_item(line: str) -> dict:
    item = {}
    item_spec = r"(?P<item>[A-Z])\s*|" r"(?P<price>\d+)\s*|" r"(?P<offers>[A-Za-z])"

    found = re.search(item_spec, line)
    if not found:
        raise ValueError("invalid item format")

    # get basic item properties
    item["item"] = found.group("item")
    item["price"] = int(found.group("price"))

    # extract separate offers from the string
    offers_str = found.group("offers")
    offers = [o.strip() for o in offers_str.split(",")]

    item["offers"] = []
    for offer in offers:
        match offer.split():
            case [n_item, "for", price]:
                pass
            case [n_item, "get", "one", "free"]:
                pass

    return item


def load_items():
    pass


