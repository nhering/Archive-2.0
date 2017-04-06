from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import Functions
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import shutil
import os
from os import listdir

def profile_window(self):
    top = Toplevel()
    top.title("Profile Manager")
    top.iconbitmap('archive.ico')
    top.minsize(330,0)

    ttk.Label(top, text = "From this window you can create, select, or delete profiles")\
        .grid(pady = 5, padx = 5, row = 0, column = 0)

    scroll = Scrollbar(top, orient = VERTICAL)
    list = Listbox(top, exportselection = 0, yscrollcommand = scroll.set)
    scroll.config(command = list.yview)
    scroll.grid(padx = (0,2), pady = (0,5), row = 2, column = 1, sticky = N+E+S+W)
    list.grid(padx = (5,0), pady = (0,5), row = 2, sticky = N+E+S+W)
    list.bind('<<ListboxSelect>>',lambda event: selected_profile(self,event))

    btns = ttk.Frame(top)
    btns.grid(padx = 5, pady = 5, sticky = N+E+S+W)

    create_profile_btn = ttk.Button(btns, text = "Create New", command = lambda: create_profile(self))
    create_profile_btn.grid(row = 0, column = 0)
    create_profile_entry = ttk.Entry(btns, text="", width = 36)
    create_profile_entry.grid(row = 0, column = 1, padx = (6,0), columnspan = 3)

    select_profile = ttk.Button(btns, text = "Use Selected", state = DISABLED)
    select_profile.grid(padx = (0,3), pady = 5, row = 1, column = 0, columnspan = 2, sticky = W+E)

    delete_profile = ttk.Button(btns, text = "Delete Selected", state = DISABLED)
    delete_profile.grid(padx = (3,0), pady = 5, row = 1, column = 2, columnspan = 2, sticky = W+E)

    def populate_list_profiles(self):
        list.delete(0, END)
        c = sqlite3.connect("db_archive.db")
        with c:
            cur = c.cursor()
            cur.execute("""SELECT COUNT(*) FROM tbl_profile""")
            count = cur.fetchone()[0]
            i = 0
            while i < count:
                cur.execute("""SELECT col_profile FROM tbl_profile""")
                var_list = cur.fetchall()[i]
                for item in var_list:
                    list.insert(0,str(item))
                    i = i + 1
        c.close()

    populate_list_profiles(self)

    def selected_profile(self):
        select_profile.config(state = NORMAL)
        delete_profile.config(state = NORMAL)

    def selected_profile(self,event):
        global profile_selection
        varList = event.widget
        select = varList.curselection()[0]
        profile_selection = varList.get(select)

    def create_profile(self):
        global current_profile
        value = create_profile_entry.get()
        value = value.strip()
        print(value)
        c = sqlite3.connect('db_archive.db')
        with c:
            cur = c.cursor()
            cur.execute("""SELECT COUNT (col_profile) FROM tbl_profile WHERE col_profile = '{}'""".format(value,))
            count = cur.fetchone()[0]
            if count == 0:
                cur.execute("""INSERT INTO tbl_profile (col_profile) VALUES (?)""", (value,))
                current_profile = value
                top.destroy()
                refresh(self)
            else:
                messagebox.showerror("Archive: Duplicate Profile",
                                    "Profile already exists.\nThis will not do.")
        cur.close()



#    def select_profile(self):
        #Close window, update all appropriate fields and variables

#    def delete_profile(self):
        #confirm delete
        #delete from table

if __name__ == "__main__":
    pass