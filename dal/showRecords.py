import sqlite3

conn = sqlite3.connect('/home/pi/Programs/ua-lpr/localpass.db')

cur = conn.execute('SELECT * FROM Access')

print 'Id, Plate, TS, Access'

for row in cur:
    show = ''
    i = 1
    for col in row:
        if i != len(row):
            show += str(col) + ', '
            i += 1
        else:
            show += str(col)
    print show

conn.close()
    
