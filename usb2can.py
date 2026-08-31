from global_vars import *
import global_vars as gv
import modbusRS485 as mod


def can_configuration():
    global dev
    devs = GsUsb.scan()
    if len(devs) == 0:
        print("Can not find gs_usb device")
        return
    #print(devs)    
    dev = devs[0]
    print(dev)
    #dev.stop() 

    # Configuration
    if not dev.set_bitrate(250000):
        print("Can not set bitrate for gs_usb")
        return
    dev.start(GS_CAN_MODE_LOOP_BACK)


def send_ctm_msg_1(x, y):
    global rpm_val
    # Prepare frames
    # data = b"\xFF\x7D\x8D\xE0\x00\x00\xFF\xFF"
    # data = b"\x12\x34\x56\x78\x9A\xBC\xDE\xF0"
    data=x
    #sff_frame = GsUsbFrame(can_id=0x7FF, data=data)
    #sff_none_data_frame = GsUsbFrame(can_id=0x7FF)
    #err_frame = GsUsbFrame(can_id=0x7FF | CAN_ERR_FLAG, data=data)
    eff_frame = GsUsbFrame(can_id=gv.MESSAGE_ID_RPM| CAN_EFF_FLAG, data=data)
    eff_none_data_frame = GsUsbFrame(can_id=gv.MESSAGE_ID_RPM | CAN_EFF_FLAG)
    #rtr_frame = GsUsbFrame(can_id=0x7FF | CAN_RTR_FLAG)
    rtr_with_eid_frame = GsUsbFrame(can_id=gv.MESSAGE_ID_RPM | CAN_RTR_FLAG | CAN_EFF_FLAG)
    rtr_with_data_frame = GsUsbFrame(can_id=gv.MESSAGE_ID_RPM | CAN_RTR_FLAG, data=data)
    frames = [
        # sff_frame,
        # sff_none_data_frame,
        # err_frame,
        eff_frame,
        eff_none_data_frame,
        #rtr_frame,
        rtr_with_eid_frame,
        rtr_with_data_frame,
    ]
    # data = x
    # eff_frame = GsUsbFrame(can_id=gv.MESSAGE_ID_RPM | CAN_EFF_FLAG, data=data)     # eff = extended frame format

    # Send frame
    for i in range(len(frames)):
        iframe = GsUsbFrame()
        if dev.read(iframe, 1):
            print("RX  {}".format(iframe))
        if dev.send(frames[i]):
            print("TX  {}".format(frames[i]))

    #dev.stop()

    rpm = mod.rpm()

    print(rpm)
    if y == 1:
        rpm_val = gv.rpm_mod_read_1
    elif y == 2:
        rpm_val = gv.rpm_mod_read_2
    elif y == 3:
        rpm_val = gv.rpm_mod_read_3
    elif y == 4:
        rpm_val = gv.rpm_mod_read_4

    if rpm == rpm_val:
        print("CTM Test 1: Passed")
        gv.test_output['CTM_Test_1'] = "Passed"
    else:
        print("CTM Test 1: Failed")
        gv.test_output['CTM_Test_1'] = "Failed"


def send_ctm_msg_2(x,y):
    global rpm_val
    # Prepare frames
    #data = x
    #eff_frame = GsUsbFrame(can_id=gv.MESSAGE_ID_RPM | CAN_EFF_FLAG, data=data)     # eff = extended frame format
    data=x
    #sff_frame = GsUsbFrame(can_id=0x7FF, data=data)
    #sff_none_data_frame = GsUsbFrame(can_id=0x7FF)
    #err_frame = GsUsbFrame(can_id=0x7FF | CAN_ERR_FLAG, data=data)
    eff_frame = GsUsbFrame(can_id=gv.MESSAGE_ID_RPM| CAN_EFF_FLAG, data=data)
    eff_none_data_frame = GsUsbFrame(can_id=gv.MESSAGE_ID_RPM | CAN_EFF_FLAG)
    #rtr_frame = GsUsbFrame(can_id=0x7FF | CAN_RTR_FLAG)
    rtr_with_eid_frame = GsUsbFrame(can_id=gv.MESSAGE_ID_RPM | CAN_RTR_FLAG | CAN_EFF_FLAG)
    #rtr_with_data_frame = GsUsbFrame(can_id=0x7FF | CAN_RTR_FLAG, data=data)
    frames = [
        # sff_frame,
        # sff_none_data_frame,
        # err_frame,
        eff_frame,
        eff_none_data_frame,
        #rtr_frame,
        rtr_with_eid_frame,
        #rtr_with_data_frame,
    ]


    # Send frame
    for i in range(len(frames)):
        iframe = GsUsbFrame()
        if dev.read(iframe, 1):
            print("RX  {}".format(iframe))
        if dev.send(frames[i]):
            print("TX  {}".format(frames[i]))
    # # Send frame
    # dev.send(eff_frame)
    # print("TX  {}".format(eff_frame))
    # time.sleep(0.5)

    # read_frame = GsUsbFrame()
    # dev.read(read_frame, 100)
    # # if read_frame.can_id & CAN_ERR_FLAG != CAN_ERR_FLAG:
    # print("RX  {}".format(read_frame))
    # read_frame = GsUsbFrame()
    # dev.read(read_frame, 100)
    # # if read_frame.can_id & CAN_ERR_FLAG != CAN_ERR_FLAG:
    # print("RX  {}".format(read_frame))


    rpm = mod.rpm()
    print(rpm)
    if y == 1:
        rpm_val = gv.rpm_mod_read_1
    elif y == 2:
        rpm_val = gv.rpm_mod_read_2
    elif y == 3:
        rpm_val = gv.rpm_mod_read_3
    elif y == 4:
        rpm_val = gv.rpm_mod_read_4
    if rpm == rpm_val:
        print("CTM Test 2: Passed")
        gv.test_output['CTM_Test_2'] = "Passed"
    else:
        print("CTM Test 2: Failed")
        gv.test_output['CTM_Test_2'] = "Failed"

