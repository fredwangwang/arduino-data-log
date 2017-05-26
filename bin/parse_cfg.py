"""This module parses the configuration of the server."""

import sys
import yaml


def load_config(filename):
    """Given the file name as param, load the yml configuration and return the cfg as a dict"""
    cfg_file = open(filename, 'r').read()
    cfg = yaml.load(cfg_file)
    return cfg


def sanitize_config(cfg):
    '''check if the configuration is a valid cfg, and will fix some minor flaws in cfg
     and return a valid one'''
    valid_sensors = ['ammonium', 'nitrate', 'none']

    # parse port settings. Not set allowed
    if not 'ports' in cfg:
        print 'ports settings missing in the configuration file, will use DEFAULT:'
        print 'analog1: ammonium'
        print 'analog2: nitrate'
        cfg['ports'] = dict()
        cfg['ports']['analog1'] = 'ammonium'
        cfg['ports']['analog2'] = 'nitrate'
    else:
        for port in cfg['ports']:
            if not cfg['ports'][port] in valid_sensors:
                print cfg['ports'][port], 'is not a valid sensor setting.'
                sys.exit(1)

    # parse calibration settings. Must set
    if not 'calibration' in cfg:
        print 'Error: calibration settings missing in the configuration file!'
        sys.exit(1)
    else:
        for sensor in cfg['calibration']:
            cal_dict = cfg['calibration'][sensor]
            if not ('Eo' in cal_dict and 'm' in cal_dict):
                print 'Error: missing Eo or m for sensor', sensor
                sys.exit(1)

    if not 'rate' in cfg:
        print 'rate settings missing in the configuration file, will use DEFAULT:'
        print 'level1: 5'
        print 'level2: 0'
        print 'level3: 0'
        cfg['rate'] = dict()
        cfg['rate']['level1'] = 5
        cfg['rate']['level2'] = 0
        cfg['rate']['level3'] = 0
    print '\n\nFinish importing the configuration!\n\n'
    return cfg


def get_config(filename):
    '''Try to get a perfectly valid config. Return good cfg or exit the program'''
    cfg = load_config(filename)
    return sanitize_config(cfg)


def print_sections(cfg):
    """Print detailed sections content of the config file"""
    for section in cfg:
        print section
        print_section(section, cfg)


def print_section(sec, cfg):
    """Print the selected section content of the config file"""
    print cfg[sec]


def yes_or_no(question):
    'Yes or no?'
    reply = str(raw_input(question + ' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")


if __name__ == '__main__':
    # if yes_or_no("Do you want to try loading the configuration file?"):
    #     FILENAME = str(raw_input('File name: ')).strip()
    #     CFG = get_config(FILENAME)
    #     print_sections(CFG)
    CFG = get_config('config.yml')
    print_sections(CFG)
