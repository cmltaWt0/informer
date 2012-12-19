#!/usr/bin/python3
#encoding: utf-8

"""
Informer application's goal is to parse some Log-server output and show missed
or ended call info.

In the future, the application must be finalized in some GUI-interface.
Need to implement running in Windows.
"""

import sys
import threading
from PyQt4 import QtGui

from parser.vlt_parser import VltParser


class QtInformer(QtGui.QWidget):
    """ Main Informer Window. """
    def __init__(self, parser):
        super().__init__()
        self.contacts_book = parser.contacts_book
        self.initUI()

    def initUI(self):
        self.setGeometry(1000, 200, 350, 550)
        self.setWindowTitle("Informer's main window")
        self.show()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Close telnet session?" + str(self.contacts_book),
            QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No,
            QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            THREAD_PARSER._stop()
            event.accept()
        else:
            event.ignore()


def qtWindow(contacts_book):
    app = QtGui.QApplication(sys.argv)
    ex = QtInformer(contacts_book)
    sys.exit(app.exec_())


def parser_start(parser):
    parser.vlt_parser()


parser = VltParser()

THREAD_PARSER = threading.Thread(target=parser_start, args=(parser,))
THREAD_WINDOW = threading.Thread(target=qtWindow, args=(parser,))


def main():
    """
    Starting window and parsing process.
    Window process close parsing process at self close.
    """
    THREAD_WINDOW.start()
    THREAD_PARSER.start()


if __name__ == '__main__':
    main()

