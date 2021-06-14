from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Choose randoms letters, symbols and numbers and add them to a list
    password_letter = [choice(letters) for letter in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]

    # Join the three lists and shuffle them
    password_list = password_letter + password_symbols + password_numbers
    shuffle(password_list)

    # Convert list to string
    password = "".join(password_list)

    # Insert the new password to the password entry
    password_input.delete(0, END)
    password_input.insert(0, password)

    # Add password to the clipboard
    pyperclip.copy(text=password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get().title()
    email = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # Check if there are any field empty.
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", mode="r") as f:
                # Reading old data
                data = json.load(f)

        except FileNotFoundError:
            # Creating a new file
            with open("data.json", mode="w") as f:
                json.dump(new_data, f, indent=4)

        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", mode="w") as f:
                # Saving updated data
                json.dump(data, f, indent=4)

        finally:
            # Clean the entries
            website_input.delete(0, END)
            password_input.delete(0, END)
            website_input.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website_to_find = website_input.get().title()

    try:
        with open("data.json", mode="r") as f:
            data = json.load(f)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")

    else:
        if website_to_find in data:
            email = data[website_to_find]["email"]
            password = data[website_to_find]["password"]
            messagebox.showinfo(title=website_to_find, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for the {website_to_find} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas SETUP
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_input = Entry(width=27)
website_input.grid(column=1, row=1)
website_input.focus()

username_input = Entry(width=45)
username_input.grid(column=1, row=2, columnspan=2)

password_input = Entry(width=27)
password_input.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate Password", width=14, command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=42, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
