from tkinter import *
from tkinter import messagebox, ttk

class MainWindow:
    def __init__(self, db_handler, user_id):
        self.db_handler = db_handler
        self.lock_img = None
        self.website_entry = None
        self.website_dropdown = None
        self.email_user_entry = None
        self.password_entry = None

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
            messagebox.showinfo(title=f'Login Information for: {selected_website}', message=f'Username: {email}\nPassword: {password}')

    def create_main_window(self):
        window = Tk()
        window.title("Password Manager")
        window.config(padx=50, pady=50, bg='white')

        canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
        self.lock_img = PhotoImage(file='logo.png')
        canvas.create_image(100, 100, image=self.lock_img)
        canvas.grid(row=0, column=1)

        website_dropdown_label = Label(text='Select Website:', bg='white', fg='black', highlightthickness=0)
        self.website_dropdown = ttk.Combobox(width=18, state="readonly", postcommand=self.update_dropdown)
        website_dropdown_label.grid(row=1, column=0)
        self.website_dropdown.grid(row=1, column=1, columnspan=2)
        self.website_dropdown.bind("<<ComboboxSelected>>", self.display_selected_website)
        # setting dropdown styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="orange", background="white")
        # creating website label and entry field
        website_label = Label(text='Website:', bg='white', fg='black', highlightthickness=0)
        self.website_entry = Entry(width=21, bg='white', highlightthickness=0, fg='black', insertbackground='black')
        website_button = Button(text='Search', width=10, fg='black', highlightthickness=0,
                                highlightbackground='white',
                                font=('Helvatical bold', 14), command=lambda: find_password_db(user_id))
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
        generate_password_button = Button(text="Generate password", width=13, command=generate_password, fg='black',
                                          highlightbackground='white', font=('Helvatical bold', 10))
        password_label.grid(row=4, column=0)
        self.password_entry.grid(row=4, column=1)
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

    def update_dropdown(self):
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