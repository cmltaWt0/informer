import os
import time
import poplib
import configparser
import threading

from viewer.notify import view_tk

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + '/../conf.ini')

class PopParser(threading.Thread):
    def __init__(self):
        super().__init__()
        self.pop3_ip = config.get('options', 'pop3_ip')
        self.pop3_user = config.get('options', 'user')
        self.pop3_pass = config.get('options', 'pass')

    def pop3_parser(self):
        while True:
            pop = poplib.POP3(self.pop3_ip)
            pop.user(self.pop3_user)
            pop.pass_(self.pop3_pass)

            if pop.stat()[0] > 0:
                numMessages = len(pop.list()[1])
                result = ''
                for i in range(numMessages):
                    result += str(i+1) + ') From: ' + pop.retr(i+1)[1][0].decode('UTF-8').split(':')[1].lstrip()[1:-1] + '\n'
                view_tk(result)

            pop.quit()
            time.sleep(120)

    run = pop3_parser