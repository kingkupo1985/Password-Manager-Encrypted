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
        self.encryption_manager = EncryptionManager()
        self.window = window
        self.filepath = None

    def import_user(self):
        # Prompt the user to select the import file
        import_file = filedialog.askopenfilename(
            title="Select File to Import",
            filetypes=[("ENC Files", "*.enc")]
        )
        if not import_file:
            return

        # Prompt the user for the passphrase
        passphrase = askstring("Enter Passphrase", "Enter the passphrase for importing user data:")
        if not passphrase:
            return

        # Read the encrypted data from the file
        with open(import_file, "rb") as file:
            encrypted_data = file.read()

        # Decrypt the data using the passphrase
        fernet_key, _ = self.encryption_manager.generate_fernet_key(passphrase)
        decrypted_data = self.decrypt_data(encrypted_data, fernet_key)

        # Import the decrypted data into the database
        if decrypted_data:
            try:
                # Decode the decrypted data from bytes to JSON
                decoded_data = decrypted_data.decode("utf-8")
                user_data = json.loads(decoded_data)

                # Import the user data into the database
                # Implement this based on the structure of user_data
                # For example:
                self.import_user_data(user_data)
                messagebox.showinfo("Import Successful", "User data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during import: {e}")

    def export_user(self, user_id, export_path, passphrase):
        # Gather user data
        user_data = self.get_user_data(user_id)
        # generate key for exporting/importing user data
        fernet_key, salt = self.encryption_manager.generate_fernet_key(passphrase)

        # Let's export the data
        if user_data:
            # Encode the bytes object to base64
            print(f"Userdata['encrypted_data']: {user_data['encrypted_data']}")
            if user_data['encrypted_data'] == "":
                try:
                    encrypted_data = self.encrypt_data(user_data, fernet_key)
                    with open(export_path, 'wb') as file:
                        file.write(encrypted_data)
                    return True
                except Exception as e:
                    messagebox.showinfo("Error Happened", "Line 40: Error: {e}")

            else:
                # encode to base 64
                encoded_data = base64.b64encode(user_data['encrypted_data']).decode('utf-8')
                # Update the dictionary with the encoded data
                user_data['encrypted_data'] = encoded_data
                try:
                    # Excrypt the data!
                    encrypted_data = self.encrypt_data(user_data, fernet_key)
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
        return user_data

    def encrypt_data(self, data, key):
        json_data = json.dumps(data)
        fernet = Fernet(key)
        encrypted_bytes = fernet.encrypt(json_data.encode())
        return encrypted_bytes

    def get_username(self):
        username = askstring("Username Export", "Enter the username you want to export: ")
        passphrase = askstring("Secret Key", "⚠️DO NOT LOSE⚠⚠️ \nKWRITE YOUR PASSPHRASE DOWN\nIF YOU LOSE IT YOU"
                                             "\nWILL NOT BE ABLE \nTO IMPORT YOUR USER DATA️")
        with sqlite3.connect(self.db_handler.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                self.filepath = self.save_to_file_path(username)
                if self.filepath:
                    if self.export_user(user_id, self.filepath, passphrase):
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
