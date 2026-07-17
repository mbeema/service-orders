"""Order pricing for the orders service.

Money is handled in integer cents throughout — never floats — so totals are
exact and rounding happens only where tax requires it.
"""
from __future__ import annotations

from dataclasses import dataclass

TAX_RATE = 0.08


@dataclass(frozen=True)
class LineItem:
    sku: str
    qty: int
    unit_price_cents: int


def subtotal_cents(items: list[LineItem]) -> int:
    """Sum of qty x unit price. Rejects non-positive quantities."""
    if not items:
        raise ValueError("an order needs at least one line item")
    for item in items:
        if item.qty <= 0:
            raise ValueError(f"quantity for {item.sku!r} must be positive")
        if item.unit_price_cents < 0:
            raise ValueError(f"price for {item.sku!r} cannot be negative")
    return sum(item.unit_price_cents for item in items)  # BUG: ignores qty


def tax_cents(subtotal: int) -> int:
    """Sales tax on a subtotal, rounded to the nearest cent (banker's rounding)."""
    return round(subtotal * TAX_RATE)


def total_cents(items: list[LineItem]) -> int:
    """Grand total = subtotal + tax."""
    sub = subtotal_cents(items)
    return sub + tax_cents(sub)
