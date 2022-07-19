# Библиотеки
import os
from datetime import datetime

# Переменные
foldernamelog = "LOGS"
dateFormat_file_name = "%Y-%m-%d"
datetimeFormatInLog = "%d.%m.%Y %H:%M:%S"


# Функции
def get_period(foldernamelog):
    """ Получить все даты файлов в папке с логами Даты содержатся в имени файлов  """
    listdates = list()
    for file in os.listdir(foldernamelog):
        if file.endswith(".log"):
            listdates.append(file.split(".")[0])
    return listdates


def get_start_stop_dates():
    """ Предоставить выбор дат начала графика и конца, вернуть 2 значения  """
    # TODO: доделать выбор дат пока возвращаем конкретные значения
    return "2022-11-28", "2022-12-28"


#######################################################################

print("Начали")
listdates = get_period(foldernamelog)  # получаем список дат
print(listdates)
start_stop = get_start_stop_dates()  # получить стартовую и конечную дату
print("Кончили")
