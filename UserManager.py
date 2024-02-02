from user_login import UserLogin
from MainWindow import MainWindow
from DatabaseUserHandler import DatabaseHandler

class UserManager:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.current_user_id = None

    def run_password_manager(self):
        user_login = UserLogin(self.db_handler)
        self.current_user_id = user_login.run_login_window()

        if self.current_user_id is not None:
            main_window = MainWindow(self.db_handler, self.current_user_id)
            main_window.create_main_window()

if __name__ == "__main__":
    password_manager = UserManager()
    password_manager.run_password_manager()