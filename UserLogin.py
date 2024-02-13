from tkinter import Tk, Label, Entry, Button
from CustomGUIFunctions import CommonFunctions

class LoginWindow(CommonFunctions):
    def __init__(self, db_handler):
        super().__init__()
        self.db_handler = db_handler
        self.user_id = None
        self.login_window = None
        self.username_entry = None
        self.password_entry = None

    # Validate User Login
    def on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.user_id = self.db_handler.get_user_id(username, password)

        if self.user_id is not None:
            self.custom_showinfo("✅Login Successful✅", f"Welcome, {username}, Your User ID:{self.user_id}!")
            self.login_window.destroy()
            return True
        else:
            self.custom_showinfo("🛑Login Failed🛑", "Invalid username or password")
            return False

    # Create the Login Window Pop
    def create_login_window(self):
        self.login_window = Tk()
        self.login_window.title("Login")
        self.center_window(self.login_window, 250, 250)
        self.login_window.config(padx=10, pady=10)

        Label(self.login_window, text="Username:").pack(pady=5)
        self.username_entry = Entry(self.login_window)
        self.username_entry.pack(pady=5)

        Label(self.login_window, text="Password:").pack(pady=5)
        self.password_entry = Entry(self.login_window, show="*")
        self.password_entry.pack(pady=5)

        Button(self.login_window, text="Login", command=self.on_login).pack(pady=10)
        Button(self.login_window, text="Create User", command=self.db_handler.create_first_user).pack(pady=10)

        self.login_window.mainloop()