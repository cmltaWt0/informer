from os import path
from pickle import load, dump
from poplib import POP3
from telnetlib import Telnet
from threading import Thread, Lock
from time import sleep
from datetime import datetime
from configparser import ConfigParser

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from viewer.notify import view_tk, view_notify
from contact import Contact


class CommonParser(Thread):
    config = ConfigParser()
    config.read(path.dirname(path.realpath(__file__)) + '/../conf.ini')

    def __init__(self):
        super().__init__()

    def parser(self):
        return "Not implemented yet."

    @staticmethod
    def write_log(file_path, text, err=''):
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

    @classmethod
    def send_mail(cls, reply):
        """
        send_mail(reply: str) -> None
        """
        msg = MIMEMultipart()
        msg['From'] = cls.config.get('smtp', 'from')
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'Missed call.'
        msg['To'] = cls.config.get('smtp', 'to')
        msg.attach(MIMEText(reply))

        smtp = SMTP(cls.config.get('smtp', 'smtp_ip'),
                    int(cls.config.get('smtp', 'smtp_port')))
        smtp.sendmail(cls.config.get('smtp', 'from'),
                      cls.config.get('smtp', 'to'), msg.as_string())

    def run(self):
        while True:
            self.parser()


class TelnetParser(CommonParser):
    def __init__(self):
        super().__init__()
        PATH = path.dirname(path.realpath(__file__)) + '/../log/' + \
               "{:%d.%m.%Y}".format(datetime.now())
        self.FILE_OUT = PATH + '-aon.log'
        self.FILE_ERR = PATH + '-aon.err'
        self.FILE_DUMP = path.dirname(path.realpath(__file__)) + '/../contact/book.pk'
        self.HOST = super().config.get('options', 'server_ip')  # Log-server IP-address
        self.SEARCH_LIST = [item[1] for item in super().config.items('search') if item[1] != '']
        self.TEXT = "Incoming call from "
        self.CONTACTS_LOCK = Lock()
        self.contacts_book = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.FILE_DUMP, 'rb') as f:
                contacts_book = load(f)
            return contacts_book
        except IOError:
            return []

    def save_contacts(self):
        with open(self.FILE_DUMP, 'wb') as f:
            dump(self.contacts_book, f)

    def parse_string(self, str_all, search_list):
        """
        Searching for a number(STR_SEARCH) in str_all.

        Assume that str_all and STR_SEARCH is a not empty string
        Result = string of caller_id and date-time of call
        :type str_all: str
        :type search_list: list
        """
        for search in search_list:
            if not isinstance(str_all, str) or not isinstance(search, str):
                raise TypeError('Input string type value please.')
            elif str_all == '' or str_all == ' ' \
                or search == '' or search == ' ':
                raise ValueError('Dont input space or empty string.')
            else:
                search_list = str_all.split()
                if search in search_list:
                    call_id = search_list[-4]  # Caller-id recognizing
                    if call_id == search:
                        return None
                    else:
                        call_time = search_list[-19].split('/')[1] + ' ' + \
                                    search_list[-19].split('/')[2] + ':' + \
                                    search_list[-17]  # Call time recognizing
                        return '0' + call_id, call_time, search

    def parser(self):
        """ TelnetParser's class method. """
        try:
            self.tn = Telnet(self.HOST)
        except Exception as e:
            self.write_log(self.FILE_ERR, 'Connection to server is not available: ', e)
            sleep(5)
        else:
            while True:
                str_all = self.tn.read_until(b'\r\r\n\r\n').decode('UTF-8')
                try:
                    call_info = self.parse_string(str_all, self.SEARCH_LIST)
                except (TypeError, ValueError) as e:
                    self.write_log(self.FILE_ERR, 'Error parsing: ', e)
                else:
                    if call_info is not None:
                        result = self.TEXT + call_info[0] + ' ' + call_info[1]

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

                        self.write_log(self.FILE_OUT, result + ' ' +
                                       str(caller) + ' to 0' + call_info[2])
                        if call_info[2] == super().config.get('search', 'search1'):
                            view_tk(result + '\n' + str(caller))
                        else:
                            self.send_mail(result + ' ' + str(caller) +
                                           ' to 0' + call_info[2])


class PopParser(CommonParser):
    def __init__(self):
        super().__init__()
        PATH = path.dirname(path.realpath(__file__)) + '/../log/' + \
               "{:%d.%m.%Y}".format(datetime.now())
        self.pop3_ip = super().config.get('options', 'pop3_ip')
        self.pop3_user = super().config.get('options', 'user')
        self.pop3_pass = super().config.get('options', 'pass')
        self.pop3_timeout = super().config.get('options', 'timeout')
        self.FILE_ERR = PATH + '-pop.err'

    def pop3_parser(self):
        """
        Method for manual mail checking.

        :rtype : str
        :return: mails
        """
        mails = []
        try:
            pop = POP3(self.pop3_ip)
        except Exception as e:
            self.write_log(self.FILE_ERR, 'Connection to server is not available: ', e)
        else:
            pop.user(self.pop3_user)
            pop.pass_(self.pop3_pass)

            if pop.stat()[0] > 0:
                numMessages = len(pop.list()[1])
                result = ''
                for i in range(numMessages):
                    tmp = str(i + 1) + ' From: ' + pop.retr(i + 1)[1][0].\
                          decode('UTF-8').split(':')[1].lstrip()[1:-1] + '\n'
                    result += tmp
                    mails.append(tmp)
                view_notify(result)

            pop.quit()
        finally:
            return mails

    def parser(self):
        self.pop3_parser()
        sleep(int(self.pop3_timeout))
