import sqlite3
import csv
import datetime


def alles_exportieren(datenbank_datei, export_datei_praefix="export"):
    
    print(f"Komplettexport gestartet.")
    try:
        select_kassenbuch = f"""SELECT 
                        kb.id
                    , kb.Buchungstag
                    , CASE WHEN kb.Zugang = 1 Then 'Zugang' ELSE 'Abgang' END as Richtung
                    , kb.betrag
                    , cast(format("%.2f",kb.Betrag) as text) 
                    , cast(kb.Steuersatz as TEXT) || '%' as Steuersatz
                    , kb.Kostenstelle as kst_id
                    , kostenstellen.Bezeichnung
                    , kb.Bemerkung
                    , datetime(kb.Zeitstempel) as Zeitstempel
                    FROM kassenbuch kb
                    left outer JOIN kostenstellen  ON (kostenstellen.kostenstelle) = (kb.Kostenstelle)

                    ORDER BY kb.id"""
        select_monat = f"""SELECT 
                            ma.id
                            , ma.jahr
                            , ma.monat
                            , round(ma.anfangsbestand,2) as anfangsbestand
                            , round(ma.endbestand,2) as endbestand
                            , ma.gueltig
                            , ma.zeitstempel  
                            FROM monatsabschluss ma
                            ORDER BY ma.jahr, ma.monat, ma.gueltig"""            

        print(f"Kassenbuchexport gestartet.") 
        daten_exportieren(datenbank_datei,select_kassenbuch,'ExportKassenbuch')
         
        print(f"Monatsabschlussexport gestartet.")    
        daten_exportieren(datenbank_datei,select_monat,'ExportMonatabschluesse')
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")



def daten_exportieren(datenbank_datei, sql_abfrage, export_datei_praefix="export"):
    """
    Führt eine SQL-Abfrage aus und exportiert die Ergebnisse in eine CSV-Datei mit Zeitstempel.

    Args:
        datenbank_datei (str): Der Pfad zur SQLite-Datenbankdatei.
        sql_abfrage (str): Die SQL-Abfrage, die ausgeführt werden soll.
        export_datei_praefix (str, optional): Das Präfix für den Dateinamen der CSV-Datei. Standardmäßig "export".
    """
    try:
        # Datenbankverbindung herstellen
        conn = sqlite3.connect(datenbank_datei)
        cursor = conn.cursor()

        # SQL-Abfrage ausführen
        cursor.execute(sql_abfrage)
        ergebnisse = cursor.fetchall()

        # Aktuellen Zeitstempel erstellen
        zeitstempel = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dateiname = f"{export_datei_praefix}_{zeitstempel}.csv"

        # CSV-Datei erstellen und schreiben
        with open(dateiname, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Header schreiben (Spaltennamen)
            header = [beschreibung[0] for beschreibung in cursor.description]
            writer.writerow(header)

            # Datenzeilen schreiben
            writer.writerows(ergebnisse)

        print(f"Daten erfolgreich in {dateiname} exportiert.")

    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    finally:
        if conn:
            conn.close()

## Beispielaufruf der Funktion
#datenbank_datei = 'meine_datenbank.db'  # Passe den Dateinamen an
#sql_abfrage = "SELECT id, name, alter FROM benutzer"  # Passe deine Abfrage an
#daten_exportieren(datenbank_datei, sql_abfrage, "benutzer_export")

# Du kannst die Funktion auch aus anderen Teilen deines Programms aufrufen
# mit unterschiedlichen Parametern
# daten_exportieren("eine_andere_datenbank.db", "SELECT * FROM produkte", "produkte_export")


#def main():
#    alles_exportieren('koschis.db')
#
#main()    