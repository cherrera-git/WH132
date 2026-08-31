from gs_usb.gs_usb import *
from gs_usb.gs_usb_frame import *
from gs_usb.constants import *
import minimalmodbus
import re
import logging
import errno
import time
import serial
from serial import Serial
import serial.tools.list_ports
import subprocess
from termcolor import colored
from colorama import Fore, Back, Style
import colorama as colorama
import sys
import os
import importlib
import datetime
import micropy_control as mpy

# config debugging
printvals = True

# global debug variable
debug = True

# CM info
manufacturer = None
operator = None


# I/O Pin Assignments
RS485A2 = 'Y1'
RS485B2 = 'Y2'
CAN_RX = 'Y3'
CAN_TX = 'Y4'
IN3_2 = 'Y5'
OUT_2 = 'Y6'
SDI_12_2 = 'Y7'
MUX_C = 'Y8'
COD_PWR = 'Y9'
COD_IN = 'Y10'
B2 = 'Y11'
B1 = 'Y12'
COD_AN_OUT = 'X1'
RELAY_PWR = 'X4'
MUX_OUT = 'X6'
RS485_PWR = 'X8'
MUX_B = 'X9'
MUX_A = 'X10'
E2 = 'X11'
D2 = 'X12'


# Part Number in JSON
part_no = 'ALT-WH132L'

# Takt time
Takt_start_time = None
Takt_finish_time = None

qr_id = None

# Micropy Variables
ADC_range = 4095    # ADC values range from 0-4095 
PY_vol = 3.3        # Voltage to board is 3.3V

# CTM
MESSAGE_ID_RPM = 0x0CF00400    #ECU CAN_ID for Engine Speed
rpm_mod_read_1 = 28
rpm_mod_read_2 = 572
rpm_mod_read_3 = 1116
rpm_mod_read_4 = 1660

# RS485
SLAVE_ADDRESS = 48
PORT = 'COM3'
BAUDRATE = 9600
BYTESIZE = 8
STOPBITS = 1
TIMEOUT = 0.2


# Continuity
net_check = {}
net_check_count = 0
net_check_template = {
    'RS485A HI':'-',
    'RS485A LO':'-',
    'RS485B HI':'-',
    'RS485B LO':'-',
    'IN3 HI':'-', 
    'IN3 LO':'-',
    'OUT HI':'-',
    'OUT LO':'-',
    'SDI_12 HI':'-',
    'SDI_12 LO':'-',
    'B HI':'-',
    'B LO':'-',
    'D HI':'-',
    'D LO':'-',
    'E HI':'-',
    'E LO':'-'
    }

net_error_msg = []

wire_colour_list ={
    'RS485A':'WHITE',
    'RS485B':'GREEN',
    'IN3':'YELLOW',
    'OUT':'RED',
    'SDI_12':' DARK BLUE', 
    'B': 'BLACK',
    'D': 'RED',
    'H': 'LIGHT BLUE',
    'I': 'ORANGE',
    'E': 'BROWN'
}

conn_A_pin_list={
    'RS485A':'(Pin 7)',
    'RS485B':'(Pin 3)',
    'IN3':'(Pin 8)',
    'OUT':'(Pin 9)',
    'SDI_12':'(Pin 10)', 
    'D': '(Pin 1)',
    'E': '(Pin 5)'
}

conn_F_pin_list={
    'RS485A':'(Pin 3)',
    'RS485B':'(Pin 2)',
    'IN3':'(Pin 5)',
    'OUT':'(Pin 1)',
    'SDI_12':'(Pin 6)',
    'D': 'not on F',
    'E': 'not on F'
}

test_output = {}
test_errors = []

# WH132 Test Result template, this is not JSON that gets uploaded
test_dict_template = {
    "cod_test_hi": None,
    "cod_test_lo": None,
    "ctm_test_1": None,
    "ctm_test_2": None,
    "continuity": None,
    "ctm_serial": None,
    "harness_id": None,
    'product_id': None,
    'device_id': None,
    'timestamp': None,
    'jig_id': None,
    'micropy_fw_ver': None,
    'takt_time(s)': None,
    'test_pass':None,
    'comment': None,
    'test_type': None,
    'PN': 'ALT_WH132L'
}



# setup logging format  #TODO create new file each time code starts
# logging.basicConfig(filename='WH132_test.log', filemode='w', format='%(asctime)s - %(message)s',
#                     datefmt='%d-%b-%y %H:%M:%S')

# dict for failures to print out at end of test
fail_dict = {}

# global variables
micropy_conn = None
mcpy_obj = None


# tolerances
# format:   call_value: [upper_tol, lower_tol] (eg: 'v_in':[12.3,11.7])
tolerance_dict = {
    'COD_volt_hi':[0.57, 0.64],
    'COD_volt_lo':[0.48, 0.56]
}
