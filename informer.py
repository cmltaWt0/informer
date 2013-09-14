#!/usr/bin/env python3
# coding=utf-8

"""
Informer application's goal is to parse some Log-server output and show missed
or ended call info.

In the future, the application must be finalized in some GUI-interface.
Need to implement running in Windows.
"""

from sys import argv, exit
from os import path

from PyQt4 import QtGui, QtCore

from parser import TelnetParser
from parser import PopParser


class QtInformer(QtGui.QWidget):
    """ Main Informer Window. """

    def __init__(self, THREAD_PARSER, POP_PARSER):
        super().__init__()
        self.THREAD_PARSER = THREAD_PARSER
        self.POP_PARSER = POP_PARSER
        self.initUI()

    def initUI(self):
        self.setGeometry(1000, 200, 350, 550)
        self.setWindowTitle("Informer's main window")
        self.setWindowIcon(QtGui.QIcon(path.dirname(path.realpath(__file__)) +
                                       '/call.png'))
        self.btn = QtGui.QPushButton('Check mail', self)
        self.connect(self.btn, QtCore.SIGNAL("clicked()"), self.clicked)
        self.btn.setToolTip('Click for check you mail.')
        self.show()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Close telnet session?\n" +
                                           str(self.THREAD_PARSER.contacts_book),
                                           QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.THREAD_PARSER._stop()
            self.POP_PARSER._stop()
            event.accept()
        else:
            event.ignore()

    def clicked(self):
        mails = self.POP_PARSER.pop3_parser()
        for i, j in enumerate(mails):
            self.label = QtGui.QLabel(j[:-1], self)
            self.label.setMinimumWidth(200)
            self.label.move(20, 30 + i * 25)
            self.label.show()


def qtWindow(THREAD_PARSER, POP_PARSER):
    app = QtGui.QApplication(argv)
    ex = QtInformer(THREAD_PARSER, POP_PARSER)
    exit(app.exec_())


TELNET_PARSER = TelnetParser()
POP_PARSER = PopParser()


def main():
    """
    Starting window and parsing process.
    Window process close parsing process at self close.
    """
    TELNET_PARSER.start()
    POP_PARSER.start()
    qtWindow(TELNET_PARSER, POP_PARSER)


if __name__ == '__main__':
    main()

