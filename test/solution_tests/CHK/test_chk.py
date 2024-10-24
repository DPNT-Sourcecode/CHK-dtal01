import pytest

from solutions.CHK import checkout_solution


@pytest.mark.parametrize("skus,total", [("A", 50), ("AA", 100), ("AA", 100)])
def test_single_sku_total(skus, total):
    assert checkout_solution.checkout(skus) == total


@pytest.mark.parametrize(
    "skus,total",
    [("AAA", 130), ("AAAA", 130 + 50), ("A" * 6, 130 * 2), ("A" * 7, 130 * 2 + 50)],
)
def test_single_sku_bundles(skus, total):
    assert checkout_solution.checkout(skus) == total


def test_multiple_skus():
    assert checkout_solution.checkout("ABCD") == 115


@pytest.mark.parametrize(
    "skus,total", [("ABCDA", 130 + 30 + 20 + 15), ("ABABCD", 130 + 30 + 20 + 15 + 50)]
)
def test_multiple_skus_with_bundles(skus, total):
    assert checkout_solution.checkout(skus) == total


