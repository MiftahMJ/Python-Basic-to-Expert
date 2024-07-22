from tkinter import *
from tkinter import messagebox
from random import choice,randint,shuffle
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
import random
letters = ['a' , 'b' , 'c', 'd', 'e', 'f', 'g', 'h','j', 'j', 'k', 'l', 'm','n','o','p','q','r', 's','t', 'u', 'v', 'w', 'x', 'y', 'z','A','B,','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
numbers =['0','1','2','3','4','5','6','7','8','9']
symbols = ['!','#','$','%','&','(',')','*','+']

def generate_password():
    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)


    password="".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website)==0 or len(password)==0:
        messagebox.showinfo(title="Oops",message="Please make sure you have not left any fields empty")

    is_ok = messagebox.askokcancel(title="website",
                                   message=f"These are the details entered:\nEmail:{email}"f"\nPassword:{password}\n is it ok to save?")
    if is_ok:
        with open("data.txt", "a") as file_data:
            file_data.write(f"{website}| {email}|{password}\n")
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pasword Generator")
window.config(padx=50, pady=50)
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)

canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username")
email_label.grid(row=2, column=0)

password_label = Label(text="password")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "miftahjabeen@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Generate password
generate_password_button = Button(text="Generate password",command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

canvas.mainloop()
