# Password-Manager-Encrypted

2024/02/14 - Functions Working Except for Dropdown Get Data function, Fixed the Crash Issue with Tkinter and Loading JSON I had multiple Instances of Tkinter running, I fixed that the app uses one Tk() object in the main.py and passes it to login window once the login is the success it creates the mainwindow. -Fixes needed: Dropdown doesn't get login data for pop up, displays n/a plus no runtime errors or compiler. JSON file loads clean but we get an error in runtime after it loads, we need to catch the exception to check it we also get the same error when adding a new entry manually to the database, however the data is entered. 

2024/02/13 - converted to OOP classes working, GUI functions, proper window login sequence, Dropdown function working, add to database working, create user working, login authentication working. Still to fix: load JSON file, Search Function, Generate Password Function

Work in progress 2024/01/24 - Working Code with following Features: Keyring to encrypt stored passwords w/ tkinter GUI
