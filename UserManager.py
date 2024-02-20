import json
import sqlite3
import base64
from cryptography.fernet import Fernet
from tkinter.simpledialog import askstring
from tkinter import messagebox, filedialog
from DatabaseDataHandler import DatabaseDataHandler
from EncryptionManager import EncryptionManager

class UserManager:
    def __init__(self, db_handler, window):
        self.db_handler = db_handler
        self.data_handler = DatabaseDataHandler(db_handler, None, None)
        self.encryption_manager= EncryptionManager()
        self.window = window
        self.filepath = None

    def export_user(self, user_id, export_path):
        # Gather user data
        user_data = self.get_user_data(user_id)
        export_key = self.encryption_manager.load_key()
        print(f"Line 20| Export Path: {export_path} :: user data type: {type(user_data)} :: user_data: {user_data} :: Export Key: {export_key}")
        # askstring("Export_Key", "PLEASE NOTICE: Create a Export Key You must remember this export key!\n If you lose your export key your data can not be recovered!\nyEnter your export/import key"))
        # Export user data to JSON file
        if user_data:
            print(f"Print line 24 User Data: {user_data} :: Export Key {export_key}")
            # Encode the bytes object to base64
            encoded_data = base64.b64encode(user_data['encrypted_data']).decode('utf-8')
            # Update the dictionary with the encoded data
            user_data['encrypted_data'] = encoded_data
            try:
                #print(f"Print line 26 User Data: {user_data}")
                encrypted_data = self.encrypt_data(user_data, export_key)
                print(f"Print Line 34| Encrypted Data: {type(encrypted_data)}")
                with open(export_path, 'wb') as file:
                    file.write(encrypted_data)
                return True
            except Exception as e:
                messagebox.showinfo("Error Happened", "Line 40: Error: {e}")
        return False

    def get_user_data(self, user_id):
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
        print(f"Line 80| {user_data}")
        print(f"Line 81| {type(user_data)}")
        return user_data

    def encrypt_data(self, data, key):
        json_data = json.dumps(data)
        fernet = Fernet(key)
        encrypted_bytes = fernet.encrypt(json_data.encode())
        print(f"Line 75| Encrypted Bytes: {encrypted_bytes}")
        return encrypted_bytes

    def get_username(self):
        username = askstring("Username Export", "Enter the username you want to export: ")
        with sqlite3.connect(self.db_handler.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                self.filepath = self.save_to_file_path(username)
                if self.filepath:
                    if self.export_user(user_id, self.filepath):
                        messagebox.showinfo(title="User Export Success",
                                            message=f"User {username}, was exported succesfully.\nKeep this file safe and "
                                                    f"delete it after importing")
                    else:
                        messagebox.showinfo("File Not Saved", "User Was Not Exported")

                else:
                    messagebox.showinfo("File Not Saved", "User Was Not Exported")
            else:
                messagebox.showinfo("No User", "Sorry that user does not exist in the database")

    def save_to_file_path(self, username):
        file = filedialog.asksaveasfile(
            title="Export User Save File Location",
            defaultextension=".enc",
            filetypes=[("ENC Files", "*.enc")],
            initialfile=f"export_user_{username}.enc",
            initialdir= "/",
        )
        if file:
            filepath = file.name
            file.close()
            return filepath
        else:
            return None
