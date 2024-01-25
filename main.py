from tkinter import *
from tkinter import messagebox, ttk, filedialog
from random import shuffle, randint, choice
import pyperclip
from cryptography.fernet import Fernet
import json
import keyring

# TODO Create User database
# TODO Create Password Storage Database with relation to users for multiple users on one app
# TODO Add in biometric login & login popup + password login based on user login
# TODO Convert into mobile app
# TODO Convert into cloud app


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_list = []
    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)
    password = ''.join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, string=f"{password}")
    pyperclip.copy(f"{password}")
    print(f"Your password is: {password}")

# ---------------------------- SEARCH FOR PASSWORD ------------------------------- #


def find_password():
    website = website_entry.get()
    key = load_key()
    try:
        with open('save_passwords.json.enc', mode='rb') as save_file:
            # Decrypt the file
            encrypted_data = save_file.read()
            decrypted_data = decrypt(encrypted_data,key)
            # Read old data and save to variable
            data = json.loads(decrypted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        with open('save_passwords.json.enc', mode='w') as save_file:
            # create file if not existing
            data = {}
    else:
        if website in data:
            email = data[website]['username']
            password = data[website]['password']
            messagebox.showinfo(title=f'Login Information for: {website}', message=f'Username:{email}\n Password:{password}')
        else:
            messagebox.showinfo(title=f'Website Not Found',
                                message=f'Sorry, No Entry Found')

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get().lower()
    username = email_user_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title='Warning', message='Please do not leave any fields blank!')
    else:
        ok_to_save = messagebox.askokcancel(title=website, message=f"These are the details you'd like to save"
                                                                   f"\nUsername: {username}\nPassword: {password}")
        if ok_to_save:
            key = load_key()
            try:
                with open('save_passwords.json.enc', mode='rb') as save_file:
                    # Read old data and save to variable
                    encrypted_data = save_file.read()
                    decrypted_data = decrypt(encrypted_data, key)
                    data = json.loads(decrypted_data)
            except (FileNotFoundError, json.JSONDecodeError):
                with open('save_passwords.json.enc', mode='w') as save_file:
                    # create file if now existing
                    data = {}
            data.update({
                website: {
                    'username': username,
                    'password': password
                }
            })
            # Encrypt the File
            encrypted_data = encrypt(json.dumps(data), key)
            #Save the encrypted file
            with open('save_passwords.json.enc', mode='wb') as save_file:
                save_file.write(encrypted_data)
            # Clear Field Entries
            website_entry.delete(0, 'end')
            email_user_entry.delete(0, 'end')
            password_entry.delete(0, 'end')

# ---------------------------- Load Drop Down Website Options Encryption SETUP ------------------------------- #

def update_dropdown():
    try:
        key = load_key()
        with open('save_passwords.json.enc', mode='rb') as save_file:
            # Read old data and save to variable
            encrypted_data = save_file.read()
            decrypted_data = decrypt(encrypted_data, key)
            data = json.loads(decrypted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        with open('save_passwords.json.enc', mode='w') as save_file:
            # create file if now existing
            data = {}
    website_list = list(data.keys())
    website_dropdown['values'] = website_list

def display_selected_website(*args):
    selected_website = website_dropdown.get()
    try:
        key = load_key()
        with open('save_passwords.json.enc', mode='rb') as save_file:
            # Read old data and save to variable
            encrypted_data = save_file.read()
            decrypted_data = decrypt(encrypted_data, key)
            data = json.loads(decrypted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        with open('save_passwords.json.enc', mode='w') as save_file:
            # create file if now existing
            data = {}
    if selected_website:
        email = data[selected_website]['username']
        password = data[selected_website]['password']
        messagebox.showinfo(title=f'Login Information for: {selected_website}', message=f'Username: {email}\nPassword: {password}')

def load_json():
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])

    if not file_path:
        return

    try:
        with open(file_path, mode='r') as json_file:
            new_data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror(title='Error', message='Failed to load JSON file.')
        return

    key = load_key()
    try:
        with open('save_passwords.json.enc', mode='rb') as save_file:
            # Read old data and save to variable
            encrypted_data = save_file.read()
            decrypted_data = decrypt(encrypted_data, key)
            data = json.loads(decrypted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        with open('save_passwords.json.enc', mode='w') as save_file:
            # create file if not existing
            data = {}

    data.update(new_data)

    # Encrypt the File
    encrypted_data = encrypt(json.dumps(data), key)
    # Save the encrypted file
    with open('save_passwords.json.enc', mode='wb') as save_file:
        save_file.write(encrypted_data)

    # Update the dropdown
    update_dropdown()

# ---------------------------- JSON Encryption SETUP ------------------------------- #

def generate_key():
    # Generate a key
    key = Fernet.generate_key()
    keyring.set_password("password_manager", "user_key", key.decode())
    return key

def load_key():
    try:
        key = keyring.get_password("password_manager", "user_key")
        if key is None:
            key = generate_key()
    except Exception as e:
        print(f"Error loading key: {e}")
        key = generate_key()
    return key

def encrypt(data, key):
    # Encrypt your data
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt(encrypted_data, key):
    # Decrypt your Data
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data


# ---------------------------- UI SETUP ------------------------------- #
# Cerating UI window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg='white')
# create logo  on screen
canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)
# creating website label and entry field
website_label = Label(text='Website:', bg='white', fg='black', highlightthickness=0)
website_entry = Entry(width=21, bg='white', highlightthickness=0, fg='black', insertbackground='black')
website_button = Button(text='Search', width=10, fg='black', highlightthickness=0, highlightbackground='white',
                        font=('Helvatical bold', 14), command=find_password)
website_label.grid(row=2, column=0)
website_entry.grid(row=2, column=1)
website_button.grid(row=2, column=2)
# Add Drop down for website function:
website_dropdown_label = Label(text='Select Website:', bg='white', fg='black', highlightthickness=0)
website_dropdown = ttk.Combobox(width=18, state="readonly", postcommand=update_dropdown)
website_dropdown_label.grid(row=1, column=0)
website_dropdown.grid(row=1, column=1, columnspan=2)
website_dropdown.bind("<<ComboboxSelected>>", display_selected_website)
#setting dropdown styling
style= ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground= "orange", background= "white")
# creating email label and entry field
email_user_label = Label(text='Email/Username', bg='white', fg='black')
email_user_entry = Entry(width=35, bg='white', fg='black', highlightthickness=0, insertbackground='black')
email_user_label.grid(row=3, column=0)
email_user_entry.grid(row=3,column=1, columnspan=2)
# creating password label, entry field, and button
password_label = Label(text='Password', bg='white', fg='black')
password_entry = Entry(width=21, bg='white', fg='black', highlightthickness=0, insertbackground='black')
generate_password_button = Button(text="Generate password", width=13, command=generate_password, fg='black',
                                  highlightbackgroun='white', font=('Helvatical bold', 10))
password_label.grid(row=4, column=0)
password_entry.grid(row=4, column=1)
generate_password_button.grid(row=4, column=2)
# creating add button to save the password
add_to_data_button = Button(text="Add", foreground='black', width=42, command=save, highlightbackgroun='white',
                            font=('Helvatical bold', 10,))
add_to_data_button.grid(row=5, column=1, columnspan=2)
# creating load button to load a JSON file
load_button = Button(text="Load JSON", foreground='black', width=42, command=load_json, highlightbackground='white',
                     font=('Helvetica bold', 10))
load_button.grid(row=6, column=1, columnspan=2)
# keep window open until closed
window.mainloop()