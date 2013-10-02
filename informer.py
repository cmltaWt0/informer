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
from datetime import datetime

from PyQt4 import QtGui, QtCore

from parser import TelnetParser, PopParser

parsers = {'telnet': TelnetParser(),
           'pop': PopParser(),
           'bar': 2,
           'foo': 3}


class QtInformer(QtGui.QWidget):
    """
    Main Informer Window.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.TelnetParser = kwargs['telnet']
        self.PopParser = kwargs['pop']
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
                                           "Close sessions?",
                                           QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.TelnetParser._stop()
            self.PopParser._stop()
            event.accept()
        else:
            event.ignore()

    def clicked(self):
        mails = self.PopParser.pop3_parser()
        for i, j in enumerate(mails):
            self.label = QtGui.QLabel(j[:-1], self)
            self.label.setMinimumWidth(200)
            self.label.move(20, 30 + i * 25)
            self.label.show()


def qtWindow(**kwargs):
    app = QtGui.QApplication(argv)
    ex = QtInformer(**kwargs)
    exit(app.exec_())


def main():
    """
    Starting window and parsing process.
    Window process close parsing process at self close.
    """
    for i in parsers.values():
        try:
            i.start()
        except AttributeError as e:
            with open(path.dirname(path.realpath(__file__)) + '/log/informer.log', 'a') as f:
                f.write("{0:%Y-%m-%d-%H:%M:} {1} {2}\n".format(datetime.now(), i, str(e)))

    qtWindow(**parsers)


if __name__ == '__main__':
    main()
