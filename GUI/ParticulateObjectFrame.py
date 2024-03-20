#Frame for particulate
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import GraphFrame

class ObjectFrame(customtkinter.CTkFrame):
    def __init__(self, master, name, Xto, Pbo, rho, kdet, index, **kwargs):
        super().__init__(master, **kwargs)

        self.name = customtkinter.StringVar(value= name)
        self.Xto = customtkinter.StringVar(value= Xto) #initial concentration 
        self.Pbo = customtkinter.StringVar(value= Pbo) #Biofilm particulates volume fraction initial condition(s)
        self.rho = customtkinter.StringVar(value= rho) #Particulate densities
        self.kdet = customtkinter.StringVar(value= kdet) #Particulates detachment coefficient
        self.master = master
        self.index = index

        name_label = customtkinter.CTkLabel(master=self, text = "name").grid(row = 0, column = 0, sticky = "w", padx = 6, columnspan = 3)
        name_entry = customtkinter.CTkEntry(master = self, textvariable= self.name)
        name_entry.grid(row = 0, column = 3, pady = 9)
                        
        Pbo_label = customtkinter.CTkLabel(master=self, text = "volume fraction initial condition").grid(row = 1, column = 0, sticky = "w", padx = 6, columnspan = 3) 
        Pbo_entry = customtkinter.CTkEntry(master = self, textvariable= self.Pbo)
        Pbo_entry.grid(row = 1, column = 3, pady = 9)

        Sbo_label = customtkinter.CTkLabel(master=self, text = "density").grid(row = 2, column = 0, sticky = "w", padx = 6, columnspan = 3) 
        Sbo_entry = customtkinter.CTkEntry(master = self, textvariable= self.rho)
        Sbo_entry.grid(row = 2, column = 3, pady = 9)

        kdet_label = customtkinter.CTkLabel(master=self, text = "detachment coefficient").grid(row = 3, column = 0, sticky = "w", padx = 6, columnspan = 3) 
        kdet_entry = customtkinter.CTkEntry(master = self, textvariable= self.kdet)
        kdet_entry.grid(row = 3, column = 3, pady = 9)

        Xto_label = customtkinter.CTkLabel(master=self, text = "initial concentration").grid(row = 4, column = 0, sticky = "w", padx = 6, columnspan = 3) 
        Xto_entry = customtkinter.CTkEntry(master = self, textvariable= self.Xto)
        Xto_entry.grid(row = 4, column = 3, pady = 9)

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

        self.delete_object_button = customtkinter.CTkButton(master = self, text = "Delete Particulate", command = deleteObject, fg_color= "red", hover_color= "darkred")
        self.delete_object_button.grid(row = 5, column = 0, columnspan = 2)
        self.add_solute_inflow_button = customtkinter.CTkButton(master = self, text = "Particulate Inflow", command = addSoluteInflow)
        self.add_solute_inflow_button.grid(row = 5, column = 2, columnspan = 2)

    def getParams(self):
        params = {}
        params["name"] = self.name.get()
        params["xto"] = self.Xto.get()
        params["pbo"] = self.Pbo.get()
        params["rho"] = self.rho.get()
        params["kdet"] = self.kdet.get()
        return params

