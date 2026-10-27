from decimal import Decimal

import pytest

from pricing_rules import (
    apply_group_discount,
    apply_premium_surcharge,
    apply_special_offer,
)


# ---------- R4: group discount ----------

def test_r4_one_member_has_no_discount():
    assert apply_group_discount(100, 1) == Decimal("100")


def test_r4_two_members_get_10_percent():
    assert apply_group_discount(100, 2) == Decimal("90")


def test_r4_many_members_get_10_percent():
    assert apply_group_discount(Decimal("420"), 3) == Decimal("378")


def test_r4_does_not_round():
    # 45 * 0.9 = 40.5, must stay 40.5 (rounding only happens at the end)
    assert apply_group_discount(45, 2) == Decimal("40.5")


# ---------- R5: special offer ----------

def test_r5_200_exact_has_no_offer():
    assert apply_special_offer(200) == Decimal("200")


def test_r5_just_above_200_subtracts_20():
    assert apply_special_offer(201) == Decimal("181")


def test_r5_400_exact_subtracts_only_20():
    assert apply_special_offer(400) == Decimal("380")


def test_r5_just_above_400_subtracts_only_50():
    # 401 - 50 = 351, never 401 - 50 - 20
    assert apply_special_offer(401) == Decimal("351")


def test_r5_below_200_has_no_offer():
    assert apply_special_offer(30) == Decimal("30")


# ---------- R6: premium surcharge ----------

def test_r6_without_premium_extra_amount_is_unchanged():
    assert apply_premium_surcharge(100, False) == Decimal("100")


def test_r6_with_premium_extra_adds_15_percent():
    assert apply_premium_surcharge(100, True) == Decimal("115")


# ---------- Chained rules R4 -> R5 -> R6 (rows of the PDF table) ----------
# Subtotals are given directly; rounding (R7) is applied here only to compare.

def _chain(subtotal, members, has_premium):
    amount = apply_group_discount(subtotal, members)
    amount = apply_special_offer(amount)
    amount = apply_premium_surcharge(amount, has_premium)
    return amount


def _round_half_up(amount):
    from decimal import ROUND_HALF_UP
    return int(amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


@pytest.mark.parametrize(
    "subtotal, members, has_premium, expected",
    [
        (30, 1, False, 30),      # BASIC, none, 1
        (70, 1, False, 70),      # STANDARD + PERSONAL_TRAINING, 1
        (90, 2, False, 81),      # BASIC + GROUP_CLASSES, 2
        (135, 3, False, 122),    # BASIC + GROUP_CLASSES, 3
        (340, 4, False, 286),    # STANDARD + GROUP_CLASSES + PERSONAL_TRAINING, 4
        (230, 2, True, 215),     # PREMIUM + GROUP_CLASSES + SPA, 2
        (420, 3, True, 412),     # PREMIUM + SPA + SPECIALIZED_PROGRAM, 3
        (660, 4, True, 626),     # PREMIUM + SPA + SPECIALIZED_PROGRAM + PERSONAL_TRAINING, 4
    ],
)
def test_chained_rules_match_pdf_table(subtotal, members, has_premium, expected):
    assert _round_half_up(_chain(subtotal, members, has_premium)) == expected