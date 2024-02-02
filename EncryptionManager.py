from cryptography.fernet import Fernet
import keyring

class EncryptionManager:
    def __init__(self, service_name="password_manager", account_name="user_key"):
        self.service_name = service_name
        self.account_name = account_name
        self.key = self.load_key()

    def generate_key(self):
        # Generate a key
        key = Fernet.generate_key()
        keyring.set_password(self.service_name, self.account_name, key.decode())
        return key

    def load_key(self):
        try:
            key = keyring.get_password(self.service_name, self.account_name)
            if key is None:
                key = self.generate_key()
        except Exception as e:
            print(f"Error loading key: {e}")
            key = self.generate_key()
        return key

    def encrypt(self, data):
        # Encrypt your data
        cipher = Fernet(self.key)
        encrypted_data = cipher.encrypt(data.encode())
        return encrypted_data

    def decrypt(self, encrypted_data):
        # Decrypt your Data
        cipher = Fernet(self.key)
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        return decrypted_data