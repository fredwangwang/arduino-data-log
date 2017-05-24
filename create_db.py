import sqlite3

conn = sqlite3.connect('data.db')

ps_createSensorInfo = '''
DROP TABLE IF EXISTS sensors;
CREATE TABLE sensors(
    id          INTEGER PRIMARY KEY,
    type        TEXT,
    calibrated  BOOLEAN1 DEFAULT 0,
    last_cal    DATE
    );
'''
ps_createSensorData = '''
DROP TABLE IF EXISTS data;
CREATE TABLE data(
    id          INTEGER PRIMARY KEY,
    sensor_id   INTEGER,
    data        DOUBLE,
    time        DATETIME,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id)
    );
'''
ps_defineSensors = '''
INSERT INTO sensors(type, last_cal) VALUES(?, CURRENT_DATE)
'''

sensors = [
    ('nh4', ),
    ('no3', )
]

conn.executescript(ps_createSensorInfo)
conn.executescript(ps_createSensorData)
conn.executemany(ps_defineSensors, sensors)

conn.commit()
conn.close()