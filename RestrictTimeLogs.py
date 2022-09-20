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
import re

#######################################################################
foldernamelog = "LOGS"                                              # имя папки с логами
dateFormat_file_name = "%Y-%m-%d"                        # формат даты в имени файла лога
dateFormatInFiles =  "%d.%m.%Y"                               # формат даты внутри файла
datetimeFormatInFiles =  "%d.%m.%Y %H:%M:%S"    # формат даты со временем внутри файла
default_days = 2    # ?временный параметр кол-во дней по-умолчанию для диаграммы 

#######################################################################
# Функции
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
    """ Получаем начальные границы дат как последняя доступная минус что-то  
        (Пока не решил это будет фиксированное кол-во дней или минус 1 месяц)
    """
    stop_date = list_all_dates[-1]  # последняя дата есть последняя дата в журнале
    
    # начальная дата диаграммы есть последняя минус default_days
    start_date = stop_date - timedelta(days=default_days)
    # ?или же будет  минус 1 месяц
    # start_date = stop_date - rltd.relativedelta(months=1)
    
    return start_date, stop_date
    
def get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_file_name, datetimeFormatInFiles):
    """ Получить данные времени из файлов с заданным диапазоном дат """
    time_content = []
    for file in os.listdir(foldernamelog):
        if file.endswith(".log"):
            filename = file.split(".")[0]
            datefile = datetime.strptime(filename, dateFormat_file_name)
            if ( start_date <= datefile.date() <= stop_date ):
               
                # Читаем строчки со временем из файла  в  time_content
                with open( foldernamelog + "\\" + file, "r",  encoding='cp866') as fileobject:
                   
                   # Флаг повторного значения минут
                   pred_min_remaind = 0 
                   
                   # Разбираем строку как <Дата> <Час>:<Минута>:.....<Осталось минут>
                   for line in fileobject: 
                        # Осталось минут в день
                        cur_min_remaind = int( re.search(r'(\d{1,2})$', line)[0] )
                        # если минут как в предыдущей строке то пропускаем строку
                        if pred_min_remaind == cur_min_remaind: 
                            continue
                        
                        pred_min_remaind = cur_min_remaind
                        # Дата в строке
                        cur_date_in_str  =  datetime.strptime( re.search(r'\d{2}\.\d{2}\.\d{4}.\d{1,2}:\d{2}:\d{2}', line)[0], datetimeFormatInFiles ) 
                        time_content.append( cur_date_in_str )

    return time_content

def get_times_from_day(time_content, curday):
    """ Получить список минут на конкретную дату """
    times = []; minutes = []
    for DT in time_content:
            if DT.date() == curday:
                t = DT.time()
                m = t.hour * 60 + t.minute          # номер минуты от начала дня
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
    #num_days = (stop_date - start_date).days +1
    num_days = (time_content - start_date).days +1
    print( "Рисуем", num_days, "дн. с", start_date, "по", stop_date, ", Точек  =", len(time_content), "шт. ")
  
    # Получаем список дней,  списки времён посещения, списки минут дня и кол-во оставшихся минут в день
    list_days = [];  list_times = []; list_minutes = []; list_txt_minutes = []; list_q_minutes = []

    # Перебираем все 
    # Перебираем день за днём от start_date до stop_date
    for curday in (start_date + timedelta(n) for n in range(num_days)):
        # получим из time_content  минуты дня и их кол-во 
        list_times_day, list_minutes_day = get_times_from_day(time_content, curday) 
        list_txt_times_day = parsed_timelist_to_string(list_times_day)
        q_minutes_day = len(list_minutes_day)
        # добавим полученное в списки
        list_days.append(curday)
        list_times.append(list_times_day)    
        list_minutes.append(list_minutes_day)
        list_txt_minutes.append(list_txt_times_day)
        list_q_minutes.append(q_minutes_day)
     
    # ?: Думаем как будем выводить данные    
    print("Список дней", parsed_timelist_to_string(list_days))    
    print("Минуты", list_txt_minutes)    
    print("Q", list_q_minutes)
    
    """ 
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
    """

def press_ok():
    """ Обработчик кнопки "Нарисовать" главного окна.
        Читаем диапазон дат, получаем данные из файлов и запускаем рисование       
    """
    # Получаем диапазон дат из гланого окна
    start_date = entryStart.get_date();   stop_date =  entryStop.get_date()
    # Читаем данные из файлов
    time_content = get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_file_name, datetimeFormatInFiles) 
    # Рисуем контент
    #print(time_content[-1], time_content[0])
    draw_diag(time_content, start_date, stop_date)
    
#######################################################################
# MAIN SCRIPT
#######################################################################

# Список всех возможных дат из имён файлов, 
# пока только для одной цели - найти крайние возможные даты которые видны в сообщении
# TODO: хотелось их как-то помечать в календаре что на эту дату есть данные
list_all_dates = get_all_dates(foldernamelog, dateFormat_file_name)  
 
 # Получаем начальную и конечную даты для диаграммы вычислением от ближайшей минус что-то
start_date, stop_date = get_start_stop_dates(list_all_dates)                

# Рисуем форму для корректировки диапазона дат с помощью виджета календаря 
# и по кнопке "Нарисовать" запускаем рисование диаграммы через press_ok()
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
