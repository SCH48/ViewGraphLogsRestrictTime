


#ticktext = ["06:00","07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00"]
ticktext = [ "0"+str(i) +":00" for i in range(1,9) ] +[ str(i) +":00" for i in range(10,24) ]

#tickvals = [360,       420,       480,         540,      600,    660,        720,       780,       840,      900,      960,       1020,       1080,   1140,   1200,     1260,     1320,     1380,   1440]
tickvals = [ i*60 for i in range(1,24)]

print(ticktext,tickvals)
