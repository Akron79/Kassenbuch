import kb_datebase as db
import kb_gui as gui

version = "1.0"
tabel_name = 'kassenbuch'
file_name = 'koschis'

con = db.sqli(file_name, tabel_name)
app = gui.main_window(version, con, tabel_name)
app.set_kostenstellen()
app.set_steuersaetze()
app.CreateStyle()
app.AddTopFrame()
app.AddInput()
app.AddTableFrame()
app.mainloop()


# Version 1.0
    # DB Export hinzugefügt
# Version 0.8.1
    # Fehler nach Änderung import datetime behoben
    # Runden bei Monatsabschluss hinzugefügt
# Version 0.8
    # Anpassung Monatsabschluss 2025 dynamisch?
# Version 0.7
    # Anpassung Monatsabschluss 2024
    # Anpassung Bestand runden
# Version 0.6
    # Anpassung Dateiname für Datevexport
    # Ermittlung LAST Monatsabschluss
# Version 0.5
    # Erste release an Yvonne
    # Admin-SQL Fenster
    # Datev-Export 
    # Monatsabschluss