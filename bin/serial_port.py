'Hanle all serial ports related issues'

from __future__ import print_function
import re
import sys
import serial.tools.list_ports


def get_com_ports():
    """Get all the active com(serial) ports of the computer"""
    return list(serial.tools.list_ports.comports())


def print_com_ports():
    """Print the available com ports"""
    ports = get_com_ports()
    for port in ports:
        # print p.device
        # print p.description
        # print p.interface
        # print p.name
        # print p.manufacturer
        # print p.product
        print (port)


def find_arduino_ports(key=None):
    """Returns a list of com ports connected to arduino"""
    result = list()
    ports = get_com_ports()
    if key is None:
        key = 'Arduino'
    for port in ports:
        if re.match(key, port.description, re.IGNORECASE):
            result.append(port)
    return result


def get_desired_port():
    '''Return user the most likely port for arduino. If the logic cannot determine
     which one is the port of firmata arduino, then ask the user to choose'''
    ports = get_com_ports()

    if not ports:
        print ('there is no available port')
        print ('please plug in the target device and try again')
        sys.exit(1)
    elif len(ports) == 1:
        print (ports[0])
        return ports[0]
    result = 0
    while not (result > 0 and result <= len(ports)):
        i = 0
        for port in ports:
            i = i + 1
            print(i, '. ', port, sep='')
        result = int(raw_input("Which one is the target device? "))

    result = result - 1
    return ports[result]
