import sqlite3
import json
import threading
from tkinter import filedialog, messagebox
from CustomGUIFunctions import CommonFunctions
from EncryptionManager import EncryptionManager

class DatabaseDataHandler(CommonFunctions):
    def __init__(self, db_handler, user_id, website_dropdown):
        super().__init__()
        self.db_handler = db_handler
        self.user_id = user_id
        self.website_dropdown = website_dropdown
        self.encryption_manager = EncryptionManager()

    def get_encrypted_dictionary(self, user_id):
        try:
            with sqlite3.connect(self.db_handler.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT encrypt_dictionary FROM passwords WHERE user_id = ?", (user_id,))
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"An error occurred while retrieving encrypted dictionary line 24:\nError:{error}")
            return None

    def get_decrypted_dictionary(self, user_id):
        try:
            with sqlite3.connect(self.db_handler.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT encrypt_dictionary FROM passwords WHERE user_id = ?", (user_id,))
                encrypted_data = cursor.fetchone()
                if encrypted_data:
                    decrypted_data = self.encryption_manager.decrypt(encrypted_data[0])
                    return json.loads(decrypted_data)
                else:
                    return {}
        except sqlite3.Error as error:
            messagebox.showinfo("Error", f"Sorry a Error Happened with SQLite3 at line 39:\nError:{error}")
            return {}

    def save_to_db(self, user_id, website_entry, email_user_entry, password_entry):
        try:
            website = website_entry.get()
            username = email_user_entry.get()
            password = password_entry.get()
            if len(website) == 0 or len(username) == 0 or len(password) == 0:
                messagebox.showinfo(
                    title='⚠️ Notice ⚠️',
                    message='Please do not leave any fields blank!')
            else:
                message = f"These are the details you'd like to save\nUsername: {username}\nPassword: {password}"
                ok_to_save = messagebox.askyesno(website, message)
                if ok_to_save:
                    try:
                        with sqlite3.connect(self.db_handler.db_name) as conn:
                            cursor = conn.cursor()
                            existing_data = self.get_encrypted_dictionary(user_id)
                            if existing_data:
                                try:
                                    existing_data_decrypted = self.encryption_manager.decrypt(existing_data)
                                except Exception as decryption_error:
                                    messagebox.showinfo(
                                        title='🛑 Warning 🛑',
                                        message=f"Decryption error at line 65:\nError:{decryption_error}")
                                    return

                                existing_data_dict = json.loads(existing_data_decrypted)
                                new_data = {
                                    website: {
                                        'username': username,
                                        'password': password
                                    }
                                }
                                existing_data_dict.update(new_data)
                                updated_data_encrypted = self.encryption_manager.encrypt(json.dumps(existing_data_dict).encode('utf-8'))
                                cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                                               (updated_data_encrypted, user_id))
                                conn.commit()
                                print(f"updated_data_encrypted: {updated_data_encrypted}")
                                messagebox.showinfo(
                                    title='✅ Success! ✅',
                                    message='Your New Entry Was Saved!')
                                website_entry.delete(0, 'end')
                                email_user_entry.delete(0, 'end')
                                password_entry.delete(0, 'end')
                            else:
                                new_data = {
                                    website: {
                                        'username': username,
                                        'password': password
                                    }
                                }
                                new_data_encrypted = self.encryption_manager.encrypt(json.dumps(new_data).encode('utf-8'))

                                cursor.execute("INSERT INTO passwords (user_id, encrypt_dictionary) VALUES (?, ?)",
                                               (user_id, new_data_encrypted))
                                conn.commit()
                                self.update_dropdown(user_id)
                                messagebox.showinfo(
                                    title='✅ Success! ✅',
                                    message='Your New Entry Was Saved!')
                                website_entry.delete(0, 'end')
                                email_user_entry.delete(0, 'end')
                                password_entry.delete(0, 'end')

                    except sqlite3.Error as error:
                        messagebox.showinfo(
                            title='🛑 Warning🛑',
                            message=f"Sorry Some Error Happened with SQLite3 line 110:]\nError:{error}")
        except Exception as error:
            messagebox.showinfo(
                title='🛑 Warning🛑',
                message=f"Sorry Some Error Happened at line 114: {error}")

    def find_password_db(self, user_id, website_entry):
        website = website_entry.get()
        try:
            existing_data = self.get_encrypted_dictionary(user_id)

            if existing_data:
                decrypted_data = self.encryption_manager.decrypt(existing_data)
                data = json.loads(decrypted_data)
            else:
                data = {}
        except (FileNotFoundError, json.JSONDecodeError) as error:
            messagebox.showinfo(
                title='Warning',
                message=f"Sorry Some Error Happened with JSON line 127:Error:{error}")
            data = {}

        if website in data:
            email = data[website]['username']
            password = data[website]['password']
            messagebox.showinfo(
                title=f'Login',
                message=f'Website:{website}\nUsername: {email}\nPassword: {password}')
        else:
            messagebox.showinfo(
                title=f'⚠️ Website Not Found ⚠️',
                message=f'Sorry, No Entry Found')

    def update_dropdown(self, user_id):
        try:
            key = self.encryption_manager.load_key()
            try:
                data = {}
                existing_data = self.get_encrypted_dictionary(user_id)

                if existing_data:
                    decrypted_data = self.encryption_manager.decrypt(existing_data)
                    data = json.loads(decrypted_data)
                else:
                    data = {}
            except (FileNotFoundError, json.JSONDecodeError) as error:
                messagebox.showinfo(
                    title='Warning',
                    message=f"Sorry Some Error Happened at Line 156 with the JSON:Error:{error}")
            finally:
                website_list = list(data.keys())

        except (FileNotFoundError, json.JSONDecodeError) as error:
            messagebox.showinfo(
                title='🛑 Warning 🛑',
                message=f"Sorry Some Error Happened with the JSON at line 163:\nError:{error}")

        website_list = list(data.keys())
        self.website_dropdown['values'] = website_list

    # Load in the JSON file
    def load_json_db(self, user_id):
        # Let's get the file to import
        try:
            file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
            if not file_path:
                return
            try:
                with open(file_path, mode='r') as json_file:
                    new_data = json.load(json_file)
                json_string = json.dumps(new_data)
                new_data_bytes = json_string.encode('utf-8')
            except (FileNotFoundError, json.JSONDecodeError) as e:
                messagebox.showinfo(title='🛑 Error 🛑', message=f'Failed to load JSON file.\nError:{e}')
                return
            # We've gotten the JSON let's add the data to the database and encrypt the data
            try:
                with sqlite3.connect(self.db_handler.db_name) as conn:
                    cursor = conn.cursor()
                    encrypted_data = self.encryption_manager.encrypt(new_data_bytes)
                    cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                                   (encrypted_data, user_id))
                    conn.commit()
                    cursor.execute("SELECT * FROM passwords WHERE user_id = ?", (user_id,))
                    existing_row = cursor.fetchone()
                    # Check it data exists and if yes update
                    if existing_row:
                        encrypted_data = self.encryption_manager.encrypt(new_data_bytes)
                        cursor.execute("UPDATE passwords SET encrypt_dictionary = ? WHERE user_id = ?",
                                       (encrypted_data, user_id))
                        conn.commit()
                        messagebox.showinfo(title='✅ Success! ✅', message=f"Your File Was Loaded and Updated Successfully!")
                    else:
                        encrypted_data = self.encryption_manager.encrypt(new_data_bytes)
                        cursor.execute("INSERT INTO passwords (user_id, encrypt_dictionary) VALUES (?, ?)",
                                       (user_id, encrypted_data))
                        conn.commit()
                        messagebox.showinfo(title='✅ Success! ✅', message=f"Your File Was Loaded and Saved Successfully!")

            except sqlite3.Error as error:
                messagebox.showinfo(title='🛑 Error 🛑', message=f"Sorry Some Error Happened with SQLite3: {error}")
                data = {}
                data.update(new_data)

            self.update_dropdown(user_id)
        except Exception as error:
            pass

    # let's make sure if we load in a json it will not cause a crash
    def load_json_concurrently_wrapper(self, user_id):
        try:
            threading.Thread(target=self.load_json_db, args=(user_id,)).start()
        except Exception as e:
            messagebox.showinfo(title='🛑 Error 🛑', message=f"Sorry Some Error Happened with the Thread: {e}")
