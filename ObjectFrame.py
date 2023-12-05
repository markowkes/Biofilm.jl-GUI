#Frame for particulate/ solute
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

class ObjectFrame(customtkinter.CTkFrame):
    def __init__(self, master, name, Sto, Sbo, Dt, Db, index, **kwargs):
        super().__init__(master, **kwargs)
        self.name = name
        self.Sto = Sto
        self.Sbo = Sbo
        self.Dt = Dt
        self.Db = Db
        self.master = master
        self.index = index

        name_label = customtkinter.CTkLabel(master=self, text = "Name").grid(row = 0, column = 0, sticky = "w", padx = 6, columnspan = 3)
        name_entry = customtkinter.CTkEntry(master = self)
        name_entry.grid(row = 0, column = 3, pady = 9)
                        
        Sto_label = customtkinter.CTkLabel(master=self, text = "tank initial concenctration").grid(row = 1, column = 0, sticky = "w", padx = 6, columnspan = 3) #Tank substrate concentration inital condition (Sto)
        Sto_entry = customtkinter.CTkEntry(master = self)
        Sto_entry.grid(row = 1, column = 3, pady = 9)
        Sto_entry.insert(0, self.Sto)

        Sbo_label = customtkinter.CTkLabel(master=self, text = "biofilm initial concentration").grid(row = 2, column = 0, sticky = "w", padx = 6, columnspan = 3) #Biofilm substrates concentration inital conditions (Sbo)
        Sbo_entry = customtkinter.CTkEntry(master = self)
        Sbo_entry.grid(row = 2, column = 3, pady = 9)
        Sbo_entry.insert(0, self.Sbo)

        Dt_label = customtkinter.CTkLabel(master=self, text = "substrate diffusion").grid(row = 3, column = 0, sticky = "w", padx = 6, columnspan = 3) #Aquious substrate diffusion through tank fluid (Dt)
        Dt_entry = customtkinter.CTkEntry(master = self)
        Dt_entry.grid(row = 3, column = 3, pady = 9)
        Dt_entry.insert(0, self.Dt)

        Db_label = customtkinter.CTkLabel(master=self, text = "Effective").grid(row = 4, column = 0, sticky = "w", padx = 6, columnspan = 3) #Effective substrate diffusion through biofilm (Db)
        Db_entry = customtkinter.CTkEntry(master = self)
        Db_entry.grid(row = 4, column = 3, pady = 9)
        Db_entry.insert(0, self.Db)

        def getIndex():
            return self.index

        def heavy():
            print("heavy called")
            heavi_y_values = np.zeros(len(self.time))
            for i in range(len(self.time)):
                heavi_y_values[i] = 0 if self.time[i] < self.per_tstart else self.per_amplitude*(1 - np.heaviside(((self.time[i] - self.per_tstart) % self.per_period) - self.per_duration, 0.5))
            #print(heavi_y_values)
            return heavi_y_values

        def updateConstY(new_y):
            self.con_ax.cla()
            self.con_y = float(new_y)
            self.con_ax.axhline(y = new_y)
            self.canvas.draw()

        def constant():
            #disable constant button, and enable other buttons in case they were discabled, then deselect other buttons.
            self.constant_button.configure(state="disabled")
            self.periodic_button.configure(state="normal")
            self.sin_button.configure(state="normal")
            self.periodic_button.deselect()
            self.sin_button.deselect()

            y_label = customtkinter.CTkLabel(master = self, text = "inflow").grid(row = 1, column = 8)
            y_entry = customtkinter.CTkEntry(master = self)
            y_entry.grid(row = 1, column = 9)
            y_entry.insert(0, 1.0)
            y_entry.bind('<Return>', command = lambda event: updateConstY(y_entry.get()))


        def updatePerAmplitude(amp):
            self.per_ax.cla()
            self.per_amplitude = float(amp)
            #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
            self.per_ax.plot(self.time, heavy())
            self.canvas.draw()

        def updatePerPeriod(per):
            self.sin_ax.cla()
            self.sin_period = float(per)
            #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
            self.per_ax.plot(self.time, heavy())
            self.canvas.draw()

        def updatePerDuration(duration):
            self.per_ax.cla()
            self.per_duration = float(duration)
            #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
            self.per_ax.plot(self.time, heavy())
            self.canvas.draw()

        def updatePerTStart(tstart):
            self.per_ax.cla()
            self.per_tstart = float(tstart)
            #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
            self.per_ax.plot(self.time, heavy())
            self.canvas.draw()

        def periodic():
            #disable periodic button, and enable other buttons in case they were discabled, then deselect other buttons.
            self.periodic_button.configure(state="disabled")
            self.constant_button.configure(state="normal")
            self.sin_button.configure(state="normal")
            self.constant_button.deselect()
            self.sin_button.deselect()

            amp_label = customtkinter.CTkLabel(master = self, text = "amplitude").grid(row = 1, column = 8)
            amp_entry = customtkinter.CTkEntry(master = self)
            amp_entry.grid(row = 1, column = 9)
            amp_entry.insert(0, 1.0)
            amp_entry.bind('<Return>', command = lambda event: updatePerAmplitude(amp_entry.get()))

            period_label = customtkinter.CTkLabel(self, text = "period").grid(row = 2, column = 8)
            period_entry = customtkinter.CTkEntry(self)
            period_entry.grid(row = 2, column = 9)
            period_entry.insert(0, 1.0)
            period_entry.bind('<Return>', command = lambda event: updatePerPeriod(period_entry.get()))

            duration_label = customtkinter.CTkLabel(self, text = "duration").grid(row = 3, column = 8)
            duration_entry = customtkinter.CTkEntry(self) 
            duration_entry.grid(row = 3, column = 9)
            duration_entry.insert(0, 1.0)
            duration_entry.bind('<Return>', command = lambda event: updatePerDuration(duration_entry.get()))

            tstart_label = customtkinter.CTkLabel(self, text = "start time").grid(row = 4, column = 8)
            tstart_entry = customtkinter.CTkEntry(self) 
            tstart_entry.grid(row = 4, column = 9)
            tstart_entry.insert(0, 1.0)
            tstart_entry.bind('<Return>', command = lambda event: updatePerTStart(tstart_entry.get()))

            self.per_amplitude = float(amp_entry.get())
            self.per_period = float(period_entry.get())
            self.per_duration = float(duration_entry.get())
            self.per_tstart = float(tstart_entry.get())
            #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
            self.per_ax.plot(self.time, heavy())
            self.canvas.draw()
            self.update()
        

        def updateSinAmplitude(amp):
            self.sin_ax.cla()
            self.sin_amplitude = float(amp)
            self.sin_ax.plot(self.time, self.sin_y_offset + self.sin_amplitude*np.sin(2*math.pi*self.time/self.sin_period))
            self.canvas.draw()

        def updateSinPeriod(per):
            self.sin_ax.cla()
            self.sin_period = float(per)
            self.sin_ax.plot(self.time, self.sin_y_offset + self.sin_amplitude*np.sin(2*math.pi*self.time/self.sin_period))            
            self.canvas.draw()

        def updateSinYOffset(offset):
            self.sin_ax.cla()
            self.sin_y_offset = float(offset)
            self.sin_ax.plot(self.time, self.sin_y_offset + self.sin_amplitude*np.sin(2*math.pi*self.time/self.sin_period))
            self.canvas.draw()

        def sin():
            #disable sin button, and enable other buttons in case they were discabled, then deselect other buttons.
            self.sin_button.configure(state="disabled")
            self.constant_button.configure(state="normal")
            self.periodic_button.configure(state="normal")
            self.constant_button.deselect()
            self.periodic_button.deselect()

            amp_label = customtkinter.CTkLabel(master = self, text = "amplitude").grid(row = 1, column = 8)
            amp_entry = customtkinter.CTkEntry(master = self)
            amp_entry.grid(row = 1, column = 9)
            amp_entry.insert(0, 2.0)
            amp_entry.bind('<Return>', command = lambda event: updateSinAmplitude(amp_entry.get()))

            period_label = customtkinter.CTkLabel(self, text = "period").grid(row = 2, column = 8)
            period_entry = customtkinter.CTkEntry(self)
            period_entry.grid(row = 2, column = 9)
            period_entry.insert(0, 1.0)
            period_entry.bind('<Return>', command = lambda event: updateSinPeriod(period_entry.get()))

            y_offset_label = customtkinter.CTkLabel(self, text = "y offset").grid(row = 3, column = 8)
            y_offset_entry = customtkinter.CTkEntry(self) #Should be able to accept a negative sign
            y_offset_entry.grid(row = 3, column = 9)
            y_offset_entry.insert(0, 0.0)
            y_offset_entry.bind('<Return>', command = lambda event: updateSinYOffset(y_offset_entry.get()))

            self.sin_y_offset = float(y_offset_entry.get())
            self.sin_period = float(period_entry.get())
            self.sin_amplitude = float(amp_entry.get())
            self.sin_ax.plot(self.time, self.sin_y_offset + self.sin_amplitude*np.sin(2*math.pi*self.time/self.sin_period))
            self.canvas.draw()
            self.update()


        def addSoluteInflow():
            self.add_solute_inflow_button.configure(state="disabled")
            self.constant_button = customtkinter.CTkRadioButton(self, text= "constant", command = constant)
            self.constant_button.grid(row = 1, column = 6, padx = 16)
            self.periodic_button = customtkinter.CTkRadioButton(self, text= "periodic", command = periodic)
            self.periodic_button.grid(row = 2, column = 6, padx = 16)
            self.sin_button = customtkinter.CTkRadioButton(self, text= "sinusoidal", command = sin)
            self.sin_button.grid(row = 3, column = 6, padx = 16)

            fig, sin_ax = plt.subplots()
            self.sin_ax = sin_ax
            fig, per_ax = plt.subplots()
            self.per_ax = per_ax
            fig, con_ax = plt.subplots()
            self.con_ax = con_ax
            self.fig = fig
            self.time = np.linspace(0, 10, 1000)

            canvas = FigureCanvasTkAgg(fig, master = self)
            self.canvas = canvas
            self.canvas.get_tk_widget().grid(row = 0, column = 7, rowspan = 5, padx = 5)
            self.update()

        def deleteObject():
            #master.deleteFrame(self)
            self.grid_forget()
            master.update()

        self.delete_object_button = customtkinter.CTkButton(master = self, text = "Delete Solute", command = deleteObject, fg_color= "red", hover_color= "darkred")
        self.delete_object_button.grid(row = 5, column = 0, columnspan = 2)
        self.add_solute_inflow_button = customtkinter.CTkButton(master = self, text = "Solute Inflow", command = addSoluteInflow)
        self.add_solute_inflow_button.grid(row = 5, column = 2, columnspan = 2)
