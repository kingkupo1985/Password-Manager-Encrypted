from tkinter import *
from tkinter import messagebox, ttk, filedialog
from tkinter import Toplevel, Label, Button, Tk
from tkinter.simpledialog import askstring
from random import shuffle, randint, choice
import pyperclip
from cryptography.fernet import Fernet
import json
import keyring
import sqlite3
import bcrypt

user_id = None

# TODO Convert in to OOP app
# TODO Convert into web/cloud app
# TODO Fix Functions, (Only Load JSON, Login, and Create Database functions work,
#  all other functions need to be converted from JSON to SQL DB
# ---------------------------- CREATE DATABASE TABLES ------------------------------- #
def create_database_tables():
    with sqlite3.connect('password_manager.db') as conn:
        cursor = conn.cursor()
        # Create the user table if not exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        ''')
        # Create the password table if not exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            encrypt_dictionary TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        print("Database Created Successfully!")
# ---------------------------- CHECK IF DATABASE EXIST ------------------------------- #
def check_and_create_databases():
    db_file_path = 'password_manager.db'
    try:
        with sqlite3.connect(db_file_path) as conn:
            # Attempt to execute a simple query to check if the tables exist
            conn.execute("SELECT 1 FROM users LIMIT 1")
            # If the query succeeds, the tables exist, and the database is not empty
            login_prompt()
    except sqlite3.OperationalError as e:
        # Handle the case where the tables or database do not exist
        create_database_tables()
        # Let user know this isthe first time running the app and create a user
        custom_showinfo(title='⚠️ Notice ⚠️', message='First Time\nRunning Password Manager.\nPlease Create a User')
        # Prompt the user to create the first user
        create_first_user()
    except Exception as e:
        # Handle other exceptions that might occur
        custom_showinfo(title='🛑 Error 🛑', message=f'An error occurred: {e}')

# ---------------------------- START DATABASE USER FUNCTIONS ------------------------------- #
def create_first_user():
    global user_id

    while True:
        # Get username using a dialog box
        username = askstring("Username", "Create a new username:")

        # Check if user canceled the input
        if username is None:
            continue  # Continue to the next iteration of the loop

        # Get password using a dialog box
        password = askstring("Password", "Enter the new user's password:")

        # Check if user canceled the input
        if password is None:
            continue  # Continue to the next iteration of the loop

        # Make sure the password was typed 2x correctly
        password_check = askstring("Password", "Enter the new user's password again:")

        if password == password_check:
            hashed_password = hash_password(password)
            with sqlite3.connect('password_manager.db') as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
                    conn.commit()
                    custom_showinfo(title='✅ Success ✅', message='User registered successfully!')
                    user_id = cursor.lastrowid
                    login_prompt()
                    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
                    result = cursor.fetchone()
                    if result:
                        # Extract the user_id and hashed password from the result
                        user_id, hashed_password = result
                        # Verify the password using bcrypt
                        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                            # Password is correct, return the user_id
                            return user_id
                except sqlite3.IntegrityError:
                    custom_showinfo(title='⚠️ Notice ⚠️', message='Username already exists!')
        else:
            custom_showinfo(title='⚠️ Notice ⚠️', message='Passwords did not match. Please try again.')
# Verify user exists in database ad return user ID
def get_user_id(username, password):
    with sqlite3.connect('password_manager.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            # Extract the user_id and hashed password from the result
            user_id, hashed_password = result
            # Verify the password using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Password is correct, return the user_id
                return user_id
    # If the username or password is incorrect, return None
    return None
# Save and Hash Password for users
def hash_password(password):
    # Hash the password using bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

# ---------------------------- END DATABASE USER FUNCTIONS ------------------------------- #

# ---------------------------- START DATABASE DATA FUNCTIONS ------------------------------- #
def get_encrypted_dictionary(user_id):
    with sqlite3.connect('password_manager.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT encrypt_dictionary FROM passwords WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
    return result[0] if result else None
#Save data to database has GUI controls
def save_to_db(user_id):
    website = website_entry.get().lower()
    username = email_user_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        custom_showinfo(title='⚠️ Notice ⚠️', message='Please do not leave any fields blank!')
    else:
        ok_to_save = messagebox.askokcancel(title=website, message=f"These are the details you'd like to save"
                                                                   f"\nUsername: {username}\nPassword: {password}")
        if ok_to_save:
            key = load_key()
            try:
                #connect to database
                # Connect to the database
                with sqlite3.connect('password_manager.db') as conn:
                    cursor = conn.cursor()

                    # Fetch the existing encrypted dictionary
                    existing_data = get_encrypted_dictionary(user_id)

                    if existing_data:
                        # Decrypt the existing data
                        existing_data_decrypted = decrypt(existing_data, key)
                        try:
                            existing_data_decrypted = decrypt(existing_data, key)
                        except Exception as decryption_error:
                            custom_showinfo(title='🛑 Warning 🛑', message=f"Decryption error: {decryption_error}")
                            return

                        # Update the existing data with new data
                        existing_data_dict = json.loads(existing_data_decrypted)
                        new_data = {
                            website: {
                                'username': username,
                                'password': password
                            }
                        }
                        existing_data_dict.update(new_data)

                        # Encrypt the updated data
                        updated_data_encrypted = encrypt(json.dumps(existing_data_dict), key)
                        updated_data_encrypted = encrypt(json.dumps(existing_data_dict).encode('utf-8'), key)

                        # Update the row in the database with the updated encrypted dictionary
                        cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                                       (updated_data_encrypted, user_id))
                        conn.commit()
                        custom_showinfo(title='✅ Success! ✅', message='Your New Entry Was Saved!')
                        website_entry.delete(0, 'end')
                        email_user_entry.delete(0, 'end')
                        password_entry.delete(0, 'end')
                    else:
                        # If no existing data, create a new entry
                        new_data = {
                            website: {
                                'username': username,
                                'password': password
                            }
                        }
                        new_data_encrypted = encrypt(json.dumps(new_data).encode('utf-8'), key)

                        # Insert a new row with the encrypted dictionary
                        cursor.execute("INSERT INTO passwords (user_id, encrypt_dictionary) VALUES (?, ?)",
                                       (user_id, new_data_encrypted))
                        conn.commit()
                        custom_showinfo(title='✅ Success! ✅', message='Your New Entry Was Saved!')
                        website_entry.delete(0, 'end')
                        email_user_entry.delete(0, 'end')
                        password_entry.delete(0, 'end')

            except sqlite3.Error as error:
                custom_showinfo(title='🛑 Warning🛑', message=f"Sorry Some Error Happened: {error}")

def find_password_db(user_id):
    # Let's find a website and its logins
    website = website_entry.get()
    # Get the key to decrypt data
    key = load_key()

    try:
        # Does the user exist and have anything stored?
        existing_data = get_encrypted_dictionary(user_id)

        if existing_data:
            decrypted_data = decrypt(existing_data, key)
            # Read old data and save to variable
            data = json.loads(decrypted_data)
        else:
            # If no data exists, set data to an empty dictionary
            data = {}
    except (FileNotFoundError, json.JSONDecodeError) as error:
        custom_showinfo(title='Warning', message=f"Sorry Some Error Happened: {error}")
        # Set data to an empty dictionary
        data = {}

    # Rest of the function remains the same
    if website in data:
        email = data[website]['username']
        password = data[website]['password']
        custom_showinfo(title=f'Login',
                            message=f'Website:{website}\nUsername: {email}\nPassword: {password}')
    else:
        custom_showinfo(title=f'⚠️ Website Not Found ⚠️', message=f'Sorry, No Entry Found')

# --- Drop Down Data Function Database --- #
def update_dropdown(user_id):
    try:
        key = load_key()
        try:
            # Does the user exist and have anything stored?
            existing_data = get_encrypted_dictionary(user_id)

            if existing_data:
                decrypted_data = decrypt(existing_data, key)
                # Read old data and save to variable
                data = json.loads(decrypted_data)
            else:
                data = {}
        except (FileNotFoundError, json.JSONDecodeError) as error:
            custom_showinfo(title='Warning', message=f"Sorry Some Error Happened: {error}")
            with open('save_passwords.json.enc', mode='w') as save_file:
                # create file if not existing
                data = {}
        finally:
            website_list = list(data.keys())
            website_dropdown['values'] = website_list
    except (FileNotFoundError, json.JSONDecodeError) as error:
        custom_showinfo(title='🛑 Warning 🛑', message=f"Sorry Some Error Happened: {error}")
        with open('save_passwords.json.enc', mode='w') as save_file:
            data = {}

    website_list = list(data.keys())
    website_dropdown['values'] = website_list


# --- Load Old JSON File to Database --- #
def load_json_db(user_id):
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if not file_path:
        return
    try:
        with open(file_path, mode='r') as json_file:
            new_data = json.load(json_file)
        # Convert new_data to bytes
        json_string = json.dumps(new_data)
        new_data_bytes = json_string.encode('utf-8')
    except (FileNotFoundError, json.JSONDecodeError):
        custom_showinfo(title='🛑 Error 🛑', message='Failed to load JSON file.')
        return
    key = load_key()
    try:
        with sqlite3.connect('password_manager.db') as conn:
            cursor = conn.cursor()
            encrypted_data = encrypt(new_data_bytes, key)  # Pass bytes to encrypt function
            cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                           (encrypted_data, user_id))
            conn.commit()
            # Check if a row with the given user_id already exists
            cursor.execute("SELECT * FROM passwords WHERE user_id = ?", (user_id,))
            existing_row = cursor.fetchone()

            if existing_row:
                # If row exists, update it
                encrypted_data = encrypt(new_data_bytes, key)  # Pass bytes to encrypt function
                cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                               (encrypted_data, user_id))
                conn.commit()
                custom_showinfo(title='✅ Success! ✅', message=f"Your File Was Loaded and Updated Successfully!")
            else:
                # If no row exists, create the first row
                encrypted_data = encrypt(new_data_bytes, key)  # Pass bytes to encrypt function
                cursor.execute("INSERT INTO passwords (user_id, encrypt_dictionary) VALUES (?, ?)",
                               (user_id, encrypted_data))
                conn.commit()
                custom_showinfo(title='✅ Success! ✅', message=f"Your File Was Loaded and Saved Successfully!")

    except sqlite3.Error as error:
        custom_showinfo(title='🛑 Error 🛑', message=f"Sorry Some Error Happened: {error}")
        # create file if not existing
        data = {}
        data.update(new_data)

    update_dropdown(user_id)

def get_decrypted_dictionary(user_id):
    key = load_key()
    try:
        with sqlite3.connect('password_manager.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT encrypt_dictionary FROM passwords WHERE user_id = ?", (user_id,))
            encrypted_data = cursor.fetchone()
            if encrypted_data:
                decrypted_data = decrypt(encrypted_data[0], key)
                return json.loads(decrypted_data)
            else:
                return {}
    except sqlite3.Error as error:
        # Handle the error appropriately (e.g., show a messagebox)
        return {}

# ---------------------------- END DATABASE DATA FUNCTIONS ------------------------------- #


# ---------------------------- START Data Encryption ------------------------------- #
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
    encrypted_data = f.encrypt(data)
    return encrypted_data
def decrypt(encrypted_data, key):
    # Decrypt your Data
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

# ---------------------------- END Data Encryption ------------------------------- #

# ---------------------------- START PASSWORD GENERATOR ------------------------------- #
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

# ---------------------------- END PASSWORD GENERATOR ------------------------------- #



# ---------------------------- START GUI ------------------------------- #

#drop down displayer GUI Class
def display_selected_website(*args): #GUI Class
    selected_website = website_dropdown.get()
    try:
        data = get_decrypted_dictionary(user_id)
    except sqlite3.Error as error:
        data = {}
        # Handle the error appropriately (e.g., show a messagebox)

    if selected_website:
        email = data.get(selected_website, {}).get('username', 'N/A')
        password = data.get(selected_website, {}).get('password', 'N/A')
        custom_showinfo(title=f'Login Information for: {selected_website}', message=f'Username: {email}\nPassword: {password}')

# ---------------------------- GUI Main Window Center Function ------------------------------- #
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x_position}+{y_position}")

#---GUI Login ---#
def login_prompt():
    global user_id
    def on_login():
        global user_id
        username = username_entry.get()
        password = password_entry.get()

        # Verify user credentials
        user_id = get_user_id(username, password)

        if user_id is not None:
            custom_showinfo(title="✅Login Successful✅", message=f"Welcome, {username}, Your User ID:{user_id}!")
            login_window.destroy()
            return True
        else:
            custom_showinfo(title="🛑Login Failed🛑", message="Invalid username or password")
            return False
    # Create login window
    login_window = Tk()
    login_window.title("Login")
    login_window_width = 250
    login_window_height = 250
    window.config(padx=10, pady=10)
    center_window(login_window, login_window_width, login_window_height)
    # Username label and entry
    Label(login_window, text="Username:").pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack(pady=5)
    # Password label and entry
    Label(login_window, text="Password:").pack(pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)
    # Login button
    login_button = Button(login_window, text="Login", command=on_login)
    login_button.pack(pady=10)
    # Create User
    login_button = Button(login_window, text="Create User", command=lambda: (login_window.destroy(), create_first_user()))
    login_button.pack(pady=10)
    # Run the login window
    login_window.mainloop()

# --- GUI Center TopLevel Window --- #
def custom_showinfo(title, message):
    top = Toplevel(window)
    top.title(title)

    top.lift()
    # Set the width and height of the toplevel window
    top_width = 300
    top_height = 100

    # Calculate the x and y coordinates to center the toplevel window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - top_width) // 2
    y_position = (screen_height - top_height) // 2

    top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

    # Create a frame to hold the label and button
    frame = Frame(top)
    frame.pack(expand=True)

    # Create and center the label
    label = Label(frame, text=message)
    label.pack(pady=(10, 0))  # Add padding only at the top

    # Create and center the button
    ok_button = Button(frame, text="OK", command=top.destroy)
    ok_button.pack(pady=(10, 0))  # Add padding only at the top

# --- GUI Main Window --- #

# Cerating UI window
window = Tk()
window.title("Password Manager")
window_width =450
window_height = 400
center_window(window, window_width, window_height)
window.config(padx=50, pady=50, bg='white')
# create logo  on screen
canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)
# creating website label and entry field
website_label = Label(text='Website:', bg='white', fg='black', highlightthickness=0)
website_entry = Entry(width=21, bg='white', highlightthickness=0, fg='black', insertbackground='black')
website_button = Button(text='Search', width=10, fg='black', highlightthickness=0,
                        highlightbackground='white',
                        font=('Helvatical bold', 14), command=lambda: find_password_db(user_id))
website_label.grid(row=2, column=0)
website_entry.grid(row=2, column=1)
website_button.grid(row=2, column=2)
# Add Drop down for website function:
website_dropdown_label = Label(text='Select Website:', bg='white', fg='black', highlightthickness=0)
website_dropdown = ttk.Combobox(width=18, state="readonly", postcommand=lambda: update_dropdown(user_id))
website_dropdown_label.grid(row=1, column=0)
website_dropdown.grid(row=1, column=1, columnspan=2)
website_dropdown.bind("<<ComboboxSelected>>", display_selected_website)
# setting dropdown styling
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="orange", background="white")
# creating email label and entry field
email_user_label = Label(text='Email/Username', bg='white', fg='black')
email_user_entry = Entry(width=35, bg='white', fg='black', highlightthickness=0, insertbackground='black')
email_user_label.grid(row=3, column=0)
email_user_entry.grid(row=3, column=1, columnspan=2)
# creating password label, entry field, and button
password_label = Label(text='Password', bg='white', fg='black')
password_entry = Entry(width=21, bg='white', fg='black', highlightthickness=0, insertbackground='black')
generate_password_button = Button(text="Generate password", width=13, command=generate_password, fg='black',
                                  highlightbackground='white', font=('Helvatical bold', 10))
password_label.grid(row=4, column=0)
password_entry.grid(row=4, column=1)
generate_password_button.grid(row=4, column=2)
# creating add button to save the password
add_to_data_button = Button(text="Add", foreground='black', width=42, command=lambda: save_to_db(user_id),
                            highlightbackground='white',
                            font=('Helvatical bold', 10,))
add_to_data_button.grid(row=5, column=1, columnspan=2)
# creating load button to load a JSON file
load_button = Button(text="Load JSON", foreground='black', width=42, command=lambda: load_json_db(user_id),
                     highlightbackground='white',
                     font=('Helvetica bold', 10))
load_button.grid(row=6, column=1, columnspan=2)
check_and_create_databases()