import random

# Display art
logo="""  _____           _       _             
 |  __ \         | |     | |            
 | |__) |___  ___| | __ _| |_ ___  _ __ 
 |  _  // _ \/ __| |/ _` | __/ _ \| '__|
 | | \ \  __/ (__| | (_| | || (_) | |   
 |_|  \_\___|\___|_|\__,_|\__\___/|_|   
"""
def format_data(account):
    
  account_name=account["username"]
  account_pswd=account["password"]
    
    
  account_email=account["email"]
  account_score=account["score"]
    
  return(f"{account_name}, a{account_pswd},{account_email},{account_score}")
# generate random account for game data
accounts = {
    'Tom Cruise': {
        'username': '',
        'password': '',
        'email': '',
        'score': 800
    },
    'Jennifer Lawrence': {
        'username': '',
        'password': '',
        'email': '',
        'score': 720
    },
    'Leonardo DiCaprio': {
        'username': '',
        'password': '',
        'email': '',
        'score': 900
    },
    'Scarlett Johansson': {
        'username': '',
        'password': '',
        'email': '',
        'score': 850
    },
    'Dwayne Johnson': {
        'username': '',
        'password': '',
        'email': '',
        'score': 950
    },
    'Emma Watson': {
        'username': '',
        'password': '',
        'email': '',
        'score': 780
    },
    'Brad Pitt': {
        'username': '',
        'password': '',
        'email': '',
        'score': 890
    },
    'Angelina Jolie': {
        'username': '',
        'password': '',
        'email': '',
        'score': 820
    },
    'Robert Downey Jr.': {
        'username': '',
        'password': '',
        'email': '',
        'score': 920
    },
    'Chris Hemsworth': {
        'username': '',
        'password': '',
        'email': '',
        'score': 880
    },
    'Gal Gadot': {
        'username': '',
        'password': '',
        'email': '',
        'score': 830
    },
    'Will Smith': {
        'username': '',
        'password': '',
        'email': '',
        'score': 940
    },
    'Margot Robbie': {
        'username': '',
        'password': '',
        'email': '',
        'score': 860
    },
    'Chris Evans': {
        'username': '',
        'password': '',
        'email': '',
        'score': 910
    },
    'Ryan Reynolds': {
        'username': '',
        'password': '',
        'email': '',
        'score': 790
    },
    'Natalie Portman': {
        'username': '',
        'password': '',
        'email': '',
        'score': 870
    },
    'Matt Damon': {
        'username': '',
        'password': '',
        'email': '',
        'score': 800
    },
    'Johnny Depp': {
        'username': '',
        'password': '',
        'email': '',
        'score': 920
    },
    'Chris Pratt': {
        'username': '',
        'password': '',
        'email': '',
        'score': 850
    },
    'Tom Hanks': {
        'username': '',
        'password': '',
        'email': '',
        'score': 930
    },
    'Anne Hathaway': {
        'username': '',
        'password': '',
        'email': '',
        'score': 810
    },
    'Jennifer Aniston': {
        'username': '',
        'password': '',
        'email': '',
        'score': 890
    },
    'Julia Roberts': {
        'username': '',
        'password': '',
        'email': '',
        'score': 870
    },
    'Daniel Radcliffe': {
        'username': '',
        'password': '',
        'email': '',
        'score': 800
    },
    'Emma Stone': {
        'username': '',
        'password': '',
        'email': '',
        'score': 920
    },
    'Kristen Stewart': {
        'username': '',
        'password': '',
        'email': '',
        'score': 860
    },
    'Vin Diesel': {
        'username': '',
        'password': '',
        'email': '',
        'score': 890
    },
    'Meryl Streep': {
        'username': '',
        'password': '',
        'email': '',
        'score': 830
    },
    'Charlize Theron': {
        'username': '',
        'password': '',
        'email': '',
        'score': 940
    },
    'Jake Gyllenhaal': {
        'username': '',
        'password': '',
        'email': '',
        'score': 780
    },
    'Eddie Redmayne': {
        'username': '',
        'password': '',
        'email': '',
        'score': 910
    },
    'Reese Witherspoon': {
        'username': '',
        'password': '',
        'email': '',
        'score': 870
    },
    'Matthew McConaughey': {
        'username': '',
        'password': '',
        'email': '',
        'score': 800
    }
    
}
# Randomly choose two different celebrity accounts for comparison
account_a = random.choice(list(accounts.keys()))
account_b = random.choice(list(accounts.keys()))
while account_a == account_b:
    account_b = random.choice(list(accounts.keys()))
print(f"Compare A:{format_data(account_a)}")
print(f"Compare B:{format_data(account_b)}")
# format account data into printable format

# ask user guess

# check if user corect

# get follower account of each count

# use if statement to check if user is correct

# give userfeedback on their guess
# make game repeatable
# making account at position b become the next acount at position a
# clear screen
