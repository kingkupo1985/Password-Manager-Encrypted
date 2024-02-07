import json
from tkinter import *
from tkinter import messagebox, ttk
from random import shuffle, randint, choice
from EncryptionManager import EncryptionManager
from CustomGUIFunctions import CommonFunctions

class MainWindow(CommonFunctions):
    def __init__(self, db_handler, user_id):
        super().__init__()
        self.db_handler = db_handler
        self.lock_img = None
        self.website_entry = None
        self.website_dropdown = None
        self.email_user_entry = None
        self.password_entry = None
        self.add_to_data_button = None
        self.load_button = None
        self.generate_password_button = None
        self.user_id = user_id

    def display_selected_website(self, *args):
        selected_website = self.website_dropdown.get()
        try:
            data = self.db_handler.get_decrypted_dictionary()
        except Exception as error:
            data = {}
            # Handle the error appropriately (e.g., show a messagebox)

        if selected_website:
            email = data.get(selected_website, {}).get('username', 'N/A')
            password = data.get(selected_website, {}).get('password', 'N/A')
            self.custom_showinfo(title=f'Login Information for: {selected_website}', message=f'Username: {email}\nPassword: {password}')

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

        # Encrypt the generated password before displaying
        encrypted_password = EncryptionManager.encrypt(password)

        # Display the encrypted password in the password_entry widget
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, string=encrypted_password)

        # Copy the decrypted password to the clipboard (optional)
        pyperclip.copy(password)

        print(f"Your password is: {password}")

    def find_password(self):
        website = self.website_entry.get()
        key = EncryptionManager.load_key()
        try:
            with open('save_passwords.json.enc', mode='rb') as save_file:
                # Decrypt the file
                encrypted_data = save_file.read()
                decrypted_data = EncryptionManager.decrypt(encrypted_data, key)
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
                self.custom_showinfo(title=f'Login Information for: {website}',
                                    message=f'Username:{email}\n Password:{password}')
            else:
                self.custom_showinfo(title=f'Website Not Found',
                                    message=f'Sorry, No Entry Found')

    def create_main_window(self):
        window = Tk()
        window.title("Password Manager")
        window.config(padx=50, pady=50, bg='white')
        #add image
        canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
        self.lock_img = PhotoImage(file='logo.png')
        canvas.create_image(100, 100, image=self.lock_img)
        canvas.grid(row=0, column=1)
        # Drop down with list of sites saves
        website_dropdown_label = Label(text='Select Website:', bg='white', fg='black', highlightthickness=0)
        self.website_dropdown = ttk.Combobox(width=18, state="readonly", postcommand=self.update_dropdown)
        website_dropdown_label.grid(row=1, column=0)
        self.website_dropdown.grid(row=1, column=1, columnspan=2)
        self.website_dropdown.bind("<<ComboboxSelected>>", self.display_selected_website)
        # setting dropdown styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="orange", background="white")
        # creating website labels and entry fields
        website_label = Label(text='Website:', bg='white', fg='black', highlightthickness=0)
        self.website_entry = Entry(width=21, bg='white', highlightthickness=0, fg='black', insertbackground='black')
        website_button = Button(text='Search', width=10, fg='black', highlightthickness=0,
                                highlightbackground='white',
                                font=('Helvatical bold', 14),
                                command=lambda: self.db_handler.find_password_db(self.user_id, self.website_entry))
        website_label.grid(row=2, column=0)
        self.website_entry.grid(row=2, column=1)
        website_button.grid(row=2, column=2)
        # creating email label and entry field
        email_user_label = Label(text='Email/Username', bg='white', fg='black')
        self.email_user_entry = Entry(width=35, bg='white', fg='black', highlightthickness=0, insertbackground='black')
        email_user_label.grid(row=3, column=0)
        self.email_user_entry.grid(row=3, column=1, columnspan=2)
        # creating password label, entry field, and button
        password_label = Label(text='Password', bg='white', fg='black')
        self.password_entry = Entry(width=21, bg='white', fg='black', highlightthickness=0, insertbackground='black')
        self.generate_password_button = Button(text="Generate password", width=13, command=self.generate_password, fg='black',
                                          highlightbackground='white', font=('Helvatical bold', 10))
        password_label.grid(row=4, column=0)
        self.password_entry.grid(row=4, column=1)
        self.generate_password_button.grid(row=4, column=2)
        # creating add button to save the password
        self.add_to_data_button = Button(text="Add", foreground='black', width=42,
                                    command=lambda: self.db_handler.save_to_db(self.user_id, self.website_entry,
                                                                               self.email_user_entry,
                                                                               self.password_entry),
                                    highlightbackground='white',
                                    font=('Helvatical bold', 10,))
        self.add_to_data_button.grid(row=5, column=1, columnspan=2)
        # creating load button to load a JSON file
        self.load_button = Button(text="Load JSON", foreground='black', width=42, command=lambda: self.db_handler.load_json_db(self.user_id,
                                                                                                                               self.website_entry),
                             highlightbackground='white',
                             font=('Helvetica bold', 10))
        self.load_button.grid(row=6, column=1, columnspan=2)
        window.mainloop()

    def update_dropdown(self):
        self.db_handler.update_dropdown(self.user_id)
        try:
            existing_data = self.db_handler.get_encrypted_dictionary()

            if existing_data:
                decrypted_data = self.db_handler.decrypt(existing_data)
                data = json.loads(decrypted_data)
            else:
                data = {}
        except (FileNotFoundError, json.JSONDecodeError) as error:
            messagebox.showinfo(title='Warning', message=f"Sorry Some Error Happened: {error}")
            data = {}

        website_list = list(data.keys())
        self.website_dropdown['values'] = website_list