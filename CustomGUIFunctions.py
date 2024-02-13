from tkinter import Toplevel, Frame, Label, Button, messagebox

class CommonFunctions:
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x_position}+{y_position}")
    def custom_showinfo(self, title, message):
        messagebox.showinfo(title, message)
        top = Toplevel()
        top.title(title)
        top.lift()
        # Set the width and height of the toplevel window
        top_width = 300
        top_height = 100

        # Use the common center_window method
        self.center_window(top, top_width, top_height)

        # Calculate the x and y coordinates to center the toplevel window
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()

        x_position = (screen_width - top_width) // 2
        y_position = (screen_height - top_height) // 2

        top.geometry(f"{top_width}x{top_height}+{x_position}+{y_position}")

        # Create a frame to hold the label and button
        frame = Frame(top)
        frame.pack(expand=True)

        # Create and center the label
        label = Label(frame, text=message)
        label.pack(pady=(10, 0))  # Add padding only at the top

        # Create and center the button
        ok_button = Button(frame, text="OK", command=top.destroy)
        ok_button.pack(pady=(10, 0))  # Add padding only at the top
