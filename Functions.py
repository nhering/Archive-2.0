from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import shutil
import os
from os import listdir
import Profiles
import Functions
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time

# Variables-------------------------------------------------------------------------------------------------------------

archive_time = time.time() - 86400
srcdir = ""
dstdir = ""
criteria = ""
archive_list = []
mod_or_create = ""
current_profile = "Default"
profile_selection = ""

# Used to enable/disable the archive button.
# Indexes signify: (valid source path), (valid destination path), and (option is selected) respectively
can_archive = [FALSE,FALSE,FALSE]



# Database--------------------------------------------------------------------------------------------------------------

# --Creates database the first time the program is run.
# --Adds 'Default' profile.
def create_db():
    c = sqlite3.connect('db_archive.db')
    with c:
        cur = c.cursor()
        cur.execute("""CREATE TABLE if not exists tbl_profile( \
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    col_profile TEXT, \
                    col_archive_time INTEGER, \
                    col_srcdir TEXT, \
                    col_dstdir TEXT, \
                    col_criteria INTEGER, \
                    col_mod_or_create INTEGER \
                    );""")
        c.commit()
        d = "Default"
        cur.execute("""SELECT COUNT (col_profile) FROM tbl_profile WHERE col_profile = '{}'""".format(d))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute("""INSERT INTO tbl_profile \
                        (col_profile, col_archive_time, col_srcdir, col_dstdir, col_criteria, col_mod_or_create) \
                         VALUES (?,?,?,?,?,?)""",(d,"","","","",""))
    cur.close()



# Refresh---------------------------------------------------------------------------------------------------------------

# Keeps the interface updated and the database synced.
def refresh(self):
    validate_src_path(self)
    validate_dst_path(self)
    paths_not_equal(self)
    if FALSE not in can_archive:
        self.archive_btn.config(state = NORMAL)
    else:
        self.archive_btn.config(state = DISABLED)

def update_database(self):
    pass



# Main interface--------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Called by src_btn: prompts for source folder
def select_src(self):
    Functions.srcdir = filedialog.askdirectory(initialdir="/", title="Select source directory.")
    refresh(self)

# Called by dst_btn: prompts for destination folder
def select_dst(self):
    Functions.dstdir = filedialog.askdirectory(initialdir="/", title="Select destination directory.")
    refresh(self)

# Called by refresh
def validate_src_path(self):
    if Functions.srcdir != "" and os.path.exists(Functions.srcdir):
        can_archive[0] = TRUE
        self.src_label.config(text = Functions.srcdir)
    else:
        can_archive[0] = FALSE
        if Functions.srcdir == "":
            self.src_label.config(text = "Please select a source folder.")
        else:
            self.src_label.config(text = "Source path no longer valid.")
            Functions.srcdir = ""

# Called by refresh
def validate_dst_path(self):
    if Functions.dstdir != "" and os.path.exists(Functions.dstdir):
        can_archive[1] = TRUE
        self.dst_label.config(text=Functions.dstdir)
    else:
        can_archive[1] = FALSE
        if Functions.dstdir == "":
            self.dst_label.config(text="Please select a destination folder.")
        else:
            self.dst_label.config(text="Destination path no longer valid.")
            Functions.dstdir = ""

# Called by refresh
def paths_not_equal(self):
     if Functions.srcdir == "" or Functions.dstdir == "":
         pass
     elif can_archive[0] and can_archive[1] and Functions.srcdir != Functions.dstdir:
         pass
     else:
         messagebox.showwarning("Archive: Path error", "Source and Destination paths may not be the same.")
         can_archive[0] = FALSE
         can_archive[1] = FALSE




def options_set(self, option):
    Functions.criteria = option
    populate_list_archive(self)
    can_archive[2] = TRUE
    refresh(self)

def populate_list_archive(self):
    global criteria
    global archive_list
    archive_list = []
    files_in_folder = listdir(Functions.srcdir)
    self.display_files.config(state='normal')
    self.display_files.delete('1.0', 'end')
    self.display_files.config(state='disabled')

    def display_file(i):
        self.display_files.config(state='normal')
        self.display_files.insert('1.0', i + '\n')
        self.display_files.config(state='disabled')

    if criteria == 'm':
        for i in files_in_folder:
            file_time = os.path.getmtime(srcdir + "\\" + i)
            if file_time > archive_time:
                archive_list.append(i)
                display_file(i)
    elif criteria == 'c':
        for i in files_in_folder:
            file_time = os.path.getctime(srcdir + "\\" + i)
            if file_time > archive_time:
                archive_list.append(i)
                display_file(i)

def archive(self):
    global archive_list
    for i in archive_list:
        print(i + " copied")
        shutil.copyfile((srcdir + "\\" + i), (dstdir + "\\" + i))
    populate_list_archive(self)

def clear_all(self):
    Functions.srcdir = ""
    Functions.dstdir = ""
    Functions.criteria = ""
    Functions.archive_list = []
    Functions.mod_or_create = 0
    Functions.can_archive = [FALSE, FALSE, FALSE]
    refresh(self)

# Profile manager-------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
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

