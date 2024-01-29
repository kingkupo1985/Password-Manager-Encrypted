import sqlite3
import bcrypt


class DatabaseHandler:
    def __init__(self, db_name='password_manager.db'):
        self.db_name = db_name

    def create_tables(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                encrypt_dictionary TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            ''')

    def is_not_database_empty(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            return count > 0
        except sqlite3.OperationalError:
            return False

    def check_and_create_databases(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                if self.is_not_database_empty(conn):
                    return True
                else:
                    return False
        except sqlite3.OperationalError:
            return False

    def create_user(self, username, password):
        hashed_password = self.hash_password(password)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None

    def get_user_id(self, username, password):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                user_id, hashed_password = result
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    return user_id
        return None

    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def get_encrypted_dictionary(self, user_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT encrypt_dictionary FROM passwords WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
        return result[0] if result else None

    def save_to_db(self, user_id, website, username, password):
        key = self.load_key()
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                existing_data = self.get_encrypted_dictionary(user_id)
                # Remaining code for saving to database
                # ...

        except sqlite3.Error as error:
            return False

# Example usage:
# db_handler = DatabaseHandler()
# db_handler.create_tables()
# if not db_handler.check_and_create_databases():
#     db_handler.create_user("username", "password")
#     user_id = db_handler.get_user_id("username", "password")
#     print(user_id)
#     # Continue with other operations
