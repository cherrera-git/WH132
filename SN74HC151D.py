from global_vars import *
import global_vars as gv
import micropy_control as mpy

mpy = mpy.Micropy()

def D0():
    # D
    mpy.write_pin(gv.MUX_A, False)
    mpy.write_pin(gv.MUX_B, False)
    mpy.write_pin(gv.MUX_C, False)
    D = mpy.read_pin(gv.MUX_OUT)
    return D

def D1():
    # E
    mpy.write_pin(gv.MUX_A, True)
    mpy.write_pin(gv.MUX_B, False)
    mpy.write_pin(gv.MUX_C, False)
    E = mpy.read_pin(gv.MUX_OUT)
    return E

def D2():
    # IN3-1
    mpy.write_pin(gv.MUX_A, False)
    mpy.write_pin(gv.MUX_B, True)
    mpy.write_pin(gv.MUX_C, False)
    IN3_1 = mpy.read_pin(gv.MUX_OUT)
    return IN3_1

def D3():
    # OUT
    mpy.write_pin(gv.MUX_A, True)
    mpy.write_pin(gv.MUX_B, True)
    mpy.write_pin(gv.MUX_C, False)
    OUT = mpy.read_pin(gv.MUX_OUT)
    return OUT

def D4():
    # SDI-12-1
    mpy.write_pin(gv.MUX_A, False)
    mpy.write_pin(gv.MUX_B, False)
    mpy.write_pin(gv.MUX_C, True)
    SDI_12_1 = mpy.read_pin(gv.MUX_OUT)
    return SDI_12_1

def D5():
    # RS485B1
    mpy.write_pin(gv.MUX_A, True)
    mpy.write_pin(gv.MUX_B, False)
    mpy.write_pin(gv.MUX_C, True)
    RS485B1 = mpy.read_pin(gv.MUX_OUT)
    return RS485B1

def D6():
    # RS485A1
    mpy.write_pin(gv.MUX_A, False)
    mpy.write_pin(gv.MUX_B, True)
    mpy.write_pin(gv.MUX_C, True)
    RS485A1 = mpy.read_pin(gv.MUX_OUT)
    return RS485A1

def D7():
    # GND
    mpy.write_pin(gv.MUX_A, True)
    mpy.write_pin(gv.MUX_B, True)
    mpy.write_pin(gv.MUX_C, True)
    D7 = mpy.read_pin(gv.MUX_OUT)
    return D7

        