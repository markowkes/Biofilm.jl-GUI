import customtkinter

class Dependancy():
    def __init__(self, parent, type, param, row, muMax):
        self.type = customtkinter.StringVar(value=type)
        self.param = customtkinter.StringVar(value=param)
        self.parent = parent
        self.row = row
        self.muMax = muMax

        #initiallize (but don't grid) entry box for parameter - in the case that the dependancy needs the extra parameter
        self.entry = customtkinter.CTkEntry(parent, textvariable=self.param, width=50)

        #initialize and grid drop down menu for type - self.type will automatically update to be equal to the dropdown selection.
        #The dropdown will call update_layout whenever the selection changes.
        self.optionmenu = customtkinter.CTkOptionMenu(parent,values=["zero", "monod", "inhibition", "first"],
                                                    variable=self.type, command = self.update_layout)
        self.optionmenu.grid(row=row, column = 2, padx = 3)

        #initialize and grid a spacer - this will be to the right of the dropdown and will be replaced with the param box if needed.
        self.spacer = customtkinter.CTkLabel(self.parent, text="")
        self.spacer.grid(row = row, column = 3, columnspan=2)


    def update_layout(self, choice): 
        #this function places the correct parameter entry box+label for the monod and inhibition equations
        type = self.type.get()
        if type == "monod":
            param_label = customtkinter.CTkLabel(self.parent, text="Km")
            param_label.grid(row = self.row, column = 3)
            self.gridEntry()
        elif type == "inhibition":
            param_label = customtkinter.CTkLabel(self.parent, text="Ki")
            param_label.grid(row = self.row, column = 3)
            self.gridEntry()
        else:
            #delete the entry if first order or zero are selected
            self.entry.grid_forget()


    def gridEntry(self):
        self.entry.grid(row = self.row, column = 4)

    
    def get(self):
        return self.type.get(), self.param.get(), self.muMax.get()


    def destroy(self):
        self.entry.destroy()
        self.optionmenu.grid_forget()
        self.optionmenu.destroy()
        self.spacer.destroy()
        del self
        
