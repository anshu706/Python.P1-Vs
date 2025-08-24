from tkinter import *
from PIL import Image, ImageTk  # pip install pillow


class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")


if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()
