# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter, OrderedDict

PRICES: dict = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40}
BUNDLES = {
    "A": {3: {"price": 130}, 5: {"price": 200}},
    "B": {2: {"price": 45}},
}


def get_items(skus: str) -> list[str]:
    """
    Given a stirng representation of the checked out items,
    return a list of individual items
    """

    return list(skus)


def get_item_price(item: str, n_items: int) -> int:
    """
    Given an item, return the price of that item
    """
    regular_price = PRICES[item]
    total_price = 0

    # check if item is part of a bundle
    if item in BUNDLES:
        # sort bundles by their size, decreasing
        # i.e. always try to fit largest bundles first
        for bundle_size, bundle in sorted(BUNDLES[item].items(), reverse=True):
            bundle_price = bundle["price"]

            # get the price for the current bundle
            # and update the number of items remaining
            bundled, n_items = (
                n_items // bundle_size,
                n_items % bundle_size,
            )

            total_price += bundled * bundle_price

    # add the price for the remaining items
    return total_price + n_items * regular_price


def checkout(skus: str) -> int:
    print(f"received '{skus}' SKU string from client")

    if not skus:
        return 0

    items = get_items(skus)
    counts = Counter(items)

    total = 0
    for item, count in counts.items():
        if item not in PRICES:
            return -1

        total += get_item_price(item, count)

    return total





