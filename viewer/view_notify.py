import pynotify


def view_notify(data):
    """Notify for AON service"""

    n = pynotify.Notification("Incoming call", data)
    n.set_hint('x', 200)
    n.set_hint('y', 400)
    pynotify.init("aon")
    n.show()