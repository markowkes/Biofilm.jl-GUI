import os
from tkinter import filedialog

class FileController():
    def __init__(self) -> None:
        pass

    def saveAs(self, content):
        current_dir = os.path.dirname(__file__)
        file_path = filedialog.asksaveasfilename( initialdir= current_dir+'../Saves',
                                                defaultextension=".jl",
                                                filetypes=[("Julia file", "*.jl")])

        # Check if a file path was selected
        if file_path:
            with open(file_path, 'w') as f:
                f.write(content)
                return file_path
