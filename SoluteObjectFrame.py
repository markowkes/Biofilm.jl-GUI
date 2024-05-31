#Frame for particulate/ solute
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import GraphFrame

class ObjectFrame(customtkinter.CTkFrame):
    def __init__(self, master, object_params, **kwargs):
        super().__init__(master, **kwargs)

        self.params = object_params
        self.master = master
        self.graph_frame = None
        self.initLabels()
        self.initButtons()


    def __repr__(self):
        message = "SoluteObjectFrame- name: {}"
        message = message.format(self.params["name"].get())
        return message


    def __str__(self):
        return self.__repr__()


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


    def addSoluteInflow(self):
        self.add_solute_inflow_button.configure(state="disabled")
        self.graph_frame = GraphFrame.GraphFrame(master = self)
        self.graph_frame.grid(row = 0, column = 4, rowspan = 5)


    def deleteObject(self):
        self.master.deleteFrame(self)
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
        if self.graph_frame == None: #case for when no inflow has been defined
            if 'Sin' in self.params: #currently, the Sin parameter will only exist if it was loaded from a file
                return self.params['Sin']
            return
        
        graph_params = self.graph_frame.getParams()
        equation = ''
        if len(graph_params) == 0:
            return '0.0'
        elif graph_params[0] == 'constant':
            equation = graph_params[1]
        elif graph_params[0] == 'periodic': #index:variable- 1:amplitude, 2:period, 3:duration, 4:tstart
            #from the SRB example:
            #(t) -> 500*smoothHeaviside(t,2.5)
            #But we want it to repeat like this: (but this uses the np.heaviside function which is not in julia)
            #self.per_amplitude*(1 - np.heaviside(((self.time[i] - self.per_tstart) % self.per_period) - self.per_duration
            equation = '{}*(1 - smoothHeaviside(t,{}) % {}) - {}'
            equation = equation.format(graph_params[1], graph_params[4], graph_params[2], graph_params[3])
        elif graph_params[0] == 'sin': #index:variable- 1:amplitude, 2:period, 3:y offset
            #self.sin_y_offset + self.sin_amplitude*np.sin(2*math.pi*self.time/self.sin_period)
            equation = '{} + {}*sind(2pi*t/{})'
            equation = equation.format(graph_params[3], graph_params[1], graph_params[2])
        else:
            print("error with getting Sin from solute graph")
        return equation