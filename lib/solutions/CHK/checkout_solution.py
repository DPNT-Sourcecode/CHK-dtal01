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


def checkout(skus: str) -> int:
    items = get_items(skus)

    counts = Counter(items)

    for item, count in counts.items():
        if item not in PRICES:
            return -1

        regular_price = PRICES[item]
        bundled, remaining = 0, count

        if item in BUNDLES:
            bundle_size = BUNDLES[item]["qty"]
            bundle_price = BUNDLES[item]["price"]

            bundled, remaining = (
                count // bundle_size,
                count % bundle_size,
            )



