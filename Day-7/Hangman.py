import random

easy=["apple", "ball", "cat", "dog", "egg"]
medium=["orange", "guitar", "python", "flower", "banana"]
hard=["hangman", "difficult", "elephant", "knowledge", "mystery"]
# Hangman stages
stages = ['''
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
      |
      |
      |
      |
=========
''']

def select_word(difficulty):
    if difficulty == 'easy':
        return random.choice(easy)
    elif difficulty == 'medium':
        return random.choice(medium)
    elif difficulty == 'hard':
        return random.choice(hard)
    else:
        print("invalid entry...defaulting to easy")
        return random.choice(easy)

def display_word(word,guessed_letter):
    display=""
    for letter in word:
        if letter in guessed_letter:
            display += letter + ""
        else:
            display += "_" 
        return display.strip() 

# Function to provide a hint
def provide_hint(word, guessed_letters):
    remaining_letters = [letter for letter in word if letter not in guessed_letters]
    if remaining_letters:
        return random.choice(remaining_letters)
    else:
        return None             
    #Hangman
def hangman():
    print("Welcome to the Hangman")
    difficulty=input("Select Difficulty level (easy,medium,hard)").lower()
    word= select_word(difficulty)
    guessed_letters = set()
    lives=6
    score=0
    hint_used=False
    print(stages[lives])
    print(display_word(word,guessed_letters))    

    while lives>0 and set(word) != guessed_letters:
        guess= input("GUess a letter:").lower()
        if guess== 'hint' and not hint_used:
            hint= provide_hint(word, guessed_letters)
            if hint:
                print(f"Hint:One of the letters is {hint}")
                hint_used=True
                score-=5
            else:
                print("No hints available")
                continue
        elif guess== 'hint' and hint_used:
            print("Hint already used!")
            continue 
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please guess a single letter.")
            continue
        
        if guess in guessed_letters:
            print("You have already guessed that letter. Try again.")
            continue

        guessed_letters.add(guess)
        
        if guess in word:
            score += 10  # Reward points for correct guess
            print(f"Good guess! {guess} is in the word.")
        else:
            lives -= 1
            score -= 1  # Deduct points for incorrect guess
            print(f"Incorrect guess. You have {lives} lives left.")
        
        print(stages[lives])
        print(display_word(word, guessed_letters))

    if set(word) == guessed_letters:
        print("Congratulations! You've won!")
        print(f"The word was: {word}")
    else:
        print("Game over. You've run out of lives.")
        print(f"The word was: {word}")

    print(f"Your final score is: {score}")

# Run the game
hangman()