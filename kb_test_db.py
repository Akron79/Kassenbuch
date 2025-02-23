import sqlite3 as sl
from datetime import datetime
import traceback
import sys

def create_table(conn):
    with conn:
        #conn.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='st3' ''')
        #if conn.fetchone()[0]==1:
        conn.execute("""DROP TABLE if exists st3;""" )
        conn.execute("""
            CREATE TABLE st3 (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Bemerkung TEXT,
                Buchungstag DATE,
                Zugang BOOLEAN,
                Betrag NUMERIC,
                Zeitstempel DATE
                 );
                """)
    
def add_st(conn, d_tag, b_zugang, t_bem, f_betrag):
    sql = 'INSERT INTO st3 (Bemerkung, Buchungstag, Zugang, Betrag, Zeitstempel) values(?, ?, ?, ?, ?)'
    data = [t_bem, d_tag, b_zugang, f_betrag, datetime.now()]
    now = datetime.now()
    #with conn:
    #    conn.executemany(sql, data)
    print('Füge ein.')
    try:
        conn.execute(sql, data)
        conn.commit()
    except sl.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        #con.close()

def get_buchungen(conn):
    with conn:
        data = conn.execute("SELECT * FROM st3")
        for row in data:
            print(row)

def main():
    con = sl.connect('kb-test.db')
    now = datetime.now()
    create_table(con)
    #add_buchung(con, now, True, 'bla', 12.4)
    print('hier')
    add_st(con, now, True, 'bla', 12.4)
    get_buchungen(con)    
    
main()    