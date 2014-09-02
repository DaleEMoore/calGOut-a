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

import datetime
#import gdata
import google_calendar_fetcher
import sys, traceback
from tkinter import * # Python3
#from Tkinter import * # Python2


account_password_dates_fields = ('Status',
                                 'Message',
                                 'Google Account',
                                 'Google Account Password',
                                 'Start Date',
                                 'End Date',
                                 'Destination File')


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
        d1 = entries['Start Date'].get()
        start_date = datetime.datetime.strptime(d1, '%m/%d/%Y')
        d1 = entries['End Date'].get()
        end_date = datetime.datetime.strptime(d1, '%m/%d/%Y')
        destination_file = entries['Destination File'].get()
        print (account, password, start_date, end_date, destination_file)
        # validate date fields since I don't have a date picker yet.
        # TODO; get events from Google
        token = google_calendar_fetcher.login(account,password)
        try:
            google_calendar_fetcher.get_calendars(token)
            google_calendar_fetcher.print_header()
            google_calendar_fetcher.print_output()
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

def makeform(root, fieldsList):
   entries = {}
   for field in fieldsList:
      row = Frame(root)
      # TODO; if name includes "Date" make it a date field. tkinter doesn't have date picker I might roll my own.
      # TODO; if name is "Message" make it multi-line.
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row, width=50)
      ent.insert(0,"")
      #ent.insert(0,"0")
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
   return entries

if __name__ == '__main__':
    #test1=raw_input("gimme something")
    #test2=raw_input("gimme more")
    root = Tk()
    ents = makeform(root, account_password_dates_fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    update_status(ents, "Starting...")
    b1 = Button(root, text='Get Events', command=(lambda e=ents: get_events(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    #b2 = Button(root, text='Monthly Payment', command=(lambda e=ents: monthly_payment(e)))
    #b2.pack(side=LEFT, padx=5, pady=5)
    b3 = Button(root, text='Quit', command=root.quit)
    b3.pack(side=LEFT, padx=5, pady=5)
    update_status(ents, "Waiting for entry...")
    update_message(ents, "Enter dates as mm/dd/yyyy!")

    ents['Google Account'].delete(0,END)
    ents['Google Account'].insert(0, "MooreWorksService")
    ents['Google Account Password'].delete(0,END)
    ents['Start Date'].delete(0,END)
    ents['Start Date'].insert(0, "01/01/0001")
    ents['End Date'].delete(0,END)
    ents['End Date'].insert(0, "12/31/9999")
    ents['Destination File'].delete(0,END)
    ents['Destination File'].insert(0, "t1")

    root.mainloop()
