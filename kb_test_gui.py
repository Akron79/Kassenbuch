import tkinter as tk
import tkinter.ttk as ttk

def buttonDurchClick():
    # Übernahme der Daten
    zahl1 = int(entryZahl1.get())
    #zahl2 = int(entryZahl2.get())
    # Verarbeitung der Daten
    ergebnis = zahl1 # // zahl2
    # Anzeige der Daten
    labelErgebnis.config(text=str(ergebnis))

#style


#tk._test()
version = "0.1.1"
#Container
root = tk.Tk()
root.title(f"Kassenbuch {version}")
root.geometry("800x640")
root.minsize(width=250, height=250)

style = ttk.Style()
style.configure(".", foreground="black", background="white", font=('Arial', 18))
#style.configure("KB.TLabel", font=('Arial', 18))
style.configure("KB.TButton",)

outer_frame = ttk.Frame(master=root, borderwidth="2", relief='groove')
outer_frame.pack()

# Label mit Aufschrift Zahl 1
labelZahl1 = ttk.Label(master=outer_frame, style='KB.TLabel', text='Zahl 1')
labelZahl1.grid(row=0, column=0, padx='5', pady='5', sticky='ew')
# Entry für Zahl 1
entryZahl1 = ttk.Entry(master=outer_frame, style='KB.TLabel', width='8')
entryZahl1.grid(row=0, column=1, padx='5', pady='5', sticky='ew')

buttonDurch = ttk.Button(master=outer_frame, text='Speichern', style='KB.TButton', command=buttonDurchClick)
buttonDurch.grid(row=0, column=2, padx='5', pady='5')

#Ergebnis
labelErgebnis = tk.Label(master=outer_frame, bg='#FFCFC9', text='Zahl 1')
labelErgebnis.grid(row=1, column=1, padx='5', pady='5', sticky='ew')


#Labels
label1 = tk.Label(root, text="Hallo Welt")
label1.pack()

root.mainloop()