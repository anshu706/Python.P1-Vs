from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk


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
        self.var_search = StringVar()
        lbl_search_courseName = Label(self.root, text="Course Name", font=(
            "goudy old style", 15, 'bold'), bg='white').place(x=720, y=60)
        txt_search_courseName = Entry(self.root, textvariable=self.var_search, font=(
            "goudy old style", 15, 'bold'), bg='white').place(x=870, y=60, width=180)
        btn_search = Button(self.root, text='Search', font=(
            "goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2").place(x=1070, y=60, width=120, height=28)

        # === Content ===
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(self.C_Frame, columns=(
            "C-Id", "Name", "Duration", "Charges", "Description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fil=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("C-Id", text="Course Id")
        self.CourseTable.heading("Name", text="Name")
        self.CourseTable.heading("Duration", text="Duration")
        self.CourseTable.heading("Charges", text="Charges")
        self.CourseTable.heading("Description", text="Description")

        self.CourseTable['show'] = 'headings'

        self.CourseTable.column("C-Id", width=100)
        self.CourseTable.column("Name", width=100)
        self.CourseTable.column("Duration", width=100)
        self.CourseTable.column("Charges", width=100)
        self.CourseTable.column("Description", width=150)

        self.CourseTable.pack(fill=BOTH, expand=1)


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
