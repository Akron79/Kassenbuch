import kb_datebase as db
import kb_gui as gui

version = "0.5"
tabel_name = 'kassenbuch'
file_name = 'koschis'

con = db.sqli(file_name, tabel_name)
app = gui.main_window(version,con, tabel_name)
app.set_kostenstellen()
app.set_steuersaetze()
app.CreateStyle()
app.AddTopFrame()
app.AddInput()
app.AddTableFrame()
app.mainloop()


# Version 06.
    # Anpassung Dateiname für Datevexport



# Version 0.5
    # Erste release an Yvonne
    # Admin-SQL Fenster
    # Datev-Export 
    # Monatsabschluss