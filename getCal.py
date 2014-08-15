# getCal.py
__author__ = 'dalem'

# Dialog box for user to enter
#   Google account and password
#   Start date and time
#   End date and time
#   Search string, like DaleM includes "Bill" or "bill" on each event like:
#       "Bill Columbia ITs for Westar accounting report improvements"

# Keep these values for the next time this program is run.
# TODO; figure out a way to keep the Google account password secret.


# From: http://stackoverflow.com/questions/18636792/tkinter-get-data-from-a-entry-widget

from Tkinter import *
select = 1
height = 2
weight = 3

user_list = Tk()
user_list.title('Users')

def add_new_user():
    global select
    global height
    global weight
    select = name.get()
    height = h.get()
    weight = w.get()
    f = ' '
    us=open("userlist3.txt","a")
    print name, height, weight
    us.write(select + f + str(height) + f + str(weight) + "\n")
    us.close()
#    add_user.destroy() # it doesn't work
    user_list.destroy()

def onSelect(ev): # (10)
    global select
    select=listb.get(listb.curselection()) # (12)
    lab.configure(text=select) # (14)
    global name
    global h
    global w
    if select == '':
        add_user = Toplevel(user_list)
        #add_user = Tk()
        add_user.title('New user')
        a=Label(add_user,text="Your username").pack()
        name = StringVar()
        NAME = Entry(add_user,textvariable = name).pack()
        b=Label(add_user,text="Your height (in cm)").pack()
        h = IntVar()
        H = Entry(add_user,textvariable = h).pack()
        c=Label(add_user,text="Your weight (in kg)").pack()
        w = IntVar()
        W = Entry(add_user,textvariable = w).pack()
        Add_New_User=Button(add_user,text="Add new user data",command=add_new_user).pack()
        add_user.mainloop()
    else:
        user_list.destroy()

a=open("userlist3.txt","r")
b =[]
for linea in a:
    b.append(linea)
a.close()
e = []
for i in range(len(b)):
    e.append(b[i].split())
userlist = []
heightlist = []
weightlist = []
for i in range(len(e)):
    userlist.append(e[i][0])
    heightlist.append(e[i][1])
    weightlist.append(e[i][2])

sbar = Scrollbar(user_list, orient=VERTICAL) # (20)
listb = Listbox(user_list, width=30, height=4) # (22)
sbar.config(command=listb.yview) # (30)
listb.config(yscrollcommand=sbar.set) # (32)
sbar.pack(side=RIGHT, fill=Y) # (40)
listb.pack() # (42)
# TODO; Double Click on no users, empty userlist3.txt, gets "bad listbox index"
lab=Label(user_list,text="Double Click on User") # (50)
lab.pack()
for c in userlist: listb.insert(END,c)
listb.bind('<Double-1>',onSelect) # (70)
user_list.mainloop()

for d in range(0,len(userlist)):
    if userlist[d] == select:
        height = int(heightlist[d])
        weight = int(weightlist[d])

print "Selected user is: ",select
print height
print weight




# From: https://docs.python.org/3.5/library/tkinter.html
#import Tkinter as tk
##import tkinter as tk
#class Application(tk.Frame):
#    def __init__(self, master=None):
#        tk.Frame.__init__(self, master)
#        self.pack()
#        self.createWidgets()
#    def createWidgets(self):
#        self.hi_there = tk.Button(self)
#        self.hi_there["text"] = "Hello World\n(click me)"
#        self.hi_there["command"] = self.say_hi
#        self.hi_there.pack(side="top")
#       self.QUIT = tk.Button(self, text="QUIT", fg="red",
#                                            command=root.destroy)
#        self.QUIT.pack(side="bottom")
#    def say_hi(self):
#        print("hi there, everyone!")
#root = tk.Tk()
#app = Application(master=root)
#app.mainloop()




# From: http://stackoverflow.com/questions/19719577/add-tkinters-intvar-to-an-integer
# TODO; <Return> or ENTER does nothing.
#from Tkinter import Entry, IntVar, Tk
#root = Tk()
#data = IntVar()
#entry = Entry(textvariable=data)
#entry.grid()
#def click(event):
#    # Get the number, add 1 to it, and then print it
#    print data.get() + 1
# Bind the entrybox to the Return key
#entry.bind("<Return>", click)
#root.mainloop()