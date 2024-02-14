from tkinter import Tk, Label, Entry, Button, messagebox
from CustomGUIFunctions import CommonFunctions
from MainWindow import MainWindow

class LoginWindow(CommonFunctions):
    def __init__(self, db_handler, window):
        super().__init__()
        self.window = window
        self.db_handler = db_handler
        self.user_id = None
        self.login_window = None
        self.username_entry = None
        self.password_entry = None
        self.window.title("Login")
        self.window.config(padx=10, pady=10)

        # Prevent window from resizing based on its contents
        self.window.grid_columnconfigure(0, weight=1)  # Make the column expandable
        self.window.grid_rowconfigure(3, weight=1)  # Make the last row expandable

        Label(self.window, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = Entry(self.window)
        self.username_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        Label(self.window, text="Password:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = Entry(self.window, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        Button(self.window, text="Login", command=self.on_login).grid(row=2, column=0, columnspan=2, sticky="ew",
                                                                      padx=5, pady=10)
        Button(self.window, text="Create User", command=self.db_handler.create_first_user).grid(row=3, column=0,
                                                                                                columnspan=2,
                                                                                                sticky="ew", padx=5,
                                                                                                pady=10)

        # Calculate and set the window size based on widget sizes
        self.window.update_idletasks()  # Update the window to calculate widget sizes
        window_width = self.window.winfo_reqwidth()
        window_height = self.window.winfo_reqheight()
        self.window.geometry(f"{window_width}x{window_height}")
        self.center_window(self.window, width=window_width, height=window_height)
    # Validate User Login
    def on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.user_id = self.db_handler.get_user_id(username, password)

        if self.user_id is not None:
            messagebox.showinfo("✅Login Successful✅", f"Welcome, {username}, Your User ID:{self.user_id}!")
            self.open_main_window()
            return True
        else:
            messagebox.showinfo("🛑Login Failed🛑", "Invalid username or password")
            return False

    def open_main_window(self):
        # close login / minimize
        self.hide_login_widgets()
        print("Line 62 login window missing but no mainwindow correct?")
        # Create an instance of MainWindow passing the LoginWindow instance
        MainWindow(self.db_handler, window=self.window, user_id=self.user_id)

    def hide_login_widgets(self):
        # Hide all login widgets
        for widget in self.window.winfo_children():
            print(widget)
            widget.destroy()