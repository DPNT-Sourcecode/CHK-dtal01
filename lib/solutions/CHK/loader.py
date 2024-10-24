import re
import pathlib

from loguru import logger


def load_offers(offers: list[str], price) -> dict:
    parsed_offers = {}

    for offer in offers:
        # handle group offers

            print(offer.split())
            print(n, group)
            group_items = group.strip("()").split(";")
            print(group_items)
            # proxy offer to add every single item to group
            parsed_offers[1] = {"group": {"key": tuple(group_items), "n": n}}
        continue

        match offer.split(" "):
            case [n_item, "for", price]:
                n = ""
                print("n_item", n_item)
                for i, c in enumerate(n_item):
                    print(c, c.isnumeric())
                    if not c.isnumeric():
                        break
                    n += c

                parsed_offers[int(n)] = {"price": int(price)}

            case [n_item, "get", "one", target, "free"]:
                n, sku = n_item[0], n_item[1:]
                if target == sku:
                    # buy N get 1 free is effectively price of N-1 items
                    parsed_offers[int(n) + 1] = {"price": price * (int(n))}
                else:
                    parsed_offers[int(n)] = {"freebie": target}
    return parsed_offers


def parse_item(line: str) -> dict:
    item = {}

    item_spec = r"(?P<item>[A-Z]+)\s*\|\s*(?P<price>\d+)\s*\|\s*(?P<offers>[A-Za-z0-9,\(\) ]+)\s*\|"
    found = re.search(item_spec, line.strip())

    if not found or not all(found.groups()):
        raise RuntimeError("invalid item format")
    print(found.groups())

    # get basic item properties
    item["item"] = found.group("item")
    item["price"] = int(found.group("price"))

    offerst_str = found.group("offers")
    offers = None
    if 'buy any' in offerst_str:
        offers = offerst_str.strip()
    else:
        offers = [
            o.strip() for o in offers_str.split(",") if not re.match(r"^\s*$", o)
        ]

    # extract separate offers from the string
    print(offers)
    item["offers"] = load_offers(offers, item["price"])

    return item


def load_items(filepath: str):
    for line in open(pathlib.Path(__file__).parent.resolve() / filepath):
        try:
            yield parse_item(line.strip())
        except RuntimeError as e:
            logger.debug(f'unable to parse line "{line.strip()}": {e}')
            continue

