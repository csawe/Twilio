from tkinter import *
import tkinter
from tkcalendar import DateEntry
from datetime import datetime
import os
import pandas as pd
from functools import partial
import matplotlib.pyplot as plt

window = Tk()
window.geometry('260x180')
window.wm_title("Twilio account Usage")

l1 = Label(window,text="Welcome to twilio usage app")
l1.grid(row=0,column=0)

l2 = Label(window, text="Enter begin date: ")
l2.grid(row=1, column=0)
begin_date = DateEntry(width=12, background='darkblue', foreground='white', borderwidth=2)
begin_date.grid(row=1, column=1)


l3 = Label(window, text="Enter end date: ")
l3.grid(row=2, column=0)
end_date = DateEntry(width=12, background='darkblue', foreground='white', borderwidth=2)
end_date.grid(row=2, column=1)


def strip_date(date):
    date = date.replace('-','')
    return date
def update_date(date):
    return datetime.strptime(date, '%Y%m%d').strftime('%d%m%Y')
def actual_date(date):
    return date[0:2]+'/'+date[2:4]+'/'+date[4:]
def date(date):
    date = strip_date(date)
    date = update_date(date)
    date = actual_date(date)
    print(date)
    return date
def main():
    begin =  str(begin_date.get_date())
    end = str(end_date.get_date())
    begin = date(begin)
    end = date(end)
    current_dir = os.getcwd()
    if os.path.isfile(f'{current_dir}\daily_data.csv'):
        data =  pd.read_csv(f'{current_dir}\daily_data.csv')
        t1.delete('1.0','end')
        t1.insert(tkinter.END, 'Loading')
        data.drop(data.columns[data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        try:
            new_data = data.loc[(data['end_date']>=begin) & (data['end_date']<end)]
            new_data = new_data.groupby(['account_name'])['price'].sum()
            t1.delete('1.0','end')
            t1.insert(tkinter.END, 'Success')
            print(new_data)
            new_data.plot.barh()
            #new_data.plot(kind='bar', x='price', y='account_sid')
            plt.show()
        except IndexError:
            t1.delete('1.0','end')
            t1.insert(tkinter.END, 'No data for those dates')
    else:
        print("You have no data yet.")

state = 'Ready'

l4 = Label(window, text="State")
l4.grid(row=3,column=0)

t1 = Text(window, height=2, width=20)
t1.grid(row=4, column=0)
t1.insert(tkinter.END, state)

action =  partial(main)
b1 = Button(text="View Account Data", command=action)
b1.grid(row=5, column=0)

b2 = Button(text='Exit', command=exit)
b2.grid(row=6,column=0) 

window.mainloop()
