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

        # Rest of the code for creating the main window...
        # (You can copy the relevant parts from your original create_main_window function)

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