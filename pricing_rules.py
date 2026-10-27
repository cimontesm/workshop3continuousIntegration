"""Pricing rules R4, R5 and R6 for the gym membership quote.
"""
from decimal import Decimal

GROUP_MIN_MEMBERS = 2
GROUP_DISCOUNT_FACTOR = Decimal("0.90")  # 10% discount
BIG_OFFER_THRESHOLD = Decimal("400")
BIG_OFFER_DISCOUNT = Decimal("50")
SMALL_OFFER_THRESHOLD = Decimal("200")
SMALL_OFFER_DISCOUNT = Decimal("20")
PREMIUM_SURCHARGE_FACTOR = Decimal("1.15")  # +15%


def _to_decimal(amount):
    """Convert numbers to Decimal through str to avoid float errors."""
    return amount if isinstance(amount, Decimal) else Decimal(str(amount))


def apply_group_discount(amount, members):
    """R4: with 2 or more members the amount gets a 10% discount."""
    amount = _to_decimal(amount)
    if members >= GROUP_MIN_MEMBERS:
        return amount * GROUP_DISCOUNT_FACTOR
    return amount


def apply_special_offer(amount):
    """R5: if amount > 400 subtract 50; otherwise if amount > 200 subtract 20.

    The two discounts never add up.
    """
    amount = _to_decimal(amount)
    if amount > BIG_OFFER_THRESHOLD:
        return amount - BIG_OFFER_DISCOUNT
    if amount > SMALL_OFFER_THRESHOLD:
        return amount - SMALL_OFFER_DISCOUNT
    return amount


def apply_premium_surcharge(amount, has_premium_extra):
    """R6: if the selection has at least one premium extra, add 15%."""
    amount = _to_decimal(amount)
    if has_premium_extra:
        return amount * PREMIUM_SURCHARGE_FACTOR
    return amount
