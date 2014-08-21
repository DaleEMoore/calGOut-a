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

import sys, traceback
from Tkinter import *
account_password_dates_fields = ('Status',
                                 'Message',
                                 'Google Account',
                                 'Google Account Password',
                                 'Start Date',
                                 'End Date')


def update_status(entries, status_description):
    entries['Status'].delete(0,END)
    entries['Status'].insert(0, status_description )
    print("Status: %s" % status_description)

def update_message(entries, message_description):
    entries['Message'].delete(0,END)
    entries['Message'].insert(0, message_description)
    print("Message: %s" % message_description)

def monthly_payment(entries):
    try:
        # period rate:
        r = (float(entries['Annual Rate'].get()) / 100) / 12
        print("r", r)
        # principal loan:
        loan = float(entries['Loan Principle'].get())
        n =  float(entries['Number of Payments'].get())
        remaining_loan = float(entries['Remaining Loan'].get())
        q = (1 + r)** n
        monthly = r * ( (q * loan - remaining_loan) / ( q - 1 ))
        monthly = ("%8.2f" % monthly).strip()
        entries['Monthly Payment'].delete(0,END)
        entries['Monthly Payment'].insert(0, monthly )
        print("Monthly Payment: %f" % monthly)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        update_message(entries, exc_traceback)

def final_balance(entries):
    try:
        # period rate:
        r = (float(entries['Annual Rate'].get()) / 100) / 12
        print("r", r)
        # principal loan:
        loan = float(entries['Loan Principle'].get())
        n =  float(entries['Number of Payments'].get())
        q = (1 + r)** n
        monthly = float(entries['Monthly Payment'].get())
        q = (1 + r)** n
        remaining = q * loan  - ( (q - 1) / r) * monthly
        remaining = ("%8.2f" % remaining).strip()
        entries['Remaining Loan'].delete(0,END)
        entries['Remaining Loan'].insert(0, remaining )
        print("Remaining Loan: %f" % remaining)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        update_message(entries, exc_traceback)

def makeform(root, fieldsList):
   entries = {}
   for field in fieldsList:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"")
      #ent.insert(0,"0")
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, account_password_dates_fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))
   update_status(ents, "Starting...")
   b1 = Button(root, text='Final Balance', command=(lambda e=ents: final_balance(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Monthly Payment', command=(lambda e=ents: monthly_payment(e)))
   b2.pack(side=LEFT, padx=5, pady=5)
   b3 = Button(root, text='Quit', command=root.quit)
   b3.pack(side=LEFT, padx=5, pady=5)
   update_status(ents, "Waiting for entry...")
   root.mainloop()
