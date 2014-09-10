# main.py
# Get user input and Google calendar events


import datetime
#import gdata
import google_calendar_fetcher
import sys, traceback
from tkinter import * # Python3
#from Tkinter import * # Python2

__author__ = 'DaleEMoore@gMail.Com'


def update_status(entries, status_description):
    entries['Status'].delete(0,END)
    entries['Status'].insert(0, status_description )
    print("Status: %s" % status_description)

def update_message(entries, message_description):
    entries['Message'].delete(0,END)
    entries['Message'].insert(0, message_description)
    print("Message: %s" % message_description)
#
#def monthly_payment(entries):
#    try:
#        # period rate:
#        r = (float(entries['Annual Rate'].get()) / 100) / 12
#        print("r", r)
#        # principal loan:
#        loan = float(entries['Loan Principle'].get())
#        n =  float(entries['Number of Payments'].get())
#        remaining_loan = float(entries['RemaininPycharmProjectsg Loan'].get())
#        q = (1 + r)** n
#        monthly = r * ( (q * loan - remaining_loan) / ( q - 1 ))
#        monthly = ("%8.2f" % monthly).strip()
#        entries['Monthly Payment'].delete(0,END)
#        entries['Monthly Payment'].insert(0, monthly )
#        print("Monthly Payment: %f" % monthly)
#    except:
#        exc_type, exc_value, exc_traceback = sys.exc_info()
#        update_message(entries, exc_traceback)

def PrintUserCalendars(calendar_client):
    feed = calendar_client.GetAllCalendarsFeed()
    print (feed.title.text)
    for i, a_calendar in enumerate(feed.entry):
        print ('\t%s. %s' % (i, a_calendar.title.text,))

def get_events(entries):
    update_status(ents, "Processing...")
    try:
        # get values from user
        account = entries['Google Account'].get()
        password = entries['Google Account Password'].get()
        #show_password = entries['Show Password'].get()
        d1 = entries['Start Date'].get()
        start_date = datetime.datetime.strptime(d1, '%Y-%m-%d')
        #start_date = datetime.datetime.strptime(d1, '%m/%d/%Y')
        d1 = entries['End Date'].get()
        end_date = datetime.datetime.strptime(d1, '%Y-%m-%d')
        #end_date = datetime.datetime.strptime(d1, '%m/%d/%Y')
        search_string = entries['Search String'].get()
        destination_file = entries['Destination File'].get()
        print (account, start_date, end_date, search_string, destination_file)
        #print (account, password, show_password, start_date, end_date, search_string, destination_file)
        # validate date fields since I don't have a date picker yet.
        # get events from Google
        token = google_calendar_fetcher.login(account,password)
        try:
            google_calendar_fetcher.get_calendars(token, start_date, end_date, search_string, destination_file)
            # filter events by Start Date, End Date and Search String.
            google_calendar_fetcher.printOut(destination_file)
            #google_calendar_fetcher.print_output()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            update_message(entries, exc_value)
            traceback.print_exc()

        #client = gdata.calendar.client.CalendarClient(source='yourCo-yourAppName-v1')
        #client.ClientLogin(account, password, client.source)
        #PrintUserCalendars(client)
        # TODO; show events to user
        pass
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        update_message(entries, exc_value)
        traceback.print_exc()
        #print exc_type
        #print exc_value
        #print exc_traceback
    update_status(ents, "Waiting for entry...")

def makeent(root, field, showAss=False):
    row = Frame(root)
    # TODO; if name includes "Date" make it a date field. tkinter doesn't have date picker I might roll my own.
    # TODO; if name is "Message" make it multi-line.
    # TODO; password entry might include 'show="*"' like the following..
    #user = makeentry(parent, "User name:", 10)
    #password = makeentry(parent, "Password:", 10, show="*")
    lab = Label(row, width=22, text=field+": ", anchor='w')
    if showAss:
        ent = Entry(row, width=50, show='*')
    else:
        ent = Entry(row, width=50)
    #s1 = "Entry(row, width=50" + entryOpt + ")"
    #s2 = exec("print(s1)")
    #ent = exec(s1)
    #ent = Entry(row, width=50)
    ent.insert(0,"")
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    return ent

def makeform(root):
    account_password_dates_fields = ('Status',
        'Message',
        'Start Date',
        'End Date',
        'Search String',
        'Destination File',
        'Google Account',
    )
    #    'Google Account Password',
    entries = {}
    for field in account_password_dates_fields:
        entries[field] = makeent(root, field)
    s1 = 'Google Account Password'
    entries[s1] = makeent(root,s1, showAss=True)
    return entries

def func(event):
    #print("You hit return.")
    get_events(ents)

#def func1(event):
#    print("You hit Alt, Control or Shift-G.")
#
#def func2(event):
#    print("You hit Alt-Q.")

if __name__ == '__main__':
    # TODO; Is there a button accelerator key for tkinter buttons?
    #       I was not able to get Alt-G or Alt-Q to bind. Something funny is going on.
    #test1=raw_input("gimme something")
    #test2=raw_input("gimme more")
    root = Tk()
    ents = makeform(root)
    #root.bind('<Return>', (get_events(root)))
    # Catch ENTER from form and don't generate an error.
    root.bind('<Return>', func)
    # ENTER goes to tkinter.__init__.CallWrapper.__call__ when not bound to something.
    #root.bind('<Return>', (lambda event, e=ents: e.get()))
    #root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    update_status(ents, "Starting...")
    b1 = Button(root, text='Get Events', command=(lambda e=ents: get_events(e)))
    #b1 = Button(root, text='Get Events', command=(lambda e=ents: get_events(e)), underline=0)
    b1.pack(side=LEFT, padx=5, pady=5)
    #root.bind('<Alt-G>', func1)
    #root.bind('<Shift-G>', func1)
    #root.bind('<Control-G>', func1)
    #b2 = Button(root, text='Monthly Payment', command=(lambda e=ents: monthly_payment(e)))
    #b2.pack(side=LEFT, padx=5, pady=5)
    b3 = Button(root, text='Quit', command=root.quit)
    #b3 = Button(root, text='Quit', command=root.quit, underline=0)
    b3.pack(side=LEFT, padx=5, pady=5)
    #root.bind('<Alt-Q>', func2)
    update_status(ents, "Waiting for entry...")
    update_message(ents, "Enter dates as mm/dd/yyyy!")
    # TODO; figure out a way to keep the Google account password secret.
    s1 = """
          google pycharm security passwords
            python master password database
                http://stackoverflow.com/questions/12042724/securely-storing-passwords-for-use-in-python-script
                http://stackoverflow.com/questions/7014953/i-need-to-securely-store-a-username-and-password-in-python-what-are-my-options
                https://docs.python.org/2/library/getpass.html
                https://charlesleifer.com/blog/creating-a-personal-password-manager/
            python Creating a personal password manager
            PyCharm password database
        Something creates a sqlite db and that could be my answer if encrypted.
            Django project.
    """
    ents['Google Account'].delete(0,END)
    ents['Google Account'].insert(0, "DaleEMoore")
    #ents['Google Account'].insert(0, "MooreWorksService")
    ents['Google Account Password'].delete(0,END)
    #ents['Google Account Password'].insert(0,END, "password")
    #ents['Show Password'].delete(0,END)
    #ents['Show Password'].insert(0, "No")
    ents['Start Date'].delete(0,END)
    # Start Date endDate - 6 days.
    ents['End Date'].delete(0,END)
    # End Date is yesterday.
    dE = datetime.date.today() - datetime.timedelta(days=1)
    dow = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    #       0         1          2            3           4         5           6
    # date.weekday(); Monday is 0 and Sunday is 6
    dS = dE - datetime.timedelta(days=6)
    ents['End Date'].insert(0, dE)
    ents['Start Date'].insert(0, dS)
    ents['Search String'].delete(0,END)
    ents['Search String'].insert(0, "Bill")
    ents['Destination File'].delete(0,END)
    ents['Destination File'].insert(0, "t1.csv")

    ents['Google Account Password'].focus()

    root.mainloop()
