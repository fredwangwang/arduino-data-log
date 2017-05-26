"""This is the main executable of the data logging server. """

import sys
import time
import threading
import functools
import schedule
import database
from serial_port import get_desired_port
from vernier_board import VernierBoard
from parse_cfg import get_config

CFGFILENAME = 'config.yml'


def schedule_data_collector(board):
    schedule.every().second.do(database.insert_data_from_board, board)


def schedule_csv_writer(cfg):
    #sschedule.every().day.at('00:01').do(database.write_to_csv, cfg)
    schedule.every(2).hours.do(database.write_to_csv, cfg)


def setup():
    cfg = get_config(CFGFILENAME)

    port = get_desired_port()
    board = VernierBoard(port)
    board.set_cfg(cfg)

    schedule_data_collector(board)
    schedule_csv_writer(cfg)
    print 'finish setup, start to collect data...\n'


def run():
    '''Start the scheduler'''
    while True:
        schedule.run_pending()
        time.sleep(.2)


if __name__ == '__main__':
    setup()
    run()
