import global_vars as gv
from global_vars import *

ALTRAC_DEVICE_TYPE_0 = 0
ALTRAC_DEVICE_TYPE_1 = 1
ALTRAC_DEVICE_CAN_SUCCESS_1 = 10
ALTRAC_DEVICE_MOD_SUCCESS_1 = 16
SLAVE_ADDRESS = 48
ALTRAC_DEVICE_SERIAL_0 = 2
ALTRAC_DEVICE_SERIAL_1 = 3
ALTRAC_DEVICE_SERIAL_2 = 4
ALTRAC_DEVICE_SERIAL_3 = 5
ALTRAC_DEVICE_SERIAL_4 = 6
ALTRAC_DEVICE_SERIAL_5 = 7
ALTRAC_DEVICE_SERIAL_6 = 8
ALTRAC_DEVICE_SERIAL_7 = 9

ENGINE_SPEED_190 = 120
HW_VERSION = 1065
SW_VERSION = 1026

def init_modbus():
    global instrument
    instrument = minimalmodbus.Instrument(gv.PORT, gv.SLAVE_ADDRESS)  # port name, slave address (in decimal)
    instrument.serial.baudrate = gv.BAUDRATE
    instrument.serial.bytesize = gv.BYTESIZE
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.stopbits = gv.STOPBITS
    instrument.serial.timeout = gv.TIMEOUT
    instrument.debug = False
    instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    instrument.clear_buffers_before_each_transaction = True


def rpm():
    rpm = instrument.read_register(ENGINE_SPEED_190, 0, 3, False)
    return rpm


def device_type_0():
    dev_type = instrument.read_register(ALTRAC_DEVICE_TYPE_0, 0, 3, False)
    print('dev type: ' + str(dev_type))
    return dev_type


def device_type_1():
    dev_type = instrument.read_register(1, 0, 3, False)
    print('dev type: ' + str(dev_type))
    return dev_type


def sw_version():
    sw_ver = instrument.read_register(SW_VERSION, 0, 3, False)
    return sw_ver


def serial_number():
    serial_data = ""
    for i in range(2,10):
        read_serial_register = hex(instrument.read_register(i, 0, 3, False)).upper()
        print(read_serial_register)
        serial_data+=read_serial_register
        time.sleep(1)
    serial_data=re.sub('[0X]','',serial_data)
    #print(serial_data)
    return serial_data
 