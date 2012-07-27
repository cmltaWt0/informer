#!/usr/bin/python
#encoding: utf-8
'''
Created on 21.12.2011

@author: maksim
'''

import telnetlib
#import smtplib
import os
import time
from viewer import view_tk
import time


year = str(time.localtime().tm_year)
mon = str(time.localtime().tm_mon)
day = str(time.localtime().tm_mday)
hour = str(time.localtime().tm_hour)
minuts = str(time.localtime().tm_min)

"""AON service.

Send message to the mail, when incoming call takes place"""

def str_parsing(str_all, str_search, pars_id = 1):
    """Проверка наличия искомого номера.

    Функция str_parsing проверяет наличие искомого номера 
    в списке элементов строки с телнет сессии и выдает
    как результат номер звонивщегоей и время звонка"""
    a = [elem for elem in (str_all.split())] # Разбивка строки на элементы
    call = 0
    if str_search in a: # Проверка на наличие оскомого номера
        call3 = a[-4] # Определение звонившего
        res = a[0] + ':' + a[2] # Определение времени звонка
        result0 = res.split("/") # Форматирование времени звонка
        result2 = result0[1:3]
        result3 = " ".join(result2)
        call = '0' + str(call3) + ' ' + result3 # Форматирование результата
    return call

host = "192.168.52.6" # IP сервера с логами звонков
file_out = '/home/maksim/Dropbox/Work/Programming/python/aon/log/' + str(time.localtime().tm_mday)+'.'+str(time.localtime().tm_mon)+'.'+str(time.localtime().tm_year)+'-aon.log'


while True:
    try:
        tn = telnetlib.Telnet(host)
    except:
        time.sleep(5)
    else:
        str_search2 = '577140400' # Искомый номер
        #try:
        #    server = smtplib.SMTP('localhost')
        #except:
        #    pass
        #FROM = "maksim@laptop.localdomain"
        #TO = ["maksim@laptop.localdomain"]
        #SUBJECT = "Incoming Call." # Пока не используется
        TEXT = "Incoming call from "
        
        while True:
            try:
                ts=tn.sock_avail()
            except:
                time.sleep(5)
                tn = telnetlib.Telnet(host)
            else:
                str_a = tn.read_until('\r\r\n\r\n')
                call2 = str_parsing(str_a, str_search2) # Результат поиска
                if call2 == 0: # Отрицательный результат
                    pass
                else:
                    result = (TEXT + str("".join(call2)))
                    
                    #try:
                    #    server.sendmail(FROM, TO, result)
                    #except:
                    #    try:
                    #        server = smtplib.SMTP('localhost')
                    #        server.sendmail(FROM, TO, result)
                    #        view_tk(result)
                    #    except:
                    #        with open(file_out, 'a') as f:
                    #            f.write('Нет подключения к SMTP серверу...' + '\n')
                    #            f.write(result + '\n')
                    #        view_tk(result)
                    #else:
#                    print(result)
                    #with open('/home/maksim/test', 'a') as f:
                    #        f.write(result + '\n')
 #                   view_tk(result)
                    with open(file_out, 'a') as f:
                        #f.write('Нет подключения к SMTP серверу...' + '\n')
                        f.write(result + '\n')
                    view_tk.view_tk(result)
