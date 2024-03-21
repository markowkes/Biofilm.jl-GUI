import customtkinter

class SimulationFrame(customtkinter.CTkFrame):
    def __init__(self, parent, params, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.params = params
        self.initSimulationFrame()
    
    def initSimulationFrame(self):
        #Simulation Parameters:
        sim_parameters = customtkinter.CTkLabel(self, text = "Simulation Parameters:")
        sim_parameters.grid(row = 0, column = 0)

        #Title:
        sp_title = customtkinter.CTkLabel(self, text = "Title: ").grid(row = 1, column = 0)
        sp_title_entry = customtkinter.CTkEntry(self, textvariable=self.params["title"]).grid(row = 1, column = 1, pady = 3)

        #Simulation Run Time:
        sp_sim_time = customtkinter.CTkLabel(self, text = "Simulation Time (days): ").grid(row = 2, column = 0)
        sp_sim_time_entry = customtkinter.CTkEntry(self, textvariable=self.params["run_time"])
        sp_sim_time_entry.grid(row = 2, column = 1, pady = 3)
        sp_sim_time_entry.insert(0, "1")

        #Tolerance:
        sp_tolerance = customtkinter.CTkLabel(self, text = "Tolerance: ").grid(row = 3, column = 0)
        sp_tolerance_entry = customtkinter.CTkEntry(self, textvariable=self.params["tolerance"])
        sp_tolerance_entry.grid(row = 3, column = 1, pady = 3)
        sp_tolerance_entry.insert(0, "1e-4")

        #output time step
        sp_output_period = customtkinter.CTkLabel(self, text = "Output period (days): ").grid(row = 4, column = 0)
        sp_output_period_entry = customtkinter.CTkEntry(self, textvariable=self.params["output_period"])
        sp_output_period_entry.grid(row = 4, column = 1, pady = 3)
        sp_output_period_entry.insert(0, "0.1")

    def getParams(self):
        return self.params