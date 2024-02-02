from tkinter import *
from tkinter import ttk
from tkinter import Toplevel, Label, Button, Tk
import sqlite3

user_id = None

# TODO Convert in to OOP app
# TODO Convert into web/cloud app
# TODO Fix Functions, (Only Load JSON, Login, and Create Database functions work,
#  all other functions need to be converted from JSON to SQL DB

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
window.mainloop()