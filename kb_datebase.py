import sqlite3 as sl
from datetime import datetime, timedelta
import traceback
from tkinter.messagebox import showinfo
import kb_datev_export as datev
import sys
import os.path

class KeineDaten(Exception):
    pass

class sqli(sl.Connection):
    def __init__(self,file_name, table_name):
        if not(os.path.isfile(file_name + '.db')):
            self.con = sl.connect(file_name + '.db')
            self.create_table(table_name)
            self.create_kostenstellen()
            self.create_steuersaetze()
        else:
            self.con = sl.connect(file_name + '.db')

    def insert_values(self, data, sql):
        try:
            print('try to insert values...')
            self.con.execute(sql, data)
            self.con.commit()
        except sl.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
    

    def execute_sql(self, sql):
        try:
            self.con.execute(sql)
            self.con.commit()
        except sl.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
    
    def select_values(self, sql_text):
        try:
            with self.con:
                data = self.con.execute(sql_text)     #(sql=sql_text)      
            return data
 
        except sl.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
    
    def select_one(self, sql_text):
    
        try:
            with self.con:
                cursor = self.con.cursor()
                # print(sql_text)
                cursor.execute(sql_text)
                rec = cursor.fetchone()
                # print('Cursor fertig.')
            if not (rec):
                # showinfo(title='Warnung', message='raise KEINE DATEN')
                raise KeineDaten
            else:
                # print('Daten gefunden-')
                data = rec[0]          
            return data
        except KeineDaten:
             pass
                
        except sl.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        except:
             showinfo(title='Warnung', message='Ein Fehler, einf Fehler!!')
            
    
    def create_steuersaetze(self):
        with self.con:
            self.con.execute(f"""DROP TABLE if exists steuersaetze;""" )
            self.con.execute(f"""
                CREATE TABLE steuersaetze (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Steuersatz NUMERIC,
                    Bezeichnung TEXT
                    );
                    """)
        sql = f'INSERT INTO steuersaetze ( Steuersatz, Bezeichnung) values(?, ?)'
        
        data = [ 0, 'ohne Steuer']
        self.insert_values(data, sql)    
        
        data = [ 7, 'Lebensmittel']
        self.insert_values(data, sql)    
        
        data = [19, 'Sonstiges']
        self.insert_values(data, sql)    
        
    def create_kostenstellen(self):
        with self.con:
            self.con.execute(f"""DROP TABLE if exists kostenstellen;""" )
            self.con.execute(f"""
                CREATE TABLE kostenstellen (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Kostenstelle TEXT,
                    Bezeichnung TEXT
                    );
                    """)
        sql = f'INSERT INTO kostenstellen ( Kostenstelle, Bezeichnung) values(?, ?)'
        
        data = ['100', 'Sonstiges']
        self.insert_values(data, sql)    
        
        data = ['101', 'Lebensmittel']
        self.insert_values(data, sql)    
        
        data = ['102', 'Getränke']
        self.insert_values(data, sql)    
        
        data = ['103', 'Putzmittel']
        self.insert_values(data, sql)    
        
        data = ['104', 'Küchenbedarf']
        self.insert_values(data, sql)    
              
        data = ['105', 'Klopapier']
        self.insert_values(data, sql)    

        data = ['106', 'Umsatz']
        self.insert_values(data, sql)    
        
        data = ['107', 'Pfand/Umsatz']
        self.insert_values(data, sql)    

        data = ['108', 'Gutschein/Umsatz']
        self.insert_values(data, sql)    

        data = ['109', 'Bürobedarf']
        self.insert_values(data, sql)    

        data = ['110', 'Reparaturbedarf']
        self.insert_values(data, sql)    

        data = ['111', 'Tanken']
        self.insert_values(data, sql)    

        data = ['112', 'Autowerkstatt']
        self.insert_values(data, sql)    

        data = ['113', 'Dekobedarf']
        self.insert_values(data, sql)    

        data = ['114', 'Cateringbedarf']
        self.insert_values(data, sql)    
        

    def create_table(self, tabel_name):
        with self.con:
            #conn.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='st3' ''')
            #if conn.fetchone()[0]==1:
            self.con.execute(f"""DROP TABLE if exists {tabel_name};""" )
            self.con.execute(f"""
                CREATE TABLE {tabel_name} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Buchungstag DATE,
                    Zugang NUMERIC,    
                    Betrag NUMERIC,
                    Steuersatz NUMERIC,
                    Kostenstelle TEXT,
                    Bemerkung TEXT,
                    Zeitstempel DATE,
                    CHECK (ZUGANG = 1 OR Zugang = -1)
                    );
                    """)
            self.con.execute(f"""DROP TABLE if exists monatsabschluss;""" )
            self.con.execute(f"""
                CREATE TABLE monatsabschluss (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Jahr NUMERIC,
                    Monat NUMERIC,
                    Anfangsbestand NUMERIC,
                    Endbestand NUMERIC,
                    Gueltig BOOLEAN,
                    Zeitstempel DATE
                    );
                    """)
        
    def add_buchung(self, tabel_name, d_tag, b_zugang, f_betrag, i_steuersatz, t_kostenstelle, t_bem):
        sql = f'INSERT INTO {tabel_name} ( Buchungstag, Zugang, Betrag, Steuersatz, Kostenstelle, Bemerkung, Zeitstempel) values(?, ?, ?, ?, ?, ?, ?)'
        data = [d_tag, b_zugang, f_betrag, i_steuersatz, t_kostenstelle, t_bem, datetime.now()]
        self.insert_values(data, sql)

    def get_last15(self, tabel_name):
        with self.con:
            data = self.con.execute(f"""SELECT 
                                      id
                                    , Buchungstag
                                    , CASE WHEN Zugang = 1 Then 'Zugang' ELSE 'Abgang' END
                                    , cast(format("%.2f",Betrag) as text) 
                                    , cast(Steuersatz as TEXT) || '%'
                                    , Kostenstelle
                                    , Bemerkung
                                    , datetime(Zeitstempel) 
                                    FROM {tabel_name} ORDER BY id desc LIMIT 15""")
            return data
    
    def get_spalten(self, tabel_name):
        with self.con:
            data = self.con.execute(f"SELECT name FROM pragma_table_info('{tabel_name}') ORDER BY cid")
            return data
        
    def get_kostenstellen(self):
        with self.con:
            data = self.con.execute(f"SELECT Kostenstelle, Bezeichnung FROM kostenstellen ORDER BY Kostenstelle")
            return data

    def get_steuersaetze(self):
        with self.con:
            data = self.con.execute(f"SELECT Steuersatz, Bezeichnung FROM steuersaetze ORDER BY Steuersatz")
            return data

    def create_datev(self, Monat, Jahr):
        d_ErsterDesMonats = datetime(Jahr, Monat, 1)
        d_letzterDesMonats = d_ErsterDesMonats.replace(month=Monat +1) - timedelta(days=1) 
        d_ErsterDesJahres = d_ErsterDesMonats.replace(month=1)

        s_ErsterDesMonats = d_ErsterDesMonats.strftime("%Y%m%d")
        s_letzterDesMonats = d_letzterDesMonats.strftime("%Y%m%d")
        s_ErsterDesJahres = d_ErsterDesJahres.strftime("%Y%m%d")
        s_timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        try:
            print('Drop datevexport')
            with self.con:
                self.con.execute(f"""DROP TABLE if exists datevexport""" )
                self.con.execute(f"""
                CREATE TABLE datevexport (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        'A' TEXT,B TEXT,C TEXT,D TEXT,E TEXT,F TEXT,G TEXT,H TEXT,I TEXT,J TEXT,K TEXT,L TEXT,M TEXT,N TEXT,O TEXT,P TEXT,Q TEXT,R TEXT,S TEXT,T TEXT,U TEXT,V TEXT,W TEXT,X TEXT,Y TEXT,Z TEXT
                    ,AA TEXT,AB TEXT,AC TEXT,AD TEXT,AE TEXT,AF TEXT,AG TEXT,AH TEXT,AI TEXT,AJ TEXT,AK TEXT,AL TEXT,AM TEXT,AN TEXT,AO TEXT,AP TEXT,AQ TEXT,AR TEXT,'A_S' TEXT,AT TEXT,AU TEXT,AV TEXT,AW TEXT,AX TEXT,AY TEXT,AZ TEXT
                    ,BA TEXT,BB TEXT,BC TEXT,BD TEXT,BE TEXT,BF TEXT,BG TEXT,BH TEXT,BI TEXT,BJ TEXT,BK TEXT,BL TEXT,BM TEXT,BN TEXT,BO TEXT,BP TEXT,BQ TEXT,BR TEXT,BS TEXT,BT TEXT,BU TEXT,BV TEXT,BW TEXT,BX TEXT,BY TEXT,BZ TEXT
                    ,CA TEXT,CB TEXT,CC TEXT,CD TEXT,CE TEXT,CF TEXT,CG TEXT,CH TEXT,CI TEXT,CJ TEXT,CK TEXT,CL TEXT,CM TEXT,CN TEXT,CO TEXT,CP TEXT,CQ TEXT,CR TEXT,CS TEXT,CT TEXT,CU TEXT,CV TEXT,CW TEXT,CX TEXT,CY TEXT,CZ TEXT
                    ,DA TEXT,DB TEXT,DC TEXT,DD TEXT,DE TEXT,DF TEXT,DG TEXT,DH TEXT,DI TEXT,DJ TEXT,DK TEXT,DL TEXT                     
                        );
                        """)
            sql = f'''INSERT INTO datevexport ( 'A',	'B',	'C',	'D',	'E',	'F',	'G',	'H',	'I',	'J',	'K',	'L',	'M',	'N',	'O',	'P',	'Q',	'R',	'S',	'T',	'U',	'V',	'W',	'X',	'Y',	'Z',	'AA',	'AB',	'AC',	'AD',	'AE',	'AF',	'AG',	'AH',	'AI',	'AJ',	'AK',	'AL',	'AM',	'AN',	'AO',	'AP',	'AQ',	'AR',	'A_S',	'AT',	'AU',	'AV',	'AW',	'AX',	'AY',	'AZ',	'BA',	'BB',	'BC',	'BD',	'BE',	'BF',	'BG',	'BH',	'BI',	'BJ',	'BK',	'BL',	'BM',	'BN',	'BO',	'BP',	'BQ',	'BR',	'BS',	'BT',	'BU',	'BV',	'BW',	'BX',	'BY',	'BZ',	'CA',	'CB',	'CC',	'CD',	'CE',	'CF',	'CG',	'CH',	'CI',	'CJ',	'CK',	'CL',	'CM',	'CN',	'CO',	'CP',	'CQ',	'CR',	'CS',	'CT',	'CU',	'CV',	'CW',	'CX',	'CY',	'CZ',	'DA',	'DB',	'DC',	'DD',	'DE',	'DF',	'DG',	'DH',	'DI',	'DJ',	'DK'
                                                ,'DL') 
                                            values(?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?
                                                    ,?)'''
            data = ['DTVF',	'510',	'21',	'Buchungsstapel',	'7', s_timestamp,	'',	'KW',	'',	'',	'8'
                   ,'10358',	s_ErsterDesJahres,	'4', s_ErsterDesMonats, s_letzterDesMonats,	'Kasse',	'',	'1',	'0',	'0',	'EUR'
                   ,'',	'',	'',	'',	'',	'',	'',	'',	'EXKB',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	''
                   ,'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	''
                   ,'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	''
                   ,'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'','']
            self.insert_values(data, sql)
            data = ['Umsatz (ohne Soll/Haben-Kz)',	'Soll/Haben-Kennzeichen',	'WKZ Umsatz',	'Kurs',	'Basis-Umsatz',	'WKZ Basis-Umsatz',	'Konto',	'Gegenkonto (ohne BU-Schlüssel)',	'BU-Schlüssel',	'Belegdatum',	'Belegfeld 1',	'Belegfeld 2',	'Skonto',	'Buchungstext',	'Postensperre',	'Diverse Adressnummer',	'Geschäftspartnerbank',	'Sachverhalt',	'Zinssperre',	'Beleglink',	'Beleginfo - Art 1',	'Beleginfo - Inhalt 1',	'Beleginfo - Art 2',	'Beleginfo - Inhalt 2',	'Beleginfo - Art 3',	'Beleginfo - Inhalt 3',	'Beleginfo - Art 4',	'Beleginfo - Inhalt 4',	'Beleginfo - Art 5',	'Beleginfo - Inhalt 5',	'Beleginfo - Art 6',	'Beleginfo - Inhalt 6',	'Beleginfo - Art 7',	'Beleginfo - Inhalt 7',	'Beleginfo - Art 8',	'Beleginfo - Inhalt 8',	'KOST1 - Kostenstelle/-träger',	'KOST2 - Kostenstelle/-träger',	'Menge1 - Wert',	'EU-Land u. UStID',	'EU-Steuersatz',	'Abw. Versteuerungsart',	'Sachverhalt L+L',	'Funktionsergänzung L+L',	'BU 49 Hauptfunktionstyp',	'BU 49 Hauptfunktionsnummer',	'BU 49 Funktionsergänzung',	'Zusatzinformation - Art 1',	'Zusatzinformation - Inhalt 1',	'Zusatzinfor-mation - Art 2',	'Zusatzinformation - Inhalt 2',	'Zusatzinformation - Art 3',	'Zusatzinformation - Inhalt 3',	'Zusatzinformation - Art 4',	'Zusatzinformation - Inhalt 4',	'Zusatzinformation - Art 5',	'Zusatzinformation - Inhalt 5',	'Zusatzinformation - Art 6',	'Zusatzinformation - Inhalt 6',	'Zusatzinformation - Art 7',	'Zusatzinformation - Inhalt 7',	'Zusatzinfor-mation - Art 8',	'Zusatzinformation - Inhalt 8',	'Zusatzinformation - Art 9',	'Zusatzinformation - Inhalt 9',	'Zusatzinformation - Art 10',	'Zusatzinformation - Inhalt 10',	'Zusatzinformation - Art 11',	'Zusatzinformation - Inhalt 11',	'Zusatzinformation - Art 12',	'Zusatzinformation - Inhalt 12',	'Zusatzinformation - Art 13',	'Zusatzinformation - Inhalt 13',	'Zusatzinfor-mation - Art 14',	'Zusatzinformation - Inhalt 14',	'Zusatzinformation - Art 15',	'Zusatzinformation - Inhalt 15',	'Zusatzinformation - Art 16',	'Zusatzinformation - Inhalt 16',	'Zusatzinformation - Art 17',	'Zusatzinformation - Inhalt 17',	'Zusatzinformation - Art 18',	'Zusatzinformation - Inhalt 18',	'Zusatzinformation - Art 19',	'Zusatzinformation - Inhalt 19',	'Zusatzinfor-mation - Art 20',	'Zusatzinformation - Inhalt 20',	'Stück',	'Gewicht',	'Zahlweise',	'Forderungsart',	'Veranlagerungsjahr',	'Zugeordnete Fälligkeit',	'Skontotyp',	'Auftragsnummer',	'Buchungstyp',	'USt-Schlüssel (Anzahlungen)',	'EU-Mitgliedstaat (Anzahlungen)',	'Sachgverhalt L+L (Anzahlungen)',	'EU-Steuersatz (Anzahlungen)',	'Erlöskonto (Anzahlungen)',	'Herkunft-Kz',	'Buchungs-GUID',	'Kost-Datum',	'SEPA-Mandantsreferenz',	'Skontosperre',	'Gesellschaftername',	'Beteiligtennummer',	'Identifikationsnummer',	'Zeichnernummer',	'Postensperre bis',	'Bezeichnung SoBil-Sachverhalt',	'Kennzeichen SoBil-Buchung',	'Festschreibung',	'Leistungsdatum'
                    ,'Datum Zuord. Steuerperiode']
            self.insert_values(data, sql)
        except sl.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        
    def get_select_datev(self, tabel_name, Monat, Jahr, Anfangsbestand, Endbestand):
        if Anfangsbestand >= 0:
            AB_Vorzeichen = '+'
        else:
            AB_Vorzeichen = '-'
        if Endbestand >= 0:
            EB_Vorzeichen = '+'
        else:
            EB_Vorzeichen = '-'
        try:
            sql_text = f"""
                  INSERT INTO datevexport (A, B, G, J, N, U, V )
                   SELECT replace(cast(kb.Betrag as text), '.', ',')  as A
     , CASE WHEN kb.Zugang = 1 then 'S'
            WHEN kb.Zugang = -1 then 'H'
            END AS "B"
     , '1000' AS "G"
     ,   ltrim(strftime('%d', kb.Buchungstag),'0') 
      || strftime('%m', kb.Buchungstag)  as J
     , kst.Bezeichnung ||
      CASE WHEN LENGTH(COALESCE(kb.Bemerkung,' ')) > 1 then ' - ' || kb.Bemerkung
           ELSE ' ' END      as N
     , 'D_Kasse' as "U"
     ,  'Umsatz EUR' || CASE WHEN kb.Zugang = 1 then '+'
            WHEN kb.Zugang = -1 then '-'
            END 
      || replace(cast(kb.Betrag as text), '.', ',') 
      ||' Datum ' || STRFTIME('%d.%m.%Y', kb.Buchungstag) || ' Text \"'|| kst.Bezeichnung ||
      CASE WHEN LENGTH(COALESCE(kb.Bemerkung,' ')) > 1 then ' - ' || kb.Bemerkung ||'\" Steuer '
           ELSE '\" Steuer ' END
      || replace(printf("%.2f", kb.Steuersatz,2), '.', ',') 
      || ' AB EUR' || '{AB_Vorzeichen}' || '{Anfangsbestand}' 
      || ' EB EUR' || '{EB_Vorzeichen}' || '{Endbestand}'
      || '  EBDatum ' || date('now','start of month','+1 month','-1 day') as "V"    


   --Umsatz EUR-5,36 Datum 01.03.2023 Text "lebensmittel" Steuer 7,00 AB EUR+531,59 EB EUR+877,22 EBDatum 31.03.2023  
 FROM kassenbuch kb 
 JOIN kostenstellen kst ON kb.Kostenstelle = kst.Kostenstelle
WHERE 1=1
  AND kb.Zugang in (1, -1)
  AND strftime('%Y', kb.Buchungstag) = '{str(Jahr)}'
  AND strftime('%m', kb.Buchungstag) = '{str(Monat).zfill(2)}'
ORDER BY kb.Buchungstag     
 """
            with self.con:
                data = self.con.execute(sql_text)
                # print(f'Monat: {str(Monat)} /// Jahr: {str(Jahr)}')
                # print('____')
                # print(f'SQL: {sql_text}')
        except sl.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
    

    def select_datev_for_export(self, Filename):
        sql_text = f"""SELECT A,	B,	C,	D,	E,	F,	G,	H,	I,	J,	K,	L,	M,	N,	O,	P,	Q,	R,	S,	T,	U,	V,	W,	X
                             ,Y,	Z,	AA,	AB,	AC,	AD,	AE,	AF,	AG,	AH,	AI,	AJ,	AK,	AL,	AM,	AN,	AO,	AP,	AQ,	AR,	A_S,	AT,	AU,	AV
                             ,AW,	AX,	AY,	AZ,	BA,	BB,	BC,	BD,	BE,	BF,	BG,	BH,	BI,	BJ,	BK,	BL,	BM,	BN,	BO,	BP,	BQ,	BR,	BS,	BT
                             ,BU,	BV,	BW,	BX,	BY,	BZ,	CA,	CB,	CC,	CD,	CE,	CF,	CG,	CH,	CI,	CJ,	CK,	CL,	CM,	CN,	CO,	CP,	CQ,	CR
                             ,CS,	CT,	CU,	CV,	CW,	CX,	CY,	CZ,	DA,	DB,	DC,	DD,	DE,	DF,	DG,	DH,	DI,	DJ,	DK,	DL

        FROM datevexport WHERE 1 = 1"""
        print(f'sql zusammengebaut / Dateiname: {Filename}')
        writer = datev.writer(Filename)
        print('Writer-Object erstellt')
        with self.con:
            Cursor = self.con.cursor()
            Cursor.execute(sql_text)
            # rec = cursor.fetchone()
            # while rec is not None:
            for rec in Cursor:
                datev.writer.intern_write_row(writer, rec)
                # print('Zeile in CSV geschrieben')
        datev.writer.close(writer)

    # def set_insert_monatsabschluss(self, monat, jahr):
    #     pass

    def get_monatssumme(self, Monat, Jahr, Fehlerausgabe):
        Summe = 0
        sql = f"""SELECT SUM(kb.Zugang*kb.Betrag) Summe
                     FROM kassenbuch kb
                    WHERE 1 = 1
                      and strftime('%m', kb.Buchungstag) = '{str(Monat).zfill(2)}'
                      and strftime('%Y', kb.Buchungstag) = '{str(Jahr)}'
                      """
    #    # showinfo(message=sql)
    #     Summe = self.select_values(sql_text=sql)
    #     for da in Summe:
    #         data = da[0]
        try:
            # print('Hier')
            Summe = self.select_one(sql_text=sql)
            # print('da')
            # print(f'Monatssumme: {Summe}')
            if not Summe and Fehlerausgabe != 0:
                print('Monatssumme leer - Raise.')
                raise KeineDaten
        
            if Summe is None:
                Summe = 0
        
        except KeineDaten:
            showinfo(title='Warnung', message=f'Es wurden keine Umsätze gefunden.\n Es wurde ein 0-Abschluss erstellt.')
            Summe = 0
        except Exception as exe:
            # showinfo(title='Warnung', message=f'Fehler....')
            print(type(exe))
            print(exe.args)
        return round(Summe,2)

    def get_endbestand(self, Monat, Jahr, Fehlerausgabe):
        sql = f"""SELECT Endbestand, ma.Gueltig
FROM monatsabschluss ma
WHERE 1 = 1
  and ma.Jahr = {Jahr}
  and ma.Monat = {Monat}
  and ma.Gueltig = TRUE"""
        try:
           
            Endbestand = self.select_one(sql_text=sql)
            if Endbestand is None:
                raise KeineDaten
        except KeineDaten:
            if Fehlerausgabe != 0:
                showinfo(title='Warnung', message=f'Es wurde kein gültiger Endbetrag gefunden.\n Es wird mit alter Bestand = 0 gerechnet')
            Endbestand = 0
        except Exception as exe:
            # showinfo(title='Warnung', message=f'Fehler....')
            print(type(exe))
            print(exe.args)
            
        return Endbestand
    
    def monatsBuchungen(connection, Monat, Jahr):
        with connection:
            data = connection.execute(f"""
                  SELECT SUM(kb.Zugang*kb.Betrag) Summe
                     FROM kassenbuch kb
                    WHERE 1 = 1
                      and strftime('%m', kb.Buchungstag) = '{str(Monat).zfill(2)}'
                      and strftime('%Y', kb.Buchungstag) = '{str(Jahr)}'
                    """)
            return data
