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
                for i in range(numMessages):
                    result = pop.retr(i+1)[1][-19] + b'\n' + pop.retr(i+1)[1][-20]
                    view_tk(result)

            pop.quit()
            time.sleep(120)

    run = pop3_parser