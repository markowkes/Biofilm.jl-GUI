import customtkinter

class StoichiometryGrid(customtkinter.CTkFrame):
    def __init__(self, parent, rows=2, columns=2, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.rows = rows
        self.columns = columns
        self.stringvars = [[customtkinter.StringVar(value='') for _ in range(rows)] for _ in range(columns)]#This array holds the stringvars, which hold the values of the coefficients
        self.entries = [[None] * columns for _ in range(rows)]
        self.create_entries()

    def create_entries(self):
        for i in range(self.rows):
            for j in range(self.columns):
                entry = customtkinter.CTkEntry(self, textvariable=self.stringvars[i][j])
                entry.grid(row=i, column=j, padx=5, pady=5)
                self.entries[i][j] = entry

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

if __name__ == "__main__":
    root = customtkinter.CTk()
    frame = StoichiometryGrid(root)
    frame.pack()

    add_row_button = customtkinter.CTkButton(root, text="Add Row", command=frame.add_row)
    add_row_button.pack()

    add_column_button = customtkinter.CTkButton(root, text="Add Column", command=frame.add_column)
    add_column_button.pack()

    remove_row_button = customtkinter.CTkButton(root, text="Remove Row", command=frame.remove_row)
    remove_row_button.pack()

    remove_column_button = customtkinter.CTkButton(root, text="Remove Column", command=frame.remove_column)
    remove_column_button.pack()

    root.mainloop()