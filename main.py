from DatabaseUserHandler import DatabaseHandler
from DatabaseDataHandler import DatabaseDataHandler
from UserLogin import LoginWindow
from MainWindow import MainWindow

# Usage example
if __name__ == "__main__":
    #Let's create our database object
    database = DatabaseHandler()
    #Let's check if the database exists, and it not let's create it this method will also prompt for the first user to be created
    database.check_and_create_databases()
    #Let's create the login window
    login_window = LoginWindow(database)
    # Let's create the login window and get the user ID
    login_window.create_login_window()
    # If the user exists let's create the Main GUI window and DatabaseData Handler
    if login_window.user_id is not None:
        print(f"User ID: {login_window.user_id}")
        #Let's create our object to handle data between the GUI window and database do I need this?
        data_handler = DatabaseDataHandler(db_handler=database, user_id=login_window.user_id, website_dropdown=None)
        # Let's create our GUI window
        gui_window = MainWindow(db_handler=database, user_id=login_window.user_id)
        gui_window.create_main_window()