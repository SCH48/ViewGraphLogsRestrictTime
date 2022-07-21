from datetime import datetime
print(datetime.strptime("2022-10-15", "%Y-%m-%d"))



import dateutil.relativedelta as rltd
d = datetime.strptime("2013-03-31", "%Y-%m-%d")
d2 = d - rltd.relativedelta(months=1)
print(d2)






