from utils import *


class Drinks:
    def __init__(self, name):
        self.price = MENU[name]['cost']
        self.name = name if name in MENU else None
        self.ingredients = MENU[name]['ingredients']

    def get_name(self):
        return self.name

    def get_ingredients(self):
        return self.ingredients

    def get_price(self):
        return self.price

    def contains_milk(self):
        return len([x for x in self.ingredients.items() if 'milk' in x]) > 0

    def print_info(self):
        print(f"{self.name} is made with {self.ingredients} and costs ${self.price}")


class Machine:
    def __init__(self):
        self.resources = resources
        self.profit = 0

    def get_profit(self):
        return self.profit

    def update_profit(self, drink_price):
        self.profit += drink_price

    def get_resources(self):
        return self.resources

    def update_resources(self, drink: Drinks):
        self.resources['coffee'] -= drink.get_ingredients()['coffee']
        self.resources['water'] -= drink.get_ingredients()['water']
        if drink.contains_milk():
            self.resources['milk'] -= drink.get_ingredients()['milk']

    def check_resources(self, drink: Drinks):
        selected_drink_ingredients = drink.get_ingredients()
        if drink.contains_milk():
            return self.resources['water'] - selected_drink_ingredients['water'] >= 0 and self.resources['milk'] - \
                selected_drink_ingredients['milk'] >= 0 and self.resources['coffee'] - selected_drink_ingredients[
                    'coffee'] >= 0
        else:
            return self.resources['water'] - selected_drink_ingredients['water'] >= 0 and self.resources['coffee'] - \
                selected_drink_ingredients['coffee'] >= 0

    def report(self):
        print(f"Water: {self.resources['water']}\n"
              f"Milk: {self.resources['milk']}\n"
              f"Coffee: {self.resources['coffee']}\n"
              f"Profit: ${self.profit}")


machine = Machine()
should_work = True
inserted_coins = 0
total_coins = 0


def insert_coins():
    p = int(input("How many pennies?"))
    n = int(input("How many nickles?"))
    q = int(input("How many quarters?"))
    d = int(input("How many dimes?"))
    return coins['q'] * q + coins['p'] * p + coins['d'] * d + coins['n'] * n


def serve(drink: Drinks, total_paid):
    print(f"Here is your {drink.get_name()}")
    if total_paid > drink.get_price():
        print(f"You will get ${round(total_paid - drink.get_price(), 2)} back")
    machine.update_resources(drink)
    machine.update_profit(drink.get_price())


while should_work:
    selection = input("What would you like?(cappuccino, latte, espresso):")
    if selection == "turn off":
        print("Turning off the machine. Goodbye")
        exit(0)
    elif selection == "report":
        machine.report()
    else:
        try:
            selected_drink = Drinks(selection)
            if machine.check_resources(selected_drink):
                print("Please insert coins")
                inserted_coins = insert_coins()

                if inserted_coins >= selected_drink.get_price():
                    serve(selected_drink, inserted_coins)
                else:
                    print(f"Not enough money, refunding {inserted_coins}")
            else:
                print(f"Not enough resources to serve you {selected_drink.get_name()}")
        except KeyError:
            print(f"{selection} is not served by this machine")
