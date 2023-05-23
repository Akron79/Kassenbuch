import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tkinter.messagebox import showinfo
from tkcalendar import DateEntry
import kb_datebase as db
from  datetime import date

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
  def __init__(self, ver, conn):
    self.version = ver
    super().__init__()
    self.title(f"Admin v_{ver}")
    self.geometry("1180x640")
    # self.minsize(width=1100, height=250)
    self.main_frame = ttk.Frame(master=self, borderwidth="2", relief='groove', width=700, height=250)
    self.main_frame.pack(fill='both')
    self.connection = conn
    self.CreateStyle()
    self.AddInnerFrame()
    
  def AddInnerFrame(self):
    self.sql_text=tk.Text(self.main_frame, width=50, font=('Arial 12'))
    self.sql_text.pack(padx=10, pady=10, fill='both')
    button=tk.Button(self.main_frame, text="Submit", command=self.button_execute_sql)
    button.pack(pady=10)
              
  def button_execute_sql(self):
    print('hi')
    try: 
        # sql = self.sql_text.get("1.0","end-1c")
        sql = self.sql_text.get(index1='1.0', index2='end')
        self.connection.execute_sql(sql)
    except:
       print('fehler')

  def CreateStyle(self):
    self.style = ttk.Style()
    self.style.configure(".", foreground="black", background="white", font=('Arial', 10))
    self.style.configure("KB.TButton", foreground="green", background="grey", font=('Arial', 14))
    self.style.configure("KB.TEntry", foreground="blue", background="white",font=('Arial', 12))
    self.style.configure("KB.TBEM", foreground="black", background="white",font=('Arial', 10))