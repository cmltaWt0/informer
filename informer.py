#!/usr/bin/env python3
# coding=utf-8

"""
Informer application's goal is to parse some Log-server output and show missed
or ended call info.

In the future, the application must be finalized in some GUI-interface.
Need to implement running in Windows.
"""

import sys
import os

from PyQt4 import QtGui, QtCore

from parsers.vlt_parser import VltParser
from parsers.pop3_parser import PopParser


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
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__)) + 
					'/call.png'))
        self.btn = QtGui.QPushButton('Button', self)
        self.connect(self.btn, QtCore.SIGNAL("clicked()"), self.clicked)
        self.btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.show()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Close telnet session?\n" + str(self.THREAD_PARSER.contacts_book),
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
        self.POP_PARSER.pop3_parser()


def qtWindow(THREAD_PARSER, POP_PARSER):
    app = QtGui.QApplication(sys.argv)
    ex = QtInformer(THREAD_PARSER, POP_PARSER)
    sys.exit(app.exec_())


THREAD_PARSER = VltParser()
POP_PARSER = PopParser()

def main():
    """
    Starting window and parsing process.
    Window process close parsing process at self close.
    """
    THREAD_PARSER.start()
    POP_PARSER.start()
    qtWindow(THREAD_PARSER, POP_PARSER)


if __name__ == '__main__':
    main()

