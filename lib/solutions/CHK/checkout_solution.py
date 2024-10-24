# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter

PRICES: dict = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40}
OFFERS = {
    "A": {3: {"price": 130}, 5: {"price": 200}},
    "B": {2: {"price": 45}},
    "E": {2: {"freebie": "B"}},
}


def get_items(skus: str) -> list[str]:
    """
    Given a stirng representation of the checked out items,
    return a list of individual items
    """

    return list(skus)


def extract_bundle(n, size: int) -> tuple[int, int]:
    """
    get the number of bundles of :size: and remaining items
    :param n: number of items
    :param size: size of the bundle
    :return: number of bundles and remaining items
    """
    bundles, remaining = (
        n // size,
        n % size,
    )
    return bundles, remaining


def get_item_price(items: Counter, item: str) -> int:
    """
    Given an item, return the price of that item
    :param items: Counter of items, passed by reference
    :param item: item to get the price for
    :return: price of the item
    """
    regular_price = PRICES[item]
    n_items = items.pop(item)
    total_price = 0

    # check if item is part of a bundle
    if item in OFFERS:
        # sort bundles by their size, decreasing
        # i.e. always try to fit largest bundles first
        for bundle_size, bundle in sorted(OFFERS[item].items(), reverse=True):
            bundles, n_items = extract_bundle(n_items, bundle_size)

            if "price" in bundle:
                # bundle is for a discount,
                # hence use the special price
                bundle_price = bundle["price"]
            elif "freebie" in bundle:
                # we get a freebie, hence bundle size
                # is just the price of all items within
                bundle_price = bundle_size * regular_price
                freebie = bundle["freebie"]

                # we've got some item for free,
                # so add them to the counter
                items.update({freebie: bundles})

            # add the price for the bundles
            total_price += bundles * bundle_price

    # add the price for the remaining items
    return total_price + n_items * regular_price


def checkout(skus: str) -> int:
    print(f"received '{skus}' SKU string from client")

    if not skus:
        return 0

    items = get_items(skus)
    counts = Counter(items)

    total = 0

    while top := counts.most_common(1):
        item, count = top
        print(f"most common: {item}")

        if item not in PRICES:
            print(f"invalid SKU: {item}")
            return -1

        total += get_item_price(item, count)

    return total



