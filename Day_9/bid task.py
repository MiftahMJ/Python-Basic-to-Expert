import os
from collections import OrderedDict

def clear_screen():
    # Function to clear the console screen for better readability
    os.system('cls' if os.name == 'nt' else 'clear')

def display_logo():
    # Display a welcome message and auction logo
    logo = """
     _    _ _____  ______ _____             _   _  _____ _    _  _____ 
    | |  | |  __ \|  ____|  __ \      /\   | \ | |/ ____| |  | |/ ____|
    | |  | | |__) | |__  | |__) |    /  \  |  \| | |    | |__| | (___  
    | |  | |  _  /|  __| |  _  /    / /\ \ | . ` | |    |  __  |\___ \ 
    | |__| | | \ \| |____| | \ \   / ____ \| |\  | |____| |  | |____) |
     \____/|_|  \_\______|_|  \_\ /_/    \_\_| \_|\_____|_|  |_|_____/ 
    """
    print(logo)
    print("Welcome to the Secret Auction Program!\n")

def get_bidder_info():
    # Get bidder's name and bid amount
    while True:
        name = input("Enter your name: ").strip()
        if name in bids:
            print("This name is already taken. Please enter a unique name.")
        else:
            break
    while True:
        try:
            bid = int(input("Enter your bid amount: $"))
            if bid > 0:
                break
            else:
                print("Bid must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return name, bid

def withdraw_bid():
    # Withdraw a bid
    name = input("Enter your name to withdraw your bid: ").strip()
    if name in bids:
        del bids[name]
        print(f"{name}'s bid has been withdrawn.")
    else:
        print("No bid found for that name.")

def view_highest_bid():
    # View the current highest bid
    if not bids:
        print("No bids have been placed yet.")
    else:
        highest_bidder = max(bids, key=bids.get)
        highest_bid = bids[highest_bidder]
        print(f"The current highest bid is ${highest_bid} by {highest_bidder}.")

def view_bid_history():
    # View the bid history
    if not bids:
        print("No bids have been placed yet.")
    else:
        print("Bid History:")
        for name, bid in bids.items():
            print(f"{name}: ${bid}")

def resolve_winner():
    # Resolve ties by determining the winner based on the earliest bid placed
    if not bids:
        return None, None
    ordered_bids = OrderedDict(sorted(bids.items(), key=lambda x: (-x[1], list(bids.keys()).index(x[0]))))
    winner = next(iter(ordered_bids))
    return winner, ordered_bids[winner]

# Initialize the bids dictionary
bids = {}

def main():
    clear_screen()
    display_logo()
    while True:
        print("\nOptions:")
        print("1. Place a bid")
        print("2. Withdraw a bid")
        print("3. View highest bid")
        print("4. View bid history")
        print("5. End the auction")
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            name, bid = get_bidder_info()
            bids[name] = bid
        elif choice == '2':
            withdraw_bid()
        elif choice == '3':
            view_highest_bid()
        elif choice == '4':
            view_bid_history()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
        
        input("\nPress Enter to continue...")
        clear_screen()

    clear_screen()
    print("Auction has ended!")
    winner, winning_bid = resolve_winner()
    if winner:
        print(f"The winner is {winner} with a bid of ${winning_bid}!")
    else:
        print("No bids were placed.")

if __name__ == "__main__":
    main()
