from tkinter import Label, Entry, messagebox
from PIL import Image, ImageTk
from os.path import join
from CustomGUIFunctions import CommonFunctions
from CustomButton import CustomButton
from MainWindow import MainWindow
from button_images import label_images

class LoginWindow(CommonFunctions):
    def __init__(self, db_handler, window):
        super().__init__()
        self.window = window
        self.window.resizable(0, 0)
        self.db_handler = db_handler
        self.user_id = None
        self.login_window = None
        self.username_entry = None
        self.password_entry = None
        self.window.title("Login")
        self.window.config(padx=10, pady=10)
        self.window.config(background="#A87C7C")

        # Prevent window from resizing based on its contents
        self.window.grid_columnconfigure(0, weight=1)  # Make the column expandable
        self.window.grid_rowconfigure(3, weight=1)  # Make the last row expandable

        # Display Username label graphics for username label
        self.display_label(labelname="username", row=0, col=0)

        # Display username entry graphics (coming soon)
        self.username_entry = Entry(self.window)
        self.username_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Display Password label graphics for username label
        self.display_label(labelname="password", row=1, col=0)
        # Display username entry graphics (coming soon)
        self.password_entry = Entry(self.window, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)


        CustomButton(self.window,
                     width=122,
                     height=40,
                     button_name="Login",
                     command=self.on_login).grid(row=2,
                                                 column=0,
                                                 padx=(50,0),
                                                 pady=10
                                                 )
        CustomButton(self.window,
                     width=122, height=40,
                     button_name="Create User",
                     command=self.db_handler.create_first_user).grid(row=2,
                                                                     column=1,
                                                                     padx=0,
                                                                     pady=10
                                                                     )
        CustomButton(self.window,
                     width=122,
                     height=40,
                     button_name="Import User",
                     command=self.on_login).grid(row=3,
                                                 column=0,
                                                 padx=(50, 0),
                                                 pady=10
                                                 )
        CustomButton(self.window,
                     width=122, height=40,
                     button_name="Export User",
                     command=self.db_handler.create_first_user).grid(row=3,
                                                                     column=1,
                                                                     padx=0,
                                                                     pady=10
                                                                     )

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
        # Create an instance of MainWindow passing the LoginWindow instance
        MainWindow(self.db_handler, window=self.window, user_id=self.user_id)

    def hide_login_widgets(self):
        # Hide all login widgets
        for widget in self.window.winfo_children():
            widget.destroy()

    def load_image(self, label):
        path = join("images/labels", label)
        image = Image.open(path).convert("RGBA")
        return ImageTk.PhotoImage(image)

    def display_label(self, labelname, row, col):
        image = label_images.get(labelname)
        label_img = self.load_image(image)
        label = Label(self.window, image=label_img, bd=0, highlightthickness=0)
        label.image = label_img
        Label(self.window, image=label_img, bd=0, highlightthickness=0).grid(row=row, column=col)
