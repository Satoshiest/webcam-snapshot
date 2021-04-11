from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
import PIL.Image
import PIL.ImageTk
import time
import os


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
        self.btn_snapshot.grid(column=1, row=0, padx=20, pady=10)

        # Close Button
        self.btn_close = ttk.Button(self.btn_frame, text='Close')
        self.btn_close.configure(width=15, command=self.close_button)
        self.btn_close.grid(column=2, row=0, padx=10, pady=10)

        # file search bar

        # File name Label
        self.s = StringVar()
        self.s.set('File Name：')
        label1 = ttk.Label(self.btn_frame, textvariable=self.s)
        label1.grid(row=0, column=4)

        # file name search bar
        self.file_path = StringVar()
        filepath_entry = ttk.Entry(self.btn_frame, textvariable=self.file_path,
                                   width=50)
        filepath_entry.grid(row=0, column=5)

        # search button
        refer_button = ttk.Button(self.btn_frame, text='Search',
                                  command=self.click_refer_button)
        refer_button.grid(row=0, column=6)

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
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

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

    # finding the file path
    def click_refer_button(self):
        fTyp = [("", "*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        self.file_path.set(filepath)


def main():
    root = tk.Tk()
    app = Application(master=root)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
