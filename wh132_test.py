from global_vars import *
import global_vars as gv
import micropy_control as mpy
import modbusRS485 as mod
import wh132_functions as fx
from wh132_functions import *
import wh132_json




RS485A1 = ""
RS485A2 = gv.RS485A2
RS485B1 = ""
RS485B2 = gv.RS485B2
IN3_1 = ""
IN3_2 = gv.IN3_2
OUT = ""
OUT_2 = gv.OUT_2
SDI_12_1 = ""
SDI_12_2 = gv.SDI_12_2
B1 = gv.B1
B2 = gv.B2
D = ""
E = ""


print(colored('********* Welcome to the WH132 test jig *********', 'cyan'))

manf_oper()
check_operator_input()
mpy.connect()
get_jig_info()
mod.init_modbus()

while 1:
    qr_scan()
    enter_scans()
    takt_start()
    initialize_test_output()
    #CTM_test()
    COD_test()
    initialize_continuity_test()
    continuity_test()
    continuity_test_summary()
    takt_finish()
    full_test_check()
    wh132_json.make_json()
    reset_test_dict()
    print('***** Test complete.  Please prepare new cable for test *****')

