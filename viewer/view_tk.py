from Tkinter import *
from view_notify import view_notify


class Application(Frame):

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


def view_tk(data):
    """Input data - string. Displaying this string using view_notify and Tk"""

    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()
    view_notify(data)
