import SN74HC151D


# Initialize GPIO pins
RS485A2 = Pin('Y1', Pin.IN)
RS485B2 = Pin('Y2', Pin.IN)
IN3_2 = Pin('Y3', Pin.IN)
OUT_2 = Pin('Y4', Pin.IN)
SDI_12_2 = Pin('Y5', Pin.IN)
B1 = Pin('Y11', Pin.IN)
B2 = Pin('Y12', Pin.IN)

# Initialize state variables
PWR = 1
GND = 0

net_check = {
    'RS485A':'-',
    'RS485B':'-',
    'IN3':'-', 
    'OUT':'-',
    'SDI_12':'-',
    'B':'-',
    'D':'-',
    'E':'-'
    }

net_check_count = 0

def compare_pins(x,y,net):
    print('x: ' + str(x) + ' y: ' + str(y))
    if x == y:
        net_check[net] = "Passed"
    elif net == "B":
        if B1 is not B2:
            if B2 == GND:
                net_check[net] = "Passed"
            else:
                net_check[net] = "Failed" + "-" + "B2 not GND"
                net_check_count += 1
        else:
            net_check[net] = "Failed"
            net_check_count += 1
    else:
        net_check[net] = "Failed"
        net_check_count += 1


compare_pins(SN74HC151D.D0(), PWR, 'D')
compare_pins(SN74HC151D.D1(), GND, 'E')
compare_pins(SN74HC151D.D2(), IN3_2.high(), 'IN3')
compare_pins(SN74HC151D.D3(), OUT_2.high(), 'OUT')
compare_pins(SN74HC151D.D4(), SDI_12_2.high(), 'SDI_12')
compare_pins(SN74HC151D.D5(), RS485B2.high(), 'RS485B')
compare_pins(SN74HC151D.D6(), RS485A2.high(), 'RS485A')
compare_pins(B1, B2, 'B')


