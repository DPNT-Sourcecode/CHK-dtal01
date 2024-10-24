import re
import pathlib

from loguru import logger


def load_offers(offers: list[str], price) -> dict:
    parsed_offers = {}

    for offer in offers:
        match offer.split():
            case ["buy", "any", n, "of", group, "for", price]:
                group_items = group.strip("()").split(",")
                # proxy offer to add every single item to group
                parsed_offers[1] = {"group": {"key": tuple(group_items), "n": n}}

            case [n_item, "for", price]:
                n = ""
                for i, c in enumerate(n_item):
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
        raise ValueError("invalid item format")

    # get basic item properties
    item["item"] = found.group("item")
    item["price"] = int(found.group("price"))

    # extract separate offers from the string
    offers = [o.strip() for o in found.group("offers").split(",")]
    item["offers"] = load_offers(offers, item["price"])

    return item


def load_items(filepath: str):
    for line in open(pathlib.Path(__file__).parent.resolve() / filepath):
        try:
            yield parse_item(line.strip())
        except ValueError as e:
            logger.debug(f'unable to parse line "{line.strip()}"')
            continue


