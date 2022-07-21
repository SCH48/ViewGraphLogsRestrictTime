# Библиотеки
import os
from datetime import date,datetime,timedelta
import dateutil.relativedelta as rltd
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

def choose_dates(list_all_dates):
    """ Получаем границы дат как последняя доступная минус 1 месяц
        Рисуем окно с выбором начальной и конечной даты для переназначения их по своему желанию
    """
    stop_date = list_all_dates[-1]
    # start_date = stop_date - timedelta(days=30)
    start_date = stop_date - rltd.relativedelta(months=1)

    # Создаём окно в котором можно выбрать свои крайние даты для графика
    root = Tk()


    return start_date, stop_date

def get_data_from_files(start_stop_dates):
    """ Отбираем данные для диаграммы из файлов с требуемым диапазоном дат """
    return start_stop_dates

def draw_diag(time_content):
    """ Рисуем диаграмму по набору дат """
    print("Рисуем",time_content)

#######################################################################

list_all_dates = get_all_dates(foldernamelog,dateFormat_file_name) # Получаем список всех дат
start_stop_dates = choose_dates(list_all_dates) # Рисуем окно с выбором начальной и конечной даты
time_content = get_data_from_files(start_stop_dates)# Получаем крайние даты и вытаскиваем из всех файлов этого периода время
draw_diag(time_content) # Рисуем диаграмму по полученным временам.
