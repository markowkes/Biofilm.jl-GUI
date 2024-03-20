#Frame for particulate/ solute
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import GraphFrame

class ObjectFrame(customtkinter.CTkFrame):
    def __init__(self, master, name, Sto, Sbo, Dt, Db, index, **kwargs):
        super().__init__(master, **kwargs)

        self.name = customtkinter.StringVar(value= name)
        self.Sto = customtkinter.StringVar(value= Sto)
        self.Sbo = customtkinter.StringVar(value= Sbo)
        self.Dt = customtkinter.StringVar(value= Dt)
        self.Db = customtkinter.StringVar(value= Db)
        self.master = master
        self.index = index

        name_label = customtkinter.CTkLabel(master=self, text = "Name").grid(row = 0, column = 0, sticky = "w", padx = 6, columnspan = 3)
        name_entry = customtkinter.CTkEntry(master = self, textvariable= self.name)
        name_entry.grid(row = 0, column = 3, pady = 9)
                        
        Sto_label = customtkinter.CTkLabel(master=self, text = "tank initial concenctration").grid(row = 1, column = 0, sticky = "w", padx = 6, columnspan = 3) #Tank substrate concentration inital condition (Sto)
        Sto_entry = customtkinter.CTkEntry(master = self, textvariable= self.Sto)
        Sto_entry.grid(row = 1, column = 3, pady = 9)
        #Sto_entry.insert(0, self.Sto.get())

        Sbo_label = customtkinter.CTkLabel(master=self, text = "biofilm initial concentration").grid(row = 2, column = 0, sticky = "w", padx = 6, columnspan = 3) #Biofilm substrates concentration inital conditions (Sbo)
        Sbo_entry = customtkinter.CTkEntry(master = self, textvariable= self.Sbo)
        Sbo_entry.grid(row = 2, column = 3, pady = 9)
        #Sbo_entry.insert(0, self.Sbo.get())

        Dt_label = customtkinter.CTkLabel(master=self, text = "substrate diffusion").grid(row = 3, column = 0, sticky = "w", padx = 6, columnspan = 3) #Aquious substrate diffusion through tank fluid (Dt)
        Dt_entry = customtkinter.CTkEntry(master = self, textvariable= self.Dt)
        Dt_entry.grid(row = 3, column = 3, pady = 9)
        #Dt_entry.insert(0, self.Dt.get())

        Db_label = customtkinter.CTkLabel(master=self, text = "Effective").grid(row = 4, column = 0, sticky = "w", padx = 6, columnspan = 3) #Effective substrate diffusion through biofilm (Db)
        Db_entry = customtkinter.CTkEntry(master = self, textvariable= self.Db)
        Db_entry.grid(row = 4, column = 3, pady = 9)


        def getIndex():
            return self.index


        def addSoluteInflow():
            self.add_solute_inflow_button.configure(state="disabled")
            self.graph_frame = GraphFrame.GraphFrame(master = self)
            self.graph_frame.grid(row = 0, column = 4, rowspan = 5)

        def deleteObject():
            #master.deleteFrame(self)
            self.grid_forget()
            master.update()

        self.delete_object_button = customtkinter.CTkButton(master = self, text = "Delete Solute", command = deleteObject, fg_color= "red", hover_color= "darkred")
        self.delete_object_button.grid(row = 5, column = 0, columnspan = 2)
        self.add_solute_inflow_button = customtkinter.CTkButton(master = self, text = "Solute Inflow", command = addSoluteInflow)
        self.add_solute_inflow_button.grid(row = 5, column = 2, columnspan = 2)

    def getParams(self):
        params = {}
        params["name"] = self.name.get()
        params["sto"] = self.Sto.get()
        params["sbo"] = self.Sbo.get()
        params["dt"] = self.Dt.get()
        params["db"] = self.Db.get()
        return params

