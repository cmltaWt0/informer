from tkinter import Tk, Frame, Button

import notify2
#import smtplib


#def send_smtp():
#    try:
#        server.sendmail(FROM, TO, result)
#    except Exception as e:
#        try:
#            writing_log(FILE_ERR, 'Trying to reassigning connection. ', e)
#           server = smtplib.SMTP('HOST')
#            server.sendmail(FROM, TO, result)
#        except Exception as e:
#            writing_log(FILE_ERR, 'Losing connection to SMTP... ', e)
#            writing_log(FILE_OUT, result)


class Application(Frame):
    """ Main Tk windows. """
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "Display call info"
        self.QUIT["fg"] = "blue"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


def view_notify(data):
    """ Notify for Informer service. """
    n = notify2.Notification("Incoming call", data)
    n.set_hint('x', 200)
    n.set_hint('y', 400)
    notify2.init('informer')
    n.show()


def view_tk(data):
    """ Input data - string. Displaying this string using view_notify and Tk. """
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()
    view_notify(data)