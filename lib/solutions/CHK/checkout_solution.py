# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter

PRICES: dict = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
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


