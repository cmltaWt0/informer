import pynotify

"""
Notify for AON service
"""


def view_notify(data):
    n = pynotify.Notification("Incoming call", data)
    n.set_hint('x', 200)
    n.set_hint('y', 400)
    pynotify.init("aon")
    n.show()