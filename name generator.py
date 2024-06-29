import random
letters = ['a' , 'b' , 'c', 'd', 'e', 'f', 'g', 'h','j', 'j', 'k', 'l', 'm','n','o','p','q','r', 's','t', 'u', 'v', 'w', 'x', 'y', 'z','A','B,','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
numbers =['0','1','2','3','4','5','6','7','8','9']
symbols = ['!','#','$','%','&','(',')','*','+']

# User input
print("Welcome to the Username Generator!")
nr_letters = int(input("How many Letters: "))
nr_numbers = int(input("How many Numbers: "))
nr_symbols = int(input("How manySymbols: "))
pattern_choice = input("Patterned (P) or Randomized (R): ").upper()
start_end_choice = input("Start (S), End (E), or No preference (N): ").upper()

if start_end_choice in ['S', 'E']:
    char_type = input("Start/End with (Letter/Number/Symbol): ").lower()
else:
    char_type = None

# Generate username
username_list = []

for name in range(nr_letters):
    username_list.append(random.choice(letters))
for name in range(nr_numbers):
    username_list.append(random.choice(numbers))
for name in range(nr_symbols):
    username_list.append(random.choice(symbols))

if pattern_choice == 'P':
    pattern_username = ''.join(username_list)
    if start_end_choice == 'S':
        if char_type == 'letter':
            start_char = random.choice(letters)
            pattern_username = start_char + pattern_username[1:]
        elif char_type == 'number':
            start_char = random.choice(numbers)
            pattern_username = start_char + pattern_username[1:]
        elif char_type == 'symbol':
            start_char = random.choice(symbols)
            pattern_username = start_char + pattern_username[1:]
    elif start_end_choice == 'E':
        if char_type == 'letter':
            end_char = random.choice(letters)
            pattern_username = pattern_username[:-1] + end_char
        elif char_type == 'number':
            end_char = random.choice(numbers)
            pattern_username = pattern_username[:-1] + end_char
        elif char_type == 'symbol':
            end_char = random.choice(symbols)
            pattern_username = pattern_username[:-1] + end_char
    username = pattern_username
else:
    random.shuffle(username_list)
    if start_end_choice == 'S':
        if char_type == 'letter':
            username_list[0] = random.choice(letters)
        elif char_type == 'number':
            username_list[0] = random.choice(numbers)
        elif char_type == 'symbol':
            username_list[0] = random.choice(symbols)
    elif start_end_choice == 'E':
        if char_type == 'letter':
            username_list[-1] = random.choice(letters)
        elif char_type == 'number':
            username_list[-1] = random.choice(numbers)
        elif char_type == 'symbol':
            username_list[-1] = random.choice(symbols)
    username = ''.join(username_list)

print(f"Your generated username is: {username}")
