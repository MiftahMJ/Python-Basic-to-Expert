# from tkinter import *
# import requests
# import time
#
# # Replace 'YOUR_API_KEY' with your actual CoinMarketCap API key
# API_KEY = "c42c554b-4fad-4ff3-ab95-e260270b107f"
#
#
# def fetch_coins():
#     headers = {
#         "X-CMC_PRO_API_KEY": API_KEY,
#         "Accept": "application/json"
#     }
#     attempt = 0
#     while attempt < 5:  # Retry up to 5 times
#         try:
#             response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
#                                     headers=headers, params={"start": "1", "limit": "100", "convert": "USD"})
#             response.raise_for_status()
#             data = response.json()
#             # Extract the coin ID and name from the data
#             return {coin['id']: coin['name'] for coin in data['data']}
#         except requests.exceptions.HTTPError as err:
#             if err.response.status_code == 429:
#                 attempt += 1
#                 wait_time = 2 ** attempt  # Exponential backoff
#                 print(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying...")
#                 time.sleep(wait_time)
#             else:
#                 print(f"HTTP Error: {err}")  # Print HTTP error details
#                 raise err
#     raise Exception("Failed to fetch coins after several attempts")
#
#
# def update_dropdown(*args):
#     search_term = search_var.get().lower()
#     filtered_coins = {k: v for k, v in crypto_names.items() if search_term in v.lower()}
#     menu = coin_menu['menu']
#     menu.delete(0, 'end')
#
#     for coin_id, coin_name in filtered_coins.items():
#         menu.add_command(label=coin_name, command=lambda value=coin_id: selected_coin.set(value))
#
#     # Update the price when dropdown is updated
#     update_crypto_price()
#
#
# def update_crypto_price():
#     crypto_id = selected_coin.get()
#     headers = {
#         "X-CMC_PRO_API_KEY": API_KEY,
#         "Accept": "application/json"
#     }
#     try:
#         response = requests.get(f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest",
#                                 headers=headers, params={"id": crypto_id, "convert": "USD"})
#         response.raise_for_status()
#         data = response.json()
#         print(data)  # Print the raw data to debug
#         if 'data' in data and crypto_id in data['data']:
#             price = data['data'][crypto_id]["quote"]["USD"]["price"]
#
#             # Format the price to 8 decimal places to avoid scientific notation
#             formatted_price = f"{price:.8f}"
#             canvas.itemconfig(price_text, text=f"{crypto_names[crypto_id]} Price: ${formatted_price}")
#         else:
#             canvas.itemconfig(price_text, text="Invalid cryptocurrency ID")
#     except requests.exceptions.HTTPError as e:
#         print(f"HTTP Error: {e}")  # Print HTTP error details
#         if e.response.status_code == 429:
#             canvas.itemconfig(price_text, text="Rate limit exceeded. Please try again later.")
#         else:
#             canvas.itemconfig(price_text, text="Error fetching price")
#     except KeyError as e:
#         print(f"Key Error: {e}")  # Print key error details
#         canvas.itemconfig(price_text, text="Error processing data")
#
#     # Schedule the function to run again after 60 seconds (60000 ms)
#     window.after(60000, update_crypto_price)
#
#
# # Fetch coin list and create a mapping of id to name
# crypto_names = fetch_coins()
#
# window = Tk()
# window.title("Crypto Price")
# window.config(padx=50, pady=50)
#
# canvas = Canvas(width=300, height=414)
# background_img = PhotoImage(file="images/background.png")  # Use your own background image
# canvas.create_image(150, 207, image=background_img)
# price_text = canvas.create_text(150, 207, text="Select a coin to get its price", width=250, font=("Arial", 20, "bold"),
#                                 fill="white")
# canvas.grid(row=0, column=0)
#
# # Entry widget for searching cryptocurrencies
# search_var = StringVar()
# search_var.trace("w", update_dropdown)  # Call update_dropdown whenever search_var changes
# search_entry = Entry(window, textvariable=search_var, font=("Arial", 14))
# search_entry.grid(row=1, column=0, pady=10)
#
# # Create an OptionMenu for selecting a cryptocurrency
# selected_coin = StringVar()
# selected_coin.set(list(crypto_names.keys())[0])  # Set default selection to the first coin
#
# coin_menu = OptionMenu(window, selected_coin, *crypto_names.values())  # Use values() for names
# coin_menu.grid(row=2, column=0, pady=10)
#
# # Create a simple button to start fetching the price
# fetch_price_button = Button(text="Start Live Price Update", command=update_crypto_price, font=("Arial", 14))
# fetch_price_button.grid(row=3, column=0)
#
# window.mainloop()
from tkinter import *
import requests
import time

# Replace 'YOUR_API_KEY' with your actual CoinMarketCap API key
API_KEY = "c42c554b-4fad-4ff3-ab95-e260270b107f"

def fetch_coins():
    headers = {
        "X-CMC_PRO_API_KEY": API_KEY,
        "Accept": "application/json"
    }
    attempt = 0
    while attempt < 5:  # Retry up to 5 times
        try:
            response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
                                    headers=headers, params={"start": "1", "limit": "100", "convert": "USD"})
            response.raise_for_status()
            data = response.json()
            # Extract the coin symbol and name from the data
            return {coin['symbol']: coin['name'] for coin in data['data']}
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                attempt += 1
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print(f"HTTP Error: {err}")  # Print HTTP error details
                raise err
    raise Exception("Failed to fetch coins after several attempts")

def update_dropdown(*args):
    search_term = search_var.get().lower()
    filtered_coins = {k: v for k, v in crypto_names.items() if search_term in v.lower()}
    menu = coin_menu['menu']
    menu.delete(0, 'end')

    for coin_id, coin_name in filtered_coins.items():
        menu.add_command(label=coin_name, command=lambda value=coin_id: selected_coin.set(value))

    # Update the price when dropdown is updated
    update_crypto_price()

def update_crypto_price():
    crypto_id = selected_coin.get()
    headers = {
        "X-CMC_PRO_API_KEY": API_KEY,
        "Accept": "application/json"
    }
    try:
        response = requests.get(f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest",
                                headers=headers, params={"symbol": crypto_id, "convert": "USD"})
        response.raise_for_status()
        data = response.json()
        if 'data' in data and crypto_id in data['data']:
            price = data['data'][crypto_id]["quote"]["USD"]["price"]

            # Format the price to 8 decimal places to avoid scientific notation
            formatted_price = f"{price:.8f}"
            canvas.itemconfig(price_text, text=f"{crypto_names[crypto_id]} Price: ${formatted_price}")
        else:
            canvas.itemconfig(price_text, text="Invalid cryptocurrency ID")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")  # Print HTTP error details
        if e.response.status_code == 429:
            canvas.itemconfig(price_text, text="Rate limit exceeded. Please try again later.")
        else:
            canvas.itemconfig(price_text, text="Error fetching price")
    except KeyError as e:
        print(f"Key Error: {e}")  # Print key error details
        canvas.itemconfig(price_text, text="Error processing data")

    # Schedule the function to run again after 60 seconds (60000 ms)
    window.after(10000, update_crypto_price)

# Fetch coin list and create a mapping of symbol to name
crypto_names = fetch_coins()

window = Tk()
window.title("Crypto Price")
window.config(padx=50, pady=50)

canvas = Canvas(width=300, height=414)
background_img = PhotoImage(file="images/background.png")  # Use your own background image
canvas.create_image(150, 207, image=background_img)
price_text = canvas.create_text(150, 207, text="Select a coin to get its price", width=250, font=("Arial", 20, "bold"),
                                fill="white")
canvas.grid(row=0, column=0)

# Entry widget for searching cryptocurrencies
search_var = StringVar()
search_var.trace("w", update_dropdown)  # Call update_dropdown whenever search_var changes
search_entry = Entry(window, textvariable=search_var, font=("Arial", 14))
search_entry.grid(row=1, column=0, pady=10)

# Create an OptionMenu for selecting a cryptocurrency
selected_coin = StringVar()
selected_coin.set(list(crypto_names.keys())[0])  # Set default selection to the first coin

coin_menu = OptionMenu(window, selected_coin, *crypto_names.keys())  # Use keys() for symbols
coin_menu.grid(row=2, column=0, pady=10)

# Create a simple button to start fetching the price
fetch_price_button = Button(text="Start Live Price Update", command=update_crypto_price, font=("Arial", 14))
fetch_price_button.grid(row=3, column=0)

window.mainloop()
