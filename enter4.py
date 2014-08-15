__author__ = 'dalem'
# From: http://stackoverflow.com/questions/10727131/tkinter-get-entry-content-with-get
# And especially from http://effbot.org/tkinterbook/entry.htm; some very cool stuff there.

import Tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text="Get", command=self.on_button)
        self.button.pack()
        self.entry.pack()

    def on_button(self):
        print self.entry.get()

    def callback(self):
        print self.entry.get()
        #print self.get()

app = SampleApp()
b3 = tk.Button(app, text='Quit', command=app.quit)
b3.pack(side=tk.LEFT, padx=5, pady=5)
b = tk.Button(app, text="get", width=10, command=app.callback)
b.pack()
app.mainloop()
