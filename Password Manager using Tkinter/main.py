from tkinter import *
from tkinter import messagebox
import pyperclip
import json
import os

# Constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Ubuntu Light"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator
from random import choice, randint, shuffle
def pass_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_letters = [choice(letters) for _ in range(nr_letters + 1)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols + 1)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers + 1)]
    
    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)
    # for char in password_list:
    #     password += char
    pyperclip.copy(password)
    passw_input.insert(END, string=password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def click_add_btn():
    
    new_data = {
        website_input.get():{
            "email": email_input.get(),
            "password": passw_input.get()
        }
    }
    
    if len(website_input.get()) < 1 or len(passw_input.get()) < 1:
        messagebox.showinfo(title = "Oops", message = "Please dont leave any fields empty")
    
    else:
        ask = messagebox.askokcancel(title = website_input.get(), message = f"These are the details entered: \nEmail: {email_input.get()} \nPassword: {passw_input.get()} \nIs it ok to save?")
        
        if ask:
            
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file) 
            
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent = 4)
            
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent = 4)
            
            finally:  
                website_input.delete(0, END)
                passw_input.delete(0, END)
                

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            web_dict = data[website]
            web_email = web_dict["email"]
            web_password = web_dict["password"]
    except FileNotFoundError:
        messagebox.showinfo(title = "Oops", message = "No Data file found")
    except KeyError:
        messagebox.showinfo(title = "Oops", message = "No details for the website exists.")
    else:
        messagebox.showinfo(title = website, message = f"Email: {web_email}\nPassword: {web_password}")
        passw_input.insert(END, string = web_password)
        email_input.delete(0, END)
        email_input.insert(END, string = web_email)

    



# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Password manager")
window.config(padx = 70, pady = 70, bg = "white")

canvas = Canvas(width = 220, height = 220, bg = "white", highlightthickness=0)
logo = PhotoImage(file = "logo.png")
canvas.create_image(110, 110, image = logo)
canvas.grid(row = 0, column = 1, columnspan=2)



# LABELS
website_label = Label(text = "Website:", bg = "white", font = (FONT_NAME, 15, 'bold'))
website_label.grid(row = 1, column = 0, padx = 10, pady = 10)

email_label = Label(text = "Email/Username:", bg = "white", font = (FONT_NAME, 15, 'bold'))
email_label.grid(row = 2, column = 0, padx = 10, pady = 10)

passw_label = Label(text = "Password:", bg = "white", font = (FONT_NAME, 15, 'bold'))
passw_label.grid(row = 3, column = 0, padx = 10, pady = 10)



# ENTRIES
website_input = Entry(width = 22, font = (FONT_NAME, 15), border=2, borderwidth=2)
website_input.focus()
website_input.grid(row = 1, column = 1, padx = 10)

email_input = Entry(width = 42, font = (FONT_NAME, 15), border=2, borderwidth=2)
email_input.grid(row = 2, column = 1, columnspan = 2)
email_input.insert(0, "example@gmail.com")

passw_input = Entry(width = 22, font = (FONT_NAME, 15), border=2, borderwidth=2)
passw_input.grid(row = 3, column = 1, padx = 10)



# BUTTONS
passw_btn = Button(text = "Generate password", bg = "red", fg = "yellow", command=pass_gen, font = (FONT_NAME, 15, 'bold'))
passw_btn.grid(row = 3, column = 2, padx = 10, pady = 10)

add_btn = Button(text = "Add", width=38, bg = "red", fg = "yellow", highlightthickness=2, command=click_add_btn, font = (FONT_NAME, 15, 'bold'))
add_btn.grid(row=4, column = 1, columnspan=2, padx = 10, pady = 10)

search_btn = Button(text = "Search", bg = "red", fg = "yellow", font = (FONT_NAME, 15, 'bold'), width=16, command=find_password)
search_btn.grid(row = 1, column = 2, padx = 10, pady = 10)
window.mainloop()