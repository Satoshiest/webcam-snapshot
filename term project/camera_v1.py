import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk
import time


class Application(tk.Frame):
    def __init__(self, master, video_source=0):
        super().__init__(master)

        self.master.title("Term project")

        self.video_cap = cv2.VideoCapture(video_source)
        self.width = self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------

        # camera frame
        self.cam_frame = tk.LabelFrame(self.master, text='Camera')
        self.cam_frame.pack(side=tk.BOTTOM)
        self.cam_frame.configure(width=self.width + 30, height=self.height + 50)
        self.cam_frame.grid_propagate(0)

        # Canvas
        self.canvas1 = tk.Canvas(self.cam_frame)
        self.canvas1.configure(width=self.width, height=self.height)
        self.canvas1.grid(column=0, row=0, padx=10, pady=10)

        # button frame
        self.btn_frame = tk.LabelFrame(self.master, text='Control')
        self.btn_frame.pack(side=tk.BOTTOM)
        self.btn_frame.configure(width=self.width + 30, height=120)
        self.btn_frame.grid_propagate(0)

        # Snapshot Button
        self.btn_snapshot = tk.Button(self.btn_frame, text='Snapshot')
        self.btn_snapshot.configure(width=15, height=1, command=self.snapshot)
        self.btn_snapshot.grid(column=0, row=0, padx=30, pady=10)

        # Close
        self.btn_close = tk.Button(self.btn_frame, text='Close')
        self.btn_close.configure(width=15, height=1, command=self.close_button)
        self.btn_close.grid(column=1, row=0, padx=20, pady=10)

        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------
        self.photo = None
        self.lag = 15
        self.update()

    def update(self):
        # Get a frame from the video source
        _, frame = self.video_cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

        # self.photo -> Canvas
        self.canvas1.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.master.after(self.lag, self.update)

    def snapshot(self):
        # Get a frame from the video source
        _, frame = self.video_cap.read()
        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite("IMG-" + time.strftime("%Y-%d-%m-%H-%M-%S")+".jpg",
                    cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

    def record(self):
        # Todo
        # to be implemented
        pass

    def close_button(self):
        self.quit()


def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = Application(master=root)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
