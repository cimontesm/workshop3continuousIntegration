from developerA import (
    calculateSubtotal,
    applyRounding
)
from pricing_rules import (
    apply_group_discount,
    apply_special_offer,
    apply_premium_surcharge,
)



def main():
    print("=== GYM MEMBERSHIP SYSTEM ===")
    
    # 1. Solicitar parámetros al usuario
    plan = input("Enter plan (BASIC, STANDARD, PREMIUM): ").strip().upper()
    
    extras_input = input("Enter extras separated by comma (GROUP CLASSES, PERSONAL TRAINING, SPA, SPECIALIZED_PROGRAM) or leave blank: ").strip()
    if extras_input:
        extras = [e.strip().upper() for e in extras_input.split(",")]
    else:
        extras = []
        
    try:
        members = int(input("Enter number of members: "))
    except ValueError:
        print("Invalid number of members. Result: -1")
        return -1

    # Verificar si incluye algún extra prémium
    premium_extras = {"SPA", "SPECIALIZED_PROGRAM"}
    has_premium_extra = any(extra in premium_extras for extra in extras)

    # 2. Ejecutar las funciones en el orden correcto
    amount = calculateSubtotal(plan, extras, members)
    if amount == -1:
        print("Invalid selection or inputs. Result: -1")
        return -1

    amount = apply_group_discount(amount, members)
    amount = apply_special_offer(amount)
    amount = apply_premium_surcharge(amount, has_premium_extra)
    
    final_result = applyRounding(amount)

    print(f"\nFinal Quoted Price: ${final_result}")

    # 3. Confirmación final (y/n)
    confirmation = input("Do you wish to confirm this quote? (y/n): ").strip().lower()
    if confirmation != 'y':
        print("Quote cancelled by user. Result: -1")
        return -1

    print("Quote confirmed successfully!")
    return final_result

if __name__ == "__main__":
    main()