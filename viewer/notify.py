from tkinter import Tk, Frame, Button

import notify2


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
    """ Notify for AON service. """
    n = notify2.Notification("Incoming call", data)
    n.set_hint('x', 200)
    n.set_hint('y', 400)
    notify2.init("aon")
    n.show()


def view_tk(data):
    """ Input data - string. Displaying this string using view_notify and Tk. """
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()
    view_notify(data)