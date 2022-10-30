#######################################################################
# Обработка журналов посещения компьютера 
# c выбором диапазона дат с помощью библтотеки tkcslendar
# и выводом результатов с помощью библиотеки Plotly
#######################################################################
import os

from datetime import date,datetime,timedelta
import dateutil.relativedelta as rltd

from tkinter.font import ITALIC
from tkinter import *
from tkcalendar import Calendar, DateEntry

import re #регулярные выражения

import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#######################################################################
# Стартовые переменные
#######################################################################
foldernamelog              = "LOGS"  # имя папки с логами
foldernamelog              = "C:/Users/Максим/AppData/Roaming/RestrictTime"   
dateFormat_Filename   = "%Y-%m-%d"                        # формат даты в имени файла лога
datetimeFormat_InFiles =  "%d.%m.%Y %H:%M:%S"    # формат даты со временем внутри файла

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

def get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_Filename, datetimeFormat_InFiles):
    """ Получить список времён из файлов с заданным диапазоном дат """
    time_content = []
    for file in os.listdir(foldernamelog):
        if file.endswith(".log"):
            filename = file.split(".")[0]
            datefile = datetime.strptime(filename, dateFormat_Filename)
            if ( start_date <= datefile.date() <= stop_date ):
               
                # Читаем строчки со временем из файла  в  time_content
                with open( foldernamelog + "\\" + file, "r",  encoding='cp866') as fileobject:
                   # Флаг повторного значения минут
                   pred_min_remaind = -1 
                   # Разбираем строку как <Дата> <Час>:<Минута>:.....<Осталось минут>
                   for line in fileobject: 
                        # Осталось минут в день
                        cur_min_remaind = int( re.search(r'(\d{1,2})$', line)[0] )
                        # если минут как в предыдущей строке то пропускаем строку
                        if pred_min_remaind == cur_min_remaind: 
                            continue
                        
                        pred_min_remaind = cur_min_remaind
                        # Дата в строке
                        cur_date_in_str  =  datetime.strptime( re.search(r'\d{2}\.\d{2}\.\d{4}.\d{1,2}:\d{2}:\d{2}', line)[0], datetimeFormat_InFiles ) 
                        time_content.append( cur_date_in_str )

    return time_content

def do_diag(time_content):
    """ Готовим данные для  графиков и вызываем их рисования"""
    start_date = time_content[0];  stop_date = time_content[-1]
    num_days = (stop_date - start_date).days +1
    print( "Выбрано:", num_days, "дн. с", start_date.date(), "по",stop_date.date(), ", Точек  =", len(time_content), "шт. ")
      
    # Определяем Список дней,  Списки минут и Список оставшихся минут в день
    list_days = [];  list_minutes = []; list_q_minutes = []
    # А также разделим даты, время и минуты
    list_dates =[]; list_times = []; list_q_times = []

    #  Для ускорения бежим по контенту и формируем списки за один проход
    curDate = time_content[0].date();   curMinutes = []
    
    for curDT in  time_content:
    
        if curDT.date() == curDate:
            t = curDT.time()  
            m = t.hour * 60 + t.minute          # номер минуты от начала дня 
            
            curMinutes.append(m)
            list_q_times.append(m)
            list_dates.append(curDT.date())
            list_times.append(curDT.time())
            continue
    
        # новый день, подводим итоги в списки
        list_days.append(curDate)
        list_minutes.append(curMinutes)
        list_q_minutes.append(len(curMinutes)) 
        # обнуляем промежуточные данные
        curDate = curDate + timedelta(days=1)
        curMinutes = []
    
    # последний день также допишем в списки
    list_days.append(curDate)
    list_minutes.append(curMinutes)
    list_q_minutes.append(len(curMinutes)) 

    fig = go.Figure()
   
    # График использования ПК поминутно
    fig.add_trace( go.Scatter (
                x = list_dates,  y = list_q_times, 
                mode = 'markers', marker_size=10, 
                name = "Время использования",
                text = list_times,
                hovertemplate = "%{x}<br>%{y} минута<br>%{text}"
            ))
    
    # Диаграмма суммарного времени использования ПК по дням
    fig.add_trace( go.Bar (
                x = list_days,  y = list_q_minutes,
                name = "Минут в день",
                hovertemplate = "%{y} минут<br>%{x}"
            )) 
            
    fig.update_layout(
                title_text="Время использования ПК",
                title_font_size=30,
                xaxis_title="Даты",
                yaxis_title="Минуты",    
            )
    
    fig.update_yaxes(  
        #["06:00","07:00", "08:00", ...  "23:00", "24:00"],
        ticktext = [ "0"+str(i) +":00" for i in range(1,10) ] +[ str(i) +":00" for i in range(10,25) ],
        #[360, 960, 1020,    ...   1380,   1440],
        tickvals = [ i*60 for i in range(1,25)]
    )
    
    fig.show()
    
def press_ok():
    """ Обработчик кнопки "Нарисовать" главного окна.
        Читаем диапазон дат, получаем данные из файлов и запускаем рисование       
    """
    # Получаем диапазон дат из гланого окна
    start_date = entryStart.get_date();   stop_date =  entryStop.get_date()
    # Читаем данные из файлов
    time_content = get_times_from_files(foldernamelog, start_date, stop_date, dateFormat_Filename, datetimeFormat_InFiles) 
    # Рисуем контент
    do_diag(time_content)
    
#######################################################################
# MAIN SCRIPT
#######################################################################

# Список всех возможных дат из имён файлов, 
# пока только для одной цели - найти крайние возможные даты которые видны в сообщении
# TODO: хотелось их как-то помечать в календаре что на эту дату есть данные
list_all_dates = get_all_dates(foldernamelog, dateFormat_Filename)  
 
 # Получаем начальную и конечную даты для диаграммы вычислением от ближайшей минус что-то
stop_date = list_all_dates[-1] 
# начальная дата есть последняя минус "что-то"
start_date = stop_date - timedelta(days=1)                 # минус дни
#start_date = stop_date - rltd.relativedelta(months=1)   # или же месяцы

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
