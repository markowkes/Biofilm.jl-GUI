#graph frame class
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.time = np.linspace(0, 10, 1000)

    def heavy(self):
        heavi_y_values = np.zeros(len(self.time))
        for i in range(len(self.time)):
            heavi_y_values[i] = 0 if self.time[i] < self.per_tstart else self.per_amplitude*(1 - np.heaviside(((self.time[i] - self.per_tstart) % self.per_period) - self.per_duration, 0.5))
        return heavi_y_values

    #Functions for CONSTANT graph:
    def updateConstY(self, new_y):
        self.con_ax.cla()
        self.con_y = float(new_y)
        self.con_ax.axhline(y = new_y)
        self.con_canvas.draw()

    def constant(self): #called when 'constant' button is selected
        #disable constant button, and enable other buttons in case they were discabled, then deselect other buttons.
        self.constant_button.configure(state="disabled")
        self.periodic_button.configure(state="normal")
        self.sin_button.configure(state="normal")
        self.periodic_button.deselect()
        self.sin_button.deselect()
        #self.graph_frame.grid_forget()
        self.sin_canvas.get_tk_widget().grid(row = 0, column = 0, rowspan = 3, padx = 5) #place canvas

        y_label = customtkinter.CTkLabel(master = self.graph_frame, text = "inflow").grid(row = 1, column = 8)
        y_entry = customtkinter.CTkEntry(master = self.graph_frame)
        y_entry.grid(row = 1, column = 9)
        y_entry.insert(0, 1.0)
        y_entry.bind('<Return>', command = lambda event: self.updateConstY(y_entry.get()))

        self.con_canvas.draw()
        self.update()

    #Functions for PERIODIC graph:
    def updatePerAmplitude(self, amp):
        self.per_ax.cla()
        self.per_amplitude = float(amp)
        #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
        self.per_ax.plot(self.time, self.heavy())
        self.per_canvas.draw()

    def updatePerPeriod(self, per):
        self.per_ax.cla()
        self.per_period = float(per)
        #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
        self.per_ax.plot(self.time, self.heavy())
        self.per_canvas.draw()

    def updatePerDuration(self, duration):
        self.per_ax.cla()
        self.per_duration = float(duration)
        #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
        self.per_ax.plot(self.time, self.heavy())
        self.per_canvas.draw()

    def updatePerTStart(self, tstart):
        self.per_ax.cla()
        self.per_tstart = float(tstart)
        #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
        self.per_ax.plot(self.time, self.heavy())
        self.per_canvas.draw()

    def periodic(self): #called when 'periodic' button is selected
        #disable periodic button, and enable other buttons in case they were discabled, then deselect other buttons.
        self.periodic_button.configure(state="disabled")
        self.constant_button.configure(state="normal")
        self.sin_button.configure(state="normal")
        self.constant_button.deselect()
        self.sin_button.deselect()
        #self.graph_frame.grid_forget()
        self.per_canvas.get_tk_widget().grid(row = 0, column = 0, rowspan = 3, padx = 5) #place canvas

        amp_label = customtkinter.CTkLabel(master = self.graph_frame, text = "amplitude").grid(row = 1, column = 8)
        amp_entry = customtkinter.CTkEntry(master = self.graph_frame)
        amp_entry.grid(row = 1, column = 9)
        amp_entry.insert(0, 1.0)
        amp_entry.bind('<Return>', command = lambda event: self.updatePerAmplitude(amp_entry.get()))

        period_label = customtkinter.CTkLabel(master = self.graph_frame, text = "period").grid(row = 2, column = 8)
        period_entry = customtkinter.CTkEntry(master = self.graph_frame)
        period_entry.grid(row = 2, column = 9)
        period_entry.insert(0, 1.0)
        period_entry.bind('<Return>', command = lambda event: self.updatePerPeriod(period_entry.get()))

        duration_label = customtkinter.CTkLabel(master = self.graph_frame, text = "duration").grid(row = 3, column = 8)
        duration_entry = customtkinter.CTkEntry(master = self.graph_frame) 
        duration_entry.grid(row = 3, column = 9)
        duration_entry.insert(0, 0.5)
        duration_entry.bind('<Return>', command = lambda event: self.updatePerDuration(duration_entry.get()))

        tstart_label = customtkinter.CTkLabel(master = self.graph_frame, text = "start time").grid(row = 4, column = 8)
        tstart_entry = customtkinter.CTkEntry(master = self.graph_frame) 
        tstart_entry.grid(row = 4, column = 9)
        tstart_entry.insert(0, 1.0)
        tstart_entry.bind('<Return>', command = lambda event: self.updatePerTStart(tstart_entry.get()))

        self.per_amplitude = float(amp_entry.get())
        self.per_period = float(period_entry.get())
        self.per_duration = float(duration_entry.get())
        self.per_tstart = float(tstart_entry.get())
        #self.params.get("per_ax").plot(self.params.get("time"), 0 if self.params.get("time") < self.params.get("per_tstart") else self.params.get("amplitude")(1 - np.heaviside(((self.params.get("time") - self.params.get("per_tstart")) % self.params.get("period")) - self.params.get("duration")), 0.5))
        self.per_ax.plot(self.time, self.heavy())
        
        self.per_canvas.draw()
        self.update()
    
    #Functions for SINUSOIDAL graph:
    def updateSinAmplitude(self, amp):
        self.sin_ax.cla()
        self.sin_amplitude = float(amp)
        self.sin_ax.plot(self.time, self.sin_y_offset + self.sin_amplitude*np.sin(2*math.pi*self.time/self.sin_period))
        self.sin_canvas.draw()

    def updateSinPeriod(self, per):
        self.sin_ax.cla()
        self.sin_period = float(per)
        self.sin_ax.plot(self.time, self.sin_y_offset + self.sin_amplitude*np.sin(2*math.pi*self.time/self.sin_period))            
        self.sin_canvas.draw()

    def updateSinYOffset(self, offset):
        self.sin_ax.cla()
        self.sin_y_offset = float(offset)
        self.sin_ax.plot(self.time, self.sin_y_offset + self.sin_amplitude*np.sin(2*math.pi*self.time/self.sin_period))
        self.sin_canvas.draw()

    def sin(self):
        #disable sin button, and enable other buttons in case they were discabled, then deselect other buttons.
        self.sin_button.configure(state="disabled")
        self.constant_button.configure(state="normal")
        self.periodic_button.configure(state="normal")
        self.constant_button.deselect()
        self.periodic_button.deselect()
        #self.graph_frame.grid_forget()
        self.sin_canvas.get_tk_widget().grid(row = 0, column = 0, rowspan = 3, padx = 5) #place canvas

        amp_label = customtkinter.CTkLabel(master = self.graph_frame, text = "amplitude").grid(row = 1, column = 8)
        amp_entry = customtkinter.CTkEntry(master = self.graph_frame)
        amp_entry.grid(row = 1, column = 9)
        amp_entry.insert(0, 2.0)
        amp_entry.bind('<Return>', command = lambda event: self.updateSinAmplitude(amp_entry.get()))

        period_label = customtkinter.CTkLabel(master = self.graph_frame, text = "period").grid(row = 2, column = 8)
        period_entry = customtkinter.CTkEntry(master = self.graph_frame)
        period_entry.grid(row = 2, column = 9)
        period_entry.insert(0, 1.0)
        period_entry.bind('<Return>', command = lambda event: self.updateSinPeriod(period_entry.get()))

        y_offset_label = customtkinter.CTkLabel(master = self.graph_frame, text = "y offset").grid(row = 3, column = 8)
        y_offset_entry = customtkinter.CTkEntry(master = self.graph_frame) #Should be able to accept a negative sign
        y_offset_entry.grid(row = 3, column = 9)
        y_offset_entry.insert(0, 0.0)
        y_offset_entry.bind('<Return>', command = lambda event: self.updateSinYOffset(y_offset_entry.get()))

        self.sin_y_offset = float(y_offset_entry.get())
        self.sin_period = float(period_entry.get())
        self.sin_amplitude = float(amp_entry.get())
        self.sin_ax.plot(self.time, self.sin_y_offset + self.sin_amplitude*np.sin(2*math.pi*self.time/self.sin_period))
        
        self.sin_canvas.draw()
        self.update()
    
    def draw(self):
        #frame for graph and parameters:
        self.graph_frame = customtkinter.CTkFrame(master= self)
        self.graph_frame.grid(row = 1, column = 2, rowspan = 3)
                    
        #Buttons:
        self.constant_button = customtkinter.CTkRadioButton(master = self.graph_frame, text= "constant", command = self.constant)
        self.constant_button.grid(row = 1, column = 1, padx = 16, pady = 30)
        self.periodic_button = customtkinter.CTkRadioButton(master = self.graph_frame, text= "periodic", command = self.periodic)
        self.periodic_button.grid(row = 2, column = 1, padx = 16, pady = 30)
        self.sin_button = customtkinter.CTkRadioButton(master = self.graph_frame, text= "sinusoidal", command = self.sin)
        self.sin_button.grid(row = 3, column = 1, padx = 16, pady = 30)

        sin_fig, sin_ax = plt.subplots()
        self.sin_ax = sin_ax
        per_fig, per_ax = plt.subplots()
        self.per_ax = per_ax
        con_fig, con_ax = plt.subplots()
        self.con_ax = con_ax
        self.sin_canvas = FigureCanvasTkAgg(sin_fig, master = self.graph_frame)
        self.per_canvas = FigureCanvasTkAgg(per_fig, master = self.graph_frame)
        self.con_canvas = FigureCanvasTkAgg(con_fig, master = self.graph_frame)
        

    draw()


