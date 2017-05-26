'''The is a wrap up class for firmata and vernier shield interface'''

import sys
from pyfirmata import Arduino, util
from calculation import calc_bta_ise_conc_from_raw
from serial_port import get_desired_port


class VernierBoard(object):
    '''The is a wrap up class for firmata and vernier shield interface'''

    def __init__(self, port):
        '''start a board class'''
        self._board = Arduino(port.device)
        self._muxpins = dict()
        self._muxpins['MSB'] = self._board.get_pin('d:11:o')
        self._muxpins['LSB'] = self._board.get_pin('d:10:o')
        self._cfg = []
        self._sensor = dict()
        self._sensor['analog1'] = self._board.get_pin('a:0:i')
        self._sensor['analog2'] = self._board.get_pin('a:2:i')
        self._sensor['digital1'] = self._board.get_pin('d:2:i')
        self._sensor['digital2'] = self._board.get_pin('d:6:i')
        self._it = util.Iterator(self._board)
        self._it.start()

    def set_mux(self, connector_num):
        '''connector_num is a number from 0 to 3 which identifies which connector
        to switch the MUX to. Where if connector num is equal to:

        0 --> Analog 1

        1 --> Analog 2

        2 --> Digital 1

        3 --> Digital 2'''
        # MUXLSB = 10
        # MUXMSB = 11

        if connector_num == 0:  # ANALOG 1 - MUX ADDR 00
            self._muxpins['MSB'].write(0)
            self._muxpins['LSB'].write(0)
        elif connector_num == 1:  # ANALOG 2 - MUX ADDR 01
            self._muxpins['MSB'].write(0)
            self._muxpins['LSB'].write(1)
        elif connector_num == 2:  # DIGITAL 1 - MUX ADDR 10
            self._muxpins['MSB'].write(1)
            self._muxpins['LSB'].write(0)
        elif connector_num == 3:  # DIGITAL 2 - MUX ADDR 11
            self._muxpins['MSB'].write(1)
            self._muxpins['LSB'].write(1)

    def set_mux_based_on_port(self, port_name):
        '''Set the mux based on the port name be passed in. Valid
        ports: [analog1, analog2, digital1, digital2]'''
        valid_ports = ['analog1', 'analog2', 'digital1', 'digital2']
        try:
            self.set_mux(valid_ports.index(port_name))
        except ValueError:
            print port_name, 'is not a valid port name'
            sys.exit(1)

    def set_cfg(self, cfg):
        '''Set the cfg to correctly read the sensor data'''
        self._cfg = cfg

    def read_sensor_data_raw(self):
        '''THIS FUNCTION MUST BE CALLED AFTER CALLING //set_cfg//
        Reads the RAW sensor data according to the cfg, and return a dict'''
        result = dict()
        for port in self._cfg['ports']:
            sensor = self._cfg['ports'][port]
            if not sensor == 'none':
                self.set_mux_based_on_port(port)
                val = self._sensor[port].read()
                result[sensor] = val
        return result

    def read_sensor_data(self):
        '''THIS FUNCTION MUST BE CALLED AFTER CALLING //set_cfg//
        Reads the sensor data in CONCENTRATION according to the cfg, and return a dict'''
        data = self.read_sensor_data_raw()
        keys = data.keys()
        for key in keys:
            rval = data[key]
            data[key] = calc_bta_ise_conc_from_raw(
                rval, self._cfg['calibration'][key])
            print key, "%.4f" % data[key]
        print ''
        return data


def debug():
    '''Test the functionality of the board'''
    port = get_desired_port()
    board = VernierBoard(port)
    while True:
        port_name = str(input('Which port?'))
        board.set_mux_based_on_port(port_name)
        print 'done'


if __name__ == '__main__':
    debug()
