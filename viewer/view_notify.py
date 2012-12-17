import notify2


def view_notify(data):
    """Notify for AON service"""

    n = notify2.Notification("Incoming call", data)
    n.set_hint('x', 200)
    n.set_hint('y', 400)
    notify2.init("aon")
    n.show()