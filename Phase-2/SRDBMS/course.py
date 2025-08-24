from tkinter import *
from PIL import Image, ImageTk  # pip install pillow


class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        # == title ==
        title = Label(self.root, text="Manage Course Details ", font=(
            "goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # === Variables ===
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()

        # === Widgets ===
        lbl_course = Label(self.root, text="Course Name", font=(
            "goudy old style", 15, 'bold'), bg='white').place(x=10, y=60)
        lbl_duration = Label(self.root, text="Duration", font=(
            "goudy old style", 15, 'bold'), bg='white').place(x=10, y=100)
        lbl_charges = Label(self.root, text="Charges", font=(
            "goudy old style", 15, 'bold'), bg='white').place(x=10, y=140)
        lbl_description = Label(self.root, text="Description", font=(
            "goudy old style", 15, 'bold'), bg='white').place(x=10, y=180)

#  ==== Entry Fields ====
        self.txt_courseName = Entry(self.root, textvariable=self.var_course, font=(
            "goudy old style", 15, 'bold'), bg='white')
        self.txt_courseName.place(x=150, y=60, width=200)

        self.txt_duration = Entry(self.root, textvariable=self.var_duration, font=(
            "goudy old style", 15, 'bold'), bg='white')
        self.txt_duration.place(x=150, y=100, width=200)

        self.txt_charges = Entry(self.root, textvariable=self.var_charges, font=(
            "goudy old style", 15, 'bold'), bg='white')
        self.txt_charges.place(x=150, y=140, width=200)

        self.txt_description = Text(self.root, font=(
            "goudy old style", 15, 'bold'), bg='white')
        self.txt_description.place(x=150, y=180, width=500, height=130)

        # ==== Buttons ====
        self.btn_add = Button(self.root, text='Save', font=(
            "goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2")
        self.btn_add.place(x=150, y=400, width=110, height=40)

        self.btn_update = Button(self.root, text='Update', font=(
            "goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2")
        self.btn_update.place(x=270, y=400, width=110, height=40)

        self.btn_delete = Button(self.root, text='Delete', font=(
            "goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2")
        self.btn_delete.place(x=390, y=400, width=110, height=40)

        self.btn_clear = Button(self.root, text='Clear', font=(
            "goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2")
        self.btn_clear.place(x=510, y=400, width=110, height=40)

        # === Search Panel ===
        lbl_search_courseName = Label(self.root, text="Search By | Course Name", font=(
            "goudy old style", 15, 'bold'), bg='white').place(x=720, y=60)


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
