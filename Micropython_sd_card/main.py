########################################################################################################################
# Written by: Rishi Uppal
# Date: Nov 21, 2022
# Module: micro_sd_fw.py
# This module is specific for the micropython PYBv1.1.
# This module connects with the WH132 interface PCBA. Micro will control I/O and take ADC readings
########################################################################################################################

import machine
import pyb
from pyb import Pin, ADC, Timer, LED, CAN

# I/O vars
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
COD_AN_OUT = ADC(Pin('X1'))
RELAY_PWR = 'X4'
MUX_OUT = 'X6'
CTM_PWR = 'X8'
MUX_B = 'X9'
MUX_A = 'X10'
E2 = 'X11'
D2 = 'X12'
red = LED(1)
green = LED(2)
yellow = LED(3)
blue = LED(4)
mcpy_fw_ver = '1.0.0'

MESSAGE_ID_RPM = 0x0CF00400
string1=b"\xFF\x7D\x8D\xE0\x00\x00\xFF\xFF"
string2=b"\xFF\x7D\x8D\xE0\x11\x00\xFF\xFF"
string3=b"\xFF\x7D\x8D\xE0\x22\x00\xFF\xFF"
string4=b"\xFF\x7D\x8D\xE0\x33\x00\xFF\xFF"

# I/O ctrl
def pin_state(pin, state):
    out_val = Pin(pin, Pin.OUT_PP)
    if state is True:
        out_val.high()
        print('PIN ' + str(pin) + ' 1')
    if state is False:
        out_val.low()
        print('PIN ' + str(pin) + ' 0')


# set COD_AN_IN pull-up
def set_cod_in():
    global cod_out
    cod_out = COD_AN_OUT #Pin(COD_AN_OUT, Pin.IN, Pin.PULL_UP)


# read COD_AN_IN
def read_cod():
    cod_out.value()


# Read pin value
def pin_read(pin):
    in_val = Pin(pin) #, Pin.IN, Pin.PULL_UP)
    val = in_val.value()
    # print('This is the mpy reading: ' + str(val))
    return val


# LED control
def led(color, state):
    led = LED(color)
    led.toggle()
    if state is True:
        led.on()
    if state is False:
        led.off(0)


# reply to init command from master
def ping():
    string = 'here bud'
    return string


# initialize pins
def init_pins():
    pin_state(RS485A2, False)
    pin_state(RS485B2, False)
    pin_state(MUX_A, False)
    pin_state(MUX_B, False)
    pin_state(MUX_C, False)
    pin_state(COD_PWR, False)
    pin_state(COD_IN, False)
    pin_state(CTM_PWR, False)
    pin_state(RELAY_PWR, False)
    pin_state(B1, False)
    pin_state(B2, False)
    # set_cod_in()
    pin_state(SDI_12_2, False)
    pin_state(OUT_2, False)
    pin_state(IN3_2, False)
    pin_state(D2, False)
    pin_state(E2, False)
    string = 'pins initialized'
    return string


# get micropy unique id which will be used as jig identifier
def get_id():
    string = machine.unique_id()
    # print(string)
    return string


# return fw version
def get_fw():
    return mcpy_fw_ver


# read COD value
def get_cod_read():
    cod = COD_AN_OUT.read()
    return cod


def can_to_RS485(data):
    string1=b"\xFF\x7D\x8D\xE0\x00\x00\xFF\xFF"
    string2=b"\xFF\x7D\x8D\xE0\x11\x00\xFF\xFF"
    string3=b"\xFF\x7D\x8D\xE0\x22\x00\xFF\xFF"
    string4=b"\xFF\x7D\x8D\xE0\x33\x00\xFF\xFF"
    MESSAGE_ID_RPM = 0x0CF00400
    can = CAN(1, CAN.LOOPBACK, extframe=True) #prescaler=40, sjw=1, bs1=14, bs2=6)
    #can = CAN(1, CAN.LOOPBACK, extframe=True, prescaler=40, sjw=1, bs1=14, bs2=6)
    can.setfilter(0, CAN.MASK16, 0, (0, 0, 0, 0))
    #print(data)
    send=can.send(data, MESSAGE_ID_RPM, rtr=False)
    print("Message 1: " + str(send))
    while True:
        while can.any(0):
            print(can.info())
            # lst = []
            data1 = can.recv(0, timeout=1000)
            # print(lst)
            print(data1)
            print(can.info())
            print("canRead")


def can_init():
    global can
    can = CAN(1, CAN.LOOPBACK, extframe=True, baudrate=250000)   
    can.setfilter(0, CAN.MASK32, 0, (0, 0))

def can_send_1():
    can.send(string1, MESSAGE_ID_RPM, timeout=5000, rtr=False)

def can_send_2():
    can.send(string2, MESSAGE_ID_RPM, timeout=5000, rtr=False)

def can_send_3():
    can.send(string3, MESSAGE_ID_RPM, timeout=5000, rtr=False)

def can_send_4():
    can.send(string4, MESSAGE_ID_RPM, timeout=5000, rtr=False)

def can_fifo():
    fifo = (can.any(0))
    print(fifo)
    return fifo

def can_read():
    rtrn = can.recv(0, timeout=5000)
    print(rtrn)
    return rtrn

def can_info():
    info = can.info()
    print(info)
    return info

def can_state():
    state = can.state()
    print(state)
    return state

def can_restart():
    can.restart()
    
def reset_micro():
    machine.reset()
    



# init pins on startup
init_pins()

