import tkinter as tk
import tkinter.ttk as ttk
# import tkinter.
from tkinter.messagebox import showinfo
from tkcalendar import DateEntry
import kb_datebase as db
from  datetime import date
from  datetime import datetime
import kb_monatsabschluss as abschluss
import kb_sql_ausfuehren  as sqla
import kb_datev_export as datev

class BetragFehler(Exception):
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
    self.title(f"Kassenbuch v_{ver}")
    # self.geometry("1180x640")
    self.minsize(width=1100, height=250)
    #self.label = ttk.Label(self, text='Hello, Tkinter!')
    #self.label.pack()
    self.main_frame = ttk.Frame(master=self, borderwidth="2", relief='groove',)
    self.main_frame.pack(padx=20, pady=20, fill='both')
    self.connection = conn
    self.buchungsdatum=tk.StringVar() # declaring string variable 
    # = self.ser #{'1':'a', '2':'v'}
    self.tabel_name = tabel_name

    self.menu = tk.Menu(self.main_frame)
    self.config(menu=self.menu)
    filemenu = tk.Menu(self.menu)
    self.menu.add_cascade(label="File", menu=filemenu)
   #  filemenu.add_command(label="New", command=NewFile)
   #  filemenu.add_command(label="Open...", command=OpenFile)
   #  filemenu.add_separator()
    filemenu.add_command(label="Exit", command=self.main_frame.quit)

    adminmenu = tk.Menu(self.menu)
    self.menu.add_cascade(label="Admin", menu=adminmenu)
    adminmenu.add_command(label="SQL ausführen", command=self.Sql_ausfuehren)

  
  def bind_kosten_stellen_changed(self,*args):
    self.kostenname.set(self.kosten_options.get(self.kostennummer.get()))
    
  def bind_kosten_bezeichnung_changed(self,*args):
    for x, y in self.kosten_options.items():
        if y == self.kostenname.get():
            self.kostennummer.set(x)
            break
    
  def AddTableFrame(self):
    self.table_frame = ttk.Labelframe(self.main_frame, text='die letzten 15 Buchungen...', padding='10')
    self.table_frame.grid(row=2, column=0, sticky='ns', padx=20, pady=20, )#.pack(fill="x", side="top", padx="10", pady="10",)

    # self.table_frame.grid_columnconfigure(0, weight=0, minsize= 100)
    # self.table_frame.grid_columnconfigure(1, weight=0, minsize= 100)
    # self.table_frame.grid_columnconfigure(2, weight=1, minsize= 100)
    # self.table_frame.grid_columnconfigure(3, weight=1, minsize= 100)
    # self.table_frame.grid_columnconfigure(4, weight=1, minsize= 100)
    # self.table_frame.grid_columnconfigure(5, weight=1, minsize= 100)
    # self.table_frame.grid_columnconfigure(6, weight=1, minsize= 100)
    
    r_spalten=db.sqli.get_spalten(self.connection, self.tabel_name)
    i = 0
    for spalte in r_spalten:
        e = tk.Label(self.table_frame,text=spalte[0].upper(), width=10, fg='black', background='white') 
        if spalte[0] == 'Bemerkung':
           e.grid(row=0, column=i, sticky='nesw',   ) 
           # self.table_frame.grid_columnconfigure(i, weight=1, minsize= 150)
    
        else:
           e.grid(row=0, column=i, sticky='ew',  ) 
        
        i = i+1
        
    r_buchungen=db.sqli.get_last15(self.connection, self.tabel_name)
    i=1 # row value inside the loop             
    for buchung in r_buchungen: 
        for j in range(len(buchung)):
            if j ==0 or j==3 or j==4:
               e = tk.Entry(self.table_frame, width=len(str(buchung[j])), fg='blue',justify='right') 
            else:
               e = tk.Entry(self.table_frame, width=len(str(buchung[j])), fg='blue',justify='center') 
            e.grid(row=i, column=j, ipadx= 15, sticky='ew') 
            e.insert(tk.END, buchung[j])
            e.config(state='disabled')
        i=i+1          
  def button_datensatz_speichern(self):
    try: 
        #showinfo(title='Information', message=self.buchungsdatum.get())
        #showinfo(title='Information', message=self.richtung.get())
        #showinfo(title='Information', message=self.entryBetrag.get())
        #showinfo(title='Information', message='Länge: ' + str(len(self.entryKNummer.get())))
        try:
            i_betrag = float(self.entryBetrag.get().replace(',','.'))   
        except:
            raise BetragFehler
        if i_betrag == 0:
            raise BetragFehler
        if 0 == len(self.entryKNummer.get()):
           raise KostenFehler
        if self.richtung.get() == 'Zugang':
           i_richtung = 1
        elif self.richtung.get() == 'Abgang':
           i_richtung = -1
        else:  
            raise ZugangFehler
        try:
           i_steuer = int(self.entrySteuer.get())
        except:
           raise SteuerFehler   
        
        try:
           db.sqli.add_buchung(self.connection
                               , self.tabel_name
                               , d_tag=self.buchungsdatum.get()
                               , b_zugang=i_richtung
                               , f_betrag=i_betrag
                               , i_steuersatz=i_steuer
                               , t_kostenstelle=int(self.entryKNummer.get())
                               , t_bem=self.entryBemerkung.get()
                               )
           self.upper_frame.destroy()
           self.table_frame.destroy()
           self.middle_frame.destroy()
           self.AddTopFrame()
           self.AddInput()
           self.AddTableFrame()
        except:
            raise InsertFehler
    
    
    except BetragFehler:
       showinfo(title='Warnung', message=f'Eingegebener Betrag "{self.entryBetrag.get()}" ist keine Komma-Zahl / enthählt ungültige Zeichen')
    except KostenFehler:
       showinfo(title='Warnung', message=f'Es wurde keine Kostenstelle ausgewählt.')
    except ZugangFehler:
       showinfo(title='Warnung', message=f'Bitte Buchungsrichtung auswählen.')
    except InsertFehler:
       showinfo(title='Warnung', message=f'Fehler beim Einfügen der Daten in die Datenbank. Bitte Admin kontaktieren.') 
    except SteuerFehler:
       showinfo(title='Warnung', message=f'Fehler beim Lesen des Steuersatzes. Bitte Admin kontaktieren.')

  def CreateStyle(self):
    self.style = ttk.Style()
    self.style.configure(".", foreground="black", background="white", font=('Arial', 10))
    self.style.configure("KB.TButton", foreground="green", background="grey", font=('Arial', 14))
    self.style.configure("KB.TEntry", foreground="blue", background="white",font=('Arial', 12))
    self.style.configure("KB.TBEM", foreground="black", background="white",font=('Arial', 10))

  def Monatsabschluss(self):
     monat = abschluss.main_window(ver=self.version, conn=self.connection, tabel_name='monatsabschluss')
     monat.mainloop()

  def Sql_ausfuehren(self):
     monat = sqla.main_window(ver=self.version, conn=self.connection)
     monat.mainloop()

  def AddTopFrame(self):
    #self.upper_frame = ttk.Frame(master=self.main_frame, borderwidth="2", relief='groove')
    self.upper_frame = ttk.Labelframe(self.main_frame, text='.......', padding='10')
    self.upper_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=20, )#.pack(fill="x", side="top", padx="10", pady="10",)
    
    self.upper_frame.grid_columnconfigure(0, weight=1)
    self.upper_frame.grid_columnconfigure(1, weight=1)
    self.upper_frame.grid_columnconfigure(2, weight=1)
   
   #  buttonDurch = ttk.Button(master=self.upper_frame, text='Button_1', style='KB.TButton', command=self.button_clicked)
   #  buttonDurch.grid(row=0, column=0, padx='5', pady='5')#, sticky='news')
    
    labelKasse = ttk.Label(master=self.upper_frame, style='KB.TLabel', text='Kassebestand')
    labelKasse.grid(row=0, column=0)
    aktuellerMonat = datetime.now().month
    aktuellesJahr = datetime.now().year
      
    if aktuellerMonat==1:
      vor_Jahr = aktuellesJahr - 1
      vor_Monat = 12
    else:
      vor_Jahr = aktuellesJahr
      vor_Monat = aktuellerMonat - 1

    kassenbestand = db.sqli.get_endbestand(self.connection,vor_Monat, vor_Jahr, 0) + round(db.sqli.get_monatssumme(self.connection, str(aktuellerMonat).zfill(2), aktuellesJahr,0),2)
                   
    labelBestand = ttk.Label(master=self.upper_frame, style='KB.TLabel', text=f'{kassenbestand} €', foreground='blue')
    labelBestand.grid(row=1, column=0, sticky='ns')
    print(f'vMonat: {vor_Monat} / vJahr: {vor_Jahr}')
   #  buttonTest = ttk.Button(master=self.upper_frame, text='Button_2', style='KB.TButton', command=lambda : datev.writer.insert_to_table(self.connection, vor_Monat, vor_Jahr, 1111, 2222))
   #  buttonTest.grid(row=0, column=1, padx='5', pady='5')#, sticky='news')
    
   #  buttonTest2 = ttk.Button(master=self.upper_frame, text='Test 2', style='KB.TButton', command=lambda : db.sqli.select_datev_for_export(self.connection))
   #  buttonTest2.grid(row=0, column=2, padx='5', pady='5')#, sticky='news')
    
    buttonMonatsabschluss = ttk.Button(master=self.upper_frame, text='Monatsabschluss', style='KB.TButton', command=self.Monatsabschluss)
    buttonMonatsabschluss.grid(row=0, column=3, rowspan=2, padx='5', pady='5')#, sticky='news')

  def AddInput(self):
    self.middle_frame = ttk.Frame(master=self.main_frame, borderwidth="2", relief='groove', )
    self.middle_frame.grid(row=1, column=0, sticky='ew', padx=20, pady=20)#.pack(fill="x", side="top", padx="10", pady="10",)
    self.middle_frame.grid_columnconfigure(0, weight=1, minsize= 100)
    self.middle_frame.grid_columnconfigure(1, weight=1, minsize= 100)
    self.middle_frame.grid_columnconfigure(2, weight=1, minsize= 100)
    self.middle_frame.grid_columnconfigure(3, weight=1, minsize= 100)
    self.middle_frame.grid_columnconfigure(4, weight=2, minsize= 100)
    self.middle_frame.grid_columnconfigure(5, weight=2, minsize= 100)
    self.middle_frame.grid_columnconfigure(6, weight=2, minsize= 100)
    
    
    #https://www.plus2net.com/python/tkinter-DateEntry.php
    labelBuchungsTag = ttk.Label(master=self.middle_frame, style='KB.TLabel', text='Buchungstag')
    labelBuchungsTag.grid(row=0, column=0)
    cal = DateEntry(master=self.middle_frame, textvariable=self.buchungsdatum, width=8, date_pattern='yyyy-MM-dd', background='green', foreground='white', borderwidth=2)
    cal.grid(row=1, column=0, padx='5', pady='5', ipadx=10, sticky='ew')
    
    #https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter
    zugang_options = [ "bitte wählen","Zugang", "Abgang",]
    self.richtung = tk.StringVar(self.middle_frame)
    labelZugang = ttk.Label(master=self.middle_frame, style='KB.TLabel', text='Buchungsrichtung')
    labelZugang.grid(row=0, column=1, padx='15', pady='15')
    entryRichtung = ttk.OptionMenu(self.middle_frame, self.richtung,zugang_options[0], *zugang_options)
    entryRichtung.grid(row=1, column=1, padx='5', pady='5', ipadx=10, sticky='ew')
    
    #entryZahl1 = ttk.Entry(master=self.middle_frame, style='KB.TEntry', font=self.style.lookup("KB.TEntry", "font"))
    #entryZahl1.grid(row=1, column=1, padx='5', pady='5', ipadx=10, sticky='ew')
    labelBetrag = ttk.Label(master=self.middle_frame, style='KB.TLabel', text='Betrag',width=10)
    labelBetrag.grid(row=0, column=2)
    self.entryBetrag = ttk.Entry(master=self.middle_frame, justify='right', style='KB.TEntry',width=10, font=self.style.lookup("KB.TEntry", "font"))
    self.entryBetrag.insert(0, '0,00')
    self.entryBetrag.grid(row=1, column=2, padx='5', pady='5', ipadx=10, sticky='ew')
           
    #Spalte 4/8 Steuersatz
    labelSteuer = ttk.Label(master=self.middle_frame, style='KB.TLabel', text='Steuersatz')
    labelSteuer.grid(row=0, column=3)
    self.entrySteuer = ttk.Combobox(self.middle_frame,justify='right', values=list(self.steuer_options.keys()),state='readonly')
    self.entrySteuer.grid(row=1, column=3, padx='5', pady='5', ipadx=10, sticky='ew')
    
    #Spalte 5/8 Kostenstelle
    self.kostennummer = tk.StringVar(self.middle_frame)
    self.kostenname = tk.StringVar(self.middle_frame)
  
    labelKNummer = ttk.Label(master=self.middle_frame, style='KB.TLabel', text='Kostenstelle')
    labelKNummer.grid(row=0, column=4)
    self.entryKNummer = ttk.Combobox(self.middle_frame,justify='right', textvariable=self.kostennummer, values=list(self.kosten_options.keys()),state='readonly')
    self.entryKNummer.grid(row=1, column=4, padx='5', pady='5', ipadx=10, sticky='ew')
    self.kostennummer.trace_add(mode='write', callback=(self.bind_kosten_stellen_changed))
    
    #Spalte 6/8 Kostenstellenbezeichnung
    labelKName = ttk.Label(master=self.middle_frame, style='KB.TLabel', text='Kostenstellen Bez.')
    labelKName.grid(row=0, column=5)
    self.entrykname = ttk.Combobox(self.middle_frame,justify='center', textvariable=self.kostenname, values=list(self.kosten_options.values()),state='readonly',)
    self.entrykname.grid(row=1, column=5, padx='5', pady='5', ipadx=10, sticky='ew')
    self.kostenname.trace_add(mode='write', callback=(self.bind_kosten_bezeichnung_changed))
    
    #Spalte 7/8 Bemerkung
    labelBemerkung = ttk.Label(master=self.middle_frame, style='KB.TLabel', text='Bemerkung (optional)')
    labelBemerkung.grid(row=0, column=6)
    self.entryBemerkung = ttk.Entry(master=self.middle_frame, style='KB.TEntry', font=self.style.lookup("KB.TBEM", "font"), foreground=self.style.lookup("KB.TBEM", "foreground"))
    self.entryBemerkung.grid(row=1, column=6, padx='5', pady='5', ipadx=10, sticky='ew')

    #Spalte 8/8 Speichern Button
    labelSpeichern = ttk.Label(master=self.middle_frame, style='KB.TLabel', text=' ',width=18)
    labelSpeichern.grid(row=0, column=7)
    buttonDurch = ttk.Button(master=self.middle_frame, text='Speichern', style='KB.TButton', command=self.button_datensatz_speichern)
    buttonDurch.grid(row=1, column=7)#, padx='5', pady='5', ipadx=10)

  def set_kostenstellen(self):
    self.kosten_options = {}
    r_kostenstellen = db.sqli.get_kostenstellen(self.connection)
    for kostenstelle in r_kostenstellen:
        self.kosten_options[kostenstelle[0]] = kostenstelle[1] 

  def set_steuersaetze(self):
    self.steuer_options = {}
    r_steuersaetze = db.sqli.get_steuersaetze(self.connection)
    for steuersatz in r_steuersaetze:
        self.steuer_options[steuersatz[0]] = steuersatz[1] 
