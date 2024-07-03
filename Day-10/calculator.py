import math

logo = """   ____      _            _       _             
  / ___|__ _| | ___ _   _| | __ _| |_ ___  _ __ 
 | |   / _` | |/ __| | | | |/ _` | __/ _ \| '__|
 | |__| (_| | | (__| |_| | | (_| | || (_) | |   
  \____\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   
                                               
 ___________________________________
|  _______________________________  |
| |  1  |  2  |  3  |  +  |       | |
| |_____|_____|_____|_____|_______| |
| |  4  |  5  |  6  |  -  |       | |
| |_____|_____|_____|_____|_______| |
| |  7  |  8  |  9  |  *  |       | |
| |_____|_____|_____|_____|_______| |
| |  0  |  .  |  =  |  /  |       | |
| |_____|_____|_____|_____|_______| |
|___________________________________|
"""
print(logo)

# add
def add(n1, n2):
    return n1 + n2

# subtract
def sub(n1, n2):
    return n1 - n2

# multiply
def multiply(n1, n2):
    return n1 * n2

# divide
def divide(n1, n2):
    if n2 != 0:
        return n1 / n2
    else:
        return "Error! Division by zero."

# exponent
def exponent(n1, n2):
    return n1 ** n2

# square root
def square_root(num1):
    if num1 >= 0:
        return math.sqrt(num1)
    else:
        return "Error! Square root of a negative number."

operations = {
    "+": add,
    "-": sub,
    "*": multiply,
    "/": divide,
    "**": exponent,
    "sqrt": square_root
}

history = []

while True:
    num1 = input("What's the first number? ")
    
    # Validate num1 input
    try:
        num1 = float(num1)
    except ValueError:
        print("Invalid number, please enter a valid number.")
        continue

    for symbol in operations:
        print(symbol)

    operation_symbol = input("Choose the symbol of operation from above: ")

    if operation_symbol not in operations:
        print("Invalid operation, please try again.")
        continue
    
    if operation_symbol == "sqrt":
        result = operations[operation_symbol](num1)
        print(f"sqrt({num1}) = {result}")
    else:
        num2 = input("What's the second number? ")
        
        # Validate num2 input
        try:
            num2 = float(num2)
        except ValueError:
            print("Invalid number, please enter a valid number.")
            continue
        
        calculation_operation = operations[operation_symbol]
        result = calculation_operation(num1, num2)
        print(f"{num1} {operation_symbol} {num2} = {result}")

    history.append(f"{num1} {operation_symbol} {num2} = {result}")

    # Ask if the user wants another calculation
    next_calculation = input("Do you want to perform another calculation? (yes/no): ")
    if next_calculation.lower() != 'yes':
        break

# Save history to a file
filename = "history.txt"
with open(filename, 'w') as file:
    for calc in history:
        file.write(calc + "\n")

print(f"Calculation history saved to {filename}.")
