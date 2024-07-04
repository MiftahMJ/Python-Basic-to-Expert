import random
logo="""  _____                       _____                       
 / ____|                     |  __ \                      
| |  __  __ _ _ __ ___   ___ | |  | | __ _ _ __ ___   ___ 
| | |_ |/ _` | '_ ` _ \ / _ \| |  | |/ _` | '_ ` _ \ / _ \
| |__| | (_| | | | | | |  __/| |__| | (_| | | | | | |  __/
 \_____|\__,_|_| |_| |_|\___||_____/ \__,_|_| |_| |_|\___|
                                                          
                                                          
"""
print(logo)
print("Welcome to the Number Guessing Game!\n")
print("I am thinking of a number between 1 and 100")
# number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
number = list(range(1, 101))
random_num = random.choice(number)

def difficulty():
    select_difficulty = input("Select Difficulty level 'easy' or 'hard'? ")
    if select_difficulty == "easy":
       return 10
    else:
       return 5
        
difficulty()

is_game_over = False
while not is_game_over:
    def guess():
        choice = int(input("Guess a number: "))
        if choice <1:
            print("Choose Greater than 1")
        elif choice >100:
            print("Choose under 100")
   

        # boundary=[]
       
        
        if random_num > choice:
            print("Too low")
        elif random_num < choice:
            print("Too high")
        elif choice==0:
            print("Warning:Choose between 1 and 100")    
        else:
            print("Hurrah! You guessed the number")
            return True
        min=[5,10,15]
        max=[5,10,15]
        min_boundary=random_num-random.choice(min)
        max_boundary=random_num+random.choice(max)
        if min_boundary< 0 and max_boundary>100:
            print("0")
            
        
        print(f"Choose between{min_boundary} and {max_boundary}")
    if guess():
        is_game_over = True
