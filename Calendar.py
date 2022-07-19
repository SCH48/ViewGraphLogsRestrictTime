import datetime
from tkinter import *
from tkcalendar import Calendar

days = []
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

# Create Object
root = Tk()
root.title("Календарь")
root.geometry("300x300")
cal = Calendar(root, selectmode='day', year=year, month=month, day=day)
cal.pack()

def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())

# Add Button and Label
Button(root, text="Get Date", command=grad_date).pack(pady=20)

date = Label(root, text="")
date.pack(pady=20)

# Execute Tkinter
root.mainloop()