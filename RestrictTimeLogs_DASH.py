#######################################################################
# Обработка журналов посещения компьютера 
# с помощью библиотеки pandas
# и выводом результатов с помощью библиотеки dash
#######################################################################
import os
from datetime import date,datetime,timedelta
import re #регулярные выражения
import dateutil.relativedelta as rltd
import pandas as pd


#######################################################################
# Стартовые переменные
#######################################################################
foldernamelog                = "LOGS"  # имя папки с логами
#foldernamelog              = "C:/Users/Максим/AppData/Roaming/RestrictTime"   
dateFormat_Filename     = "%Y-%m-%d"                        # формат даты в имени файла лога
datetimeFormat_InFiles  =  "%d.%m.%Y %H:%M:%S"    # формат даты со временем внутри файла
count_month                  = 2 # стартовый период в месяцах

#######################################################################
# Функции
#######################################################################
def get_all_dates(foldernamelog, dateFormat_Filename):
    """ Получить список всех дат файлов в папке с логами из имён файлов  """
    listdates = []
    
    for file in os.listdir(foldernamelog):
        if file.endswith(".log"):
            filename = file.split(".")[0]
            datefile = datetime.strptime(filename, dateFormat_Filename)
            listdates.append(datefile)
    
    return listdates

def get_data_from_files(foldernamelog,start_date, stop_date, dateFormat_Filename, datetimeFormat_InFiles ):
    
    """ Получить данные из всех журналов в таблицу DF с полями:

         DT                      - datetime - полный формат времени события, из файла
         Days                   - date  - дата события, из DT
         Time_of_days     - time - время события, из DT
         Min_of_days       - int - минута дня события, считаем по циклам дня
         Min_to_end        - int - осталось минут до истечения срока, из файла
    """
    data = []
    cur_datefile=0
    
    # Бежим по все файлам с расширением .log и читаем построчно
    for file in os.listdir(foldernamelog):
        if file.endswith(".log"):
            filename = file.split(".")[0]
                        
            datefile = datetime.strptime(filename, dateFormat_Filename)
    
            if ( start_date <= datefile <= stop_date ):  # фильтруем нужный период #? может стоит это убрать
                
                # День изменился? 
                if cur_datefile != datefile:
                    cur_datefile = datefile # начинаем новый день
                    cur_min_of_day = 0    # обнуляем счётчик минут дня
               
                # Читаем строчки из файла 
                with open( foldernamelog + "\\" + file, "r",  encoding='cp866') as fileobject:
                   
                   pred_min_remaind = -1  # флаг повторного значения оставшихся минут для отсева дублирования
                   
                   # Разбираем строку как <Дата> <Час>:<Минута>:.....<Осталось минут>
                   for line in fileobject: 
                        # Осталось минут в день
                        cur_min_remaind = int( re.search(r'(\d{1,2})$', line)[0] )
                        
                        # если минут как в предыдущей строке то пропускаем строку
                        if pred_min_remaind == cur_min_remaind: 
                            continue
                        # иначе строка защитана, снимаем показания
                        pred_min_remaind = cur_min_remaind
                        cur_min_of_day += 1
                        
                        # Дата из строки
                        cur_datetime_in_str  =  datetime.strptime( re.search(r'\d{2}\.\d{2}\.\d{4}.\d{1,2}:\d{2}:\d{2}', line)[0], datetimeFormat_InFiles ) 
                                             
                        # Собираем данные для таблицы
                                           
                        data.append({ 
                                    'DT'                  : cur_datetime_in_str, 
                                    'Days'               : cur_datetime_in_str.date(),
                                    'Time_of_days' : cur_datetime_in_str.time(),
                                    'Min_of_days'   : cur_min_of_day,
                                    'Min_to_end'    : cur_min_remaind
                                    })
                            
    return data


#######################################################################
# MAIN SCRIPT
#######################################################################

# Список всех возможных дат из имён файлов
list_all_dates = get_all_dates(foldernamelog, dateFormat_Filename)  

# последняя дата
stop_date = list_all_dates[-1] 
# начальная дата есть последняя минус  count_month месяцев
start_date = stop_date - rltd.relativedelta(months=count_month) 

# !на время отладки достаточно дни, потом уберём
start_date = stop_date - timedelta(days=3) 

data = get_data_from_files(foldernamelog,start_date, stop_date, dateFormat_Filename, datetimeFormat_InFiles)

df = pd.DataFrame(data)

print(df)


