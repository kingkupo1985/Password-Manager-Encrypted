import json
from tkinter import *
from tkinter import messagebox, ttk
from random import shuffle, randint, choice
from os.path import join
from PIL import Image, ImageTk
from EncryptionManager import EncryptionManager
from CustomGUIFunctions import CommonFunctions
from DatabaseDataHandler import DatabaseDataHandler
from CustomButton import CustomButton
from button_images import label_images


class MainWindow(CommonFunctions):
    def __init__(self, db_handler, window, user_id):
        super().__init__()
        self.db_handler = db_handler
        self.window = window
        # Prevent user Resizing Window
        self.window.resizable(0, 0)
        self.lock_img = None
        self.website_entry = None
        self.website_dropdown = None
        self.email_user_entry = None
        self.password_entry = None
        self.add_to_data_button = None
        self.load_button = None
        self.generate_password_button = None
        self.user_id = user_id
        self.encryption_manager = EncryptionManager()
        self.data_handler = DatabaseDataHandler(self.db_handler, self.user_id, self.website_dropdown)
        self.window.title("Password Manager")
        self.window.config(padx=20, pady=20, bg='white')
        # Allow window resizing based on its contents
        self.window.grid_columnconfigure(0, weight=1)  # Make the column expandable
        self.window.grid_rowconfigure(6, weight=1)  # Make the last row expandable
        style = ttk.Style()
        # add image
        canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0, relief="flat")
        self.lock_img = PhotoImage(file='images/logo/logo.png')
        canvas.create_image(100, 100, image=self.lock_img)
        canvas.grid(row=0, column=0, columnspan=3, pady=5)

        # Drop down with list of sites saves
        self.display_label(labelname="select one", row=1, col=0)
        self.website_dropdown = ttk.Combobox(width=19,
                                             state="readonly",
                                             postcommand=self.update_dropdown,
                                             background="#3e3232",
                                             foreground="#3E3232",
                                             font=("Poppins", 24, "bold")
                                             )
        self.website_dropdown.grid(row=1, column=1, columnspan=2, padx=(5, 0))
        self.website_dropdown.bind("<<ComboboxSelected>>", self.display_selected_website)
        # setting dropdown styling
        style.theme_use("clam")
        style.configure(style="TCombobox",
                        fieldbackground=[("readonly","#3E3232"),("active", "#3E3232")],
                        background="#3E3232",
                        font=("Poppins", 24, "bold"),
                        bd=0
                        )
        # creating website labels and entry fields
        self.website_entry = Entry(width=20,
                                   background="#A87C7C",
                                   font=("Poppins", 24, "bold"),
                                   foreground="#503C3C",
                                   insertbackground="#503C3C",  # set color of the cursor in entry field
                                   highlightbackground='#A87C7C',  # entry field color when not inm focus
                                   highlightcolor='#503C3C',  # entry field when in focus
                                   highlightthickness=5)
        website_button = CustomButton(self.window,
                                      width=122,
                                      height=40,
                                      button_name="Search",
                                      command=lambda: self.data_handler.find_password_db(user_id=self.user_id,
                                                                                         website_entry=self.website_entry,))
        self.display_label(labelname="website", row=2, col=0)
        self.website_entry.grid(row=2, column=1, padx=(5,0), columnspan=2)
        website_button.grid(row=5, column=2)

        # creating email label and entry field
        self.email_user_entry = Entry(width=20,
                                      background="#A87C7C",
                                      font=("Poppins", 24, "bold"),
                                      foreground="#503C3C",
                                      insertbackground="#503C3C",  # set color of the cursor in entry field
                                      highlightbackground='#A87C7C',  # entry field color when not inm focus
                                      highlightcolor='#503C3C',  # entry field when in focus
                                      highlightthickness=5
                                      )
        self.display_label(labelname="email", row=3, col=0)
        self.email_user_entry.grid(row=3, column=1, pady=5, padx=(5,0), columnspan=2)
        # creating password label, entry field, and button
        self.password_entry = Entry(width=20,
                                    background="#A87C7C",
                                    font=("Poppins", 24, "bold"),
                                    foreground="#503C3C",
                                    insertbackground="#503C3C",  # set color of the cursor in entry field
                                    highlightbackground='#A87C7C',  # entry field color when not inm focus
                                    highlightcolor='#503C3C',  # entry field when in focus
                                    highlightthickness=5
                                    )
        self.generate_password_button = CustomButton(self.window,
                                                     width=122,
                                                     height=40,
                                                     button_name="Generate Password",
                                                     command=self.generate_password)
        self.display_label(labelname="password", row=4, col=0)
        self.password_entry.grid(row=4, column=1, padx=(5,0), columnspan=2)
        self.generate_password_button.grid(row=5, column=1, padx=(25,0), pady=5)
        # creating add button to save the password
        self.add_to_data_button = CustomButton(self.window,
                                               width=122, height=40,
                                               button_name="Add",
                                               command=lambda: self.pre_save_to_db(user_id=self.user_id,
                                                                                   website_entry=self.website_entry,
                                                                                   email_user_entry=self.email_user_entry,
                                                                                   password_entry=self.password_entry),
                                               )
        self.add_to_data_button.grid(row=5, column=0)
        # creating load button to load a JSON file
        self.load_button = CustomButton(self.window,
                                        width=122,
                                        height=40,
                                        button_name="Load JSON",
                                        command=lambda: self.data_handler.load_json_concurrently_wrapper(self.user_id))
        self.load_button.grid(row=6, column=0)
        self.clear_button = CustomButton(self.window,
                                         width=122,
                                         height=40,
                                         button_name="Clear",
                                         command=self.clear_entry)
        self.clear_button.grid(row=6, column=1, padx=(25,0), pady=5)
        self.logout_button = CustomButton(self.window,
                                          width=122,
                                          height=40,
                                          button_name="Logout",
                                          command=self.logout)
        self.logout_button.grid(row=6, column=2)
        self.window.update_idletasks()  # Update the window to calculate widget sizes
        window_width = self.window.winfo_reqwidth()
        window_height = self.window.winfo_reqheight()
        self.window.geometry(f"{window_width}x{window_height}")
        self.center_window(self.window, width=window_width, height=window_height)

    def generate_password(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
        password_list = [choice(letters) for _ in range(randint(8, 10))]
        password_list += [choice(symbols) for _ in range(randint(2, 4))]
        password_list += [choice(numbers) for _ in range(randint(2, 4))]
        shuffle(password_list)
        password = ''.join(password_list)

        # Display the password in the password_entry widget
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, string=password)

        #print(f"Your generated password is: {password}")

    def display_selected_website(self, *args):
        selected_website = self.website_dropdown.get()
        try:
            # Retrieve the decrypted dictionary data
            data = self.data_handler.get_decrypted_dictionary(user_id=self.user_id)
        except Exception as error:
            data = {}
            messagebox.showinfo(title='Warning', message=f'Something Happened: {error}')
        if selected_website:
            email = data.get(selected_website, {}).get('username', 'N/A')
            password = data.get(selected_website, {}).get('password', 'N/A')
            messagebox.showinfo(title=f'Login Information for: {selected_website}',
                                message=f'Website:{selected_website}\nUsername: {email}\nPassword: {password}')
            self.website_entry.delete(0, END)
            self.website_entry.insert(0, selected_website)
            self.email_user_entry.delete(0,END)
            self.email_user_entry.insert(0, email)
            self.password_entry.delete(0, END)
            self.password_entry.insert(0, password)

    def update_dropdown(self):
        try:
            existing_data = self.data_handler.get_encrypted_dictionary(self.user_id)

            if existing_data:
                decrypted_data = self.encryption_manager.decrypt(existing_data)
                data = json.loads(decrypted_data)
            else:
                data = {}
        except (FileNotFoundError, json.JSONDecodeError, TypeError) as error:
            messagebox.showinfo(title='Warning', message=f"Sorry Some Error Happened: {error}")
            data = {}

        website_list = list(data.keys())
        self.website_dropdown['values'] = website_list

    def pre_save_to_db(self, user_id, website_entry, email_user_entry, password_entry):

        # Call the function from the other class
        self.data_handler.save_to_db(user_id, website_entry, email_user_entry, password_entry)

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

    def clear_entry(self):
        self.website_entry.delete(0, END)
        self.email_user_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.website_dropdown.set("")

    def logout(self):
        from UserLogin import LoginWindow
        for widget in self.window.winfo_children():
            widget.destroy()
        self.user_id = None
        LoginWindow(self.db_handler, self.window)

