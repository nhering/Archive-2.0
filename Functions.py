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
# ----------------------------------------------------------------------------------------------------------------------

archive_time = time.time() - 86400
srcdir = ""
dstdir = ""
criteria = ""
archive_list = []
mod_or_create = 0
current_profile = "Default"
profile_selection = ""

# Used to enable/disable the archive button.
# Indexes signify: (valid source path), (valid destination path), and (option is selected) respectively
can_archive = [FALSE,FALSE,FALSE]



# Main interface--------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Keeps the interface updated.
def refresh(self):
    validate_src_path(self)
    validate_dst_path(self)
    paths_not_equal(self)
    populate_list_archive(self)
    update_archive_button(self)
    update_info(self)

# Keeps database synced with current selections
def update_database(self):
    c = sqlite3.connect('db_archive.db')
    with c:
        cur = c.cursor()
        cur.execute("""UPDATE tbl_profile
                    SET col_archive_time = ?,
                        col_srcdir = ?,
                        col_dstdir = ?,
                        col_criteria = ?,
                        col_mod_or_create = ?
                    WHERE col_profile = ?""",
                    (Functions.archive_time,
                     Functions.srcdir,
                     Functions.dstdir,
                     Functions.criteria,
                     Functions.mod_or_create,
                     Functions.profile_selection))
        c.commit()
    cur.close()

# Only used when loading a profile
def update_option(self):
    if Functions.mod_or_create == 0:
        self.mod_create_opt0.invoke()
    elif Functions.mod_or_create == 1:
        self.mod_create_opt1.invoke()
    else:
        self.mod_create_opt2.invoke()

# Called by refresh
# Enables/Disables the archive button according to required parameters being set
def update_archive_button(self):
    if FALSE not in can_archive:
        self.archive_btn.config(state = NORMAL)
    else:
        self.archive_btn.config(state = DISABLED)

def update_info(self):
    self.info_1.config(text = "Current profile: " + Functions.current_profile)
    last_archive = time.strftime("%I:%M %p - %A %B,%d %Y",time.localtime(Functions.archive_time))
    self.info_2.config(text = "Last archive performed: " + str(last_archive))

# Called by src_btn: prompts for source folder
def select_src(self):
    Functions.srcdir = filedialog.askdirectory(initialdir="/", title="Select source directory.")
    refresh(self)
    update_database(self)

# Called by dst_btn: prompts for destination folder
def select_dst(self):
    Functions.dstdir = filedialog.askdirectory(initialdir="/", title="Select destination directory.")
    refresh(self)
    update_database(self)

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

# Called by option buttons
def options_set(self, option):
    Functions.criteria = option
    populate_list_archive(self)
    can_archive[2] = TRUE
    #set Functions.mod_or_create = (value of the selected option)
    refresh(self)
    update_database(self)

# Called by options_set
def populate_list_archive(self):
    if can_archive[0]:
        Functions.archive_list = []
        files_in_folder = listdir(Functions.srcdir)
        self.display_files.config(state='normal')
        self.display_files.delete('1.0', 'end')
        self.display_files.config(state='disabled')
        def display_file(i):
            self.display_files.config(state='normal')
            self.display_files.insert('1.0', i + '\n')
            self.display_files.config(state='disabled')
        if Functions.criteria == 'm':
            Functions.mod_or_create = 1
            for i in files_in_folder:
                file_time = os.path.getmtime(srcdir + "\\" + i)
                if file_time > archive_time:
                    Functions.archive_list.append(i)
                    display_file(i)
        elif Functions.criteria == 'c':
            Functions.mod_or_create = 2
            for i in files_in_folder:
                file_time = os.path.getctime(srcdir + "\\" + i)
                if file_time > archive_time:
                    Functions.archive_list.append(i)
                    display_file(i)
    else:
        self.display_files.config(state='normal')
        self.display_files.delete('1.0', 'end')
        self.display_files.config(state='disabled')

# Called by archive button
def archive(self):
    for i in Functions.archive_list:
        print(i + " copied")
        shutil.copyfile((srcdir + "\\" + i), (dstdir + "\\" + i))
    populate_list_archive(self)
    Functions.archive_time = time.time()
    update_database(self)
    update_info(self)

# Called by menu item 'clear all'
def clear_all(self):
    Functions.srcdir = ""
    Functions.dstdir = ""
    Functions.criteria = ""
    Functions.archive_list = []
    Functions.mod_or_create = 0
    self.mod_create_opt0.invoke()
    self.display_files.config(state='normal')
    self.display_files.delete('1.0', 'end')
    self.display_files.config(state='disabled')
    Functions.can_archive = [FALSE, FALSE, FALSE]
    Functions.archive_time = time.time() - 86400
    refresh(self)



# Database--------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

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
                         VALUES (?,?,?,?,?,?)""",(d,Functions.archive_time,"","","",0))
    cur.close()



# Profile manager-------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Called when profile manager is opened
def populate_list_profiles(self):
    self.list_profiles.delete(0, END)
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
                self.list_profiles.insert(0,str(item))
                i = i + 1
    c.close()

# Called any time an item in the profile list is selected
def selected_profile(self,event):
    var_list = event.widget
    select = var_list.curselection()[0]
    Functions.profile_selection = var_list.get(select)
    self.select_profile.config(state = NORMAL)
    if Functions.profile_selection == "Default":
        self.delete_profile.config(state = DISABLED)
    else:
        self.delete_profile.config(state = NORMAL)


def create_profile(self):
    new_profile = self.create_profile_entry.get()
    new_profile = new_profile.strip()
    c = sqlite3.connect('db_archive.db')
    with c:
        cur = c.cursor()
        cur.execute("""SELECT COUNT (col_profile) FROM tbl_profile WHERE col_profile = '{}'""".format(new_profile,))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute("""INSERT INTO tbl_profile \
                        (col_profile, col_archive_time, col_srcdir, col_dstdir, col_criteria, col_mod_or_create) \
                         VALUES (?,?,?,?,?,?)""",(new_profile,Functions.archive_time,"","","",0))
            c.commit()
            c.close()
            Functions.current_profile = new_profile
            self.top.destroy()
            Functions.refresh(self)
        else:
            c.close()
            messagebox.showerror("Archive: Duplicate Profile",
                                "Profile already exists.\nThis will not do.",
                                 parent = self.top)
            self.create_profile_entry.delete(0,END)
            self.create_profile_entry.config(state = ACTIVE)

# Called by select profile
def use_selected_profile(self):
    c = sqlite3.connect("db_archive.db")
    with c:
        cursor = c.cursor()
        cursor.execute("""SELECT * FROM tbl_profile WHERE col_profile = '{}'""".format(Functions.profile_selection))
        record = cursor.fetchall()
        for i in record:
            print(i)
            Functions.current_profile = i[1]
            Functions.archive_time = i[2]
            if i[3] == "":
                Functions.srcdir = ""
            else:
                Functions.srcdir = i[3]
            if i[4] == "":
                Functions.dstdir = ""
            else:
                Functions.dstdir = i[4]
            Functions.criteria = i[5]
            Functions.mod_or_create = i[6]
    c.close()
    self.top.destroy()
    Functions.update_option(self)
    refresh(self)

# Called by delete profile
def delete_selected_profile(self):
    confirm = messagebox.askokcancel\
        ("Archive: Confirm delete.",
         "Profile: '" + Functions.profile_selection + "' will be deleted.\nAnd all that that implies...",
         parent = self.top, icon = WARNING)
    if confirm:
        c = sqlite3.connect("db_archive.db")
        with c:
            cursor = c.cursor()
            cursor.execute("""DELETE FROM tbl_profile WHERE col_profile = '{}'""".format(Functions.profile_selection))
            c.close
        Functions.populate_list_profiles(self)
    else:
        pass