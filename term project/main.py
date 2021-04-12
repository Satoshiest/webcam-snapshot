import tkinter as tk
from camera import Application

# implemented by Satoshi Kameyama
# install opencv-python (cv2)
# install pillow (PIL)


def main():
    root = tk.Tk()
    app = Application(master=root)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
