import customtkinter
import numpy as np

class StoichiometryGrid(customtkinter.CTkFrame):
    def __init__(self, parent, params, rows, columns, particulates, solutes, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.params = params
        self.rows = rows
        self.columns = columns
        self.solute_arr = solutes
        self.particulate_arr = particulates
        self.stringvars = np.zeros((rows, columns), dtype=customtkinter.StringVar)
        for r in range(rows):
            for c in range(columns):
                self.stringvars[r][c] = customtkinter.StringVar(value=params["yield_coefficients"][r][c])
        #[[self.stringvars[r][c] = customtkinter.StringVar(value=Yxs[r][c]) for r in range(rows)] for c in range(columns)]#This array holds the stringvars, which hold the values of the coefficients
        self.entries = np.full((rows, columns), None, dtype=customtkinter.CTkEntry)
        self.createLabels()
        self.createEntries()


    def add_object(self, object, is_solute):
        if is_solute == True:  #Handling new solute being added
            self.columns += 1
            #add new label
            label = customtkinter.CTkLabel(self, text = self.solute_arr[-1].getName())
            label.grid(row = 0, column = self.columns)
 
            if self.columns >= 1:
                #make new stringVars
                self.stringvars = np.c_[self.stringvars, [customtkinter.StringVar(value='0.0') for i in range(self.rows)]]
                #make space for new entries
                self.entries = np.c_[self.entries, [None for i in range(self.rows)]]

        else: #Handling new particulate being added (new row)
            self.rows += 1
            #add new label
            label = customtkinter.CTkLabel(self, text = self.particulate_arr[-1].getName())
            label.grid(row = self.rows, column = 0)

            if self.rows >= 1:
                #make new stringVars
                self.stringvars = np.vstack((self.stringvars, [customtkinter.StringVar(value='0.0') for i in range(self.columns)]))
                #make space for new entries
                self.entries = np.vstack((self.entries, [None for i in range(self.columns)]))

        self.createEntries()
        self.createLabels()


    def delete_object(self, object, is_solute, index):
        print("deleting")

        if is_solute: #destroy column
            self.entries = np.delete(self.entries, index, axis=1)
            self.stringvars = np.delete(self.stringvars, index, axis=1)
            self.columns -=1
        else: #destroy row
            self.entries = np.delete(self.entries, index, axis=0)
            self.stringvars = np.delete(self.stringvars, index, axis=0)
            self.rows -=1

        for child in self.winfo_children():
            child.grid_forget()

        self.createLabels()
        self.createEntries()    


    def entryChangedCallback(self, index_i, index_j):
        val = self.stringvars[index_i][index_j].get()
        self.params["yield_coefficients"][index_i][index_j] = val
    

    def createLabels(self):
        row = 1
        for par in self.particulate_arr:
            label = customtkinter.CTkLabel(self, text = par.getName())
            label.grid(row = row, column = 0)
            row += 1
        col = 1
        for sol in self.solute_arr:
            label = customtkinter.CTkLabel(self, text = sol.getName())
            label.grid(row = 0, column = col)
            col += 1


    def createEntries(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.entries[i][j] == None:
                    entry = customtkinter.CTkEntry(self, textvariable=self.stringvars[i][j])
                    entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                    entry.bind("<FocusOut>", lambda event, i=i, j=j: self.entryChangedCallback(index_i=i, index_j=j))
                    self.entries[i][j] = entry
                elif self.entries[i][j].winfo_ismapped() == False:
                    self.entries[i][j].grid(row=i+1, column=j+1, padx=5, pady=5)

                
    