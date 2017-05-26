import sqlite3
import csv
import time
from datetime import date, timedelta
from collections import defaultdict

ps_insert = """INSERT INTO data(sensor, data, time, second) VALUES(?, ?, ?, ?)"""
ps_get = """SELECT second, time, data FROM data WHERE time > ? AND sensor = ? AND second % ? = 0 ORDER BY second"""

DEBUG = True
conn = sqlite3.connect('data.db')


def insert_data(data):
    '''Pass the value, insert the data into db'''
    for key, value in data.iteritems():
        conn.execute(
            ps_insert, (key, value, time.strftime("%Y-%m-%d %H:%M:%S"), int(time.time())))
    conn.commit()


def insert_data_from_board(board):
    insert_data(board.read_sensor_data())


def make_header(cfg):
    header = ['time']
    for port in cfg['ports']:
        header.append(cfg['ports'][port])
    return header


def gen_file_name(cfg, interv=0):
    path = cfg['directory'] + '/'
    if interv == 0:
        return path + time.strftime("%Y%m%d") + '.csv'
    return path + time.strftime("%Y%m%d") + '_' + str(interv) + 'sec.csv'


def get_readings(conn, cfg, interv, date_str):
    readings = []
    for port in cfg['ports']:
        sensor = cfg['ports'][port]
        if not sensor == 'none':
            cursor = conn.execute(ps_get, (date_str, sensor, interv))
            readings.append(cursor.fetchall())
    return readings


def refactor_rows(rds):
    '''pass in the readings, return a result list'''
    result = []
    i = 0
    rows_refactor = defaultdict(list)
    for read in rds:
        for row in read:
            second = row[0]
            timestamp = row[1]
            data = row[2]
            if not rows_refactor[second]:
                rows_refactor[second].append(timestamp)
                rows_refactor[second].extend([None] * i)
            rows_refactor[second].append(data)
    keylist = rows_refactor.keys()
    keylist.sort()
    for key in keylist:
        result.append(rows_refactor[key])
    return result


def query_to_csv(header, rds, file_name):
    rows = refactor_rows(rds)
    with open(file_name, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(header)
        spamwriter.writerows(rows)


def write_to_csv(cfg):
    '''Call this function with cfg file to write to the output csv'''
    start = time.clock()

    yesterday = date.today() - timedelta(1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    for lvl in cfg['rate']:
        interval = cfg['rate'][lvl]
        if interval != 0:
            header = make_header(cfg)
            file_name = gen_file_name(cfg, interval)
            readings = get_readings(conn, cfg, interval, yesterday_str)
            query_to_csv(header, readings, file_name)

    end = time.clock()
    print 'output to csv in', "%.3f" %(end - start), 'second'
