#######################################################################
# Обработка лога посещения компьютера
#######################################################################
import os
from datetime import date,datetime,timedelta
from tkinter.font import ITALIC
import dateutil.relativedelta as rltd
from tkinter import *
from tkcalendar import Calendar, DateEntry
import matplotlib.pyplot as plt
import matplotlib.dates as matd
#######################################################################
foldernamelog = "LOGS"
dateFormat_file_name = "%Y-%m-%d"
datetimeFormatInFiles =  "%d.%m.%Y %H:%M:%S"
default_days = 2
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
    """ Получаем начальные границы дат как последняя доступная минус что-то  """
    stop_date = list_all_dates[-1]
    start_date = stop_date - timedelta(days=default_days)
    #start_date = stop_date - rltd.relativedelta(months=1)
    return start_date, stop_date
    
def get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_file_name, datetimeFormatInFiles):
    """ Получить данные из файлов с заданным диапазоном дат """
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

def get_times_from_date(time_content, curday):
    """ Получить список минут на конкретную дату """
    times = []; minutes = []
    for DT in time_content:
            if DT.date() == curday:
                t = DT.time()
                m = t.hour * 60 + t.minute          # минута дня
                times.append(t)
                minutes.append(m)
    return  times, minutes

def parsed_timelist_to_string(listtimes):
    """ Преобразовать список дат или времён в текстовый вид """
    parsed_times = []
    for t in listtimes:
        t_parsed = str(t)
        parsed_times.append(t_parsed)
    return parsed_times

def draw_diag(time_content, start_date, stop_date):
    """ Рисуем графики """
    num_days = (stop_date - start_date).days +1
    print( "Рисуем", num_days, "дн. с", start_date, "по", stop_date, ", Точек  =", len(time_content), "шт. ")
  
    # Получаем список дней,  списки времён посещения, списки минут дня и кол-во минут в день
    list_days = [];  list_times = []; list_minutes = []; list_txt_minutes = []; list_q_minutes = []

    # Перебираем день за днём от start_date до stop_date
    for curday in (start_date + timedelta(n) for n in range(num_days)):
        # получим из time_content  минуты дня и их кол-во 
        list_times_day, list_minutes_day = get_times_from_date(time_content, curday) 
        list_txt_times_day = parsed_timelist_to_string(list_times_day)
        q_minutes_day = len(list_minutes_day)-1
        # добавим полученное в списки
        list_days.append(curday)
        list_times.append(list_times_day)    
        list_minutes.append(list_minutes_day)
        list_txt_minutes.append(list_txt_times_day)
        list_q_minutes.append(q_minutes_day)
     
    # ?: Думаем как будем выводить данные    
    print(parsed_timelist_to_string(list_days))    
    print(list_q_minutes)

    # TODO: рисование
    
    # fig, ax = plt.subplots()
    # ax.set_title("Активность пользователя")
    # fig.suptitle("График")
    # #x = matd.date2num(datadays)
    # x = datadays
    # y = datatimes
    
    # ax.hist(datadays, bins = 50, rwidth = 0.4)

    # plt.plot_date(x,y)
    # plt.title("Активность пользователя")
    # plt.xlabel("Даты")
    # plt.ylabel("Время")
    # plt.legend()    
    # plt.gcf().autofmt_xdate()
    # plt.show()
 
def press_ok():
    """ Получаем диапазон дат, читаем данные из файлов и отправляем на рисование """
    start_date = entryStart.get_date()
    stop_date =  entryStop.get_date()
    time_content = get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_file_name, datetimeFormatInFiles) 
    draw_diag(time_content, start_date, stop_date)

#######################################################################
# MAIN SCRIPT
#######################################################################
# Получаем список всех дат из имён файлов по формату
list_all_dates = get_all_dates(foldernamelog, dateFormat_file_name) 
# Получаем начальную и конечную даты диапазона выбора
start_date, stop_date = get_start_stop_dates(list_all_dates) 

# Корректируем диапазон дат с помощью виджета и по кнопке рисуем диаграмму
root = Tk()
root.resizable(width=False, height=False)
root.title("Статистика посещений")

lblTop = Label(root, text="Выберите период", font='Arial 13 bold')
lblTop.pack(side=TOP, padx=100, pady=5)

# Диапазон доступных дат
txt_start = datetime.strftime(list_all_dates[0],"%d.%m.%Y")
txt_stop = datetime.strftime(list_all_dates[-1],"%d.%m.%Y")
text_period_dat = "Доступны даты с {} по {}.".format(txt_start, txt_stop)
lblDates = Label(root,text=text_period_dat, font=("Arial 11 italic"))
lblDates.pack(side=TOP)

# Выбор начальной даты
lblStart = Label(root,text="Начало:")
lblStart.pack(side=LEFT, padx=5)
entryStart = DateEntry(root, cursor="hand2")
entryStart.set_date(start_date)
entryStart.pack(side=LEFT)

# Выбор конечной даты
lblStop = Label(root,text=" Конец:")
lblStop.pack(side=LEFT,  padx=5)
entryStop = DateEntry(root, cursor="hand2")
entryStop.set_date(stop_date)
entryStop.pack(side=LEFT)

btnOK = Button(root, text='Нарисовать', bg= "#408080", fg="#a8e824", activebackground="yellow", activeforeground="red", command=press_ok)
btnOK.pack(side=BOTTOM, padx=10, pady=10)
   
root.mainloop()
#######################################################################
