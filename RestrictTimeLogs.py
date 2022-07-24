import os
from datetime import date,datetime,timedelta
import dateutil.relativedelta as rltd
from tkinter import *
from tkcalendar import Calendar, DateEntry
import matplotlib.pyplot as plt
import matplotlib.dates as matd
#######################################################################
foldernamelog = "LOGS"
dateFormat_file_name = "%Y-%m-%d"
datetimeFormatInFiles =  "%d.%m.%Y %H:%M:%S"
#######################################################################
# Functions
#######################################################################
def get_all_dates(foldernamelog, dateFormat_file_name):
    """ Получить все даты файлов в папке с логами Даты содержатся в имени файлов  """
    listdates = []
    for file in os.listdir(foldernamelog):
        if file.endswith(".log"):
            filename = file.split(".")[0]
            datefile = datetime.strptime(filename, dateFormat_file_name)
            listdates.append(datefile)
    return listdates

def get_start_stop_dates(list_all_dates):
    """ Получаем границы дат как последняя доступная минус 1 месяц   """
    stop_date = list_all_dates[-1]
    start_date = stop_date - timedelta(days=7)
    #start_date = stop_date - rltd.relativedelta(months=1)
    return start_date, stop_date
    
def get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_file_name, datetimeFormatInFiles):
    """ Получаем данные из файлов с заданным диапазоном дат """
    time_content = []
    for file in os.listdir(foldernamelog):
        if file.endswith(".log"):
            filename = file.split(".")[0]
            datefile = datetime.strptime(filename, dateFormat_file_name)
            if ( start_date <= datefile.date() <= stop_date ):
                # читаем строчки со временем из файла  в  time_content
                with open( foldernamelog + "\\" + file, "r") as fileobject:
                    # итерация по строкам
                    for line in fileobject:
                        str = line[:18]
                        time_from_str = datetime.strptime(str,datetimeFormatInFiles)
                        time_content.append(time_from_str)
    return time_content

def draw_diag(time_content):
    """ Рисуем диаграмму """
    print("Рисуем точек = ", len(time_content))
    minutes_in_day = 1440
    num_days = (time_content[-1]-time_content[0]).days + 1
    print ("Дней = ", num_days)

    
    x = matd.date2num(time_content)
    y = list(map(lambda t:  datetime.strftime( t,  "%H-%M-%S" ), time_content))
    

    plt.plot_date(x,y)
        
    plt.title("Активность пользователя")
    plt.xlabel("Даты")
    plt.ylabel("Время")
    plt.legend()    
    plt.show()
    



def press_ok():
    """ Нажата 'Применить' получаем диапазон, читаем данные из файлов и отправляем на рисование """
    start_date = entryStart.get_date()
    stop_date =  entryStop.get_date()
    time_content = get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_file_name, datetimeFormatInFiles) 
    draw_diag(time_content)

#######################################################################
# MAIN SCRIPT
#######################################################################

# Получаем список всех дат из имён файлов по формату
list_all_dates = get_all_dates(foldernamelog, dateFormat_file_name) 

# Получаем начальную и конечную даты диапазона выбора
start_stop_dates = get_start_stop_dates(list_all_dates) 

# Корректируем диапазон дат с помощью виджета и по кнопке Применить рисуем диаграмму
Ww = Tk()
Ww.title("Статистика посещений")
    
lblTop = Label(Ww, text="Выберите период", font='bold', fg='blue')
lblTop.grid(row=0,  column=0,  columnspan=4, padx=100, pady=10) 

 #start date
lblStart = Label(Ww,text="Начало:")
lblStart.grid(row=1,  column=0, sticky=E)
entryStart = DateEntry(Ww, cursor="hand2")
entryStart.set_date(start_stop_dates[0])
entryStart.grid(row=1, column=1, sticky=W)

#stop date
lblStop = Label(Ww,text="Конец:")
lblStop.grid(row=1,  column=2, sticky=E)
entryStop = DateEntry(Ww, cursor="hand2")
entryStop.set_date(start_stop_dates[1])
entryStop.grid(row=1, column=3, sticky=W)

btnOK = Button(Ww, text='Применить', command=press_ok)
btnOK.grid(row=2, column=1, columnspan=2, pady=20, sticky=NSEW )
    
Ww.mainloop()

#######################################################################
