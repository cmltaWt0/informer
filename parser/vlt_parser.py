__author__ = 'Maksim Sokolski'

import os
import time
import pickle

import telnetlib

from viewer.notify import view_tk
from contact.contact import Contact


FILE_OUT = os.path.dirname(os.path.realpath(__file__)) + '/../log/' +\
           str(time.localtime().tm_mday) +\
           '.' + str(time.localtime().tm_mon) +\
           '.' + str(time.localtime().tm_year) + '-aon.log'
FILE_ERR = os.path.dirname(os.path.realpath(__file__)) + '/../log/' +\
           str(time.localtime().tm_mday) +\
           '.' + str(time.localtime().tm_mon) +\
           '.' + str(time.localtime().tm_year) + '-aon.err'
FILE_DUMP = os.path.dirname(os.path.realpath(__file__)) + '/../contact/book.pk'

HOST = "192.168.52.6"  # Log-server IP-address
STR_SEARCH = '577140400'  # Searched phone number
#FROM = "user@localdomain"
#TO = ["user@localdomain"]
#SUBJECT = "Incoming Call."
TEXT = "Incoming call from "


def parse_string(str_all, STR_SEARCH):
    """
    Searching for a number(STR_SEARCH) in str_all.

    Assume that str_all and STR_SEARCH is a not empty string
    Result = string of caller_id and date-time of call
    """

    if not isinstance(str_all, str) or not isinstance(STR_SEARCH, str):
        raise TypeError('Input string type value please.')
    elif str_all == '' or str_all == ' '\
         or STR_SEARCH == '' or STR_SEARCH == ' ':
        raise ValueError('Dont input space or empty string.')
    else:
        search_list = str_all.split()
        if STR_SEARCH in search_list:
            call_id = search_list[-4]  # Caller-id recognizing
            call_time = search_list[-19].split('/')[1] + ' ' +\
                        search_list[-19].split('/')[2] + ':' +\
                        search_list[-17]  # Call time recognizing
            return ('0' + call_id, call_time)


def write_log(file_path, text, err=''):
    """
    Writing text to file_path file with some err.
    If no err is present - writing nothing.
    """

    try:
        with open(file_path, 'a') as f:
            f.write(str(time.localtime().tm_year) + '-' +
                    str(time.localtime().tm_mon) + '-' +
                    str(time.localtime().tm_mday) + '-' +
                    str(time.localtime().tm_hour) + ':' +
                    str(time.localtime().tm_min) + ': ' +
                    text + str(err) + '\n')
    except IOError as e:
        view_tk(str(e))


def load_contacts():
    try:
        with open(FILE_DUMP, 'rb') as f:
            contacts_book = pickle.load(f)
        return contacts_book
    except IOError:
        return []


def save_contacts(contacts_book):
    with open(FILE_DUMP, 'wb') as f:
        pickle.dump(contacts_book, f)


def vlt_parser():
    contacts_book = load_contacts()
    while True:
        try:
            tn = telnetlib.Telnet(HOST)
        except Exception as e:
            write_log(FILE_ERR, 'Connection to server is not available: ', e)
            time.sleep(5)
        else:
            while True:
                try:
                    tn.sock_avail()
                except Exception as e:
                    write_log(FILE_ERR, 'Connection is not active.', e)
                    time.sleep(5)
                    tn = telnetlib.Telnet(HOST)
                else:
                    str_all = str(tn.read_until(b'\r\r\n\r\n'))
                    try:
                        call_info = parse_string(str_all, STR_SEARCH)
                    except (TypeError, ValueError) as e:
                        write_log(FILE_ERR, 'Error parsing: ', e)
                    else:
                        if call_info is not None:
                            result = TEXT + call_info[0] + ' ' + call_info[1]

                            for contact in contacts_book:
                                if call_info[0] == contact.phone:
                                    caller = contact
                                    break
                            else:
                                caller = Contact(call_info[0])
                                contacts_book.append(caller)
                                save_contacts(contacts_book)

                            write_log(FILE_OUT, result + ' ' + str(caller))
                            view_tk(result + '\n' + str(caller))