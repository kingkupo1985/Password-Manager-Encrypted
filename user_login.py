from tkinter import *
from tkinter.simpledialog import askstring
from tkinter import messagebox
from database_handler import DatabaseHandler
from MainWindow import MainWindow

class UserLogin:
    def __init__(self, db_handler, user_id):
        self.db_handler = db_handler
        self.user_id = user_id

    def on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.user_id = self.db_handler.get_user_id(username, password)
            if self.user_id is not None:
                messagebox.showinfo("Login Successful", f"Welcome, {username}, Your User ID: {self.user_id}!")
                self.login_window.destroy()
                self.create_main_window()  # Create the main window after successful login
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def create_user(self):
        username = askstring("Username", "Create a new username:")
        password = askstring("Password", "Enter the new user's password:")
        password_check = askstring("Password", "Enter the new user's password again:")

        if password == password_check:
            try:
                created_user_id = self.db_handler.create_user(username, password)
                if created_user_id is not None:
                    messagebox.showinfo(title='Success', message='User registered successfully!')
                    self.user_id = created_user_id
                    self.login_window.destroy()
                    self.create_main_window()  # Create the main window after successful user creation
                else:
                    messagebox.showerror(title='Error', message='Username already exists!')
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showinfo(title='Warning', message='Passwords did not match, user not created')

    def create_main_window(self):
        main_window = MainWindow(self.db_handler, self.user_id)
        main_window.create_main_window()

    def run_login_window(self):
        self.login_window = Tk()
        self.login_window.title("Login")

        Label(self.login_window, text="Username:").pack(pady=5)
        self.username_entry = Entry(self.login_window)
        self.username_entry.pack(pady=5)

        Label(self.login_window, text="Password:").pack(pady=5)
        self.password_entry = Entry(self.login_window, show="*")
        self.password_entry.pack(pady=5)

        login_button = Button(self.login_window, text="Login", command=self.on_login)
        login_button.pack(pady=10)

        create_user_button = Button(self.login_window, text="Create User", command=self.create_user)
        create_user_button.pack(pady=10)

        self.login_window.mainloop()

# Example usage:
# db_handler = DatabaseHandler()
# user_login = UserLogin(db_handler)
# user_login.run_login_window()