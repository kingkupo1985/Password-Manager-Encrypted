import json, sqlite3, base64, bcrypt, os
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
        self.filepath = self.open_file_path()
        passphrase = askstring("User Import", "What is your passphrase you created when exporting your user data:?")
        try:
            # Read the encrypted data and salt from the import file
            with open(self.filepath, 'rb') as file:
                lines = file.readlines()
                encrypted_data = lines[0].strip()
                salt = lines[1].strip()
            # Decode encypted_data bytes to base64
            encoded_encrypted_data = base64.b64encode(encrypted_data).decode('utf-8')

            # Derive the key from the passphrase and the salt
            key = self.encryption_manager.generate_fernet_key(passphrase, salt)

            # Decrypt the data using the derived key
            decrypted_data_dict = self.decrypt_data(encoded_encrypted_data, key)
            # Loop through decrypted data to update user passwords
            for key, value in decrypted_data_dict.items():
                print(f"line 36: {key} {value}")
                # connect to the database
                with sqlite3.connect(self.db_handler.db_name) as conn:
                    cursor = conn.cursor()

                # Check if the user exists
                user_id = self.db_handler.get_user_id(username)
                if user_id is not None:
                    # Update the existing user's password
                    cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                                   (base64.b64encode(
                                       json.dumps({key: {'username': username, 'password': password}}).encode(
                                           'utf-8')), user_id))
                    conn.commit()
                else:
                    # Insert a new user and their password
                    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                                   (username, encrypted_password))
                    user_id = cursor.lastrowid
                    cursor.execute("INSERT INTO passwords (user_id, encrypt_dictionary) VALUES (?, ?)",
                                   (user_id, base64.b64encode(
                                       json.dumps({key: {'username': username, 'password': password}}).encode(
                                           'utf-8'))))
                    conn.commit()
            return True
        except Exception as e:
            print(f"Error importing user: {e}")
            return False

    def export_user(self, user_id, export_path, passphrase):
        # Gather user data
        user_data = self.get_user_data(user_id)
        # generate key for exporting/importing user data
        salt = os.urandom(16)
        # Derive the key from the passphrase and the salt
        key = self.encryption_manager.generate_fernet_key(passphrase, salt)
        # Let's export the data
        if user_data:
            try:
                # Handle the case when 'encrypted_data' is empty
                if user_data['encrypted_data'] == "":
                    # Serialize the entire dictionary to JSON
                    json_data = json.dumps(user_data)
                else:
                    # Handle the 'encrypted_data' separately and encode it to base64
                    user_data['encrypted_data'] = base64.b64encode(user_data['encrypted_data']).decode('utf-8')
                    # Serialize the dictionary to JSON
                    json_data = json.dumps(user_data)

                # Encrypt the JSON data using the derived key
                encrypted_user_export = self.encrypt_data(json_data, key)
                print(f"Line 104: Export Key:{key}")
                # Write the encrypted data and salt to the export file
                with open(export_path, 'wb') as file:
                    file.write(encrypted_user_export + b'\n' + salt)
                return True
            except Exception as e:
                messagebox.showinfo("Error Happened", f"Error: {e}")

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
        fernet = Fernet(key)
        encrypted_bytes = fernet.encrypt(data.encode())
        return encrypted_bytes

    def decrypt_data(self, data, key):
        try:
            # Decode Base64-encoded string to binary
            decoded_data = base64.b64decode(data)
            if decoded_data is None:
                print("Decoded data is None")
                return None

            # Decrypt the binary data using the encryption key
            fernet = Fernet(key)
            decrypted_bytes = fernet.decrypt(decoded_data)

            # Decode the decrypted bytes into a string
            decrypted_data_str = decrypted_bytes.decode('utf-8')

            # Log the decrypted string for inspection
            print("Decrypted data string:", decrypted_data_str)

            # Attempt to parse the decrypted string as JSON
            decrypted_data_dict = json.loads(decrypted_data_str)
            print(f"Line 157| decrypted_data_dict type: {type(decrypted_data_dict)}")

            # Check if the parsed JSON is a dictionary
            if isinstance(decrypted_data_dict, dict):
                print("Decrypted data is a dictionary")
                return decrypted_data_dict
            else:
                print("Decrypted data is not a dictionary")
                return None
        except json.JSONDecodeError as json_error:
            print("JSON decoding error:", json_error)
            return None
        except Exception as e:
            print("Error decrypting data:", e)
            return None

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

    def open_file_path(self):
        file = filedialog.askopenfile(
            title="Export User Save File Location",
            defaultextension=".enc",
            filetypes=[("ENC Files", "*.enc")],
            initialdir="/",
        )
        if file:
            filepath = file.name
            file.close()
            return filepath
        else:
            return None
