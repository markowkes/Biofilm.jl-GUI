import customtkinter

class GeometryFrame(customtkinter.CTkFrame):
    def __init__(self, parent, params, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.params = params
        self.initGeometryFrame()

    def initGeometryFrame(self):
        geometry_parameters = customtkinter.CTkLabel(self, text = "Tank Parameters:")
        geometry_parameters.grid(row = 0, column = 0, columnspan = 2)

        #Volume:
        volume_label = customtkinter.CTkLabel(self, text = "Volume (cubic meters): ").grid(row = 1, column = 0)
        volume_entry = customtkinter.CTkEntry(self, textvariable=self.params["volume"])
        volume_entry.grid(row = 1, column = 1, pady = 3)

        #Surface Area:
        surface_area_label = customtkinter.CTkLabel(self, text = "Surface area of biofilm (square meters)").grid(row = 2, column = 0)
        surface_area_entry = customtkinter.CTkEntry(self, textvariable=self.params["surface_area"])
        surface_area_entry.grid(row = 2, column = 1, pady = 3)

        #Flowrate:
        flowrate_label = customtkinter.CTkLabel(self, text = "Flowrate through tank (cubic meters/day)").grid(row = 3, column = 0, padx = 8)
        flowrate_entry = customtkinter.CTkEntry(self, textvariable=self.params["flowrate"])
        flowrate_entry.grid(row = 3, column = 1, pady = 3)

        #Biofilm Parameters:
        spacer = customtkinter.CTkLabel(self, text="", height = 0).grid(row = 4, column = 0)
        biofilm_parameters = customtkinter.CTkLabel(self, text = "Biofilm Parameters:")
        biofilm_parameters.grid(row = 5, column = 0, columnspan = 2)

        #Number of Gridpoints:
        gridpoints_label = customtkinter.CTkLabel(self, text = "Number of gridpoints in biofilm").grid(row = 6, column = 0) #must be an int
        gridpoints_entry = customtkinter.CTkEntry(self, textvariable=self.params["gridpoints"])
        gridpoints_entry.grid(row = 6, column = 1, pady = 3)

        #Biofilm Initial Thickness
        initial_thickness_label = customtkinter.CTkLabel(self, text = "Biofolm inital thickness (meters)").grid(row = 7, column = 0)
        initial_thickness_entry = customtkinter.CTkEntry(self, textvariable=self.params["initial_thickness"])
        initial_thickness_entry.grid(row = 7, column = 1, pady = 3)

        #Boundary Layer Thickness
        boundary_thickness_label = customtkinter.CTkLabel(self, text = "Boundary layer thickness (meters)").grid(row = 8, column = 0)
        boundary_thickness_entry = customtkinter.CTkEntry(self, textvariable=self.params["layer_thickness"])
        boundary_thickness_entry.grid(row = 8, column = 1, pady = 3)

    def getParams(self):
        return self.params
