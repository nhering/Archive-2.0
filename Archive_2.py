# -*- coding: utf-8 -*-
#
# Python Ver:   3.6.0
#
# Author:       Nathan D. Hering
#
# Purpose:      Archive version 2.0 can copy files from one folder to another folder based on the criteria of when the
#               files were created or modified. It will overwrite files in the destination folder if they have the same
#               name.
#
# Tested OS:    This code was written and tested to work with Windows 10.


from tkinter import *
from tkinter import ttk
import Profiles
import Functions


Functions.create_db()

class Archive:
    def __init__(self, master, *args, **kwargs):
        master.wm_title("Archive")
        self.master = master
        #master.geometry('420x470+10+10')
        Functions.geo_center_screen(self, 420, 470)
        master.maxsize(420, 470);
        master.minsize(420, 470);

        # Menus---------------------------------------------------------------------------------------------------------
        menubar = Menu(master)

        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Profiles", command = lambda: Profiles.profile_window(self,master))
        filemenu.add_command(label = "Clear All", command = lambda: Functions.clear_all(self))
        filemenu.add_command(label = "Exit", command = master.quit)
        menubar.add_cascade(label = "File", menu = filemenu)

        helpmenu = Menu(menubar, tearoff = 0)
        helpmenu.add_command(label = "About", command=lambda: "")
        menubar.add_cascade(label = "Help", menu = helpmenu)

        master.config(menu=menubar)

        # Paths---------------------------------------------------------------------------------------------------------
        paths = ttk.Frame(master)
        paths.grid(padx=5, pady=5, sticky=W, row=1, column=0)

        self.src_btn = ttk.Button(paths, text="Source", command=lambda: Functions.select_src(self))
        self.src_btn.grid(pady=5, row=0, column=0)
        self.src_label = ttk.Label(paths, text=Functions.srcdir, justify=LEFT, width=64)
        self.src_label.grid(padx=5, pady=5, sticky=SW, row=0, column=1, columnspan=2)

        self.dst_btn = ttk.Button(paths, text="Destination", command=lambda: Functions.select_dst(self))
        self.dst_label = ttk.Label(paths, justify=LEFT, width=64, text=Functions.dstdir)
        self.dst_btn.grid(pady=5, row=1, column=0)
        self.dst_label.grid(padx=5, pady=5, sticky=SW, row=1, column=1, columnspan=2)

        # Options-------------------------------------------------------------------------------------------------------
        options = ttk.Frame(master)
        options.grid(padx=5, pady=5, sticky=W, row=2, column=0)

        self.options_text = ttk.Label(options, text= "Select archive option.")
        self.options_text.grid(pady=5, sticky=W, row=0, column=0, columnspan=3)

        self.mod_create_opt0 = ttk.Radiobutton(options, text = "", variable = Functions.mod_or_create, value = 0,)

        self.mod_create_opt1 = ttk.Radiobutton(options,
                                               text = "MODIFIED since last archive performed.",
                                               variable = Functions.mod_or_create, value = 1,
                                               command = lambda: Functions.options_set(self, option = "m"))
        self.mod_create_opt1.grid(padx = 2, sticky = W, row = 1, column = 0)

        self.mod_create_opt2 = ttk.Radiobutton(options,
                                               text="CREATED  since last archive performed.",
                                               variable = Functions.mod_or_create, value = 2,
                                               command = lambda: Functions.options_set(self, option = "c"))
        self.mod_create_opt2.grid(padx = 2, sticky = W, row = 2, column = 0)

        # File info-----------------------------------------------------------------------------------------------------
        feedback = ttk.Frame(master)
        feedback.grid(padx = 5, row = 3, column = 0, sticky = W)

        ttk.Label(feedback, text="The following files will be copied").grid(row=0, column=0, sticky=W, pady=5)

        self.display_files = Text\
            (feedback, width=50, height=10, state='disabled')
        self.display_files.grid(pady=5, row=1, column=0, sticky=W)

        self.archive_btn = ttk.Button\
            (feedback, text="Archive Now", state=DISABLED, command=lambda: Functions.archive(self))
        self.archive_btn.grid(pady=5, row=2, column=0, sticky=W)

        # Misc. info----------------------------------------------------------------------------------------------------
        misc_info = ttk.Frame(master)
        misc_info.grid(padx = 5, row = 4, column = 0, sticky  = W)

        self.info_1 = ttk.Label(misc_info,)
        self.info_1.grid(pady = (3,0), row = 0, column = 0, sticky = S+W)

        self.info_2 = ttk.Label(misc_info)
        self.info_2.grid(row = 1, column = 0, sticky = S+W)

        self.info_3 = ttk.Label(misc_info)
        self.info_3.grid(row = 2, column = 0, sticky = S+W)

        self.info_4 = ttk.Label(misc_info)
        self.info_4.grid(row = 3, column = 0, sticky = S+W)

        Functions.refresh(self)

def main():
    root = Tk()
    root.iconbitmap('archive.ico')
    app = Archive(root)
    root.mainloop()



if __name__ == "__main__":
    main()
