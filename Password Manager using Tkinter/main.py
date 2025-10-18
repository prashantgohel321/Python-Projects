import tkinter as tk
from tkinter import messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pyperclip
import json
from random import choice, randint, shuffle

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Helvetica"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generates a random, strong password and copies it to the clipboard."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title="Password Generated", message="Password copied to clipboard!")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Saves the website, email, and password to a JSON file."""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if not website or not password:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
        return

    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                      f"\nPassword: {password} \nIs it ok to save?")
    if is_ok:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        
        data.update(new_data)

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        website_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    """Finds and displays the password for a given website."""
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror(title="Error", message="No Data File Found.")
        return
    
    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        pyperclip.copy(password)
        messagebox.showinfo(title="Copied", message="Password for {} copied to clipboard.".format(website))
    else:
        messagebox.showerror(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = ttk.Window(themename="superhero")
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
logo_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, pady=(0, 20))

# Labels
website_label = ttk.Label(text="Website:", font=(FONT_NAME, 12))
website_label.grid(row=1, column=0, sticky="W")
email_label = ttk.Label(text="Email/Username:", font=(FONT_NAME, 12))
email_label.grid(row=2, column=0, sticky="W")
password_label = ttk.Label(text="Password:", font=(FONT_NAME, 12))
password_label.grid(row=3, column=0, sticky="W")

# Entries
website_entry = ttk.Entry(width=32)
website_entry.grid(row=1, column=1, pady=5, sticky="EW")
website_entry.focus()
email_entry = ttk.Entry(width=50)
email_entry.grid(row=2, column=1, columnspan=2, pady=5, sticky="EW")
email_entry.insert(0, "example@email.com")
password_entry = ttk.Entry(width=32)
password_entry.grid(row=3, column=1, pady=5, sticky="EW")

# Buttons
search_button = ttk.Button(text="Search", width=14, command=find_password, style="info.TButton")
search_button.grid(row=1, column=2, sticky="EW", padx=(5,0))
generate_password_button = ttk.Button(text="Generate Password", command=generate_password, style="success.TButton")
generate_password_button.grid(row=3, column=2, sticky="EW", padx=(5,0))
add_button = ttk.Button(text="Add", width=43, command=save, style="primary.TButton")
add_button.grid(row=4, column=1, columnspan=2, pady=(10,0), sticky="EW")


window.mainloop()
