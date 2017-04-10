import Functions
from tkinter import *


def about_window(self):
    self.about = Toplevel()
    self.about.title("About Archive")
    self.about.iconbitmap('archive.ico')
    geo = Functions.geo_center_screen(self, 800, 500)
    self.about.geometry(geo)
    self.about.focus_set()

    self.about_bg = PhotoImage(file = 'AboutBG.gif')
    text = "Archive 2.0\n\n" \
           "Author: Nathan Hering\n\n" \
           "copyright 2017"

    about_canvas = Canvas(self.about, width = 800,  height = 500)
    about_canvas.grid(padx = 0, sticky = N+E+S+W)

    about_canvas.create_image(0, 0, anchor = NW, image = self.about_bg)
    about_canvas.create_text(100, 360, font=('console', 15), anchor = NW,  text = text)



if __name__ == "__main__":
    pass