from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    entry_password.delete(0, END)
    entry_password.insert(0, "".join(password))
    pyperclip.copy(password)

def search():
    website = entry_website.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title=website, message=f"No details for {website} exists.")
    


def save():
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(message="Please don't leave any fields empty!")
        return
    is_ok = messagebox.askokcancel(title=website, message=f"These are the details enterd:\nWebsite: {website}\nEmail: {email}\nPassword: {password}\nIs it okay to save?")
    if is_ok:
        new_data = {
                    website:{
                        "email": email,
                        "password":password 
                    }
                }
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            with open('data.json', 'w') as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_password.delete(0, END)

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
password_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_image)
canvas.grid(row=0,column=1)

label_website = Label(text="Website: ")
label_website.grid(row=1, column=0)

label_email = Label(text="Email/Username: ")
label_email.grid(row=2, column=0)

label_password = Label(text="Password: ")
label_password.grid(row=3, column=0)

entry_website = Entry(width=21)
entry_website.grid(row=1, column=1, sticky="w")
entry_website.focus()

entry_email = Entry(width=38)
entry_email.insert(0, 'test@gmail.com')
entry_email.grid(row=2, column=1, columnspan=2, sticky="w")

entry_password = Entry(width=21)
entry_password.grid(row=3, column=1, sticky="w")

button_password = Button(text="Generate Password", command=generate_password)
button_password.grid(row=3, column=2)

button_add = Button(text="Add", width=36, command=save)
button_add.grid(row=4, column=1, columnspan=2)

button_search = Button(text="Search", width=12, command=search)
button_search.grid(row=1, column=2)
window.mainloop()