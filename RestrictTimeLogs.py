#######################################################################
# Обработка лога посещения компьютера
#######################################################################

import os
from datetime import date,datetime,timedelta
import dateutil.relativedelta as rltd

from tkinter.font import ITALIC
from tkinter import *
from tkcalendar import Calendar, DateEntry

import re #регулярные выражения

import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#import numpy as np
#import pandas as pd

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
    """ Получить все даты файлов в папке с логами Даты содержатся в именах файлов  """
    listdates = []
    for file in os.listdir(foldernamelog):
        if file.endswith(".log"):
            filename = file.split(".")[0]
            datefile = datetime.strptime(filename, dateFormat_file_name)
            listdates.append(datefile)
    return listdates

def init_start_stop_dates(list_all_dates):
    """ Получаем начальные границы дат как последняя доступная минус что-то  
        (Пока не решил это будет фиксированное кол-во дней или минус 1 месяц)
    """
     # последняя дата есть последняя дата в журнале
    stop_date = list_all_dates[-1] 
    # начальная дата есть последняя минус default_days
    start_date = stop_date - timedelta(days=default_days)
    # ?или же будет  минус 1 месяц
    # start_date = stop_date - rltd.relativedelta(months=1)
    
    return start_date, stop_date
    
def get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_file_name, datetimeFormatInFiles):
    """ Получить список времён из файлов с заданным диапазоном дат """
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

def parsed_timelist_to_string(listtimes):
    """ Преобразовать список дат или времён в текстовый вид """
    parsed_times = []
    for t in listtimes:
        t_parsed = str(t)
        parsed_times.append(t_parsed)
    return parsed_times

def separate_date(list_times):
    """ разделить формат времни на два списка дат и времён """
    sep_dates = []; sep_times = []
    for DT in list_times:
        sep_dates.append(DT.date())
        sep_times.append(DT.time())
    return sep_dates, sep_times

def graph_px(xdata, ydata):
    """ Рисуем гистограмму используемых минут """
    print(xdata,ydata)
    
    fig = px.bar(x=xdata, y=ydata)
    fig.show()
    
def graph_go(xdata, ydata):
    """ Рисуем гистограмму используемых минут """
    
    
    
    

def do_diag(time_content):
    """ Готовим данные для  графиков и вызываем их рисования"""
    start_date = time_content[0];  stop_date = time_content[-1]
    num_days = (stop_date - start_date).days +1
    print( "Выбрано:", num_days, "дн. с", start_date.date(), "по",stop_date.date(), ", Точек  =", len(time_content), "шт. ")
      
    # Определяем Список дней,  Списки минут и Список оставшихся минут в день
    list_days = [];  list_minutes = []; list_q_minutes = []

    # Список дней по-быстрому, но если есть пропуски в днях то формируется неверно
    # ?оставлено для образца
    #for curday in (start_date + timedelta(n) for n in range(num_days)):
        #list_days.append(curday.date())

    #  НО для ускорения бежим по контенту и формируем списки за один проход
    # ? а нужны ли эти списки ? 
    curDate = time_content[0].date();   curMinutes = []
    
    for curDT in  time_content:
    
        if curDT.date() == curDate:
            t = curDT.time()  
            m = t.hour * 60 + t.minute          # номер минуты от начала дня 
            curMinutes.append(m)
            continue
    
        # новый день, подводим итоги в списки
        list_days.append(curDate)
        list_minutes.append(curMinutes)
        list_q_minutes.append(len(curMinutes)) 
        # обнуляемся
        curDate = curDate + timedelta(days=1)
        curMinutes = []
    
    # последний день тоже дописать в списки
    list_days.append(curDate)
    list_minutes.append(curMinutes)
    list_q_minutes.append(len(curMinutes)) 

    # ?: Думаем как будем выводить данные    
    #print("Список дней", parsed_timelist_to_string(list_days))    
    #print("Q", list_q_minutes)

    graph_px(list_days,list_q_minutes)
    #graph_go(list_days,list_minutes)
    #graph(time_content)
    
    
    
def press_ok():
    """ Обработчик кнопки "Нарисовать" главного окна.
        Читаем диапазон дат, получаем данные из файлов и запускаем рисование       
    """
    # Получаем диапазон дат из гланого окна
    start_date = entryStart.get_date();   stop_date =  entryStop.get_date()
    # Читаем данные из файлов
    time_content = get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_file_name, datetimeFormatInFiles) 
    # Рисуем контент
    do_diag(time_content)
    
#######################################################################
# MAIN SCRIPT
#######################################################################

# Список всех возможных дат из имён файлов, 
# пока только для одной цели - найти крайние возможные даты которые видны в сообщении
# TODO: хотелось их как-то помечать в календаре что на эту дату есть данные
list_all_dates = get_all_dates(foldernamelog, dateFormat_file_name)  
 
 # Получаем начальную и конечную даты для диаграммы вычислением от ближайшей минус что-то
start_date, stop_date = init_start_stop_dates(list_all_dates)                

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
