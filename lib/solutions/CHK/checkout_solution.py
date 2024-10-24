# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter

PRICES: dict = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}
BUNDLES = {
    "A": {"qty": 3, "price": 130},
    "B": {"qty": 2, "price": 45},
}


def get_items(skus: str) -> list[str]:
    """
    Given a stirng representation of the checked out items,
    return a list of individual items
    """

    return list(skus)


def get_item_price(item: str, count: int) -> int:
    """
    Given an item, return the price of that item
    """
    regular_price = PRICES[item]
    bundled, remaining = 0, count
    total = 0

    # check if item is part of a bundle
    if item in BUNDLES:
        bundle_size = BUNDLES[item]["qty"]
        bundle_price = BUNDLES[item]["price"]

        # get the number of bundles that can be made,
        # and the number of items that are left over
        bundled, remaining = (
            count // bundle_size,
            count % bundle_size,
        )

        total = bundled * bundle_price

    total += remaining * regular_price
    return total


def checkout(skus: str) -> int:
    print(f"received '{skus}' SKU string from client")

    if not skus:
        return -1

    items = get_items(skus)
    counts = Counter(items)

    total = 0
    for item, count in counts.items():
        if item not in PRICES:
            return -1

        total += get_item_price(item, count)

    return total

