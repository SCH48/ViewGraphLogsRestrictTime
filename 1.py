import datetime 
import numpy as np 
import matplotlib.dates as mdates 
import matplotlib.pyplot as plt 
# dates for xaxis 
event_date = [datetime.datetime(2008, 12, 3), datetime.datetime(2009, 1, 5), datetime.datetime(2009, 2, 3)] 
# # base date for yaxis can be anything, since information is in the time 
anydate = datetime.date(2001,1,1) 
# # event times 
event_start = [datetime.time(20, 12), datetime.time(12, 15), datetime.time(8, 1,)] 
event_finish = [datetime.time(23, 56), datetime.time(16, 5), datetime.time(18, 34)] 
# # translate times and dates lists into matplotlib date format numpy arrays 
start = np.fromiter((mdates.date2num(datetime.datetime.combine(anydate, event)) 
for event in event_start), dtype = 'float', count = len(event_start)) 
finish = np.fromiter((mdates.date2num(datetime.datetime.combine(anydate, event)) 
for event in event_finish), dtype = 'float', count = len(event_finish)) 
date = mdates.date2num(event_date) 
# calculate events durations 
duration = finish - start 
fig = plt.figure() 
ax = fig.add_subplot(1, 1, 1) 
# use errorbar to represent event duration 
ax.errorbar(date, start, [np.zeros(len(duration)), duration], linestyle = '')
# make matplotlib treat both axis as times 
ax.xaxis_date() 
ax.yaxis_date() 
plt.show()