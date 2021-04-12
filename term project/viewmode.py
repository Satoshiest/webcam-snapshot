import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

# implemented by Satoshi Kameyama
# install opencv-python (cv2)
# install pillow (PIL)


class ViewMode(tk.Frame):
    def __init__(self, master, file):
        super().__init__(master)
        self.master.title("View Mode")
        self.width = 1280
        self.height = 720
        self.file = file

        # camera frame
        self.cam_frame = ttk.LabelFrame(self.master, text='Photo')
        self.cam_frame.pack(side=tk.BOTTOM)
        self.cam_frame.configure(width=self.width + 30, height=self.height + 50)
        self.cam_frame.grid_propagate(0)

        self.canvas1 = tk.Canvas(self.cam_frame,
                                 width=self.width, height=self.height)
        self.canvas1.configure(width=self.width, height=self.height)
        self.canvas1.grid(column=0, row=0, padx=10, pady=10)
        self.canvas1.place(x=0, y=0)

        self.img1 = Image.open(open(f'{self.file}', 'rb'))
        self.img = ImageTk.PhotoImage(self.img1, master=self.cam_frame)  # image
        self.canvas1.create_image(640, 360, image=self.img)
