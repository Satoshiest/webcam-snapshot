import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import time
import os

# created by Satoshi Kameyama
# install opencv-python (cv2)
# install pillow (PIL)


def view_image():
    fTyp = [("", ".jpg")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)

    root = tk.Tk()
    app = ViewMode(root, filepath.split('/')[-1])  # Inherit
    app.mainloop()


def watch_video():
    fTyp = [("", ".mp4")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    cap = cv2.VideoCapture(filepath)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Video", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        #  exit when played till end
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.title("Term project")

        self.camera = cv2.VideoCapture(0)
        self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # for video recording fps
        self.fps = int(self.camera.get(cv2.CAP_PROP_FPS))

        # video file format
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------

        # camera frame
        self.cam_frame = ttk.LabelFrame(self.master, text='Camera')
        self.cam_frame.pack(side=tk.BOTTOM)
        self.cam_frame.configure(width=self.width + 30, height=self.height + 50)
        self.cam_frame.grid_propagate(0)

        # Canvas
        self.canvas1 = tk.Canvas(self.cam_frame)
        self.canvas1.configure(width=self.width, height=self.height)
        self.canvas1.grid(column=0, row=0, padx=10, pady=10)

        # button frame
        self.btn_frame = ttk.LabelFrame(self.master, text='Control')
        self.btn_frame.pack(side=tk.BOTTOM)
        self.btn_frame.configure(width=self.width + 30, height=120)
        self.btn_frame.grid_propagate(0)

        # Snapshot Button
        self.btn_snapshot = ttk.Button(self.btn_frame, text='Snapshot')
        self.btn_snapshot.configure(width=15, command=self.snapshot)
        self.btn_snapshot.grid(column=0, row=0, padx=30, pady=10)

        # Record Button
        self.btn_snapshot = ttk.Button(self.btn_frame, text='Record')
        self.btn_snapshot.configure(width=15, command=self.record)
        self.btn_snapshot.grid(column=1, row=0, padx=30, pady=10)

        # View button
        self.view = ttk.Button(self.btn_frame, text='View Image')
        self.view.configure(width=15, command=view_image)
        self.view.grid(column=2, row=0, padx=30, pady=10)

        # Watch button
        self.view = ttk.Button(self.btn_frame, text='Watch Video')
        self.view.configure(width=15, command=watch_video)
        self.view.grid(column=3, row=0, padx=30, pady=10)

        # Close Button
        self.btn_close = ttk.Button(self.btn_frame, text='Close')
        self.btn_close.configure(width=15, command=self.close_button)
        self.btn_close.grid(column=4, row=0, padx=30, pady=10)

        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------
        self.photo = None
        self.lag = 15
        self.update()

    def update(self):
        # Get a frame from the video source
        _, frame = self.camera.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

        # self.photo -> Canvas
        self.canvas1.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.master.after(self.lag, self.update)

    def snapshot(self):
        # Get a frame from the video source
        _, frame = self.camera.read()
        cv2.imwrite("IMG-" + time.strftime("%Y-%d-%m-%H-%M-%S")+".jpg",
                    cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                                 cv2.COLOR_BGR2RGB))

    def record(self):
        video = cv2.VideoWriter(f'{time.strftime("%Y-%d-%m-%H-%M-%S")}.mp4',
                                self.fourcc, self.fps,
                                (self.width, self.height))
        while True:
            _, frame = self.camera.read()
            cv2.imshow('Enter Q to stop recording', frame)
            video.write(frame)
            # enter q to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def close_button(self):
        self.quit()


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


def main():
    root = tk.Tk()
    app = Application(master=root)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
