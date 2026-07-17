import pytest

from app.orders import LineItem, subtotal_cents, tax_cents, total_cents


def test_subtotal_sums_quantities_and_prices():
    items = [LineItem("widget", 2, 500), LineItem("gadget", 1, 300)]
    assert subtotal_cents(items) == 1300


def test_tax_rounds_to_nearest_cent():
    assert tax_cents(1300) == 104          # 1300 * 0.08 = 104.0
    assert tax_cents(1299) == 104          # 103.92 -> 104


def test_total_is_subtotal_plus_tax():
    assert total_cents([LineItem("widget", 2, 500)]) == 1080   # 1000 + 80


def test_empty_order_is_rejected():
    with pytest.raises(ValueError):
        subtotal_cents([])


def test_non_positive_quantity_is_rejected():
    with pytest.raises(ValueError):
        subtotal_cents([LineItem("widget", 0, 500)])


def test_negative_price_is_rejected():
    with pytest.raises(ValueError):
        subtotal_cents([LineItem("widget", 1, -1)])
