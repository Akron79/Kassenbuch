import kb_datebase as db
import csv
from datetime import datetime

class writer():
    def __init__(self, FileName):
        self.CsvFile = open (file=FileName,mode='w', newline='')
        self.o_writer = csv.writer(self.CsvFile, delimiter=';')
        
    def close(self):
        self.CsvFile.close()

    def insert_to_table(connection, Monat, Jahr, Anfangsbestand, Endbestand):
        # print('versuche erstellung')
        FileName = f'DatevExport_{Jahr}{str(Monat).zfill(2)}.csv'
        # print('piep 1')
        db.sqli.create_datev(connection, Monat, Jahr)
        # print('piep 2')
        db.sqli.get_select_datev(connection,'kassenbuch', Monat, Jahr, Anfangsbestand, Endbestand)
        # print('piep 3')
        db.sqli.select_datev_for_export(connection, FileName)
        # print('piep 4')

    def export_csv(self):
        data1 = ['aa', 'bb', '', '4', '5']
        data2 = ['cc', 'ddd', '6', '7', '8']
        self.o_writer.writerow(data1)
        self.o_writer.writerow(data2)
        pass

    def write_row():
        pass

    def intern_write_row(self, Row):
        self.o_writer.writerow(Row)
        pass