'''
Created on 2020-09-03

@author: Rishi Uppal

This module contains functions that interacts with a
Zebra printer using ZPL.
'''
import zebra

_PRINTER_NAME = "ZDesigner ZT411-203dpi ZPL"

""" Prints the input strings to a label using the
input printer. """


# def print_label(nin_string, mac_string):
def print_label(mac_string):
    # Guide to the ZPL commands below:
    # ^XA = all command blocks start with this
    # ^FOxxx = Field origin, first number is x, second is y (in printer pixels)
    # ^BXN = QR style barcode - N means normal orientation
    # ^FD = Field start - text or variable after this is what is actually printed
    # ^FS = Field stop, matches the previous ^FD
    # ^ADN = select internal font 'D' with normal orientation
    # ^XZ - all command blocks end with this

    # Each %s is a string variable - the list provided after the command block will
    # be inserted in the order they are encountered

    commands = """

        ^XA
        ^MD15
        ^PR5
        ^FO 70,10
        ^BQN, 2,3
        ^FDHQ,%s^FS


        ^FO 160,25
        ^A0N,20,20
        ^FDWH132   v1.0^FS

        ^FO 160,60
        ^A0N,40,40
        ^FD%s^FS

        ^XZ

        """ % (mac_string, mac_string[5:14])

    z = zebra.Zebra()
    z.getqueues()
    z.setqueue(_PRINTER_NAME)
    z.output(commands)