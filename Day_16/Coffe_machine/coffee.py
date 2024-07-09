import money_machine as mm

is_on = True

while is_on:
    choice = input("What would you like? (espresso/latte/cappuccino): ").lower()

    if choice == "off":
        is_on = False
    elif choice == "report":
        print(f"Water: {mm.resources['water']} ml")
        print(f"Milk: {mm.resources['milk']} ml")
        print(f"Coffee: {mm.resources['coffee']} g")
        print(f"Money: ${mm.profit}")
    else:
        drink = mm.MENU[choice]
        if mm.is_resource_sufficient(drink["ingredients"]):
            payment = mm.process_coins()
            if mm.is_transaction_successful(payment, drink["cost"]):
                mm.make_coffee(choice, drink["ingredients"])
