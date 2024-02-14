from DatabaseUserHandler import DatabaseHandler
from UserLogin import LoginWindow
from tkinter import *

# Usage example
if __name__ == "__main__":
    #Let's create our database object
    database = DatabaseHandler()
    #Let's check if the database exists, and it not let's create it this method will also prompt for the first user to be created
    database.check_and_create_databases()
    #Let's create the window object to make the app run smooth I hope
    window = Tk()
    #Let's create the login window
    login_window = LoginWindow(database, window)
    # Let's get GUI
    window.mainloop()