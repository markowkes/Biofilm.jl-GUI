import customtkinter
import numpy as np

class StoichiometryGrid(customtkinter.CTkFrame):
    def __init__(self, parent, Yxs, rows, columns, particulates, solutes, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.yxs = Yxs
        self.rows = rows
        self.columns = columns
        self.solute_arr = solutes
        self.particulate_arr = particulates
        self.stringvars = np.zeros((rows, columns), dtype=customtkinter.StringVar)
        for r in range(rows):
            for c in range(columns):
                self.stringvars[r][c] = customtkinter.StringVar(value=Yxs[r][c])
        #[[self.stringvars[r][c] = customtkinter.StringVar(value=Yxs[r][c]) for r in range(rows)] for c in range(columns)]#This array holds the stringvars, which hold the values of the coefficients
        self.entries = [[None] * columns for _ in range(rows)]
        self.createLabels()
        self.createEntries()


    def entryChangedCallback(self, index_i, index_j):
        val = self.stringvars[index_i][index_j].get()
        self.yxs[index_i][index_j] = val
    
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
                entry = customtkinter.CTkEntry(self, textvariable=self.stringvars[i][j])
                entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                entry.bind("<FocusOut>", lambda event, i=i, j=j: self.entryChangedCallback(index_i=i, index_j=j))
                self.entries[i][j] = entry
                

'''
    def add_row(self):
        for j in range(self.columns):
            entry = customtkinter.CTkEntry(self)
            entry.grid(row=self.rows, column=j, padx=5, pady=5)
            self.entries.append(entry)
        self.rows += 1

    def add_column(self):
        for i in range(self.rows):
            entry = customtkinter.CTkEntry(self)
            entry.grid(row=i, column=self.columns, padx=5, pady=5)
            self.entries[i].append(entry)
        self.columns += 1

    def remove_row(self):
        if self.rows > 0:
            for entry in self.entries[-1]:
                entry.forget()
            self.entries.pop()
            self.rows -= 1

    def remove_column(self):
        if self.columns > 0:
            for i in range(self.rows):
                self.entries[i][-1].forget()
                self.entries[i].pop()
            self.columns -= 1
            '''

    