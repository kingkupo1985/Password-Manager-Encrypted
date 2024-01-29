from database_handler import DatabaseHandler
from EncryptionManager import EncryptionManager
from user_login import UserLogin
from MainWindow import MainWindow
from UserManager import UserManager

# Usage example
if __name__ == "__main__":
    db_handler = DatabaseHandler()
    encryption_manager = EncryptionManager()

    user_login = UserLogin(db_handler, encryption_manager)
    main_window = MainWindow(db_handler, encryption_manager)
    user_manager = UserManager(db_handler, encryption_manager)

    user_login.run_login_window()