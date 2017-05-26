import sqlite3

conn = sqlite3.connect('data.db')

ps_createSensorInfo = '''
DROP TABLE IF EXISTS sensors;
CREATE TABLE sensors(
    id          INTEGER PRIMARY KEY,
    type        TEXT,
    calibrated  BOOLEAN DEFAULT 0,
    last_cal    DATE
    );
'''
ps_createSensorData = '''
DROP TABLE IF EXISTS data;
CREATE TABLE data(
    id          INTEGER PRIMARY KEY,
    sensor      TEXT,
    data        DOUBLE,
    time        DATETIME,
    second      INTEGER,
    FOREIGN KEY (sensor) references sensors(type)
    );
'''

ps_defineSensors = '''
INSERT INTO sensors(type, last_cal) VALUES(?, CURRENT_DATE)
'''

sensors = [
    ('ammonium', ),
    ('nitrate', ),
    ('none', )
]

conn.executescript(ps_createSensorInfo)
conn.executescript(ps_createSensorData)
conn.executemany(ps_defineSensors, sensors)

conn.commit()
conn.close()
