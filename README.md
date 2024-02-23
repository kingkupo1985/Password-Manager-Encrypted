# Password-Manager-Encrypted

This was my own thought project, with everyone needing a password for so many sites, this was a pratical solution to store passwords securely, and keep track of memberships. The benefits to this app over using a online password vault is this app can run without the internet on a computer that isn't connected to the internet. Allowing you a digital safe place to store your passwords and keep track and don't worry I have a data migration feature that will securly export your user data using a passphrase. This is if you get a new computer and need to migrate the data. 

#### Milestones in this project for my learning purposes: ####

FERNET - Encryption Used to Store Sensitive Data. We use Fernet for creating a unique key stored to the user's keyring on their PC so only they can access and decrypt the data while logged into their user

BCRYPT - We use Bcrypt for having and storing the user password to access the app itself so when you create a user their password to login is fairly safe and hard to access from what I've read

GUI Objects - Tkinter learned to use 1 window object and pass it between required classes to prevent errors and crashes this prevented a JSON loading crash regularly I had multiple Tk()'s and when I would try to load a JSON to store it securely the app would crash and give me an error popup from my OS, not the terminal runtime or tkinter popup python would crash. It was a good learning curve about the GUI windows, how to collect data and pass it like the USER to make sure we have the correct encrypted data to display when they want to retrieve an old password to log in. 

GUI Tkinter DROPDOWN - Never used a Dropdown Object in Tkinter only online. Was a great widget to learn how to use, update, and retrieve data with. 

SQLITE3 - First time using a database through an offline app with SQLITE3, I've used jinja, and flask in the past for online apps like a blog build but never a stand-alone app. Had to build SQL commands and couldn't use SQLAlchemy which I was familiar with. 

CLASS INHERITANCE - Only used inherit properties from other classes but this time I created a class and had another class inherit the properties, wanted all windows to be centered when created so I created a CommonFunction to center Tkinter windows when they're created, and classes MainWindow and LoginWindow both inherit CommonFunctions properties to call the center screen function.

THREADING - Wrapped JSON loader to make sure we didn't have a concurrency error between Tk() window and filedialog opening to load in a file. 

ENCRYPTION - I learned a lot about salt, and other encryption protocols mentioned above, the final program can have multiple users up to the limits of an SQLite database, we keep user login and a hash of their password in the user's table using bcrypt, for the stored data in the database for each user we encrypt a json file that stores their encrypted data, the data is encrypted using Fernet. What made this unique was learning about bytes and strings. To make sure the data was handled properly when being created/updated. When it came to user exports we allows the userto create a passphrase to allow them to import their user on a system migration keeping their stored data. 

BYTES - I learned how to store bytes ad a string and retereve those bytes to be used this was crucial because the bytes string was encrypted against a key, so the the bytes string was altered the data would not be able to be decrypted. This was for the import/export user functions.I learned a lot from this alone

STORING DATA SECURELY - User data was encrypted using a passphrase that users create, the passphrase is salted and the encryption key is derived from the salted passphrase this passphrase is required to import the user data for Station Migration.

The original app from the Udemy course was a simple 117-line password generator and storing app it only generated a random password and saved it to a readable JSON file that anyone could read in plain English and worse it was in JSON format making it easier for an app to read the data. I took it upon myself to make this a potential app for a personal storage app of one's passwords. In a growing world of apps we use it's hard to remember every password and every website we join. So this helps keep it all stored securely in one spot. I DO NOT recommend I will repeat I DO NOT recommend using this app  for storing and saving your passwords unless you are savvy with python and computers. This app now has a database that can have multiple users using the app each with their own encrypted store of passwords. Like a family all using one computer... Like it's still the early 2000's lol... Let's be real this was for my own knowledge of objects, classes, databases and logins not using a web app. 
Final App: 989 lines

#### UPDATES Below ####

2024/02/22 - All Functions are Working: Import/Export User, Save Encrypted Data, Generate Password, Import JSON, Clear

2024/02/20 - The export function working 100% for users with data and users with no data, we started working on the import user function

2024/02/19 - Finally found the JSON bytes error in the data['encrypted_data'] in the dict was already in bytes format, had to catch this instance and convert it to string and add it back to the dict for exporting

2024/02/16 - Added Import/Export Buttons to Login Window, and created user_export function - Datatype Error: Bytes Not JSON serializable, updated graphics of all buttons, now looks like clicked when pushed.

2024/02/14 - Functions Working Except for Dropdown Get Data function, Fixed the Crash Issue with Tkinter and Loading JSON I had multiple Instances of Tkinter running, I fixed that the app uses one Tk() object in the main.py and passes it to login window once the login is the success it creates the mainwindow. -Fixes needed: Dropdown doesn't get login data for pop up, displays n/a plus no runtime errors or compiler. JSON file loads clean but we get an error in runtime after it loads, we need to catch the exception to check it we also get the same error when adding a new entry manually to the database, however the data is entered. 

2024/02/13 - converted to OOP classes working, GUI functions, proper window login sequence, Dropdown function working, add to database working, create user working, login authentication working. Still to fix: load JSON file, Search Function, Generate Password Function

2024/01/24 - Working Code with following Features: Keyring to encrypt stored passwords w/ Tkinter GUI (Main2.py) - Fully working app as a standalong single file app, but the windows load all at once, if I change that the JSON won't load but I think I know how to fix that now (24/2/14)

2024/01/22 - Idea came to me on this day take old boring basic non secure Udemy Password app fom coding course and make it a realworld app!