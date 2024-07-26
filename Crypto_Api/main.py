from tkinter import *
import requests
import time


def fetch_coins():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets",
                                params={"vs_currency": "usd"})
        response.raise_for_status()
        data = response.json()
        return {coin['id']: coin['name'] for coin in data}
    except requests.exceptions.HTTPError as err:
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting before retrying...")
            time.sleep(60)  # Wait for 60 seconds before retrying
            return fetch_coins()  # Retry fetching coins
        else:
            raise err


def update_dropdown(*args):
    search_term = search_var.get().lower()
    filtered_coins = {k: v for k, v in crypto_names.items() if search_term in v.lower()}
    menu = coin_menu['menu']
    menu.delete(0, 'end')

    for coin_id in filtered_coins:
        menu.add_command(label=filtered_coins[coin_id],
                         command=lambda value=coin_id: selected_coin.set(value))

    # Update the price when dropdown is updated
    update_crypto_price()


def update_crypto_price():
    crypto_id = selected_coin.get()
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd")
        response.raise_for_status()
        data = response.json()
        price = data[crypto_id]["usd"]

        # Format the price to 8 decimal places to avoid scientific notation
        formatted_price = f"{price:.8f}"
        canvas.itemconfig(price_text, text=f"{crypto_names[crypto_id]} Price: ${formatted_price}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            canvas.itemconfig(price_text, text="Rate limit exceeded. Please try again later.")
        else:
            canvas.itemconfig(price_text, text="Error fetching price")

    # Schedule the function to run again after 5000 ms (5 seconds)
    window.after(1000, update_crypto_price)


# Fetch coin list and create a mapping of id to name
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

coin_menu = OptionMenu(window, selected_coin, *crypto_names.keys())
coin_menu.grid(row=2, column=0, pady=10)

# Create a simple button to start fetching the price
fetch_price_button = Button(text="Start Live Price Update", command=update_crypto_price, font=("Arial", 14))
fetch_price_button.grid(row=3, column=0)

window.mainloop()
# c42c554b-4fad-4ff3-ab95-e260270b107f