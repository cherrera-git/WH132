########################################################################################################################
# Written by: Rishi Uppal
# Date: Nov 21, 2022
# Module: micropy_control.py
# This module makes direct calls to micropy_sd_fw running on micropy via serial comms
# Requires global_vars.py for all libraries
########################################################################################################################
import time
import logging
from global_vars import *
import global_vars as gv


ser_del = 0  # serial delay
ERROR_1 = 'Communication error with module, please check connection and try again'

debug = False

class Micropy(object):

    def __init__(self):
        self.baud = 921600
        self.ports = list(serial.tools.list_ports.comports())
        self.ping = None
        self.ser = None
        self.port = None
        self.micro_on = None
        self.led_on = None
        self.in1 = 'Y1'
        self.in2 = 'Y2'
        self.in3 = 'Y3'
        self.out1 = 'Y4'
        self.rpm = 'Y5'
        self.usb_pwr = 'Y7'
        self.dut_pwr = 'Y8'
        self.led_pwr = 'X9'
        self.dev_id = None
        self.dev_fw = None
        self.pin_init = None
        self.pout_dev = None
        self.rpm = None
        self.can_recv = None

    # Scan all com ports for micropy
    def connect(self):
        connected = []
        ping_string = 'here bud'
        for element in self.ports:
            connected.append(element.device)
        if debug is True:
            print("Connected COM ports: " + str(connected))
        num_ports = len(connected)
        print(num_ports)
        x = 0

        # comment this out for auto detect
        # OK the original COM port assignment didn't work with COM4
        # The working COM port is COM5 with exist test Jig we have
        # for CM Mountain Tech. 
        # COM7 is for another test jig in head office
        #---------------------------------------
        self.port = 'COM7'
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        print(self.ser)
        gv.micropy_conn = True
        self.init_pins()
        return
        #---------------------------------------

        if x == num_ports:
            self.port = str(connected[num_ports - 1])
            if debug is True:
                print(num_ports)
                print(self.port)
                # port = 'COM6'
            print(colored('Checking port: ' + str(self.port) + ' for Test Micro', 'blue'))
            # self.ser = serial.Serial(self.port, self.baud, timeout=1)
            try:
                self.ser = serial.Serial(self.port, self.baud, timeout=1)
                string = str.encode('ping()\r\n')
                self.ser.write(string)
                time.sleep(ser_del)
                self.ping = self.ser.read(40)
                if debug is True:
                    print(self.ping)
                if ping_string in str(self.ping):
                    print(colored('\nUsing ' + self.port + ' for micropy communication', 'green'))
                    gv.micropy_conn = True
                    self.init_pins()
                    self.write_pin('X9', True)
                    return
            except:
                # else:
                logging.error('MICROPY: ' + str(ConnectionError))
                gv.micropy_conn = False

        while x < num_ports:
            self.port = str(connected[num_ports - 1])
            if debug is True:
                print(num_ports)
                print(self.port)
                # port = 'COM6'
            print(colored('Checking port: ' + str(self.port) + ' for Test Micro', 'blue'))
            try:
                self.ser = serial.Serial(self.port, self.baud, timeout=1)
                string = str.encode('ping()\r\n')
                self.ser.write(string)
                time.sleep(ser_del)
                self.ping = self.ser.read(40)
                if debug is True:
                    print(self.ping)
                if ping_string in str(self.ping):
                    print(colored('\nUsing ' + self.port + ' for micropy communication', 'green'))
                    gv.micropy_conn = True
                    self.init_pins()
                    self.write_pin('X9', True)
                    return
            except:
                # else:
                logging.error('MICROPY: ' + str(ConnectionError))
                gv.micropy_conn = False
            num_ports -= 1

    # Turns on 3.3V LED
    def micro_pwr(self, state):
        string = str.encode('led_ctrl(' + str(state) + ')\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string)
        time.sleep(ser_del)
        self.led_on = self.ser.read(40)
        # add in error check

    # turn pins on/off micropy
    def write_pin(self, pin, state):
        string = str.encode('pin_state(' + "'" + pin + "'," + str(state) + ')\r\n')
        if debug is True:
            print('This is micro: ' + str(string))
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string)
        time.sleep(ser_del)
        reply = self.ser.read(40)
        if debug is True:
            print('mp reply: ' + str(reply))
        if reply is not None:
            if debug is True:
                print('mp_ack')
            return reply
        else:
            if debug is True:
                print('mp_error: ')
            logging.error('MICROPY: CALL_FAIL')
            return errno.ESRCH

    # read pin state
    def read_pin(self, pin):
        string = str.encode('pin_read(' + "'" + pin + "'" + ')\r')
        if debug is True:
            print('This is micro: ' + str(string))
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string)
        time.sleep(ser_del)
        reply = self.ser.read(40)
        if debug is True:
            print('This is pin state: ' + str(reply))
        if reply is not None:
            if debug is True:
                print('ack')
            return reply
        else:
            if debug is True:
                print('error: ')
            logging.error('MICROPY: CALL_FAIL')
            return errno.ESRCH

    # get mac/ID of micro
    def get_dev_mac(self):
        string = str.encode('get_id()\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string)
        time.sleep(ser_del)
        self.dev_id = self.ser.read(40)
        # if self.dev_fw is None:
        #     return ERROR_1
        return self.dev_id

    # get fw version on micro
    def get_dev_fw(self):
        string = str.encode('get_fw()\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string)
        time.sleep(ser_del)
        self.dev_fw = self.ser.read(40)
        # if self.dev_fw is None:
        #     return ERROR_1
        # print(self.dev_fw)
        return self.dev_fw

    # init pins
    def init_pins(self):
        string = str.encode('init_pins()\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string)
        time.sleep(ser_del)
        self.pin_init = self.ser.read(40)
        # if self.dev_fw is None:
        #     return ERROR_1
        # print(self.dev_fw)
        return self.pin_init

    # get cod
    def get_cod_read(self):
        string = str.encode('get_cod_read()\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string)
        time.sleep(ser_del)
        self.pout_dev = self.ser.read(40)
        return self.pout_dev

    def can_init(self):
        string1=str.encode('can_init()\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string1)
        time.sleep(ser_del)

    def send_can_msg_1(self):
        string2 = str.encode('can_send_1()\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string2)
        time.sleep(ser_del)

    def send_can_msg_2(self):
        string2 = str.encode('can_send_2()\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string2)
        time.sleep(ser_del)

    def send_can_msg_3(self):
        string2 = str.encode('can_send_3()\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string2)
        time.sleep(ser_del)

    def send_can_msg_4(self):
        string2 = str.encode('can_send_4()\r\n')
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(string2)
        time.sleep(ser_del)

    
