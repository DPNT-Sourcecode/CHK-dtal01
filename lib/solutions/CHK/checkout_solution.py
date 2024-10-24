# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter

PRICES: dict = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}


def checkout(skus: str) -> int:

    items = skus.split()

