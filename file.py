from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import planesections as ps
import numpy as np
import matplotlib.pyplot as plt

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Beams for The TOP G')

        self.len_str = StringVar()
        self.fix1_pos = StringVar()
        self.fix2_pos = StringVar()
        self.fix1_type = StringVar()
        self.fix2_type = StringVar()
        self.load_amount = StringVar()
        self.load_place = StringVar()
        self.up = IntVar()
        self.lastpos = 0

        self.dist_len = StringVar()
        self.dist_amount = StringVar()
        self.dist_place = StringVar()

        self.list_of_loads = []
        # button
        # self.button = ttk.Button(self, text='Click Me')
        # self.button['command'] = self.button_clicked
        # self.button.pack()
        #input beam length 
        ctk.CTkLabel(self, text="Beam Length").grid(column=0, row=5,padx =10 ,pady =10)
        self.len_entry = ctk.CTkEntry(self, textvariable=self.len_str).grid(column=1, row=5,padx=10,pady =10) 

        
        ctk.CTkLabel(self, text="Fixity Points").grid(column=0, row=8)
        ctk.CTkLabel(self, text="Fixity Point A").grid(column=1, row=7)
        ctk.CTkLabel(self, text="Fixity Point B").grid(column=2, row=7)

        self.fixity1_entry = ctk.CTkEntry(self, textvariable=self.fix1_pos).grid(column=1, row=8)
        self.fixity2_entry = ctk.CTkEntry(self, textvariable=self.fix2_pos).grid(column=2, row=8)

        ctk.CTkLabel(self,text="type for fixity A").grid(column=1, row=10)
        ctk.CTkLabel(self,text="type for fixity B").grid(column=2, row=10)
        note = ctk.CTkLabel(self,text="---Note : 1 is pinned , 2 is fixed and 3 is roller---")
        note.grid(column = 1, row = 9, columnspan = 2, sticky ="EW")
        note.configure(font=('Arial', 9))
        self.fixity1_type_entry = ctk.CTkEntry(self, textvariable=self.fix1_type).grid(column=1, row=11)
        self.fixity2_type_entry = ctk.CTkEntry(self, textvariable=self.fix2_type).grid(column=2, row=11)



        ctk.CTkLabel(self, text="Load in KN").grid(column=1, row=12)
        ctk.CTkLabel(self, text="Load pos on the X axis").grid(column=2, row=12)
        ctk.CTkLabel(self,text="Point Load").grid(column=0, row=14)
        point_load_btn = ctk.CTkButton(self, text="Add Point Load",command=self.add_point_load).grid(column=4, row=14)

        self.load_entry = ctk.CTkEntry(self,textvariable=self.load_amount).grid(column=1, row=14)
        self.load_pos_entry = ctk.CTkEntry(self,textvariable=self.load_place).grid(column=2, row=14)

        ctk.CTkLabel(self, text="dist in KN").grid(column=1, row=16)
        ctk.CTkLabel(self, text="dist pos on the X axis").grid(column=2, row=16)
        ctk.CTkLabel(self, text="dist length").grid(column=3, row=16)
        ctk.CTkLabel(self,text="dist Load").grid(column=0, row=18)
        point_dist_btn = ctk.CTkButton(self, text="Add dist Load",command=self.add_dist).grid(column=4, row=18,pady=10,padx=10)
        
        self.dist_length = ctk.CTkEntry(self,textvariable=self.dist_len).grid(column=3, row=18)
        self.dist_entry = ctk.CTkEntry(self,textvariable=self.dist_amount).grid(column=1, row=18)
        self.dist_pos_entry = ctk.CTkEntry(self,textvariable=self.dist_place).grid(column=2, row=18)


        ctk.CTkCheckBox(self, text='Force is Down',variable=self.up, onvalue=-1, offvalue=1).grid(column=3, row=14 ,padx =10,pady =10)
        ctk.CTkButton(self, text="MAKE ME A BEAM", command=self.make_beam).grid(column=1, row=30,padx=10,pady= 10)
        ctk.CTkButton(self, text="plot it", command=self.plot).grid(column=2, row=30,padx=10,pady= 10)
        ctk.CTkButton(self, text="Analyze it", command=self.analyze).grid(column=2, row=35,padx=10,pady= 10)

        ctk.CTkButton(self, text="Quit", command=self.quit).grid(column=1, row=35)

    def make_beam(self):
        L = float(self.len_str.get())
        #supp dict [[pos , type]]
        supp_num = []
        supp1_type = []
        supp2_type = []
        fixity1_pos = float(self.fix1_pos.get())
        fixity2_pos = float(self.fix2_pos.get())
        
        supp_type = []
        supp_num.append(self.fix1_type.get())
        supp_num.append(self.fix2_type.get())
        for i , supp in enumerate(supp_num):
            if supp == "1" or supp.lower() == "pinned": #pinned
                supp_type = [1,1,0]
            if supp == "2" or supp.lower() == "fixed": #"fixed"
                supp_type = [1,1,1]
            if supp == "3"  or supp.lower() == "roller": #"roller"
                supp_type = [0,1,0]
            if(i == 0):
                supp1_type = supp_type
            else:
                supp2_type = supp_type
            
        self.beam = ps.newEulerBeam2D(L)
        self.beam.setFixity(fixity1_pos, supp1_type, label = "A")
        self.beam.setFixity(fixity2_pos, supp2_type, label = "B")

        
    def add_point_load(self):
        f = float(self.load_amount.get())
        pos = float(self.load_place.get())
        up = self.up.get()
        Pz = 1000
        self.beam.addVerticalLoad(pos, f*Pz*up , label="{}KN".format(f))
        if(self.lastpos == 0):
            ctk.CTkLabel(self,text="Load in kN").grid(column=3, row=5+self.lastpos)
            ctk.CTkLabel(self,text="Position on X").grid(column=4, row=5+self.lastpos)
            ctk.CTkLabel(self,text="Force is Down '-Y' ").grid(column=5, row=5+self.lastpos)
        self.lastpos += 1
        ctk.CTkLabel(self,text="{}KN".format(f)).grid(column=3, row=5+self.lastpos)
        ctk.CTkLabel(self,text="{}m".format(pos)).grid(column=4, row=5+self.lastpos)
        if(up == 1):
            ctk.CTkLabel(self,text="UP +Y".format(pos)).grid(column=5, row=5+self.lastpos)
        elif(up == -1):
            ctk.CTkLabel(self,text="Down =Y".format(pos)).grid(column=5, row=5+self.lastpos)
    def add_dist(self):
        Pz = -1000
        dist_len = float(self.dist_len.get())
        f = float(self.dist_amount.get())
        pos = float(self.dist_place.get())
        self.beam.addDistLoadVertical(pos, dist_len, f*Pz)
    def plot(self):
        ps.plotBeamDiagram(self.beam)    
        plt.show()
    def analyze(self):
        analysis = ps.OpenSeesAnalyzer2D(self.beam)
        analysis.runAnalysis()
        # Plot the SFD and BMD
        ps.plotMoment2D(self.beam)
        var = ps.plotShear2D(self.beam)
        plt.show()



if __name__ == "__main__":
    app = App()
    app.mainloop()



