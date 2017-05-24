"""This module parses the configuration of the server."""

import yaml


def load_config(filename):
    """Given the file name as param, load the yml configuration and return the cfg as a dict"""
    cfg_file = open(filename, 'r').read()
    cfg = yaml.load(cfg_file)
    return cfg


def print_sections(cfg):
    """Print detailed sections content of the config file"""
    for section in cfg:
        print section
        print_section(section, cfg)


def print_section(sec, cfg):
    """Print the selected section content of the config file"""
    print cfg[sec]


def get_cfg_nh4(cfg):
    """Get configuration of nh4"""
    a = 0


def get_cfg_no3(cfg):
    """Get configuration of no3"""
    a = 0
