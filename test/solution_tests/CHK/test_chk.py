import pytest

from solutions.CHK import checkout_solution


@pytest.mark.parametrize("skus,total", [("A", 50), ("AA", 100), ("AA", 100)])
def test_single_sku_total(skus, total):
    assert checkout_solution.checkout(skus) == total


@pytest.mark.parametrize(
    "skus,total",
    [
        ("AAA", 130),
        ("AAAA", 130 + 50),
        ("A" * 6, 200 + 50),
        ("A" * 7, 200 + 50 * 2),
        ("A" * 9, 200 + 130 + 50),
    ],
)
def test_single_sku_bundles(skus, total):
    assert checkout_solution.checkout(skus) == total


def test_multiple_skus():
    assert checkout_solution.checkout("ABCD") == 115


@pytest.mark.parametrize(
    "skus,total", [("AABCDA", 130 + 30 + 20 + 15), ("AABABCD", 130 + 45 + 20 + 15)]
)
def test_multiple_skus_with_bundles(skus, total):
    assert checkout_solution.checkout(skus) == total


def test_freebie_value_is_added():
    skus = "EE"
    # we should get vlaue of 2E and 1B because of the freebie
    total = 40 * 2 + 30
    assert checkout_solution.checkout(skus) == total


@pytest.mark.parametrize("skus,total", [("EEBB", 80 + 75)])
def test_freebie_counts_in_bundle(skus, total):
    """
    Items received for free should be account for
    in the total value. The calcualtion should
    be order-invariant
    """
    assert checkout_solution.checkout(skus) == total


@pytest.mark.parametrize("skus,total", [("EEB", 80 + 45), ("BEE", 80 + 45)])
def test_freebie_counts_order_invariant(skus, total):
    """
    Items received for free should be account for
    in the total value. The calcualtion should
    be order-invariant
    """
    assert checkout_solution.checkout(skus) == total


