'''This module contains the calculation for vernier sensors '''

import math

def calc_bta_ise_conc_from_raw(voltage, cal):
    '''given a voltage reading, calc
     Vernier analog (BTA) Ion Selective Electrode (ISE) sensor reading (Concentration)'''
    electrode_reading = 137.55 * voltage - 0.1682
    val = (electrode_reading - cal['Eo'])/ cal['m']
    conc = math.exp(val)
    return conc
