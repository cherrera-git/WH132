from global_vars import *
import global_vars as gv
import micropy_control as mpy
import modbusRS485 as mod

mpy = mpy.Micropy()

def debug_print(msg):
    if gv.printvals and msg is not None:
        print(Fore.BLUE+str(msg)+Style.RESET_ALL)

# get test jig ID and FW version
def get_jig_info():
    print(colored('Getting jig info...', 'white'))
    time.sleep(0.5)
    mpy_ret = mpy.get_dev_mac() # get MAC/ID of micropy module inside jig
    if debug is True:
        print('this is ret from py: ' + str(mpy_ret))
    if mpy_ret == b'':
        get_jig_info()
    mpy_ret = mpy_ret.decode('ascii')
    mpy_ret = re.split("b|'\'", mpy_ret)
    mpy_ret = re.split("x|'\'|\r\n", mpy_ret[1])
    x = len(mpy_ret[3][:-1])
    if x != 9:
        print('MAC/ID not valid') # This will need better error handling if errors occur
        return
    test_output['jig_id'] = mpy_ret[3][:-1] # insert MAD/ID into test json
    mpy_ret = mpy.get_dev_fw() # get FW version on micropy
    mpy_ret = mpy_ret.decode('ascii')
    mpy_ret = re.split("b|\r\n", mpy_ret)
    x = len(mpy_ret[1][1:-1])
    if x != 5:
        print('Wrong FW version reported')
        return
    test_output['micropy_fw_ver'] = mpy_ret[1][1:-1] # insert micropy FW version into test json
    print(colored('test jig info obtained. micropy_fw_ver:' + str(test_output['micropy_fw_ver']), 'yellow'))

def initialize_test_output():
    test_output['cod_test_hi'] = test_dict_template['cod_test_hi']
    test_output['cod_test_lo'] = test_dict_template['cod_test_lo']
    test_output['ctm_test_1'] = test_dict_template['ctm_test_1']
    test_output['ctm_test_2'] = test_dict_template['ctm_test_2']
    test_output['timestamp'] = test_dict_template['timestamp']
    test_output['takt_time(s)'] = test_dict_template['takt_time(s)']

def initialize_continuity_test():
    net_check['RS485A HI'] = net_check_template['RS485A HI']
    net_check['RS485A LO'] = net_check_template['RS485A LO']
    net_check['RS485B HI'] = net_check_template['RS485B HI']
    net_check['RS485B LO'] = net_check_template['RS485B LO']
    net_check['IN3 HI'] = net_check_template['IN3 HI']
    net_check['IN3 LO'] = net_check_template['IN3 LO']
    net_check['OUT HI'] = net_check_template['OUT HI']
    net_check['OUT LO'] = net_check_template['OUT LO']
    net_check['SDI_12 HI'] = net_check_template['SDI_12 HI']
    net_check['SDI_12 LO'] = net_check_template['SDI_12 LO']
    net_check['B HI'] = net_check_template['B HI']
    net_check['B LO'] = net_check_template['B LO']
    net_check['D HI'] = net_check_template['D HI']
    net_check['D LO'] = net_check_template['D LO']
    net_check['E HI'] = net_check_template['E HI']
    net_check['E LO'] = net_check_template['E LO']

def reset_pins():
    mpy.init_pins()

def analog_to_voltage(x):
    """Analog to digital voltage converter."""
    x = x*PY_vol/ADC_range
    return x

def COD_test():
    """Inputs 0-5V to COD board and checks H net voltage.\n 
    High and low tests are compared to allowable tolerances."""

    # Turn on COD pwr
    mpy.write_pin(COD_PWR, True)
    time.sleep(0.5) # Add delay for power to stabilize

    # High voltage (5V) test
    mpy.write_pin(COD_IN, True)
    time.sleep(0.5) # Add delay for high signal to settle
    COD_analog = mpy.get_cod_read()
    COD_hi_ret = COD_analog.decode('ascii').split()[1]
    debug_print(COD_hi_ret)
    COD_voltage_hi = analog_to_voltage(int(COD_hi_ret))
    debug_print(COD_voltage_hi)
    test_output['cod_hi_out'] = round(COD_voltage_hi, 3)

    # input('Measure COD_IN')

    # Low voltage (0V) test
    mpy.write_pin(COD_IN, False)
    time.sleep(0.5) # Add delay for low signal to settle/drain
    COD_analog = mpy.get_cod_read()
    COD_lo_ret = COD_analog.decode('ascii').split()[1]
    debug_print(COD_lo_ret)
    COD_voltage_lo = analog_to_voltage(int(COD_lo_ret))
    debug_print(COD_voltage_lo)
    test_output['cod_lo_out'] = round(COD_voltage_lo, 3)

    # Turn off COD pwr
    mpy.write_pin(COD_PWR, False)

    if COD_voltage_hi > tolerance_dict['COD_volt_hi'][0] and COD_voltage_hi < tolerance_dict['COD_volt_hi'][1]:
        test_output['cod_test_hi'] = True
        print("COD Test 1: Pass")
    else:
        test_output['cod_test_hi'] = False
        print("COD Test 1: Failed")
        print(test_output)

    if COD_voltage_lo > tolerance_dict['COD_volt_lo'][0] and COD_voltage_lo < tolerance_dict['COD_volt_lo'][1]:
        test_output['cod_test_lo'] = True
        print("COD Test 2: Pass")
    else:
        test_output['cod_test_lo'] = False
        print("COD Test 2: Failed")
        print(test_output)

def takt_start():
    gv.Takt_start_time = time.time()
    debug_print("Takt timer started.")

def takt_finish():
    gv.Takt_finish_time = time.time()
    duration = gv.Takt_finish_time - gv.Takt_start_time
    test_output['takt_time(s)'] = int(duration.__floordiv__(1))
    test_output['timestamp'] = str(int(gv.Takt_finish_time.__floordiv__(1)))
    print('Test time:' + str(test_output['takt_time(s)']) + " sec.")

def check_modbus(register, value):
    """Checks that the modbus is reading values before performing CTM test."""
    try:
        x = register
        debug_print(x)
        if x == value:
            return True
        else:
            return False
    except minimalmodbus.InvalidResponseError:
        print("Checksum error with modbus.")
        return False

def check_mod_recon(register, value):
    check_mod_count = 0
    while check_mod_count < 6:
        check_mod = check_modbus(register, value)
        if check_mod is False:
            check_mod_count += 1
            time.sleep(1)
            print("Checking modbus again...")
            continue
        elif check_mod_count == 5:
            return False
        elif check_mod is True:
            debug_print(register)
            return register

def CTM_test():
    """Sends message over CANbus channel and reads corresponding register on RS485."""
    try:
        check_mod = check_modbus(mod.device_type_0(), 193)
        print('This is mod: ' + str(check_mod))
    except:
        check_mod = False
    
    if check_mod is False:
        test_errors.append("RS485 read failure")
        check_mod_recon()
    
    try:
        CTM_id = mod.serial_number()
        print("The CTM serial number is: " + CTM_id)
        test_output['ctm_serial'] = CTM_id
    except minimalmodbus.InvalidResponseError:
        print("Checksum Error: Could not read CTM serial number")

    mpy.can_init()
    # Test 1
    mpy.write_pin(RELAY_PWR, False)
    mpy.send_can_msg_1()
    
    try:
        rpm1 = mod.rpm()
        debug_print(rpm1)
    except minimalmodbus.InvalidResponseError:
        mpy.send_can_msg_1()
        x = check_mod_recon(mod.rpm(), rpm_mod_read_1)
        if x is False:
            return
        else:
            rpm1 = x
            
    if rpm1 == rpm_mod_read_1:
        test_output['ctm_test_1'] = True
    else:
        test_output['ctm_test_1'] = False

    mpy.send_can_msg_2()
    
    try:
        rpm2 = mod.rpm()
        debug_print(rpm2)
    except minimalmodbus.InvalidResponseError:
        mpy.send_can_msg_2()
        x = check_mod_recon(mod.rpm(), rpm_mod_read_2)
        if x is False:
            return
        else:
            rpm2 = x
            
    if rpm2 == rpm_mod_read_2:
        test_output['ctm_test_1'] = True
    else:
        test_output['ctm_test_1'] = False

    if test_output['ctm_test_1'] is True:
        print("CTM Test 1: Passed")
    else:
        print("CTM Test 1: Failed")

    mpy.write_pin(RELAY_PWR, True)

    mpy.send_can_msg_3()
    try:
        rpm3 = mod.rpm()
        debug_print(rpm3)
    except minimalmodbus.InvalidResponseError:
        mpy.send_can_msg_3()
        x = check_mod_recon(mod.rpm(), rpm_mod_read_3)
        if x is False:
            return
        else:
            rpm3 = x
            
    if rpm3 == rpm_mod_read_3:
        test_output['ctm_test_2'] = True
    else:
        test_output['ctm_test_2'] = False

    mpy.send_can_msg_4()
    try:
        rpm4 = mod.rpm()
        debug_print(rpm4)
    except minimalmodbus.InvalidResponseError:
        mpy.send_can_msg_4()
        x = check_mod_recon(mod.rpm(), rpm_mod_read_4)
        if x is False:
            return
        else:
            rpm4 = x
            
    if rpm4 == rpm_mod_read_4:
        test_output['ctm_test_2'] = True
    else:
        test_output['ctm_test_2'] = False

    if test_output['ctm_test_2'] is True:
        print("CTM Test 2: Passed")
    else:
        print("CTM Test 2: Failed")

def MUX_select(a, b, c, bypass):
    """Multiplexer select. Input boolean True or False for 1 and 0 in order of A, B, C. """
    if bypass is False:
        mpy.write_pin(MUX_A, a)
        mpy.write_pin(MUX_B, b)
        mpy.write_pin(MUX_C, c)
    net = mpy.read_pin(MUX_OUT).decode('ascii').split()[1]
    return net

def continuity_test_summary():
    if net_check_count == 0:
        print("No errors.")
        test_output['continuity'] = True
    else:
        test_output['continuity'] = False
        # for x in range(len(net_error_msg)):
        #     print(net_error_msg[x])
    print(test_output)
    net_error_msg=[]

def compare_FET_pins():
    global net_check_count
    test1_B1 = mpy.write_pin(B1, True).decode('ascii').split()[3]
    debug_print(test1_B1)
    test1_B2 = mpy.read_pin(B2).decode('ascii').split()[1]
    debug_print(test1_B2)
    
    if test1_B1 == '1':
        if test1_B2 == '0':
            test_output['b_hi'] = True
            print("B HI: Passed")
        else:
            gv.test_output['b_hi'] = False
            print("B HI: Failed")
            error = "Check B net BLACK wire on Connector A and J4."
            net_error_msg.append(error)
            net_check_count += 1
    else:
        test_output['b_hi'] = False
        print("B HI: Failed")
        error = "Check B net BLACK wire on Connector A and J4."
        net_error_msg.append(error)
        net_check_count += 1
        
    test2_B2 = mpy.write_pin(B2, False).decode('ascii').split()[3]
    debug_print(test2_B2)
    test2_B1 = mpy.read_pin(B1).decode('ascii').split()[1]
    debug_print(test2_B1)
    
    if test2_B2 == '0':
        if test2_B1 == '1':
            test_output['b_lo'] = True
            print("B LO: Passed")
        else:
            test_output['b_lo'] = False
            print("B HI: Failed")
            error = "Check B net BLACK wire on Connector A and J4."
            net_error_msg.append(error)
            net_check_count+=1
    else:
        test_output['b_lo'] = False
        print("B HI: Failed")
        error = "Check B net BLACK wire on Connector A and J4."
        net_error_msg.append(error)
        net_check_count+=1

def compare_GPIO_MUX_pins(x,y,net,type):
    global net_check_count
    if type is True:
        test_type = "HI"
        test_logic = 1 
    else:
        test_type = "LO"
        test_logic = 0
    
    debug_print(test_logic)
    net1 = net + " " + test_type

    if net == 'D':
        pin_number = conn_A_pin_list[net]
    if net == 'E':
        pin_number = conn_A_pin_list[net] 
        
    if net != 'B':
        if x is not test_logic:
            connector = "A"
            pin_number = conn_A_pin_list[net]
        if y is not test_logic:
            connector = "F"
            pin_number = conn_F_pin_list[net]
            
        if x == y:
            net_check[net1] = True
            print(net1 + ": Passed")
        else:
            net_check[net1] = False
            ret_error = "Check " + net + " " + wire_colour_list[net] + " " + pin_number + " wire on Connector " + connector
            net_error_msg.append(ret_error)
            print(net1 + ": Failed")
            print(net_error_msg[net_check_count])
            net_check_count += 1
            #reset_pins()

def IO_control(net2, net_name, a, b, c):
    """Micropython IO control to perform continuity high and low tests."""
    if net_name != 'B':
        # Set pins high.
        test2_net2 = mpy.write_pin(net2, True).decode('ascii').split()[3]
        print(test2_net2)
        test2_net1 = MUX_select(a, b, c, False)
        print(test2_net1)
        compare_GPIO_MUX_pins(test2_net1, test2_net2, net_name, True)
        
        # Check that initialized low pins read low.
        test1_net2 = mpy.write_pin(net2, False).decode('ascii').split()[3]
        test1_net1 = MUX_select(a, b, c, True)
        compare_GPIO_MUX_pins(test1_net1, test1_net2, net_name, False)
    else:
        compare_FET_pins()

def continuity_test():
    """The continuity test checks individual nets using the Micropython GPIO pins.
    The nets include D, E, IN3, OUT, SDI_12, RS485A, RS485B and B."""

    IO_control(gv.B2, 'B', None, None, None)
    IO_control(gv.D2, 'D', False, False, False) # D1 => SN74HC151D D0
    IO_control(gv.E2, 'E', True, False, False) # E1 => SN74HC151D D1
    IO_control(gv.IN3_2, 'IN3', False, True, False) # IN3_2 => SN74HC151D D2
    IO_control(gv.OUT_2, 'OUT', True, True, False) # OUT => SN74HC151D D3
    IO_control(gv.SDI_12_2, 'SDI_12', False, False, True) # SDI_12_1 => SN74HC151D D4
    IO_control(gv.RS485B2, 'RS485B', True, False, True) # RS485B1 => SN74HC151D D5
    
    mpy.write_pin(gv.RS485_PWR, True) # Cuts signal from RS485 dongle (approx 2.5v)
    time.sleep(0.5)
    IO_control(gv.RS485A2, 'RS485A', False, True, True) # RS485A1 => SN74HC151D D6
    mpy.write_pin(gv.RS485_PWR, False)

# manual entry of manufacturer
def manf_oper():
    Manufacturer = input('\n\nPlease enter the manufacturer name: ')
    Operator = input('Please enter the operator name: ')
    
    if Manufacturer == '':
        print(colored("\n\n!!!!!Please do not leave any blank entry!!!!!", 'yellow'))
        manf_oper()
    elif Operator == '':
        print(colored('\n!!!!!Please do not leave any blank entry!!!!!', 'yellow'))
        manf_oper()
    else:
        gv.manufacturer = Manufacturer.upper()
        gv.operator = Operator.upper()

# manual entry of operator at CM
def check_operator_input():
    print("Manufacturer name:", gv.manufacturer)
    print("Operator name:", gv.operator)
    check_input = input('\nIs this correct(Y/N): ')
    check_input = check_input.upper()
    
    if check_input == 'N':
        gv.entry = False
    elif check_input == 'Y':
        gv.entry = True
        test_output['manufacturer'] = gv.manufacturer
        test_output['operator'] = gv.operator
        return
    elif check_input != 'Y' or check_input != 'N':
        print(colored('\n!!!!!Enter Valid Input!!!!!\n', 'yellow'))
        check_operator_input()

# scan in QR of WH132
def qr_scan():
    gv.qr_id = input(colored('\nPlease scan in QR on WH132 cable: ', 'white'))
    if len(gv.qr_id) != 14:
        print(colored('Scan in correct QR', 'yellow'))
        qr_scan()

# enter scans into dict
def enter_scans():
    test_output['device_id'] = gv.qr_id

# reset test dict
def reset_test_dict():
    manf = test_output['manufacturer']
    oper = test_output['operator']
    jig_id = test_output['jig_id']
    mpy_fw = test_output['micropy_fw_ver']

    for key in test_output.keys():
        test_output[key] = None

    test_output['manufacturer'] = manf
    test_output['operator'] = oper
    test_output['jig_id'] = jig_id
    test_output['micropy_fw_ver'] = mpy_fw

# check for any fails
def full_test_check():
    gv.test_output['PN'] = gv.part_no
    test_pass = all(x is not False for x in test_output.values())
    
    if test_pass is True:
        gv.test_output['test_pass'] = True
        print(colored('\n\n***** Test for ' + str(gv.test_output['device_id']) + ' passed *****', 'green'))
    else:
        gv.test_output['test_pass'] = False
        print(colored('\n\n***** Test for ' + str(gv.test_output['device_id']) + ' failed *****', 'red'))
