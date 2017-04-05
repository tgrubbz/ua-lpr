import sqlite3

def connect():
    return sqlite3.connect('/home/pi/Programs/ua-lpr/localpass.db', detect_types = sqlite3.PARSE_DECLTYPES)


def exists(table):
    conn = connect()
    cur = conn.execute('''
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?''', (table,))
    return cur.fetchone() != None


def createAccessTable():
    conn = connect()
    conn.execute('''
        CREATE TABLE Access
        (
            Id          INTEGER PRIMARY KEY AUTOINCREMENT,
            Plate       TEXT    UNIQUE      NOT NULL,
            Timestamp   TEXT                NOT NULL,
            Access      BIT                 NOT NULL
        );''')
    

def addAccess(record):
    if not exists('Access'):
        createAccessTable()

    conn = connect()
    cur = conn.execute('''
        INSERT INTO Access
        (Plate, Timestamp, Access)
        VALUES
        (:plate, :timestamp, :access)
        ''', record)
    conn.commit()
    return cur.rowcount


def readAccess(plate):
    if not exists('Access'):
        createAccessTable()

    conn = connect()
    cur = conn.execute('SELECT * FROM Access WHERE Plate = ?', (plate,))

    row = cur.fetchone()

    if row == None:
        return False
    
    return row['Access']


def removeAccess(plate):
    if not exists('Access'):
        createAccessTable()

    conn = connect()
    cur = conn.execute('DELETE FROM Access WHERE Plate = ?', (plate,))
    conn.commit()
    return cur.rowcount


def updateAccess(record):
    if not exists('Access'):
        createAccessTable()

    conn = connect()
    cur = conn.execute('''
        UPDATE Access SET
            Plate = :plate,
            Timestamp = :timestamp,
            Access = :access
        ''', record)
    conn.commit()
    return cur.rowcount
    
