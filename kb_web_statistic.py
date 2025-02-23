import sys
import pandas as pd
import kb_datebase as db
import plotly_express as pe
import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime as strun


def externer_starten():
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())


def main():
    TABLE_NAME = 'kassenbuch'
    FILE_NAME = 'koschis'
    ANZAHL_MONATE_VERGANGENHEIT = 5

    st.set_page_config(page_title="Auswertung",
                    layout="wide"
                    )

    connection = db.sqli(FILE_NAME, TABLE_NAME)
    df = pd.read_sql_query(
        sql="""SELECT kb.Buchungstag
                    ,strftime('%m',kb.Buchungstag) AS Buchungsmonat
                    ,strftime('%Y',kb.Buchungstag) AS Buchungsjahr
                    ,kb.Kostenstelle
                    ,ks.Bezeichnung AS Kostenstellen_Bezeichnung
                    ,kb.Bemerkung
                    ,CASE WHEN kb.Zugang = 1 THEN 'ZUGANG' ELSE 'ABGANG' 
                            END AS Buchungsrichtung
                    ,ROUND(kb.Zugang * kb.Betrag,2) as Saldo_inkl_Richtung       
                FROM kassenbuch kb
    LEFT OUTER JOIN kostenstellen ks on kb.kostenstelle = ks.kostenstelle
    WHERE 1=1
    and kb.Buchungstag >= date('now', 'Start of Month', '-5 months')""",
        con=connection.con
                        )

    st.sidebar.header("Filtern...")
    monat = st.sidebar.multiselect(
        "Monat auswählen:",
        options=df["Buchungsmonat"].unique(),
        default=df["Buchungsmonat"].unique()
    )
    jahr = st.sidebar.multiselect(
        "Jahr auswählen:",
        options=df["Buchungsjahr"].unique(),
        default=df["Buchungsjahr"].unique()
    )
    kostenstelle = st.sidebar.multiselect(
        "Kostenstelle auswählen:",
        options=df["Kostenstelle"].unique(),
        default=df["Kostenstelle"].unique()
    )
    kostenstellen_bezeichnung = st.sidebar.multiselect(
        "Bezeichnung der Kostenstelle auswählen:",
        options=df["Kostenstellen_Bezeichnung"].unique(),
        default=df["Kostenstellen_Bezeichnung"].unique()
    )


    df_selection = df.query(
        "Kostenstelle == @kostenstelle & Kostenstellen_Bezeichnung == @kostenstellen_bezeichnung & Buchungsmonat == @monat & Buchungsjahr == @jahr"

    )

    auswertung_kostenstellen = (
        df_selection.groupby(by=["Kostenstellen_Bezeichnung"]).sum()[["Saldo_inkl_Richtung"]].sort_values(by="Saldo_inkl_Richtung")
    )

    graph_kostenstellen = pe.bar(
        auswertung_kostenstellen,
        x="Saldo_inkl_Richtung",
        y=auswertung_kostenstellen.index,
        orientation="h",
        title="<b>Auswertung der einzelnen Kostenstellen</b>",
        color_discrete_sequence=["#0083B8"] * len(auswertung_kostenstellen),
        template="plotly_white",
    )

    # erste_spalte, zweite_spalte = st.columns(2)
    # erste_spalte.dataframe(df_selection)
    # zweite_spalte.plotly_chart(graph_kostenstellen, use_container_width=True)

    st.plotly_chart(graph_kostenstellen)
    st.dataframe(df_selection)
    # print(df)



if __name__ == '__main__':
    if strun.Runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
