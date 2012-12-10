import telnetlib
#import smtplib
import os
import time
from viewer.view_tk import view_tk


"""
AON service.
"""

host = "192.168.52.6"  # Log-server IP-address


file_out = os.path.dirname(os.path.realpath(__file__)) + '/log/' + \
            str(time.localtime().tm_mday) + \
            '.' + str(time.localtime().tm_mon) + \
            '.' + str(time.localtime().tm_year) + '-aon.log'
file_err = os.path.dirname(os.path.realpath(__file__)) + '/log/' + \
            str(time.localtime().tm_mday) + \
            '.' + str(time.localtime().tm_mon) + \
            '.' + str(time.localtime().tm_year) + '-aon.err'

str_search = '577140400'  # Searched phone number
#FROM = "user@localdomain"
#TO = ["user@localdomain"]
#SUBJECT = "Incoming Call."
TEXT = "Incoming call from "


def str_parsing(str_all, str_search, pars_id=1):

    """Searching for a number(str_search) in str_all.
    Assume that str_all and str_search is a not empty string
    Result = string contaning caller_id and date-time of call"""

    if not isinstance(str_all, str) or not isinstance(str_search, str):
        raise TypeError('Input string type value please.')
    elif str_all == '' or str_all == ' ' \
    or str_search == '' or str_search == ' ':
        raise ValueError('Dont input space or empty string.')
    else:
        search_list = str_all.split()
        if str_search in search_list:
            call_id = search_list[-4]  # Caller-id recognizing
            call_time = search_list[-19].split('/')[1] + ' ' + \
                        search_list[-19].split('/')[2] + ':' + \
                        search_list[-17]  # Call time recognizing
            return '0' + call_id + ' ' + call_time  # Result formatting

#def send_smtp():
#    try:
#        server.sendmail(FROM, TO, result)
#    except Exception as e:
#        try:
#            writing_log(file_err, 'Trying to reassing connection. ', e)
#            server = smtplib.SMTP('localhost')
#            server.sendmail(FROM, TO, result)
#        except Exception as e:
#            writing_log(file_err, 'Losing connection to SMTP... ', e)
#            writing_log(file_out, result)


def writing_log(file_path, text, err=''):
    try:
        with open(file_path, 'a') as f:
            f.write(str(time.localtime().tm_year) + '-' +
                    str(time.localtime().tm_mon) + '-' +
                    str(time.localtime().tm_mday) + '-' +
                    str(time.localtime().tm_hour) + ':' +
                    str(time.localtime().tm_min) + ': ' +
                    text + str(err) + '\n')
    except IOError as e:
        view_tk(str(e))


def main():
    while True:
        try:
            tn = telnetlib.Telnet(host)
        except Exception as e:
            writing_log(file_err, 'Connection to server is not available: ', e)
            time.sleep(5)
        else:
            while True:
                try:
                    tn.sock_avail()
                except Exception as e:
                    writing_log(file_err, 'Connection is not active.', e)
                    time.sleep(5)
                    tn = telnetlib.Telnet(host)
                else:
                    str_all = tn.read_until('\r\r\n\r\n')
                    try:
                        call_info = str_parsing(str_all, str_search)  # Parsing
                    except (TypeError, ValueError) as e:
                        writing_log(file_err, 'Error parsing: ', e)
                    else:
                        if call_info is not None:  # Not negative result
                            result = (TEXT + str("".join(call_info)))
#                           send_smtp()
                            writing_log(file_out, result)
                            view_tk(result)