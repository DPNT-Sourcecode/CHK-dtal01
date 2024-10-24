# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter

from loguru import logger

from . import loader


PRICES, OFFERS = {}, {}

for item in loader.load_items("items.txt"):
    print(item["price"])
    PRICES.update({item["item"]: item["price"]})
    OFFERS.update({item["item"]: item["offers"]})

logger.info(f"loaded {len(PRICES)} items")


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


def apply_offers(cart: Counter, item: str) -> int:
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

        if not bundles:
            continue

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

    # returning the total value of all found bundles
    return bundled_price


def checkout(skus: str) -> int:
    logger.info("-" * 40)
    logger.info(f"received '{skus}' SKU string from client")

    if not skus:
        return 0

    counts = Counter(get_items(skus))

    total = 0

    # sort items with freebie offers first
    items_by_offer = sorted(
        counts.keys(),
        key=lambda item: any(["freebie" in v for v in OFFERS.get(item, {}).values()]),
        reverse=True,
    )

    for item in items_by_offer:
        logger.info(f"finding bundles for {item}")
        logger.info(
            f"remaining items: {', '.join([f'{k}, {c}' for k,c in counts.items()])}"
        )
        if item not in PRICES:
            logger.error(f"invalid SKU: {item}")
            return -1

        total += apply_offers(counts, item)

    for item in counts:
        logger.info(f"finding bundles for {item}")
        logger.info(
            f"remaining items: {', '.join([f'{k}, {c}' for k,c in counts.items()])}"
        )
        logger.debug(f"{counts[item]=}", {PRICES[item]})
        total += counts[item] * PRICES[item]

    return total

