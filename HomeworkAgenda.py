from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
import csv
import os

lst = []

class HomeworkAgenda:

    def __init__(self, root) -> None:
        self.wndw = root
        self.wndw.title("Homework Agenda")
        self.wndw.geometry('600x400')

        self.container = Frame(self.wndw)
        self.container.pack(fill=BOTH, expand=True)

        # Center the first label across multiple columns
        self.lb1 = Label(self.container, text="Welcome to your Homework Agenda!")
        self.lb1.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.lb2 = Label(self.container, text="Please select a subject: ")
        self.lb2.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.var = StringVar()
        self.subjectlabel = Combobox(self.container, textvariable=self.var, values=lst)
        self.subjectlabel.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.lb3 = Label(self.container, text="Set subjects: ")
        self.lb3.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.entry = Entry(self.container)
        self.entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.btn1 = Button(self.container, text="Update", command=self.func_update)
        self.btn1.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.lb4 = Label(self.container, text="Enter Assignment Name: ")
        self.lb4.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.entry1 = Entry(self.container)
        self.entry1.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.lb5 = Label(self.container, text="Enter Assignment Details: ")
        self.lb5.grid(row=4, column=0, padx=10, pady=10, sticky="ne")

        self.entry2 = Text(self.container, height=4, width=40)
        self.entry2.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.btn2 = Button(self.container, text="Write to CSV", command=self.write2csv)
        self.btn2.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.btn3 = Button(self.container, text="View Homework", command=self.view_homework)
        self.btn3.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        # Configure the rows and columns to expand properly
        for i in range(6):
            self.container.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.container.grid_columnconfigure(i, weight=1)

    def func_update(self) -> None:
        lst.append(self.entry.get())
        self.subjectlabel.configure(values=lst)

    def write2csv(self) -> None:
        subject = self.subjectlabel.get()
        aname = self.entry1.get()
        detail = self.entry2.get("1.0", END).strip()
        fname = "assignments.csv"
        with open(fname, "a", newline='') as fh:
            writer = csv.writer(fh)
            writer.writerow([subject, aname, detail])

    def view_homework(self):
        new_window = Toplevel(self.wndw)
        new_window.geometry('400x400')
        DisplayHomework(new_window)

class DisplayHomework(Frame):

    def __init__(self, slave) -> None:
        super().__init__(slave)
        self.pack(fill=BOTH, expand=True)

        # Treeview setup with a tree structure
        self.tree = Treeview(self, columns=("Assignment", "Detail"))
        self.tree.heading("#0", text="Subject")
        self.tree.heading("Assignment", text="Assignment")
        self.tree.heading("Detail", text="Detail")

        # Add a scrollbar
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Load data from CSV
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "assignments.csv")
        self.load_data_from_csv(filename)

    def load_data_from_csv(self, csv_filename):
        if not os.path.exists(csv_filename):
            print(f"File not found: {csv_filename}")
            return
        
        with open(csv_filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = {}

            for row in reader:
                if len(row) == 3:
                    tab, assignment, detail = row
                    if tab not in data:
                        data[tab] = []
                    data[tab].append((assignment, detail))

            # Insert data into Treeview
            for tab, items in data.items():
                parent = self.tree.insert("", "end", text=tab, values=(tab,))
                for assignment, detail in items:
                    self.tree.insert(parent, "end", values=(assignment, detail))


root = Tk()
root.geometry('600x400')
app = HomeworkAgenda(root)
root.mainloop()
