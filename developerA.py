import math

def calculateSubtotal(plan, extras, members):
    plan_prices = {
        "BASIC": 30,
        "STANDARD": 45,
        "PREMIUM": 70
    }

    if plan not in plan_prices:
        return -1

    extra_prices = {
        "GROUP CLASSES": {"price": 15, "PREMIUM": False},
        "PERSONAL TRAINING": {"price": 25, "PREMIUM": False},
        "SPA": {"price": 30, "PREMIUM": True},
        "SPECIALIZED_PROGRAM": {"price": 40, "PREMIUM": True}
    }

    extra_price = 0
    for extra in extras: 
        if extra not in extra_prices:
            return -1

        if extra_prices[extra]["PREMIUM"] and plan != "PREMIUM":
            return -1

        extra_price += extra_prices[extra]["price"]

    if members < 1:
        return -1

    subtotal = (plan_prices[plan] + extra_price) * members
    return subtotal



def applyRounding(subtotal):
    if subtotal < 0:
        return -1
        
    amount = float(subtotal)
    whole = math.floor(amount)
    decimal = amount - whole
    total = whole + 1 if decimal >= 0.5 else whole
    
    return int(total)