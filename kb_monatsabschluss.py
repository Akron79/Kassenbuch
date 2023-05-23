import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tkinter.messagebox import showinfo
from tkcalendar import DateEntry
import kb_datebase as db
import kb_datev_export as datev
from  datetime import date

class BetragFehler(Exception):
    pass

class EsGibtAbschluss(Exception):
    pass

class ZugangFehler(Exception):
    pass

class KostenFehler(Exception):
    pass

class InsertFehler(Exception):
    pass

class SteuerFehler(Exception):
    pass

class main_window(tk.Tk):
  def __init__(self, ver, conn, tabel_name):
    self.version = ver
    super().__init__()
    self.title(f"Monatsabschluss v_{ver}")
    # self.geometry("1180x640")
    self.minsize(width=1100, height=250)
    self.main_frame = ttk.Frame(master=self, borderwidth="2", relief='groove',)
    self.main_frame.pack(padx=20, pady=20, fill='both')
    self.connection = conn
    self.tabel_name = tabel_name
    self.CreateStyle()
    self.AddInnerFrame()
    
  def AddInnerFrame(self):
    self.inner_frame = ttk.Labelframe(self.main_frame, text='Berechne Monatsabschluss und erstelle Datev-Export.', padding='10')
    self.inner_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20, )
    
    labelBesch = ttk.Label(master=self.inner_frame, style='KB.TLabel', text='Bei Neuberechnung eines älteren Monatsabschluss, werden auch alle folgenden neu berechnet.')
    labelBesch.grid(row=0, column=0, columnspan=3, padx='15', pady='15')
    
    jahr_options = [ 2023, 2022]
    labelJahr = ttk.Label(master=self.inner_frame, style='KB.TLabel', text='Buchungsjahr')
    labelJahr.grid(row=1, column=0, padx='1', pady='1')
    self.entryJahr =  ttk.Combobox(self.inner_frame,justify='center', values=list(jahr_options),state='readonly')
    self.entryJahr.current(0)
    self.entryJahr.grid(row=2, column=0, padx='5', pady='1', ipadx=10, sticky='ew')
    
    monat_options = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    labelMonat = ttk.Label(master=self.inner_frame, style='KB.TLabel', text='Buchungsmonat')
    labelMonat.grid(row=1, column=1, padx='1', pady='1')
    self.entryMonat = ttk.Combobox(self.inner_frame,justify='center', values=list(monat_options),state='readonly')
    self.entryMonat.current(0)
    self.entryMonat.grid(row=2, column=1, padx='5', pady='1', ipadx=10, sticky='ew')
    
    buttonBerech = ttk.Button(master=self.inner_frame, text='Abschluss erstellen.', style='KB.TButton', command=self.button_clicked)
    buttonBerech.grid(row=1, column=2, rowspan=2, padx='0', pady='0', sticky='news')
    
              
  def button_clicked(self):
    print('Erstelle Monatsabschluss')
    sql_check_exists_abschluss = f"""SELECT """
    db.sqli.select_one(self.connection, sql_check_exists_abschluss)
    
    try:         
        s_Jahr = self.entryJahr.get()
        s_Monat = self.entryMonat.get()  
        n_Jahr = int(s_Jahr)
        n_Monat = int(s_Monat)
        sql_check_exists_abschluss = f"""SELECT ID FROM monatsabschluss ma WHERE 1=1 
                                        and ma.Jahr = {n_Jahr}
                                        and ma.Monat = {n_Monat}
                                        and ma.Gueltig = TRUE"""
        print(sql_check_exists_abschluss)                                
        existingBestand = db.sqli.select_one(self.connection, sql_check_exists_abschluss)
        if existingBestand is not None:
                raise EsGibtAbschluss
            
        if n_Monat==1:
           vor_Jahr = n_Jahr - 1
           vor_Monat = 12
        else:
           vor_Jahr = n_Jahr
           vor_Monat = n_Monat - 1
        
        n_Anfangsbestand = db.sqli.get_endbestand(self.connection, vor_Monat, vor_Jahr, 1)
        # showinfo(title='Information', message=f"Anfangsbestand: {n_Anfangsbestand}")
        
        n_Endbestand = db.sqli.get_monatssumme(self.connection, n_Monat, n_Jahr, 1) + n_Anfangsbestand
        # showinfo(title='Information', message=f"_Endbestand: {n_Endbestand}")
        
        b_gueltig = True

        sql = f'''UPDATE monatsabschluss SET Gueltig = FALSE WHERE Jahr = {n_Jahr} AND Monat = {n_Monat}'''
        db.sqli.execute_sql(self.connection,sql)    
        
        sql = f'''INSERT INTO monatsabschluss ( Jahr, Monat, Anfangsbestand, Endbestand, Gueltig, Zeitstempel) 
                 values(?, ?, ?, ?, ?, ?)'''
        data = [n_Jahr, n_Monat, n_Anfangsbestand, n_Endbestand, b_gueltig, datetime.now()]
        # showinfo(title='Information', message=f"SQL: {sql}")
        # for d in data:
        #    print(d)
        self.connection.create_datev(n_Monat, n_Jahr)
        self.connection.insert_values(data, sql)    
        print('Datensatz in Monatsabschluss eingefügt')
        datev.writer.insert_to_table(self.connection, n_Monat, n_Jahr, n_Anfangsbestand, n_Endbestand)
        print('Aufruf Datev-Modul abgeschlossen')
        self.destroy()

        
        showinfo(title='Information', message='Monatsabschluss erstellt')      
    except EsGibtAbschluss:
       showinfo(title='Warnung', message=f'Es existiert bereits ein Monatsabschluss. Es wurde kein neuer Abschluss erstellt.')
            
    # except BetragFehler:
    #    showinfo(title='Warnung', message=f'Eingegebener Betrag "{self.entryBetrag.get()}" ist keine Komma-Zahl / enthählt ungültige Zeichen')
    # except KostenFehler:
    #    showinfo(title='Warnung', message=f'Es wurde keine Kostenstelle ausgewählt.')
    # except ZugangFehler:
    #    showinfo(title='Warnung', message=f'Bitte Buchungsrichtung auswählen.')
    # except InsertFehler:
    #    showinfo(title='Warnung', message=f'Fehler beim Einfügen der Daten in die Datenbank. Bitte Admin kontaktieren.') 
    # except SteuerFehler:
    #    showinfo(title='Warnung', message=f'Fehler beim Lesen des Steuersatzes. Bitte Admin kontaktieren.')

    except:
       pass
  def CreateStyle(self):
    self.style = ttk.Style()
    self.style.configure(".", foreground="black", background="white", font=('Arial', 10))
    self.style.configure("KB.TButton", foreground="green", background="grey", font=('Arial', 14))
    self.style.configure("KB.TEntry", foreground="blue", background="white",font=('Arial', 12))
    self.style.configure("KB.TBEM", foreground="black", background="white",font=('Arial', 10))