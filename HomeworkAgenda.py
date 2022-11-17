from tkinter import *
from tkinter.scrolledtext import ScrolledText
import os
a = lambda i: i[:i.find('.txt')]
path = "D:/Homework/ComputerSecurity/"
path1 = "D:/Homework/Database/"
for root, dir_ls, files in os.walk(path):
    files = files
files = sorted(files)
word_sup_ls = list(map(a, files))
for root1, dir_ls1, file1 in os.walk(path1):
    files1 = file1
files1 = sorted(files1)
word_sup_ls1 = list(map(a, files1))


class HomeworkAgenda:
    def __init__(self, master):
        self.wndw = master
        container = Frame(self.wndw)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for i in (StartPage, Database, ComputerSecurity):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        for i, y in zip(files, word_sup_ls):
            frame = TextPage(container, self, i, y, path)
            self.frames[path+y] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        for i, y in zip(files1, word_sup_ls1):
            frame = TextPage(container, self, i, y, path1)
            self.frames[path1+y] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, slave, master):
        Frame.__init__(self, slave)
        label = Label(self, text="Start page")
        label.grid(row=0, column=4)
        Button(self, text='Database', command=lambda: master.show_frame(Database)).grid()
        Button(self, text='Computer Security', command=lambda: master.show_frame(ComputerSecurity)).grid()


class Database(Frame):
    def __init__(self, slave, master):
        Frame.__init__(self, slave)
        Label(self, text='Database Homework').grid(row=0, column=4)
        for i, y in zip(files, word_sup_ls):
            Button(self, text=y, command=lambda word=os.path.join(path, y): master.show_frame(word)).grid()
        Button(self, text='Start Page', command=lambda: master.show_frame(StartPage)).grid()


class ComputerSecurity(Frame):
    def __init__(self, slave, master):
        Frame.__init__(self, slave)
        Label(self, text='Computer Security',).grid(row=0, column=4)
        for i, y in zip(files, word_sup_ls1):
            Button(self, text=y, command=lambda word=os.path.join(path1, y): master.show_frame(word)).grid()
        Button(self, text='Start Page', command=lambda: master.show_frame(StartPage)).grid()


class TextPage(Frame):
    def __init__(self, slave, master, obj, name, route):
        Frame.__init__(self, slave)
        Label(self, text=name).grid(row=0, column=4)
        love_handle = open(route+obj, 'r')
        hw_assign = ScrolledText(self)
        hw_assign.insert('1.0', love_handle.read())
        hw_assign.grid()
        Button(self, text='Database HomePage', command=lambda: master.show_frame(Database)).grid()
        Button(self, text='Computer Security Homepage', command=lambda: master.show_frame(ComputerSecurity)).grid()


root = Tk()
root.geometry('500x500')
app = HomeworkAgenda(root)
mainloop()
