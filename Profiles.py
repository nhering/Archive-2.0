import Functions
from tkinter import *
from tkinter import ttk


def profile_window(self,master):
    self.top = Toplevel()
    geo = Functions.geo_center_master(master, 330, 250)
    self.top.geometry(geo)
    self.top.grab_set()
    self.top.title("Profile Manager")
    self.top.iconbitmap('archive.ico')
    #self.top.minsize(330,250)
    #self.top.maxsize(330,250)

    # list of profiles--------------------------------------------------------------------------------------------------
    scroll = Scrollbar(self.top, orient = VERTICAL)
    self.list_profiles = Listbox(self.top, exportselection = 0, yscrollcommand = scroll.set)
    scroll.config(command = self.list_profiles.yview)
    scroll.grid(padx = (0,2), pady = (10,5), row = 2, column = 1, sticky = N+E+S+W)
    self.list_profiles.grid(padx = (5,0), pady = (10,5), row = 2, sticky = N+E+S+W)
    self.list_profiles.bind('<<ListboxSelect>>',lambda event: Functions.selected_profile(self,event))

    # buttons-----------------------------------------------------------------------------------------------------------
    btns = ttk.Frame(self.top)
    btns.grid(padx = 5, pady = 5, sticky = N+E+S+W)

    self.create_profile_btn = ttk.Button(btns, text = "Create New", command = lambda: Functions.create_profile(self))
    self.create_profile_btn.grid(row = 0, column = 0)
    self.create_profile_entry = ttk.Entry(btns, text="", width = 36)
    self.create_profile_entry.grid(row = 0, column = 1, padx = (6,0), columnspan = 3)

    self.select_profile = ttk.Button\
        (btns, text = "Use Selected", command = lambda: Functions.use_selected_profile(self), state = DISABLED)
    self.select_profile.grid(padx = (0,3), pady = 5, row = 1, column = 0, columnspan = 2, sticky = W+E)

    self.delete_profile = ttk.Button(btns, text = "Delete Selected", state = DISABLED, command = lambda: Functions.delete_selected_profile(self))
    self.delete_profile.grid(padx = (3,0), pady = 5, row = 1, column = 2, columnspan = 2, sticky = W+E)

    Functions.populate_list_profiles(self)

if __name__ == "__main__":
    pass