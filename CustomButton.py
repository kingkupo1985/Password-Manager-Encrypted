import tkinter as tk
from tkinter import messagebox
from os.path import join
from PIL import Image, ImageTk
from button_images import button_images

class CustomButton(tk.Canvas):
    def __init__(self, master=None, corner_radius=8, button_name=None, command=None, **kwargs):
        try:
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
        except Exception as e:
            messagebox.showerror("Error", f"Error in CustomButton initialization: {e}")

    def load_image(self, imagename):
        try:
            if imagename:
                path = join("images/buttons", imagename)
                image = Image.open(path)
                image = image.resize((self.winfo_reqwidth(), self.winfo_reqheight()))
                self.photo_image = ImageTk.PhotoImage(image)
                self.create_image(0, 0, anchor="nw", image=self.photo_image)
                self.create_rounded_rectangle(0, 0, self.winfo_reqwidth(), self.winfo_reqheight(), fill="", outline="")
                return ImageTk.PhotoImage(image)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image {imagename}: {e}")

    def load_images(self):
        try:
            self.images = button_images.get(self.button_name)
            self.hover_image = self.load_image(self.images['hover'])
            self.pressed_image = self.load_image(self.images['pressed'])
            self.base_image = self.load_image(self.images['base'])
        except Exception as e:
            messagebox.showerror("Error", f"Error loading images for button {self.button_name}: {e}")

    # 100% AI made function for GUI map to create clip corners and make rounded
    def create_rounded_rectangle(self, x1, y1, x2, y2, **kwargs):
        try:
            radius = self.corner_radius
            self.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, start=90, extent=90, **kwargs)
            self.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, start=0, extent=90, **kwargs)
            self.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, start=180, extent=90, **kwargs)
            self.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, **kwargs)
            self.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)
            self.create_rectangle(x1, y1 + radius, x2, y2 - radius, **kwargs)
        except Exception as e:
            messagebox.showerror("Error", f"Error creating rounded rectangle: {e}")

    def update_image(self, image):
        try:
            self.current_image = image
        except Exception as e:
            messagebox.showerror("Error", f"Error updating image: {e}")

    def on_click(self, event):
        try:
            self.load_image(self.images['pressed'])
        except Exception as e:
            messagebox.showerror("Error", f"Error on click: {e}")

    def on_release(self, event):
        try:
            self.load_image(self.images['hover'])
            if self.command:
                self.command()
        except Exception as e:
            messagebox.showerror("Error", f"Error on release: {e}")

    def on_enter(self, event):
        try:
            self.load_image(self.images['hover'])
        except Exception as e:
            messagebox.showerror("Error", f"Error on enter: {e}")

    def on_leave(self, event):
        try:
            self.load_image(self.images['base'])
        except Exception as e:
            messagebox.showerror("Error", f"Error on leave: {e}")

    def button_clicked(self):
        try:
            messagebox.showinfo("Button Clicked", f"You clicked the {self.button_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Error in button_clicked: {e}")

# Example usage
# root = tk.Tk()
# button1 = CustomButton(root, width=122, height=40, button_name="Login")
# button1.place(x=189, y=230)
# button2 = CustomButton(root, width=122, height=40, button_name="Add")
# button2.place(x=189, y=275)
# root.geometry(f"{500}x{500}")
# root.mainloop()
