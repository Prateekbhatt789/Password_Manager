import math
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- Password Generator ------------------ #
smallcharlist = list(range(ord('a'), ord('z')+1))
capitallist = list(range(ord('A'), ord('Z')+1))
numberlist = list(range(ord('0'), ord('9')+1))
valid_symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '{', '}', '[', ']']
def generate_password():
    length = random.randint(8, 13)
    symbol = math.ceil(length/5)
    number = symbol+1
    cap_alphabet = random.randint(1, 4)
    small_alphabet = length - (symbol+number + cap_alphabet)
    pwd = ""

    for i in range(small_alphabet):
        pwd += chr(random.choice(smallcharlist))
    for i in range(cap_alphabet):
        pwd += chr(random.choice(capitallist))
    for i in range(number):
        pwd += chr(random.choice(numberlist))
    for i in range(symbol):
        pwd += random.choice(valid_symbols)

    pwd = list(pwd)
    random.shuffle(pwd)
    pwd = ''.join(pwd)
    password_entry.insert(0, pwd)
    pyperclip.copy(pwd)
# ---------------------------- Save Password ----------------------- #

def Save():
    new_website = website_entry.get()
    new_email = Email_entry.get()
    new_password = password_entry.get()
    new_data = {new_website: {
            'email': new_email,
            'password': new_password,
            }
    }
    if len(new_website) == 0 or len(new_password) == 0:
        messagebox.showinfo("❌Invalid Entry❌", "Please fill all the required fields")
    else:
        IsOk = messagebox.askokcancel(new_website, f"These are the details entered:\nwebsite: {new_website}\npassword: {new_password}\n Press 'OK' to save it")
        if IsOk:
            try:
                with open("pwd_data.json", 'r') as datafile:
                    # json.dump(new_data, dataFile, indent=4)   # write in json
                    # data = json.load(dataFile)   # reading from json
                    # 1. reading the json file
                    data = json.load(datafile)
            except FileNotFoundError:
                with open("pwd_data.json", 'w') as datafile:
                    json.dump(new_data, datafile, indent=4)
            else:
                # 2. updating the json file
                data.update(new_data)
                # 3. Update file with new data
                with open("pwd_data.json", 'w') as datafile:
                    json.dump(data, datafile, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
            # print(data)
# ---------------------------- Search Password ---------------------------- #
def find_pwd():
    website_name = website_entry.get()
    if website_name == "":
        messagebox.showinfo("Error", "Please enter the website name to be Searched.")
    else:
        try:
            with open("pwd_data.json") as dataFile:
                data = json.load(dataFile)
        except FileNotFoundError:
            messagebox.showinfo("Error", "No Data File Found.")
        else:
            if website_name in data:
                data_website = data[website_name]
                web_email = data_website['email']
                website_pwd = data_website['password']
                messagebox.showinfo(f"{website_name}", f"Email: {web_email}\nPassword: {website_pwd}")
            else:
                messagebox.showinfo(title="Record Not Found", message=f"No details of \"{website_name}\" website exist.")

# ---------------------------- UI Setup ---------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, highlightthickness=0)
canvas = Canvas(width=200, height=200, highlightthickness=0)
image_Lock = PhotoImage(file="Lock.png")
canvas.create_image(100, 100, image=image_Lock)
canvas.grid(row=0, column=1)

# Website label
website = Label(text="Website :")
website.grid(row=1, column=0)

# Website Entry
website_entry = Entry(width=27)
website_entry.grid(row=1, column=1)
website_entry.focus()

# Search Button
search = Button(text='Search', width=13, highlightthickness=0, command=find_pwd)
search.grid(row=1, column=2)

# Email label
email = Label(text="Email/Username :")
email.grid(row=2, column=0)

# Email Entry
Email_entry = Entry(width=45)
Email_entry.insert(0, string="prateekbhatt789@gmail.com")
Email_entry.grid(row=2, column=1, columnspan=2)


# Password label
password = Label(text="Password :")
password.grid(row=3, column=0)

# Password Entry
password_entry = Entry(width=27)
password_entry.grid(row=3, column=1)

# Generate button
generate = Button(text="Generate Password", command=generate_password)
generate.grid(row=3, column=2)

# add button
add = Button(text="Add", width=36, command=Save)
add.grid(row=4, column=1, columnspan=2)
window.mainloop()