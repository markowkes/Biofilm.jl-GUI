#Frame for particulate/ solute
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import GraphFrame

class ObjectFrame(customtkinter.CTkFrame):
    def __init__(self, master, object_params, index, **kwargs):
        super().__init__(master, **kwargs)

        self.params = object_params
        self.master = master
        self.index = index
        self.initLabels()
        self.initButtons()


    def initLabels(self):
        name_label = customtkinter.CTkLabel(master=self, text = "Name").grid(row = 0, column = 0, sticky = "w", padx = 6, columnspan = 3)
        name_entry = customtkinter.CTkEntry(master = self, textvariable= self.params["name"])
        name_entry.grid(row = 0, column = 3, pady = 9)
                        
        Sto_label = customtkinter.CTkLabel(master=self, text = "tank initial concenctration").grid(row = 1, column = 0, sticky = "w", padx = 6, columnspan = 3) #Tank substrate concentration inital condition (Sto)
        Sto_entry = customtkinter.CTkEntry(master = self, textvariable= self.params["sto"])
        Sto_entry.grid(row = 1, column = 3, pady = 9)

        Sbo_label = customtkinter.CTkLabel(master=self, text = "biofilm initial concentration").grid(row = 2, column = 0, sticky = "w", padx = 6, columnspan = 3) #Biofilm substrates concentration inital conditions (Sbo)
        Sbo_entry = customtkinter.CTkEntry(master = self, textvariable= self.params["sbo"])
        Sbo_entry.grid(row = 2, column = 3, pady = 9)

        Dt_label = customtkinter.CTkLabel(master=self, text = "substrate diffusion").grid(row = 3, column = 0, sticky = "w", padx = 6, columnspan = 3) #Aquious substrate diffusion through tank fluid (Dt)
        Dt_entry = customtkinter.CTkEntry(master = self, textvariable= self.params["dt"])
        Dt_entry.grid(row = 3, column = 3, pady = 9)

        Db_label = customtkinter.CTkLabel(master=self, text = "Effective").grid(row = 4, column = 0, sticky = "w", padx = 6, columnspan = 3) #Effective substrate diffusion through biofilm (Db)
        Db_entry = customtkinter.CTkEntry(master = self, textvariable= self.params["db"])
        Db_entry.grid(row = 4, column = 3, pady = 9)


    def getIndex(self):
        return self.index


    def addSoluteInflow(self):
        self.add_solute_inflow_button.configure(state="disabled")
        self.graph_frame = GraphFrame.GraphFrame(master = self)
        self.graph_frame.grid(row = 0, column = 4, rowspan = 5)


    def deleteObject(self):
        self.master.deleteFrame(self.index)
        self.grid_forget()
        self.master.update()


    def initButtons(self):
        self.delete_object_button = customtkinter.CTkButton(master = self, text = "Delete Solute", command = self.deleteObject, fg_color= "red", hover_color= "darkred")
        self.delete_object_button.grid(row = 5, column = 0, columnspan = 2)
        self.add_solute_inflow_button = customtkinter.CTkButton(master = self, text = "Solute Inflow", command = self.addSoluteInflow)
        self.add_solute_inflow_button.grid(row = 5, column = 2, columnspan = 2)


    def getParams(self):
        return self.params


    def getName(self):
        return self.params["name"].get()
    

    def getInflowParams(self):
        return self.graph_frame.getParams()