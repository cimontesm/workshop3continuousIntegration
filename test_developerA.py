import pytest
from developerA import calculateSubtotal, applyRounding

def test_plan_basico_sin_extras():
    # R1 & R3: Plan BASIC (30), sin extras, 1 miembro -> Subtotal 30
    subtotal = calculateSubtotal("BASIC", [], 1)
    assert subtotal == 30
    assert applyRounding(subtotal) == 30

def test_plan_standard_con_extra_no_premium():
    # R1, R2 & R3: STANDARD (45) + PERSONAL TRAINING (25) * 1 miembro = 70
    subtotal = calculateSubtotal("STANDARD", ["PERSONAL TRAINING"], 1)
    assert subtotal == 70
    assert applyRounding(subtotal) == 70

def test_plan_premium_con_extra_premium():
    # R1, R2 & R3: PREMIUM (70) + SPA (30) * 2 miembros = 200
    subtotal = calculateSubtotal("PREMIUM", ["SPA"], 2)
    assert subtotal == 200
    assert applyRounding(subtotal) == 200

def test_redondeo_half_up_hacia_arriba():
    # R7: Decimal >= 0.5 redondea hacia arriba (121.5 -> 122)
    assert applyRounding(121.5) == 122

def test_redondeo_half_up_hacia_abajo():
    # R7: Decimal < 0.5 redondea hacia abajo (121.4 -> 121)
    assert applyRounding(121.4) == 121

def test_error_plan_invalido():
    # R1: Plan no registrado devuelve -1
    assert calculateSubtotal("INVALID_PLAN", [], 1) == -1

def test_error_extra_desconocido():
    # R2: Extra no registrado devuelve -1
    assert calculateSubtotal("BASIC", ["MASAJE"], 1) == -1

def test_error_extra_premium_en_plan_basico():
    # R2: Extra prémium (SPA) no permitido en plan BASIC -> -1
    assert calculateSubtotal("BASIC", ["SPA"], 1) == -1

def test_error_miembros_menor_a_uno():
    # R3: Cantidad de miembros menor a 1 devuelve -1
    assert calculateSubtotal("BASIC", [], 0) == -1

def test_redondeo_monto_negativo():
    # R7: Manejo de error (-1) en redondeo
    assert applyRounding(-1) == -1