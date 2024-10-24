# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter, defaultdict
from pprint import pprint

from loguru import logger

from . import loader


PRICES, OFFERS, GROUPS = {}, {}, {}

for item in loader.load_items("items.txt"):
    PRICES.update({item["item"]: item["price"]})
    OFFERS.update({item["item"]: item["offers"]})


for item, item_offers in OFFERS.items():
    for key, offer in item_offers.items():
        print(key, offer)
        # initialise purchase groups
        if "group" in offer:
            GROUPS[offer["group"]["key"]] = {
                "n": offer["group"]["n"],
                "price": offer["group"]["price"],
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


def apply_offers(cart: Counter, item: str, groups: dict[tuple, list]) -> int:
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
        # all items are going into the group
        if "group" in bundle:
            group = bundle["group"]
            cnt = cart.pop(item, 0)
            print("group item in cart", item, cnt)
            groups[group["key"]].extend([item] * cnt)
            continue

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
    found_groups: dict[tuple, list] = defaultdict(list)

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

        total += apply_offers(counts, item, found_groups)

    print("all groups", GROUPS)
    # process groups
    for key, items in found_groups.items():
        print("found group ", key, items)
        if not items:
            continue

        required_size = GROUPS[key]["n"]
        group_bundles, remaining = (
            len(items) // required_size,
            len(items) % required_size,
        )

        # sort items by price, so that remaining items are the cheapest
        items = sorted(items, key=lambda x: PRICES[x])

        total += group_bundles * GROUPS[key]["price"]
        # put remaining items back into the cart
        for i in items[:remaining]:
            counts[i] += 1

    for item in counts:
        total += counts[item] * PRICES[item]

    return total




