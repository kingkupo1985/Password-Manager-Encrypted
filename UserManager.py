import json
import sqlite3
from tkinter.simpledialog import askstring
from tkinter import messagebox, filedialog
from DatabaseDataHandler import DatabaseDataHandler

class UserManager:
    def __init__(self, db_handler, window):
        self.db_handler = db_handler
        self.data_handler = DatabaseDataHandler(db_handler, None, None)
        self.window = window
        self.filepath = None

    def export_user(self, user_id, export_path):
        # Gather user data
        user_data = self._get_user_data(user_id)

        # Export user data to JSON file
        if user_data:
            try:
                with open(export_path, 'w') as file:
                    json.dump(user_data, file, indent=4)
                return True
            except Exception as e:
                print(f"Error exporting user data: {e}")
        return False

    def _get_user_data(self, user_id):
        # Retrieve user data from the database
        user_data = {
            "username": "",
            "password_hash": "",
            "encrypted_data": "",
            "keyring_key": ""
        }

        # Retrieve username and password hash
        with sqlite3.connect(self.db_handler.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, password_hash FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                user_data["username"] = result[0]
                user_data["password_hash"] = result[1]

        # Retrieve encrypted data and keyring key using DatabaseDataHandler
        encrypted_data = self.data_handler.get_encrypted_dictionary(user_id)
        if encrypted_data:
            user_data["encrypted_data"] = encrypted_data
            user_data["keyring_key"] = self.data_handler.encryption_manager.load_key()

        return user_data

    def get_username(self):
        username = askstring("Username Export", "Enter the username you want tio export: ")
        with sqlite3.connect(self.db_handler.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                user_id = result
                self.save_to_file_path()
                self.export_user(user_id, self.filepath)
            else:
                messagebox.showinfo("No User", "Sorry that user does not exist in the database")

    def save_to_file_path(self):
        self.filepath = filedialog.asksaveasfile(defaultextension=".enc", filetypes=[("ENC Files", "*.enc")])
        filedialog.as
