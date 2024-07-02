import string

def display_logo():
    logo = """
     ____                       ____ _       _           
    / ___| __ _ _ __ ___   ___ / ___(_)_ __ | |__  _   _ 
   | |  _ / _` | '_ ` _ \ / _ \ |   | | '_ \| '_ \| | | |
   | |_| | (_| | | | | | |  __/ |___| | | | | | | | |_| |
    \____|\__,_|_| |_| |_|\___|\____|_|_| |_|_| |_|\__, |
                                                   |___/ 
    """
    print(logo)

def get_user_choice():
    while True:
        choice = input("Would you like to encode or decode a message? (Enter 'encode' or 'decode'): ").lower()
        if choice in ['encode', 'decode']:
            return choice
        else:
            print("Invalid choice. Please enter 'encode' or 'decode'.")

def get_shift_amount():
    while True:
        try:
            shift = int(input("Enter the shift amount: "))
            return shift
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def process_message(message, shift, encode=True):
    result = []
    for char in message:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            new_char = chr((ord(char) - offset + (shift if encode else -shift)) % 26 + offset)
            result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)

def save_to_file(message):
    filename = input("Enter the filename to save the message: ")
    with open(filename, 'w') as file:
        file.write(message)
    print(f"Message saved to {filename}")

def read_from_file():
    filename = input("Enter the filename to read the message from: ")
    try:
        with open(filename, 'r') as file:
            message = file.read()
        return message
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None

def main():
    display_logo()
    while True:
        choice = get_user_choice()
        if choice == 'encode':
            message = input("Enter the message to encode: ")
            shift = get_shift_amount()
            encoded_message = process_message(message, shift, encode=True)
            print(f"Encoded message: {encoded_message}")
            
            save_option = input("Would you like to save the encoded message to a file? (yes/no): ").lower()
            if save_option == 'yes':
                save_to_file(encoded_message)
        
        elif choice == 'decode':
            read_option = input("Would you like to read the encoded message from a file? (yes/no): ").lower()
            if read_option == 'yes':
                message = read_from_file()
                if message is None:
                    continue
            else:
                message = input("Enter the message to decode: ")
            
            shift = get_shift_amount()
            decoded_message = process_message(message, shift, encode=False)
            print(f"Decoded message: {decoded_message}")
        
        restart = input("Would you like to encode/decode another message? (yes/no): ").lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
