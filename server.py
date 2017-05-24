"""This is the main executable of the data logging server. """

import re
import time
import sqlite3
import schedule
import serial.tools.list_ports
from pyfirmata import Arduino, util

CFGFILENAME = 'config.yml'

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
        print port


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
######################################################
ps = """INSERT INTO data(sensor_id, data, time) VALUES(?, ?, CURRENT_TIMESTAMP)"""
# ps_get10sec = """SELECT data, """
# ps_get60sec
# ps_get600sec

arduinoPorts = find_arduino_ports()
board = Arduino(arduinoPorts[0].device)
print board.firmata_version
it = util.Iterator(board)
it.start()

analog0 = board.get_pin('a:0:i')
analog1 = board.get_pin('a:1:i')
digi14 = board.get_pin('a:4:i')
digi15 = board.get_pin('a:5:i')

conn = sqlite3.connect('data.db')

def print_sth():
    print 'this works'

def collect_data():
    val0 = analog0.read()
    val1 = analog1.read()
    print val0
    print val1
    conn.execute(ps, (1, val0))
    conn.execute(ps, (2, val1))
    conn.commit()

def output_csv():
    asd = 0

def read_digi():
    val0 = digi14.read()
    val1 = digi15.read()
    print val0
    print val1

schedule.every(10).seconds.do(collect_data)
schedule.every().day.at('00:01').do(print_sth)
schedule.every().second.do(read_digi)

# main loop
while True:
    schedule.run_pending()
    time.sleep(1)
