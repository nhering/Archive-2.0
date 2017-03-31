from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import shutil
import os
from os import listdir
import time

archive_time = time.time() - 86400
instructions = "Step 1: Select the source directory\nStep 2: Select the destination directory\nStep 3: Select desired option for archiving\nStep 4: Press the 'Archive Now' button to perfom the archive"
srcdir = "Please select a source folder."
dstdir = ""
criteria = ""
archive_list = []
show_instruct=1


class Archive:
    def __init__(self, master):
        master.wm_title("Archive")

        # Menus---------------------------------------------------------------------------------------------------------
        menubar = Menu(master)

        def ins_menu():
            if show_instruct == 1:
                helpmenu.entryconfig(0, label = "Hide Instructions")
            else:
                helpmenu.entryconfig(0, label = "Show Instructions")

        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Clear All", command = lambda: clear_all(self))
        filemenu.add_command(label = "Exit", command = master.quit)
        menubar.add_cascade(label = "File", menu = filemenu)

        helpmenu = Menu(menubar, tearoff = 0, postcommand = ins_menu)
        helpmenu.add_command(label = "Hide Instructions", command=lambda: show_hide_instruct(self))
        helpmenu.add_command(label = "About", command=lambda: "")
        menubar.add_cascade(label = "Help", menu = helpmenu)

        master.config(menu=menubar)

        def clear_all(self):
            global srcdir, dstdir, criteria, archive_list
            srcdir = "Please select a source folder."
            dstdir = ""
            criteria = ""
            archive_list = []
            self.display_files.config(state='normal')
            self.display_files.delete('1.0', 'end')
            self.display_files.config(state='disabled')
            self.src_label.config(text=srcdir)
            self.dst_label.config(text=dstdir)
            feedback.grid_forget()
            options.grid_forget()
            self.dst_btn.grid_forget()
            self.dst_label.grid_forget()
            self.archive_btn.config(state=DISABLED)


        def show_hide_instruct(self):
            global show_instruct
            show_instruct = show_instruct * -1
            if show_instruct == 1:
                ins.grid(sticky=W, row=0, column=0)
            else:
                ins.grid_forget()


        # Instructions--------------------------------------------------------------------------------------------------
        ins = ttk.Frame(master)
        if show_instruct == 1:
            ins.grid(sticky=W, row=0, column=0)
        else:
            ins.grid_forget()

        self.instruct = ttk.Label(ins, text=instructions, justify=LEFT, width=65)
        self.instruct.grid(padx=5, pady=5, sticky=W, row=0, column=0)

        # Paths---------------------------------------------------------------------------------------------------------
        paths = ttk.Frame(master)
        paths.grid(padx=5, pady=5, sticky=W, row=1, column=0)

        self.src_btn = ttk.Button(paths, text="Source", command=lambda: select_src(self))
        self.src_btn.grid(pady=5, row=0, column=0)
        self.src_label = ttk.Label(paths, text=srcdir, justify=LEFT, width=64)
        self.src_label.grid(padx=5, pady=5, sticky=SW, row=0, column=1, columnspan=2)

        self.dst_btn = ttk.Button(paths, text="Destination", command=lambda: select_dst(self))
        self.dst_label = ttk.Label(paths, justify=LEFT, width=64, text=dstdir)

        def select_src(self):
            global srcdir
            srcdir = filedialog.askdirectory(initialdir="/", title="Select source directory.")
            self.src_label.config(text=srcdir)
            validate_paths(self)

        def select_dst(self):
            global dstdir
            dstdir = filedialog.askdirectory(initialdir="/", title="Select destination directory.")
            self.dst_label.config(text=dstdir)
            validate_paths(self)

        def validate_paths(self):
            if srcdir == "":
                self.archive_btn.config(state=DISABLED)
                self.display_files.config(state='normal')
                self.display_files.delete('1.0', 'end')
                self.display_files.config(state='disabled')
                if dstdir == "":
                    self.src_label.config(text="Please select a source folder.")
                    self.dst_label.config(text="")
                else:
                    self.src_label.config(text="Please select a source folder.")
            else:
                self.dst_btn.grid(pady=5, row=1, column=0)
                self.dst_label.grid(padx=5, pady=5, sticky=SW, row=1, column=1, columnspan=2)
                populate_list(self)
                if dstdir == "":
                    self.archive_btn.config(state=DISABLED)
                    self.dst_label.config(text="Please select a destination folder.")
                elif srcdir == dstdir:
                    self.archive_btn.config(state=DISABLED)
                    messagebox.showinfo("Archive: Path error",
                                        "You may not select the same folder for both the source and destination.")
                else:
                    options.grid(padx=5, pady=5, sticky=W, row=2, column=0)
                    self.archive_btn.config(state=ACTIVE)

        # Options-------------------------------------------------------------------------------------------------------
        options = ttk.Frame(master)

        def test():

        mod_or_create = ""

        self.options_text = ttk.Label(options, text="Select archive option.")
        self.options_text.grid(pady=5, sticky=W, row=0, column=0, columnspan=3)

        self.mod_create_opt1 = ttk.Radiobutton(options,
                                               text="Files that have been MODIFIED in the past 24 hours.",
                                               variable=mod_or_create, value=1,
                                               command=lambda: options_set(self, option="m"))
        self.mod_create_opt1.grid(padx=2, sticky=W, row=1, column=0)

        self.mod_create_opt2 = ttk.Radiobutton(options,
                                               text="Files that have been CREATED in the past 24 hours.",
                                               variable=mod_or_create, value=2,
                                               command=lambda: options_set(self, option="c"))
        self.mod_create_opt2.grid(padx=2, sticky=W, row=2, column=0)

        def options_set(self, option):
            global criteria
            criteria = option
            feedback.grid(padx=5, row=3, column=0, sticky=W)
            populate_list(self)

        # Feedback------------------------------------------------------------------------------------------------------
        feedback = ttk.Frame(master)

        ttk.Label(feedback, text="The following files will be copied").grid(row=0, column=1, sticky=W, pady=5)

        self.display_files = Text(feedback, width=50, height=10, state='disabled')
        self.display_files.grid(pady=5, row=1, column=1, sticky=W)

        self.archive_btn = ttk.Button(feedback, text="Archive Now", state=DISABLED, command=lambda: archive(self))
        self.archive_btn.grid(pady=5, row=2, column=1, sticky=W)

        def archive(self):
            global archive_list
            for i in archive_list:
                print(i + " copied")
                shutil.copyfile((srcdir + "\\" + i), (dstdir + "\\" + i))
            populate_list(self)

        def populate_list(self):
            global criteria
            global archive_list
            archive_list = []
            files_in_folder = listdir(srcdir)
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


def main():
    root = Tk()
    root.iconbitmap('archive.ico')
    app = Archive(root)
    root.mainloop()


if __name__ == "__main__":
    main()
