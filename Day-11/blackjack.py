import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_logo():
    logo = """
     ____  _            _        _            _    
    | __ )| | __ _  ___| | __   / \   ___ __ | | __
    |  _ \| |/ _` |/ __| |/ /  / _ \ / __/ _` | |/ /
    | |_) | | (_| | (__|   <  / ___ \ (_| (_| |   < 
    |____/|_|\__,_|\___|_|\_\/_/   \_\___\__,_|_|\_\
    """
    print(logo)

def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def compare(user_score, computer_score):
    if user_score == computer_score:
        return "It's a Draw!"
    elif computer_score == 0:
        return "You lose, opponent has a Blackjack!"
    elif user_score == 0:
        return "You win with a Blackjack!"
    elif user_score > 21:
        return "You went over. You lose!"
    elif computer_score > 21:
        return "Opponent went over. You win!"
    elif user_score > computer_score:
        return "You win!"
    else:
        return "You lose!"

def play_game(balance):
    clear_screen()
    display_logo()

    bet = 0
    valid_bet = False
    while not valid_bet:
        try:
            bet = int(input(f"Your current balance is ${balance}. Enter your bet amount: "))
            if bet > balance:
                print("You cannot bet more than your current balance.")
            elif bet <= 0:
                print("Bet amount must be greater than zero.")
            else:
                valid_bet = True
        except ValueError:
            print("Please enter a valid number.")

    user_cards = []
    computer_cards = []

    for _ in range(2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())

    is_gameover = False
    while not is_gameover:
        user_score = calculate_score(user_cards)
        computer_score = calculate_score(computer_cards)

        print(f"Your cards: {user_cards}, current score: {user_score}")
        print(f"Computer's first card: {computer_cards[0]}")

        if user_score == 0 or computer_score == 0 or user_score > 21:
            is_gameover = True
        else:
            user_should_deal = input("Type 'y' to get another card, type 'n' to pass: ")
            if user_should_deal == "y":
                user_cards.append(deal_card())
            else:
                is_gameover = True

        user_score = calculate_score(user_cards)  # Update user score after dealing a new card

    while computer_score != 0 and computer_score < 17:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    result = compare(user_score, computer_score)
    print(result)

    print(f"Your final hand: {user_cards}, final score: {user_score}")
    print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")

    if "win" in result:
        balance += bet
    elif "lose" in result:
        balance -= bet

    return balance, input("Do you want to play again? Type 'y' for yes, 'n' for no: ")

def main():
    balance = 1000  # Starting balance
    while balance > 0:
        balance, play_again = play_game(balance)
        if play_again.lower() != 'y':
            break
    print("Thanks for playing! Your final balance is ${}".format(balance))

main()
