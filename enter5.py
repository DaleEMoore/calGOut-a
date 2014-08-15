__author__ = 'dalem'
# From:http://stackoverflow.com/questions/10727131/tkinter-get-entry-content-with-get

from Tkinter import *

master = Tk()
v = StringVar()
e = Entry(master, textvariable=v)
e.pack()

v.set("a default value")
s = v.get()
print s