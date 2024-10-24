# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter

from loguru import logger

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


def get_bundles_price(cart: Counter, item: str) -> int:
    """
    Given an item, return the total value of all found bundles
    :param items: Counter of items, passed by reference
    :param item: item to get the price for
    :return: price of the item
    """
    regular_price = PRICES[item]
    n_items = cart[item]

    bundled_price = 0

    logger.debug(f"item: {item} x {n_items}")

    # check if item is part of a bundle
    offers = OFFERS.get(item, {})

    # sort bundles by their size, decreasing
    # i.e. always try to fit largest bundles first
    for bundle_size, bundle in sorted(offers.items(), reverse=True):
        bundles, n_items = extract_bundle(n_items, bundle_size)
        # update remaining unbundled items in the cart
        cart[item] = n_items

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
            if freebie in cart:
                get_free = min(cart[freebie], bundles)
                logger.debug(
                    f"got {get_free} {freebie} for free, from {bundles} bundles"
                )
                cart.update({freebie: -get_free})
                logger.debug(f"{freebie} count is now {cart[freebie]}")

        # add the price for the bundles
        bundled_price += bundles * bundle_price
        logger.debug(
            f"got {bundles} bundle(s) of size {bundle_size}, total price {bundles * bundle_price}"
        )

    # returning the total value of all found bundles
    return bundled_price


def checkout(skus: str) -> int:
    logger.info("-" * 40)
    logger.info(f"received '{skus}' SKU string from client")

    if not skus:
        return 0

    items = get_items(skus)
    counts = Counter(items)

    total = 0

    while top := counts.most_common(1):
        item, _ = top[0]

        logger.info(f"calculating price for {item}")
        logger.info(
            f"remaining items: {', '.join([f'{k}, {c}' for k,c in counts.items()])}"
        )
        if item not in PRICES:
            logger.error(f"invalid SKU: {item}")
            return -1

        total += get_bundles_price(counts, item)

    return total


