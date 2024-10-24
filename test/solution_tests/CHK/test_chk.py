import pytest

from solutions.CHK import checkout_solutions


@pytest.mark.parametrize("skus,total", [("A", 50), ("A A", 100), ("AA", 100)])
def test_single_sku_total(skus, total):
    assert checkout_solutions.checkout(skus) == total


@pytest.mark.parametrize(
    "skus,total",
    [("AAA", 130), ("AAAA", 130 + 50), ("A" * 6, 130 * 2), ("A" * 7, 130 * 2 + 50)],
)
def test_single_sku_bundles(skus, total):
    assert checkout_solutions.checkout(skus) == total

