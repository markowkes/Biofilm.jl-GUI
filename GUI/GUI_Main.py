import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import numpy as np
import threading

import customtkinter
import CTkMenuBar
#import CTkToolTip
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ParticulateObjectFrame
import ScrollableObjectFrame
import SoluteObjectFrame
import SimulationFrame
import GeometryFrame
import ReactionFrame

import SaveFileBuilder
import FileLoader
import FileController
import PlotWindow
import Dependancy

#TODO:
'''
 For 1.0 release:
load Sin from file

Build a distributable package 

 After 1.0 release:
when you load up a new file, should it have a simple base case in it?
Displaying the plots generated by Biofilm.jl in an interactive way, add entry box which shows time, allows for entry
Support for user defined interactions between particulates/solutes
csv file
Address performance issues - especially when resizing
Implement tool tips and units for all parameters
Equation viewer/editor 
Test distributable across operating systems and screens
'''

#BUGS: 
'''
Deleting a solute when no particulates have been made causes error
must open reactions menu before using 'save as' button
scrolling on soluteSOF not working?
closing window after adding solute inflow prints errors, python terminal needs to be killed. This is a bug in customtkinter.
'''

class BiofilmApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #inisializing customtkinter.CTk object, which the BiofilmApp class extends/inherits from
        self.set_up_window()
        self.params = self.initialize_parameters()
        self.particulates_arr = []
        self.solutes_arr = []
        self.dependancy_string = None

        self.create_menu()
        self.appFrame.pack() #because the menu bar, which holds the 'file' button ect. uses the 'pack' placement method, a frame for the whole app must also be packed if the 'grid' placement method is to be used.
        self.create_parameter_frame()
        self.create_frames()

        self.protocol("WM_DELETE_WINDOW", self.exit)

        self.mainloop()


    def exit(self):
        print("TEST")
        self.SoluteSOF.exit()
        self.destroy()


    def set_up_window(self):
        customtkinter.set_appearance_mode("System") #takes the system's light/dark mode setting
        customtkinter.set_default_color_theme("blue")
        self.title("Biofilm.py")
        self.height = self.winfo_screenheight()
        self.width = self.winfo_screenwidth()
        self.appFrame = customtkinter.CTkFrame(master = self, width=self.width, height=self.height)
        self.appFrame.pack_propagate(0) #make the appFrame take up the whole window
        self.geometry("%dx%d+0+0" % (self.width, self.height - 100)) #defining window size
        self.update() #apply changes to window


    def initialize_parameters(self):
        #dictionary of parameters, each value is a stringvalue, which is a wrapper around a string which can be put in an entry box widget, and the variable automatically updates the value.
        #enter default values of variables here
        params = {
            "title": customtkinter.StringVar(value=""),
            "run_time": customtkinter.StringVar(value="1"),
            "tolerance": customtkinter.StringVar(value="1e-4"),
            "output_period": customtkinter.StringVar(value="0.1"),
            "kdet": customtkinter.StringVar(value="100"),
            "volume": customtkinter.StringVar(value="1"),
            "surface_area": customtkinter.StringVar(value="1"),
            "flowrate": customtkinter.StringVar(value="1"),
            "gridpoints": customtkinter.StringVar(value="40"),
            "initial_thickness": customtkinter.StringVar(value="0.1"),
            "layer_thickness": customtkinter.StringVar(value="10e-4"),
            "yield_coefficients": np.empty(0), #will hold an np array where rows represent particulates, columns represent solutes. data type is float.
            "file_path": ""     #Note, because file_path will never be used with an entryBox, it is just a string
        }
        self.plot_window = None
        return params
    
    
    def do_nothing(self): #for setting commands of buttons to do nothing - temprorary helper
        pass


    def create_menu(self):
        #Create menu bar - File Edit ect.

        menubar = CTkMenuBar.CTkMenuBar(self)
        file_button = menubar.add_cascade("file") #add 'file' button
        filemenu = CTkMenuBar.CustomDropdownMenu(widget = file_button) #place 'file' button on menu bar

        #add buttons to 'file' dropdown:
        filemenu.add_option(option="Open", command=self.load)
        filemenu.add_option(option="Save", command=self.save)
        filemenu.add_option(option="Save as...", command=self.save_as)

        #define menu_frame, which sits on the left side of the window at all times, and holds the buttons for the different pages.

        menu_frame = customtkinter.CTkFrame(self.appFrame, width=self.winfo_screenwidth() / 5, height=self.winfo_screenheight() - 40)
        menu_frame.grid(row=0, column=0, pady=5, ipady=40, padx=5, sticky="N")
        menu_frame.grid_propagate(0)

        # Define buttons for different pages: (this looks complex but it isn't- for every button, define it - text label, size, command - then place it using .grid())
        sim_button = customtkinter.CTkButton(menu_frame, text="Simulation Parameters", width=(self.winfo_screenwidth() / 5) - 20, command=self.simulation_button_func)
        sim_button.grid(row=1, column=0, pady=5, padx=10)

        geometry_button = customtkinter.CTkButton(menu_frame, text="Geometry Parameters", width=(self.winfo_screenwidth() / 5) - 20, command=self.geometry_button_func)
        geometry_button.grid(row=2, column=0, pady=5, padx=10)

        particulate_button = customtkinter.CTkButton(menu_frame, text="Particulate Parameters", width=(self.winfo_screenwidth() / 5) - 20, command=self.particulate_button_func)
        particulate_button.grid(row=3, column=0, pady=5, padx=10)

        solute_button = customtkinter.CTkButton(menu_frame, text="Solute Parameters", width=(self.winfo_screenwidth() / 5) - 20, command=self.solute_button_func)
        solute_button.grid(row=4, column=0, pady=5, padx=10)

        reaction_button = customtkinter.CTkButton(menu_frame, text="Reactions", width=(self.winfo_screenwidth() / 5) - 20, command=self.reaction_button_func)
        reaction_button.grid(row=5, column=0, pady=5, padx=10)

        self.run_sim_button = customtkinter.CTkButton(menu_frame, text="Run Simulation", width=(self.winfo_screenwidth() / 5) - 20, command=self.run_handler)
        self.run_sim_button.grid(row=6, column=0, pady=50, padx=10, sticky="s")
        customtkinter.CTkButton(menu_frame, text="Test", width=(self.winfo_screenwidth() / 5) - 20, command=self.open_plot_window).grid(row=7, column=0, pady=50, padx=10, sticky="s")
        self.menu_buttons = [sim_button, geometry_button, particulate_button, solute_button, reaction_button] #array for holding buttons, so they can be referenced outside this function
        self.menu_frame = menu_frame


    def create_parameter_frame(self):
        self.parameter_frame = customtkinter.CTkFrame(self.appFrame, height=self.winfo_screenheight(), width=(4 * self.winfo_screenwidth() / 5) - 26)
        self.parameter_frame.grid(row=0, column=1, pady=5, padx=5, sticky="N")
        self.parameter_frame.grid_propagate(0)


    def create_frames(self): #calls the functions which initializes the different frames (screens) that the side menu can open.
        self.init_simulation_frame()
        self.init_geometry_frame()
        self.particulate_frame = customtkinter.CTkFrame(self.parameter_frame, height=self.winfo_screenheight(), width=(4 * self.winfo_screenwidth() / 5) - 60)
        self.init_particulate_frame()
        self.solute_frame = customtkinter.CTkFrame(self.parameter_frame, height=self.winfo_screenheight(), width=(4 * self.winfo_screenwidth() / 5) - 60)
        self.init_solute_frame()
        self.reaction_frame = customtkinter.CTkFrame(self.parameter_frame, height=self.winfo_screenheight(), width=(4 * self.winfo_screenwidth() / 5) - 60)
        self.init_reaction_frame()
        self.particulateSOF.add_reaction_frame_reference(self.reactionSF)
        self.SoluteSOF.add_reaction_frame_reference(self.reactionSF)
        

    def save_as(self):
        kinetics = self.reactionSF.getKinetics()
        sin = self.SoluteSOF.get_inflow_params()
        SFB = SaveFileBuilder.SaveFileBuilder(self.params, self.particulates_arr, self.solutes_arr, sin, kinetics)
        content = SFB.makeSaveFileContent()
        fc = FileController.FileController()
        file_path = fc.saveAs(content)
        self.params['file_path'] = file_path


    def save(self):
        if self.params['file_path'] == '':
            self.save_as()
            return
        kinetics = self.reactionSF.getKinetics()
        sin = self.SoluteSOF.get_inflow_params()
        SFB = SaveFileBuilder.SaveFileBuilder(self.params, self.particulates_arr, self.solutes_arr, sin, kinetics)
        content = SFB.makeSaveFileContent()
        fc = FileController.FileController()
        fc.save(content, self.params['file_path'])


    def load(self): #i.e 'open'
        fc = FileController.FileController()
        #invoke load method on fileController, this uses filedialog to open the window where the user selects file to load
        #this method returns the file path of the selected load file and a string 'file_contents' which is the whole file in one sring
        file_path, file_contents = fc.load()
        if file_path != 0:
            #update 'file_path' pointer in params
            self.params['file_path'] = file_path

            #make new FileLoader object, passing in file contents string. 
            fl = FileLoader.FileLoader(file_contents)
            #This function loads the file's params into self.params, and makes the solute/partuculate objects and the yxs matrix
            solutes, particulates, yxs, dependancy_string, sin_string = fl.saveDataToStructures(self.params, self.SoluteSOF, self.particulateSOF, self.reactionSF)
            self.solutes_arr = solutes
            self.SoluteSOF.loadFrames(solutes)
            self.particulates_arr = particulates
            self.particulateSOF.loadFrames(particulates)
            self.params["yield_coefficients"] = yxs
            self.dependancy_string = dependancy_string
            self.init_reaction_frame()

            #update the reaction frame reference on the solute and particuate frames
            self.particulateSOF.add_reaction_frame_reference(self.reactionSF)
            self.SoluteSOF.add_reaction_frame_reference(self.reactionSF)

            self.SoluteSOF.load_inflow(sin_string)
            

    def clearParameterFrame(self):
        self.simulation_frame.grid_forget()
        self.geometry_frame.grid_forget()
        self.particulate_frame.grid_forget()
        self.solute_frame.grid_forget()
        self.reaction_frame.grid_forget()


    #Initializing different side menu options:
    def init_simulation_frame(self):
        self.simulation_frame = SimulationFrame.SimulationFrame(params=self.params, parent=self.parameter_frame, height=self.winfo_screenheight(), width=(4 * self.winfo_screenwidth() / 5) - 60)


    def init_geometry_frame(self):
        self.geometry_frame = GeometryFrame.GeometryFrame(params=self.params, parent=self.parameter_frame, height=self.winfo_screenheight(), width=(4 * self.winfo_screenwidth() / 5) - 60)


    def init_particulate_frame(self):
        self.particulateSOF = ScrollableObjectFrame.ScrollableObjectFrame(self.params, self.particulate_frame, self.particulates_arr, False, height = self.winfo_screenheight()-140, width = ((4*self.winfo_screenwidth())/5)-50)
        self.particulateSOF.grid(row = 0, column = 0)


    def init_solute_frame(self):
        self.SoluteSOF = ScrollableObjectFrame.ScrollableObjectFrame(self.params, self.solute_frame, self.solutes_arr, True, height = self.winfo_screenheight()-140, width = ((4*self.winfo_screenwidth())/5)-50)
        self.SoluteSOF.grid(row = 0, column = 0)
    

    def init_reaction_frame(self):
        self.reactionSF = ReactionFrame.ReactionFrame(self.reaction_frame, self.params, self.solutes_arr, self.particulates_arr, dependancies=self.dependancy_string, height = self.winfo_screenheight()-20, width = ((4*self.winfo_screenwidth())/5)-50) #ReactionSF = reactionScrollableFrame
        self.reactionSF.grid(row = 0, column = 0)


    #Functions for side menu buttons:
    def enableAllButtons(self):
        for button in self.menu_buttons:
            button.configure(state="normal")


    def disableButton(self, button_index): #disable a menu button of a given index, indices are defined here: [sim_button, geometry_button, particulate_button, solute_button, reaction_button]
        self.menu_buttons[button_index].configure(state = "disabled")


    def menuButtonPress(self, button_index):
        self.clearParameterFrame() #clear out the right side of the screen (everything but the menu)
        self.enableAllButtons() #the previously selected option will be disabled, so make sure all buttons are enabled
        self.disableButton(button_index) #disable the button that was just pressed
    

    def simulation_button_func(self):
        self.menuButtonPress(button_index=0)
        self.simulation_frame.grid(row = 0, column = 0, pady = 5, padx = 5, ipadx = 5, ipady = 3) 


    def geometry_button_func(self):
        self.menuButtonPress(button_index=1)
        self.geometry_frame.grid(row = 0, column = 0, pady = 5, padx = 5, ipadx = 5, ipady = 3) 


    def particulate_button_func(self):
        self.menuButtonPress(button_index=2)
        self.particulate_frame.grid(row = 0, column = 0, pady = 5, padx = 5, ipadx = 5, ipady = 3)


    def solute_button_func(self):
        self.menuButtonPress(button_index=3)
        self.solute_frame.grid(row = 0, column = 0, pady = 5, padx = 5, ipadx = 5, ipady = 3) 


    def reaction_button_func(self):
        self.menuButtonPress(button_index=4)
        self.reactionSF.force_update()
        self.reaction_frame.grid(row = 0, column = 0, pady = 5, padx = 5, ipadx = 5, ipady = 3)        
        #self.reactionSF.update() 


    def run_handler(self): #called when 'run simulation' is pressed
        # Disable 'run simulation' button
        self.run_sim_button.configure(state = "disabled")

        self.init_sim_progress_bar()

        # Run the run_julia_script() function on a seperate thread so the GUI is still responsive
        def target(): 
            return_val, content = self.run_julia_script()
            # Return_val == 0 if no error running the file
            if return_val == 0:
                self.open_plot_window()

        threading.Thread(target=target).start()

    
    def cancel_simulation(self):
        # Terminate the subprocess
        if self.process and self.process.poll() is None:
            self.process.terminate()  

        # Delete simulation progress widgets
        self.sim_progress_text.grid_forget()
        self.sim_progress_time_text.grid_forget()
        self.sim_progress_bar.grid_forget()
        self.cancel_sim_button.grid_forget()

        # Enable 'run simulation' button
        self.run_sim_button.configure(state = "normal")


    def init_sim_progress_bar(self):
        self.sim_progress_text = customtkinter.CTkLabel(master = self.menu_frame, text = "Simulation Progress (days):")
        self.sim_progress_text.grid(row = 8, column = 0)

        self.sim_progress_time_text = customtkinter.CTkLabel(master = self.menu_frame, text = "t = 0.000")
        self.sim_progress_time_text.grid(row = 9, column = 0)

        self.sim_progress_bar = customtkinter.CTkProgressBar(master=self.menu_frame, orientation='horizontal',width=(self.winfo_screenwidth() / 5) - 20)
        self.sim_progress_bar.set(0) # Start progress at 0
        self.sim_progress_bar.grid(row = 10, column = 0)

        self.cancel_sim_button = customtkinter.CTkButton(master = self.menu_frame, text = "Cancel Simulation", fg_color= "red", hover_color= "darkred", command = self.cancel_simulation)
        self.cancel_sim_button.grid(row = 11, column = 0, pady = 5)


    def update_sim_progress(self, line):
        # Remove whitespace
        line = line.strip()

        # Check if line is a number, not one of the lines with column titles 
        if not self.is_number_with_decimals(line):
            return
        
        # Convert line to float, as we know it represents the current time.
        time = float(line)
        t_final = float(self.params.get('run_time').get())

        # Progress will be a decimal between 0 and 1 that represents the amount of time that has already been simulated
        progress = time/t_final

        # Round to 3 decimal places
        progress = round(progress, 3)

        # Update text 
        self.sim_progress_time_text.configure(text=f"t = {str(time)}")

        # Update progress bar
        self.sim_progress_bar.set(progress)


    def is_number_with_decimals(self, num): #similar to the python isdigit() function, but accepts floats as well as integers.
        try:
            float(num)
            return True
        except ValueError:
            return False


    def open_plot_window(self):
        if self.plot_window is None or not self.plot_window.winfo_exists():
            step = float(self.params.get('output_period').get())
            tfinal = float(self.params.get('run_time').get())
            self.plot_window = PlotWindow.PlotWindow(master = self, tfinal = tfinal, step = step)  # create window if its None or destroyed
            self.plot_window.focus()
        else:
            self.plot_window.focus()  # if window exists focus it
        self.plot_window.lift()
        self.plot_window.attributes('-topmost', True)
        self.plot_window.after(200, lambda: self.plot_window.attributes('-topmost', False))


    def run_julia_script(self):
        # Function to run save file, which is a .jl (julia) file
        print("RUNNING SCRIPT")

        # Start the subprocess
        process = subprocess.Popen(['julia', self.params["file_path"]],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        self.process = process
        # Capture stdout line by line while the process is running
        output = ''
        while True:
            # Read a line from the stdout
            line = process.stdout.readline()
            if not line:
                break
            # Update the progress bar and its accompanying text
            self.update_sim_progress(line[:10])
            # Append the line to the output variable
            output += line
            # You can print the line if you want to see it in real-time
            print(line, end='')

        # Wait for the process to finish
        process.wait()

        # Get stderr
        error = process.stderr.read()

        # Check for errors
        if process.returncode != 0:
            print("Error:", error)

        # Now 'output' contains the entire stdout of the subprocess
        return process.returncode, output
          

app = BiofilmApp()
app.mainloop()




