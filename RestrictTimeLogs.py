import os
from datetime import date,datetime,timedelta
import dateutil.relativedelta as rltd
from tkinter import *
from tkcalendar import Calendar, DateEntry


foldernamelog = "LOGS"

# Functions
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
    # start_date = stop_date - timedelta(days=30)
    start_date = stop_date - rltd.relativedelta(months=1)

    return start_date, stop_date

def correct_start_stop_dates (start_stop_dates):
    """ Виджет изменения начальных дат"""
        # Создаём окно в котором можно выбрать свои крайние даты для графика
    Ww = Tk()
    Ww.title("Статистика посещений")
    
    lblTop = Label(Ww, text="Выберите период", font='bold', fg='blue')
    lblTop.grid(row=0,  column=0,  columnspan=4, padx=100, pady=10) 

    #start date
    lblBegin = Label(Ww,text="Начало:")
    lblBegin.grid(row=1,  column=0, sticky=E)
    entryBegin = DateEntry(Ww, cursor="hand2")
    entryBegin.set_date(start_stop_dates[0])
    entryBegin.grid(row=1, column=1, sticky=W)

    #stop date
    lblBegin = Label(Ww,text="Начало:")
    lblBegin.grid(row=1,  column=2, sticky=E)
    entryBegin = DateEntry(Ww, cursor="hand2")
    entryBegin.set_date(start_stop_dates[1])
    entryBegin.grid(row=1, column=3, sticky=W)

    btnOK = Button(Ww, text='Применить' )
    btnOK.grid(row=2, column=1, pady=20)
    btnCancel = Button(Ww, text='Отменить' )
    btnCancel.grid(row=2, column=2, pady=20)
    
    Ww.mainloop()

    return start_stop_dates
    
def get_times_from_files(start_stop_dates, datetimeFormatInFiles):
    """ Получаем данные из файлов с заданным диапазоном дат """
    return start_stop_dates

def draw_diag(time_content):
    """ Рисуем диаграмму """
    print("Рисуем",time_content)

#######################################################################

list_all_dates = get_all_dates(foldernamelog,"%Y-%m-%d") # Получаем список всех дат из имён файлов по формату
start_stop_dates = get_start_stop_dates(list_all_dates) # Получаем начальную и конечную даты диапазона выбора
start_stop_dates = correct_start_stop_dates(start_stop_dates) # Корректируем диапазон дат с помощью виджета
time_content = get_times_from_files(start_stop_dates, "%d.%m.%Y %H:%M:%S") # Вытаскиваем  из всех файлов заданного периода время
draw_diag(time_content) # Рисуем диаграмму по полученным временам.


