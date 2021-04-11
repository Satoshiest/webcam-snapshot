import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk
import time


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
        self.is_recording = True

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

        # Record Button
        self.btn_snapshot = tk.Button(self.btn_frame, text='Record')
        self.btn_snapshot.configure(width=15, height=1, command=self.record)
        self.btn_snapshot.grid(column=1, row=0, padx=20, pady=10)

        # Close Button
        self.btn_close = tk.Button(self.btn_frame, text='Close')
        self.btn_close.configure(width=15, height=1, command=self.close_button)
        self.btn_close.grid(column=2, row=0, padx=10, pady=10)

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
        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite("IMG-" + time.strftime("%Y-%d-%m-%H-%M-%S")+".jpg",
                    cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

    def record(self):
        video = cv2.VideoWriter(f'{time.strftime("%Y-%d-%m-%H-%M-%S")}.mp4',
                                self.fourcc, self.fps,
                                (self.width, self.height))
        while True:
            _, frame = self.camera.read()
            cv2.imshow('Now recording', frame)
            video.write(frame)
            # enter q to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def close_button(self):
        self.quit()


def main():
    root = tk.Tk()
    app = Application(master=root)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
