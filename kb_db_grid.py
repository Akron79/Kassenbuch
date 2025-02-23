import kb_datebase as db
import tkinter as tk
import tkinter.ttk as ttk
import platform

# ************************
# Scrollable Frame Class
# ************************
class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
            
        self.viewPort.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.onLeave)                                 # unbind wheel events when the cursorl leaves the control

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)
        #whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):
        '''cross platform scroll wheel event'''
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
    
    def onEnter(self, event):
        '''bind wheel events when the cursor enters the control'''
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):
        '''unbind wheel events when the cursorl leaves the control'''
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")


class Dataset(tk.Frame):
    '''create Frame / row / data set '''
    def __init__(self, parent, dataset, row, connection):
        '''init /
        dict = id_nummer, buchungstag, zugang, betrag, steuersatz
             , kostenstelle, bemerkung'''
        tk.Frame.__init__(self, parent)
        self.grid()
        self.dataset = []
        self.dataset = dataset
        self.con = connection
        self.variables = {}
        j = 0
        for j, data in enumerate(dataset):
            self.make_data_field(str(data), row, j)
        self.make_widgets(row, j+1)
        # self.make_scrollbar()

    def make_data_field(self, val, row, col):
        '''insert data field in row'''
        self.widget = {}
        value = tk.StringVar()
        value.set(val)
        self.variables['var_' + '_' + str(col)] = tk.Entry(self,
                          textvariable=value,
                          fg='blue',
                          justify='right',
                          width=10)
        self.variables['var_' + '_' + str(col)].grid(sticky="nsew", row=row, column=col)
        # widget.pack(side='left')

    def update_data_set(self, row):
        sql = "UPDATE kassenbuch SET Bemerkung = ? WHERE id = ?"
        bemerkung = self.variables['var_' + '_' + str(6)].get()
        data = [bemerkung, '90']
        db.sqli.insert_or_update_values(self.con, data, sql)
    
    def make_widgets(self, row, col):
        '''place the button'''
        widget = tk.Button(self, text='Update', 
                           command=lambda: self.update_data_set(row))
        widget.grid(sticky='ns', row=row, column=col)
        # widget.pack(side='left')

    def make_scrollbar(self):
        '''test button'''
        scrollbar = tk.Scrollbar(master=self, orient='vertical')
        scrollbar.grid(sticky='ns')

    def message(self):
        '''test fnc for button'''
        row = self.dataset[0]
        print(f'Hello frame world {row}!')


def main():
    '''Hauptroutine zum Testen als Stand-Alone'''
    tabel_name = 'kassenbuch'
    file_name = 'koschis'
    con = db.sqli(file_name, tabel_name)
    r_buchungen = db.sqli.get_last15(con, tabel_name)
    r_spalten = db.sqli.get_spalten(con, tabel_name)

    window = tk.Tk()
    window.geometry('600x300')
    # add a new scrollable frame.
    scroll_frame = ScrollFrame(window)

    i = 1
    Dataset(scroll_frame.viewPort, r_spalten, i, con)#.grid(row=i)
    i = i + 1
    # row value inside the loop
    for buchung in r_buchungen:
        Dataset(scroll_frame.viewPort, buchung, i, con).grid(row=i)
        i = i+1

    scroll_frame.pack(side="top", fill="both", expand=True)
    window.mainloop()


if __name__ == '__main__':
    main()
