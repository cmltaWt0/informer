"""Module for Contact data type and methods"""


class Contact(object):
    """
    Class for Contact data type.

    Initialize:
        first_name - string type
        last_name - string type
        phone = string type
        email - string type
    """
    def __init__(self, phone, first_name='Name', last_name='Second', email=''):
        self.first_name = first_name
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)