                        
                        
                        # Дата в строке
                        cur_date_in_str  =  datetime.strptime( re.search(r'\d{2}.\d{2}.\d{4}', line)[0], datetimeFormatInFiles ) 

                        # Часов и минут в строке
                        #cur_hour_time_in_str  = int( re.findall(r'(\d{1,2}):', line)[0] )
                        #cur_min_time_in_str  = int( re.findall(r':(\d{2})', line)[0] )
                        # Вычисляем минуту дня для данной строки
                        #cur_min_in_day = cur_hour_time_in_str * 60 + cur_min_time_in_str

                        #print("Дата:", cur_date_in_str, "Час:", cur_hour_time_in_str, "Минут:", cur_min_time_in_str, "Осталось минут:",cur_min_remaind, "Минута дня:", cur_min_in_day)


