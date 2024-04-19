#Frame for particulate
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
        name_label = customtkinter.CTkLabel(master=self, text = "name").grid(row = 0, column = 0, sticky = "w", padx = 6, columnspan = 3)
        name_entry = customtkinter.CTkEntry(master = self, textvariable= self.params["name"])
        name_entry.grid(row = 0, column = 3, pady = 9)
                        
        Pbo_label = customtkinter.CTkLabel(master=self, text = "volume fraction initial condition").grid(row = 1, column = 0, sticky = "w", padx = 6, columnspan = 3) 
        Pbo_entry = customtkinter.CTkEntry(master = self, textvariable= self.params["pbo"])
        Pbo_entry.grid(row = 1, column = 3, pady = 9)

        Sbo_label = customtkinter.CTkLabel(master=self, text = "density").grid(row = 2, column = 0, sticky = "w", padx = 6, columnspan = 3) 
        Sbo_entry = customtkinter.CTkEntry(master = self, textvariable= self.params["rho"])
        Sbo_entry.grid(row = 2, column = 3, pady = 9)

        Xto_label = customtkinter.CTkLabel(master=self, text = "initial concentration").grid(row = 3, column = 0, sticky = "w", padx = 6, columnspan = 3) 
        Xto_entry = customtkinter.CTkEntry(master = self, textvariable= self.params["xto"])
        Xto_entry.grid(row = 3, column = 3, pady = 9)

    def getIndex(self):
        return self.index


    def addSoluteInflow(self):
        self.add_solute_inflow_button.configure(state="disabled")
        self.graph_frame = GraphFrame.GraphFrame(master = self)
        self.graph_frame.grid(row = 0, column = 4, rowspan = 5)


    def deleteObject(self):
        #master.deleteFrame(self)
        self.grid_forget()
        self.master.update()


    def initButtons(self):
        self.delete_object_button = customtkinter.CTkButton(master = self, text = "Delete Particulate", command = self.deleteObject, fg_color= "red", hover_color= "darkred")
        self.delete_object_button.grid(row = 5, column = 0, columnspan = 2)
        self.add_solute_inflow_button = customtkinter.CTkButton(master = self, text = "Particulate Inflow", command = self.addSoluteInflow)
        self.add_solute_inflow_button.grid(row = 5, column = 2, columnspan = 2)

    def getParams(self):
        return self.params
    
    def getName(self):
        return self.params["name"].get()

