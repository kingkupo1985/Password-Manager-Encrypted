import sqlite3
import json
from tkinter import filedialog
from CustomGUIFunctions import CommonFunctions
from EncryptionManager import EncryptionManager

class DatabaseDataHandler(CommonFunctions):
    def __init__(self, db_handler, user_id, website_dropdown):
        super().__init__()
        self.db_handler = db_handler
        self.user_id = user_id
        self.website_dropdown = website_dropdown

    def get_encrypted_dictionary(self, user_id):
        with sqlite3.connect(self.db_handler) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT encrypt_dictionary FROM passwords WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
        return result[0] if result else None

    # Save data to database has GUI controls
    def save_to_db(self, user_id, website_entry, email_user_entry, password_entry):
        website = website_entry.get()
        username = email_user_entry.get()
        password = password_entry.get()
        if len(website) == 0 or len(username) == 0 or len(password) == 0:
            self.custom_showinfo(title='⚠️ Notice ⚠️', message='Please do not leave any fields blank!')
        else:
            ok_to_save = self.custom_showinfo(title=website, message=f"These are the details you'd like to save"
                                                                       f"\nUsername: {username}\nPassword: {password}")
            if ok_to_save:
                key = EncryptionManager.load_key() #add encryption class import
                try:
                    # Connect to the database
                    with sqlite3.connect('password_manager.db') as conn:
                        cursor = conn.cursor()
                        # Fetch the existing encrypted dictionary
                        existing_data = self.get_encrypted_dictionary(user_id)
                        if existing_data:
                            # Decrypt the existing data
                            try:
                                existing_data_decrypted = EncryptionManager.decrypt(existing_data, key)
                            except Exception as decryption_error:
                                self.custom_showinfo(title='🛑 Warning 🛑', message=f"Decryption error: {decryption_error}")
                                return

                            # Update the existing data with new data
                            existing_data_dict = json.loads(existing_data_decrypted)
                            new_data = {
                                website: {
                                    'username': username,
                                    'password': password
                                }
                            }
                            existing_data_dict.update(new_data)
                            # Encrypt the updated data
                            updated_data_encrypted = EncryptionManager.encrypt(json.dumps(existing_data_dict).encode('utf-8'), key)
                            # Update the row in the database with the updated encrypted dictionary
                            cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                                           (updated_data_encrypted, user_id))
                            conn.commit()
                            self.custom_showinfo(title='✅ Success! ✅', message='Your New Entry Was Saved!')
                            website_entry.delete(0, 'end')
                            email_user_entry.delete(0, 'end')
                            password_entry.delete(0, 'end')
                        else:
                            # If no existing data, create a new entry
                            new_data = {
                                website: {
                                    'username': username,
                                    'password': password
                                }
                            }
                            new_data_encrypted = EncryptionManager.encrypt(json.dumps(new_data).encode('utf-8'), key)

                            # Insert a new row with the encrypted dictionary
                            cursor.execute("INSERT INTO passwords (user_id, encrypt_dictionary) VALUES (?, ?)",
                                           (user_id, new_data_encrypted))
                            conn.commit()
                            self.custom_showinfo(title='✅ Success! ✅', message='Your New Entry Was Saved!')
                            website_entry.delete(0, 'end')
                            email_user_entry.delete(0, 'end')
                            password_entry.delete(0, 'end')

                except sqlite3.Error as error:
                    self.custom_showinfo(title='🛑 Warning🛑', message=f"Sorry Some Error Happened: {error}")

    def find_password_db(self, user_id, website_entry):
        # Let's find a website and its logins
        website = website_entry.get()
        # Get the key to decrypt data
        key = EncryptionManager.load_key()

        try:
            # Does the user exist and have anything stored?
            existing_data = self.get_encrypted_dictionary(user_id)

            if existing_data:
                decrypted_data = EncryptionManager.decrypt(existing_data, key)
                # Read old data and save to variable
                data = json.loads(decrypted_data)
            else:
                # If no data exists, set data to an empty dictionary
                data = {}
        except (FileNotFoundError, json.JSONDecodeError) as error:
            self.custom_showinfo(title='Warning', message=f"Sorry Some Error Happened: {error}")
            # Set data to an empty dictionary
            data = {}

        # Rest of the function remains the same
        if website in data:
            email = data[website]['username']
            password = data[website]['password']
            self.custom_showinfo(title=f'Login',
                            message=f'Website:{website}\nUsername: {email}\nPassword: {password}')
        else:
            self.custom_showinfo(title=f'⚠️ Website Not Found ⚠️', message=f'Sorry, No Entry Found')

    # --- Drop Down Data Function Database --- #
    def update_dropdown(self, user_id):
        try:
            key = EncryptionManager.load_key()
            try:
                # Does the user exist and have anything stored?
                existing_data = self.get_encrypted_dictionary(user_id)

                if existing_data:
                    decrypted_data = EncryptionManager.decrypt(existing_data, key)
                    # Read old data and save to variable
                    data = json.loads(decrypted_data)
                else:
                    data = {}
            except (FileNotFoundError, json.JSONDecodeError) as error:
                self.custom_showinfo(title='Warning', message=f"Sorry Some Error Happened: {error}")
                with open('save_passwords.json.enc', mode='w') as save_file:
                    # create file if not existing
                    data = {}
            finally:
                website_list = list(data.keys())
                self.website_dropdown['values'] = website_list
        except (FileNotFoundError, json.JSONDecodeError) as error:
            self.custom_showinfo(title='🛑 Warning 🛑', message=f"Sorry Some Error Happened: {error}")
            with open('save_passwords.json.enc', mode='w') as save_file:
                data = {}

        website_list = list(data.keys())
        website_dropdown['values'] = website_list

    # --- Load Old JSON File to Database --- #
    def load_json_db(self, user_id):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        try:
            with open(file_path, mode='r') as json_file:
                new_data = json.load(json_file)
            # Convert new_data to bytes
            json_string = json.dumps(new_data)
            new_data_bytes = json_string.encode('utf-8')
        except (FileNotFoundError, json.JSONDecodeError):
            self.custom_showinfo(title='🛑 Error 🛑', message='Failed to load JSON file.')
            return
        key = EncryptionManager.load_key()
        try:
            with sqlite3.connect(self.db_handler) as conn:
                cursor = conn.cursor()
                encrypted_data = EncryptionManager.encrypt(new_data_bytes, key)  # Pass bytes to encrypt function
                cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                               (encrypted_data, user_id))
                conn.commit()
                # Check if a row with the given user_id already exists
                cursor.execute("SELECT * FROM passwords WHERE user_id = ?", (user_id,))
                existing_row = cursor.fetchone()

                if existing_row:
                    # If row exists, update it
                    encrypted_data = EncryptionManager.encrypt(new_data_bytes, key)  # Pass bytes to encrypt function
                    cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                                   (encrypted_data, user_id))
                    conn.commit()
                    self.custom_showinfo(title='✅ Success! ✅', message=f"Your File Was Loaded and Updated Successfully!")
                else:
                    # If no row exists, create the first row
                    encrypted_data = EncryptionManager.encrypt(new_data_bytes, key)  # Pass bytes to encrypt function
                    cursor.execute("INSERT INTO passwords (user_id, encrypt_dictionary) VALUES (?, ?)",
                                   (user_id, encrypted_data))
                    conn.commit()
                    self.custom_showinfo(title='✅ Success! ✅', message=f"Your File Was Loaded and Saved Successfully!")

        except sqlite3.Error as error:
            self.custom_showinfo(title='🛑 Error 🛑', message=f"Sorry Some Error Happened: {error}")
            # create file if not existing
            data = {}
            data.update(new_data)

        update_dropdown(user_id) # data for the drop down combobox in GUI handler for main window somehow

    def get_decrypted_dictionary(self, user_id):
        key = EncryptionManager.load_key()
        try:
            with sqlite3.connect(self.db_handler) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT encrypt_dictionary FROM passwords WHERE user_id = ?", (user_id,))
                encrypted_data = cursor.fetchone()
                if encrypted_data:
                    decrypted_data = EncryptionManager.decrypt(EncryptionManager.decrypt(encrypted_data[0], key))
                    return json.loads(decrypted_data)
                else:
                    return {}
        except sqlite3.Error as error:
            self.custom_showinfo(title='🛑 Error 🛑', message=f"Sorry Some Error Happened: {error}")
            return {}

    # ---------------------------- END DATABASE DATA FUNCTIONS ------------------------------- #