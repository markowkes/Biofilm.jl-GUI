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
            
    def getPlotFilenames(self):
        folder_path = "Biofilm.jl-main/savePlots"

        # Get the full path by joining the current directory and the relative folder path
        full_path = os.path.join(os.getcwd(), folder_path)

        # Get all files in the folder
        png_files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f)) and f.endswith('.png')]
        return png_files
    

    def getCurrDir(self):
        return os.getcwd()
    

    def load(self):
            #root.withdraw()  # Hide the root window

            # Open a file dialog and get the selected file's path
            file_path = filedialog.askopenfilename()

            # Read the contents of the file into a string
            if file_path:
                with open(file_path, 'r') as file:
                    file_contents = file.read()

                return file_path, file_contents
            return 0,0
