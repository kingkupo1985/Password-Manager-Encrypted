import tkinter as tk
from os.path import  join
from PIL import Image, ImageTk
from button_images import button_images

class CustomButton(tk.Canvas):
    def __init__(self, master=None, corner_radius=8, button_name=None, command=None, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.button_name = button_name
        self.corner_radius = corner_radius
        self.command = command
        self.images = None
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.load_images()

    def load_image(self, imagename):
        if imagename:
            path = join("images/buttons", imagename)
            image = Image.open(path)
            image = image.resize((self.winfo_reqwidth(), self.winfo_reqheight()))
            self.photo_image = ImageTk.PhotoImage(image)
            self.create_image(0, 0, anchor="nw", image=self.photo_image)
            self.create_rounded_rectangle(0, 0, self.winfo_reqwidth(), self.winfo_reqheight(), fill="", outline="")
            return ImageTk.PhotoImage(image)

    def load_images(self):
        self.images = button_images.get(self.button_name)
        self.hover_image = self.load_image(self.images['hover'])
        self.pressed_image = self.load_image(self.images['pressed'])
        self.base_image = self.load_image(self.images['base'])


    # This function is suppose to create rounded square canvas objects to cut off the corners
    # but I still see black or gray where it  should be transparent pixels
    def create_rounded_rectangle(self, x1, y1, x2, y2, **kwargs):
        radius = self.corner_radius
        self.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, start=90, extent=90, **kwargs)
        self.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, start=0, extent=90, **kwargs)
        self.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, start=180, extent=90, **kwargs)
        self.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, **kwargs)
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, **kwargs)

    def update_image(self, image):
        self.current_image = image

    def on_click(self, event):
        self.load_image(self.images['pressed'])

    def on_release(self, event):
        self.load_image(self.images['hover'])
        if self.command:
            self.command()

    def on_enter(self, event):
        self.load_image(self.images['hover'])

    def on_leave(self, event):
        self.load_image(self.images['base'])

    def button_clicked(self):
        print(f"You clicked the {self.button_name}")

# Example usage
# root = tk.Tk()
# button1 = CustomButton(root, width=122, height=40, button_name="Login")
# button1.place(x=189, y=230)
# button2 = CustomButton(root, width=122, height=40, button_name="Add")
# button2.place(x=189, y=275)
# root.geometry(f"{500}x{500}")
# root.mainloop()
