# Библиотеки
import os
from datetime import date,datetime,timedelta
from tkinter import *

# Переменные
foldernamelog = "LOGS"
dateFormat_file_name = "%Y-%m-%d"
datetimeFormat_InLog = "%d.%m.%Y %H:%M:%S"

# Функции
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
    """ Получаем начальные границы дат как последняя доступная минус 1 месяц """
    last_date = list_all_dates[-1]
    start_date = last_date - timedelta()
    return start_date,last_date

def draw_select_dates(start_stop_dates):
    """ Рисуем окно с выбором начальной и конечной даты """
    start_date = start_stop_dates[0]
    stop_date = start_stop_dates[1]

    # Создаём окно
    root = Tk()



def get_data_for_diag():
    """ Отбираем данные для диаграммы из файлов с требуемым диапазоном дат """
    pass

def draw_diag():
    """ Рисуем диаграмму по набору дат """
    pass

#######################################################################
print("Начали")

list_all_dates = get_all_dates(foldernamelog,dateFormat_file_name)
start_stop_dates = get_start_stop_dates(list_all_dates) # Получить начальные даты как текущая дата минус 30 дней
draw_select_dates(start_stop_dates) # Рисуем окно с выбором начальной и конечной даты
get_data_for_diag()# Получаем две даты и вытаскиваем из всех файлов этого периода время
draw_diag() # Рисуем диаграмму по полученным временам.

print("Кончили")
