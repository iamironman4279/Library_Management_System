from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os
import sys
from tkinter import ttk
py=sys.executable

#creating window
class MainWin(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.configure(bg='light green')
        self.maxsize(1566, 1000)
        self.minsize(1566, 1000)
        self.state('zoomed')
        self.title('Library Administration')
        self.a = StringVar()
        self.b = StringVar()
        self.mymenu = Menu(self)
#calling scripts
        def a_s():
            os.system('%s %s' % (py, 'Add_Student.py'))

        def a_b():
            os.system('%s %s' % (py, 'Add_Books.py'))

        def r_b():
            os.system('%s %s' % (py, 'remove_book.py'))

        def r_s():
            os.system('%s %s' % (py, 'Remove_student.py'))

        def ib():
            os.system('%s %s' % (py, 'issueTable.py'))

        def rb1():
            os.system('%s %s' % (py, 'renew.py'))

        def ret():
            os.system('%s %s' % (py, 'ret.py'))

        def sea():
            os.system('%s %s' % (py,'Search.py'))

        # def handle(event):
        #     if self.listTree.identify_region(event.x,event.y) == "separator":
        #         return "break"
        def add_user():
            os.system('%s %s' % (py, 'Reg.py'))
        def rem_user():
            os.system('%s %s' % (py, 'Rem.py'))
        def cfine():
            os.system('%s %s' % (py,'fine.py'))
        def sest():
            os.system('%s %s' % (py,'Search_Student.py'))

#creating table

        self.listTree = ttk.Treeview(self,height=13,columns=('SID','Name','Fine','Book Name','Issue Date','Return Date'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.hsb = ttk.Scrollbar(self,orient="horizontal",command=self.listTree.xview)
        self.listTree.configure(yscrollcommand=self.vsb.set,xscrollcommand=self.hsb.set)
        self.listTree.heading("#0",text='Book ID',anchor = 'center')
        self.listTree.column("#0",width=100,minwidth=100,anchor='center')
        self.listTree.heading("#1", text='SID')
        self.listTree.column("#1",width=100,minwidth=100,anchor='center')
        self.listTree.heading("Name", text='Name')
        self.listTree.column("Name", width=150,minwidth=150,anchor='center')
        self.listTree.heading("Fine", text='Fine')
        self.listTree.column("Fine", width=100,minwidth=100,anchor='center')
        self.listTree.heading("Book Name", text='Book Name')
        self.listTree.column("Book Name", width=200, minwidth=200,anchor='center')
        self.listTree.heading("Return Date", text='Return Date')
        self.listTree.column("Return Date", width=125, minwidth=125,anchor='center')
        self.listTree.heading("Issue Date", text='Issue Date')
        self.listTree.column("Issue Date", width=125, minwidth=125,anchor='center')
        # self.listTree.bind('<Button-1>',handle) if you don't want to expand column activat this and the above handle function
        self.listTree.place(x=40,y=400)
        self.vsb.place(x=943,y=400,height=287)
        self.hsb.place(x=41,y=687,width=902)
        ttk.Style().configure("Treeview",font=('Times new Roman',15))

        list1 = Menu(self)
        list1.add_command(label="Student", command=a_s)
        list1.add_command(label="Book", command=a_b)

        list2 = Menu(self)
        list2.add_command(label="Student", command=r_s)
        list2.add_command(label="Book", command=r_b)

        list3 = Menu(self)
        list3.add_command(label = "Add User",command = add_user)
        list3.add_command(label = "Remove User",command = rem_user)
        list3.add_command(label = "Clear Fine",command = cfine)

        self.mymenu.add_cascade(label='Add', menu=list1)
        self.mymenu.add_cascade(label='Remove', menu=list2)
        self.mymenu.add_cascade(label = 'Admin Tools', menu = list3)

        self.config(menu=self.mymenu)

        def ser():
            try:
                self.conn = sqlite3.connect('library_administration.db')
                self.myCursor = self.conn.cursor()
        
        # Fetching the student ID from the Entry widget
                student_id = self.a.get()  
        
        # Query to fetch the required data
                self.myCursor.execute("""
            SELECT issue.BID, issue.SID, students.name,students.Fine, books.Book_name, issue.Issue_date, issue.Return_date 
            FROM issue 
            JOIN books ON issue.BID = books.Book_Id 
            JOIN students ON issue.SID = students.Student_Id 
            WHERE issue.SID = ?
        """, [student_id])
        
                results = self.myCursor.fetchall()
        
                if results:
            # Clear the treeview widget
                    self.listTree.delete(*self.listTree.get_children())
            
            # Insert fetched data into the treeview widget
                    for row in results:
                        self.listTree.insert("", 'end', text=row[0],values=(row[1], row[2], row[3], row[4], row[5], row[6]))
                else:
                    messagebox.showinfo("Information", "No books issued to this student ID.")
            
            except Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")



        def ent():
            try:
        # Establish database connection
                self.conn = sqlite3.connect('library_administration.db')
                self.myCursor = self.conn.cursor()

        # Fetching the Book ID from the Entry widget
                book_id = self.b.get()

        # Query to fetch the required data
                self.myCursor.execute("""
            SELECT issue.BID, issue.SID, students.name, students.Fine, books.Book_name, issue.Issue_date, issue.Return_date 
            FROM books 
            JOIN issue ON issue.BID = books.Book_Id 
            JOIN students ON issue.SID = students.Student_Id 
            WHERE issue.BID = ?
        """, [book_id])
        
                results = self.myCursor.fetchall()

                if results:
            # Clear the treeview widget
                    self.listTree.delete(*self.listTree.get_children())

            # Insert fetched data into the treeview widget
                    for row in results:
                        self.listTree.insert("", 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6]))
                else:
            # Display a message if no results are found
                    messagebox.showinfo("Information", "No information available for this book ID or the book is not issued.")
            
            except Error as e:
        # Display an error message if any exception occurs
                messagebox.showerror("Error", f"An error occurred: {e}")

        def check():
            try:
                conn = sqlite3.connect('library_administration.db')
                mycursor = conn.cursor()
                mycursor.execute("Select * from admin")
                z = mycursor.fetchone()
                if not z:
                    messagebox.showinfo("Error", "Please Register A user")
                    x = messagebox.askyesno("Confirm","Do you want to register a user")
                    if x:
                        self.destroy()
                        os.system('%s %s' % (py, 'Reg.py'))
                else:
                    #label and input box
                    self.label3 = Label(self, text='Welcome To  Library', bg='light green', font=('Arial', 45, 'bold'))
                    self.label3.place(x=290, y=80)
                    self.label4 = Label(self, text="Enter Student Id", bg='light green', font=('Arial', 20, 'bold'))
                    self.label4.place(x=100, y=200)
                    self.e1 = Entry(self, textvariable=self.a, width=40).place(x=400, y=210)
                    self.srt = Button(self, text='Search', width=15,bg='green', font=('arial', 10),command = ser).place(x=700, y=206)
                    self.label5 = Label(self, text='OR', bg='light green', font=('arial', 16, 'bold')).place(x=170, y=235)
                    self.label5 = Label(self, text="Enter Book Id", bg='light green', font=('Arial', 20, 'bold'))
                    self.label5.place(x=100, y=260)
                    self.e2 = Entry(self, textvariable=self.b, width=40).place(x=400, y=270)
                    self.brt = Button(self, text='Find',bg='green', width=15, font=('arial', 10),command = ent).place(x=700, y=266)
                    self.label6 = Label(self, text="Details", bg='light green', font=('Arial', 15, 'underline', 'bold'))
                    self.label6.place(x=20, y=350)
                    self.button = Button(self, text='Search Student', bg='green',width=20, font=('Arial', 20), command=sest).place(x=1000,y=250)
                    self.button = Button(self, text='Search Book', bg='green', width=20, font=('Arial', 20), command=sea).place(x=1000,y=350)
                    self.brt = Button(self, text="Issue Book", bg='green', width=20, font=('Arial', 20), command=ib).place(x=1000, y=450)
                    self.brt = Button(self, text="Renew Book", bg='green', width=20, font=('Arial', 20), command=rb1).place(x=1000, y=550)
                    self.brt = Button(self, text="Return Book", bg='green', width=20, font=('Arial', 20), command=ret).place(x=1000, y=650)
            except Error:
                messagebox.showerror("Error", "Something Goes Wrong")
        check()

MainWin().mainloop()