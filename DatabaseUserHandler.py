import sqlite3
import bcrypt
from tkinter import messagebox
from tkinter.simpledialog import askstring
from CustomGUIFunctions import CommonFunctions


class DatabaseHandler(CommonFunctions):
    def __init__(self, db_name='password_manager.db'):
        super().__init__()
        self.db_name = db_name
        self.user_id = None

    def create_database_tables(self):
        with sqlite3.connect(self.db_name) as conn:
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
    def check_and_create_databases(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                # Attempt to execute a simple query to check if the tables exist
                conn.execute("SELECT 1 FROM users LIMIT 1")
                # If the query succeeds, the tables exist, and the database is not empty
                #login_prompt()
        except sqlite3.OperationalError as e:
            # Handle the case where the tables or database do not exist
            self.create_database_tables()
            # Let user know this isthe first time running the app and create a user
            messagebox.showinfo(title='⚠️ Notice ⚠️', message='First Time\nRunning Password Manager.\nPlease Create a User')
            # Prompt the user to create the first user
            self.create_first_user()
        except Exception as e:
            # Handle other exceptions that might occur
            messagebox.showinfo(title='🛑 Error 🛑', message=f'An error occurred: {e}')

    # ---------------------------- START DATABASE USER FUNCTIONS ------------------------------- #
    def create_first_user(self):
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
                hashed_password = self.hash_password(password)
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                                       (username, hashed_password))
                        conn.commit()
                        messagebox.showinfo(title='✅ Success ✅', message='User registered successfully!')
                        self.user_id = cursor.lastrowid
                        #login_prompt()
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
                        messagebox.showinfo(title='⚠️ Notice ⚠️', message='Username already exists!')
            else:
                messagebox.showinfo(title='⚠️ Notice ⚠️', message='Passwords did not match. Please try again.')

    # Verify user exists in database ad return user ID
    def get_user_id(self, username, password):
        with sqlite3.connect(self.db_name) as conn:
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
    def hash_password(self, password):
        # Hash the password using bcrypt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')