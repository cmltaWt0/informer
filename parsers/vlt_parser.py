import os
import pickle
import telnetlib
import threading
from time import sleep
from datetime import datetime

from viewer.notify import view_tk
from contact.contact import Contact
import configparser

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


PATH = os.path.dirname(os.path.realpath(__file__)) + '/../log/' +\
       "{:%d.%m.%Y}".format(datetime.now())
FILE_OUT = PATH + '-aon.log'
FILE_ERR = PATH + '-aon.err'
FILE_DUMP = os.path.dirname(os.path.realpath(__file__)) + '/../contact/book.pk'

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + '/../conf.ini')


HOST = config.get('options', 'server_ip')  # Log-server IP-address

items = config.items('search')
SEARCH_LIST = [item[1] for item in items if item[1] != '']  # All numbers to monitor

TEXT = "Incoming call from "

CONTACTS_LOCK = threading.Lock()


def vlt_parser(self):
    """ VltParser's class method. """
    while True:
        try:
            self.tn = telnetlib.Telnet(HOST)
        except Exception as e:
            self.write_log(FILE_ERR, 'Connection to server is not available: ', e)
            sleep(5)
        else:
            while True:
                str_all = self.tn.read_until(b'\r\r\n\r\n').decode('UTF-8')
                try:
                    call_info = self.parse_string(str_all, SEARCH_LIST)
                except (TypeError, ValueError) as e:
                    self.write_log(FILE_ERR, 'Error parsing: ', e)
                else:
                    if call_info is not None:
                        result = TEXT + call_info[0] + ' ' + call_info[1]

                        self.CONTACTS_LOCK.acquire(1)
                        for contact in self.contacts_book:
                            if call_info[0] == contact.phone:
                                caller = contact
                                break
                        else:
                            caller = Contact(call_info[0])
                            self.contacts_book.append(caller)
                            self.save_contacts()
                        self.CONTACTS_LOCK.release()

                        self.write_log(FILE_OUT, result + ' ' + str(caller) + 'to 0' + call_info[2])
                        if call_info[2] == config.get('search', 'search1'):
                            view_tk(result + '\n' + str(caller))
                        else:
                            self.send_mail(result + ' ' + str(caller) + 'to 0' + call_info[2])


class VltParser(threading.Thread):

    def __init__(self):
        super().__init__()
        self.contacts_book = self.load_contacts()
        self.CONTACTS_LOCK = CONTACTS_LOCK

    run = vlt_parser

    def load_contacts(self):
        try:
            with open(FILE_DUMP, 'rb') as f:
                contacts_book = pickle.load(f)
            return contacts_book
        except IOError:
            return []

    def save_contacts(self):
        with open(FILE_DUMP, 'wb') as f:
            pickle.dump(self.contacts_book, f)

    def write_log(self, file_path, text, err=''):
        """
        Writing text to file_path file with some err.
        If no err is present - writing nothing.
        """
        try:
            with open(file_path, 'a') as f:
                f.write("{:%Y-%m-%d-%H:%M: }".format(datetime.now()) +
                    text + str(err) + '\n')
        except IOError as e:
            view_tk(str(e))

    def parse_string(self, str_all, search_list):
        """
        Searching for a number(STR_SEARCH) in str_all.

        Assume that str_all and STR_SEARCH is a not empty string
        Result = string of caller_id and date-time of call
        """
        for search in search_list:
            if not isinstance(str_all, str) or not isinstance(search, str):
                raise TypeError('Input string type value please.')
            elif str_all == '' or str_all == ' '\
                or search == '' or search == ' ':
                raise ValueError('Dont input space or empty string.')
            else:
                search_list = str_all.split()
                if search in search_list:
                    call_id = search_list[-4]  # Caller-id recognizing
                    if call_id == search:
                        return None
                    else:
                        call_time = search_list[-19].split('/')[1] + ' ' +\
                                    search_list[-19].split('/')[2] + ':' +\
                                    search_list[-17]  # Call time recognizing
                        return '0' + call_id, call_time, search

    def send_mail(self, reply):
        """
        send_mail(reply: str) -> None
        """
        msg = MIMEMultipart()
        msg['From'] = config.get('smtp', 'from')
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'Missed call.'
        msg['To'] = config.get('smtp', 'to')
        msg.attach(MIMEText(reply))

        smtp = smtplib.SMTP(config.get('smtp', 'smtp_ip'), int(config.get('smtp', 'smtp_port')))
        smtp.sendmail(config.get('smtp', 'from'), config.get('smtp', 'to'), msg.as_string())
