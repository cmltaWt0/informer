#!/usr/bin/python
#encoding: utf-8
'''
Created on 21.12.2011

@author: maksim
'''

from Tkinter import *
from view_notify import view_notify

class Application(Frame):
    '''
    classdocs
    '''

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "Показать информацию о звонке"
        self.QUIT["fg"] = "blue"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "left"})

    def __init__(self, master=None):
        '''
        Constructor
        '''
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
def view_tk(data):
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()
    view_notify(data)