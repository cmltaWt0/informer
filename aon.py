#!/usr/bin/python
#encoding: utf-8

import telnetlib
#import smtplib
import os
import time
from viewer import view_tk
import time


"""
AON service.
"""

year = str(time.localtime().tm_year)
mon = str(time.localtime().tm_mon)
day = str(time.localtime().tm_mday)
hour = str(time.localtime().tm_hour)
minuts = str(time.localtime().tm_min)

host = "192.168.52.6" # Sip-server IP-address
file_out = os.getcwd() + '/log/' + str(time.localtime().tm_mday) \
           +'.'+ str(time.localtime().tm_mon) + \
           '.' + str(time.localtime().tm_year) + '-aon.log'
str_search = '577140400' #Searched phone number
#FROM = "maksim@laptop.localdomain"
#TO = ["maksim@laptop.localdomain"]
#SUBJECT = "Incoming Call." # Not utilizing yet
TEXT = "Incoming call from "

def str_parsing(str_all, str_search, pars_id = 1):
    
    """Проверка наличия искомого номера.
    Функция str_parsing проверяет наличие искомого номера 
    в списке элементов строки с телнет сессии и выдает
    как результат номер звонивщегоей и время звонка"""
    
    search_list = str_all.split()

    if str_search in search_list:
        call_id = search_list[-4] #Caller-id recognizing     
        call_time = search_list[-19].split('/')[1] + ' ' + \
                    search_list[-19].split('/')[2] + ':' + \
                    search_list[-17] #Call time recognizing
        return '0' + call_id + ' ' + call_time #Result formatting

#def send_smtp():   
#    try:
#        server.sendmail(FROM, TO, result)
#    except:
#        try:
#            server = smtplib.SMTP('localhost')
#            server.sendmail(FROM, TO, result)
#           view_tk(result)
#        except:
#            with open(file_out, 'a') as f:
#                f.write('Losing connection to SMTP...' + '\n')
#                f.write(result + '\n')
#            view_tk(result)
#    else:
#        print(result)
#    with open('os.getcwd() + '/test', 'a') as f:
#        f.write(result + '\n')
#    view_tk(result)

if __name__ == "__main__": 
    while True:
        try:
            tn = telnetlib.Telnet(host)
        except:
            time.sleep(5)
        else:
            while True:
                try:
                    ts=tn.sock_avail()
                except:
                    time.sleep(5)
                    tn = telnetlib.Telnet(host)
                else:
                    str_a = tn.read_until('\r\r\n\r\n')
                    call_info = str_parsing(str_a, str_search) #Search results
                
                    if call_info is not None: #Not negative result
                        result = (TEXT + str("".join(call_info)))

#                      send_smtp()
                    
                        with open(file_out, 'a') as f:
                            f.write(result + '\n')
                        view_tk.view_tk(result)
