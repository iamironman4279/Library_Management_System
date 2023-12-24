from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os
import sys
py = sys.executable
class issue(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.title('Library Administration')
        self.maxsize(500, 500)
        self.minsize(500, 500)
        c = StringVar()
        d = StringVar()

        def isb():
            if len(c.get()) == 0 or len(d.get()) == 0:
                messagebox.showinfo("Error", "Please Enter The Id's")
            else:
                try:
                    self.conn = sqlite3.connect('library_administration.db')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select Availiability from books where Book_Id = ?", [c.get()])
                    temp = self.mycursor.fetchone()
                    if str(temp[0]) == '0':
                        messagebox.showinfo("Oops", "Book Already Issued")
                    else:
                        self.mycursor.execute("Select Fine from students where Student_Id = ?", [d.get()])
                        fine = list(self.mycursor.fetchone())
                        
                        # Fetch the current count of books issued by the student
                        self.mycursor.execute("Select Books_Issued from students where Student_Id = ?", [d.get()])
                        current_books_issued = self.mycursor.fetchone()

                        if current_books_issued:
                            current_count = current_books_issued[0]
                            
                            if current_count < 2:
                                if fine[0] > 100:
                                    messagebox.showerror('Oops', 'Cannot Issue. Please Pay the Fine')
                                elif fine[0] == 0:
                                    self.mycursor.execute("INSERT INTO issue VALUES (?,?,date('now'),date('now','+15 days'))", [c.get(), d.get()])
                                    self.mycursor.execute("UPDATE books set Availiability=0 where Book_Id = ?", [c.get()])
                                    updated_count = current_count + 1  # Increment by 1 for the book just issued
                                    self.mycursor.execute("UPDATE students set Books_Issued = ? where Student_Id = ?", [updated_count, d.get()])
                                    self.conn.commit()
                                    self.conn.close()
                                    messagebox.showinfo('Save', 'Successfully Issued')
                                    conf = messagebox.askyesno("Confirm", "Do you want to issue another book?")
                                    if conf:
                                        self.destroy()
                                        os.system('%s %s' % (py, 'issueTable.py'))
                                    else:
                                        self.destroy()
                                else:
                                    Confirm = messagebox.askyesno('Confirm', 'Are you sure you want to issue. There is a fine')
                                    if Confirm:
                                        self.mycursor.execute("INSERT INTO issue VALUES (?,?,date('now'),date('now','+15 days'))", [c.get(), d.get()])
                                        self.mycursor.execute("UPDATE books set Availiability=0 where Book_Id = ?", [c.get()])
                                        updated_count = current_count + 1  # Increment by 1 for the book just issued
                                        self.mycursor.execute("UPDATE students set Books_Issued = ? where Student_Id = ?", [updated_count, d.get()])
                                        self.conn.commit()
                                        self.conn.close()
                                        messagebox.showinfo('Save', 'Successfully Issued')
                                        conf = messagebox.askyesno("Confirm", "Do you want to issue another book?")
                                        if conf:
                                            self.destroy()
                                            os.system('%s %s' % (py, 'issueTable.py'))
                                        else:
                                            self.destroy()
                                    else:
                                        messagebox.showinfo('Oops', 'Not Issued')
                            else:
                                messagebox.showerror("Can't Issue", "Maximum number of books already issued")
                        else:
                            messagebox.showerror("Error", "Failed to fetch Books_Issued count for the student")
                except Error:
                    messagebox.showerror("Error", "Something Goes Wrong")
        Label(self, text='Book Issuing', font=('Arial Black', 35)).place(x=100, y=40)
        Label(self, text='Book ID  :', font=('Arial', 15), fg='red').place(x=60, y=153)
        Entry(self, textvariable=c, width=40).place(x=190, y=160)
        Label(self, text='Student ID  :', font=('Arial', 15), fg='red').place(x=60, y=193)
        Entry(self, textvariable=d, width=40).place(x=190, y=200)
        Button(self, text="ISSUE", width=30, command=isb).place(x=150, y=290)
issue().mainloop()
