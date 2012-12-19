#!/usr/bin/python3
#encoding: utf-8

"""
Informer application's goal is to parse some Log-server output and show missed
or ended call info.

In the future, the application must be finalized in some GUI-interface.
Need to implement running in Windows.
"""

from parser.vlt_parser import vlt_parser


if __name__ == "__main__":
    vlt_parser()
