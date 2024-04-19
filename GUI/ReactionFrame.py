import customtkinter
import StoichiometryGrid
import numpy as np

#In this file the classes ReactionFrame, Kinetics, and Dependancy are defined.

#Class for the 'Reactions' menu
class ReactionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent, params, solutes, particulates, *args, **kwargs): #takes in pointer to parent frame, the parameters dictionary, the array of soluteObjectFrames, and the array of ParticulateObjectFrames.
        super().__init__(parent, *args, **kwargs)
        self.params = params
        self.solute_arr = solutes
        self.particulate_arr = particulates

        #Init dependancy_matrix. This will hold a 2d np array of 'Dependancy' objects, as defined at the end of this file. 
        #Rows are particulates, and columns are solutes. ex. row 1 col 2 represents the dependancy of particulate 1 on solute 2
        self.dependancy_matrix = np.empty((len(particulates), len(solutes)), dtype=Dependancy) 
        self.initReactionFrame()
        

    def initReactionFrame(self):
        #initialize and grid frame for stoichiometry 
        self.StoichFrame = customtkinter.CTkFrame(self)
        self.StoichFrame.grid(row = 1, column = 0) 
        self.initStoichGrid()

        #initialize and grid frame for kinetics 
        self.kineticsFrame = customtkinter.CTkFrame(self)
        self.kineticsFrame.grid(row=3, column = 0, pady = 5)
        self.initKinetics()


    def initStoichGrid(self): #At the top of the reaction frame is the stoichiometry grid, which contains the yeild coeffcients for our solutes/particulates
        label = customtkinter.CTkLabel(self, text= 'Stoichiometry')
        label.cget("font").configure(size=20)
        label.grid(row = 0, column = 0)       

        Yxs = self.params['yield_coefficients']
        self.StoichGrid = StoichiometryGrid.StoichiometryGrid(self.StoichFrame, Yxs, rows = len(self.particulate_arr), columns = len(self.solute_arr), solutes = self.solute_arr, particulates=self.particulate_arr)
        self.StoichGrid.grid(row = 1, column = 1) #place the stoich grid in the stoich frame


    def initKinetics(self):
        #initialize and grid label for kinetics section
        label = customtkinter.CTkLabel(self, text= 'Kinetics')
        label.cget("font").configure(size=20) #increase font size
        label.grid(row = 2, column = 0)

        #initialize and grid kinetics frame object for each particulate (kinetics object defined below)
        for index in range(len(self.particulate_arr)):
            par = self.particulate_arr[index]
            k = Kinetic(self.kineticsFrame, par, self.solute_arr, self.dependancy_matrix, index)
            k.grid(row=index, column = 0)


    def getKinetics(self):
        #this function is used in the saveFileBuilder to get the source terms. It builds an array of strings which look like:
        # 'mumax*(S[1]./(KmB1.+S[1])).*(S[3]./(KmB3.+S[3]))' as an example. This goes in the 'mu' variable in the particulate parameters section
        # This string is built here rather than in the SaveFileBuilder because it is more simple.
        kinetics_arr = np.full(shape=len(self.particulate_arr), dtype=str, fill_value='')
        row_index = 0
        for row in self.dependancy_matrix:
            string = ""
            solute_index = 0
            for solute in row:
                #get info from dependancy object 
                type, param, muMax = solute.get() 
                
                #insert muMax at start of string
                if solute_index == 0:
                    string = muMax + ' * '

                #insert correct dependancy equation
                if type == "monod":
                    string = "( S[{}] / ({} + S[{}]) )"
                    string = string.format(str(solute_index), str(param), str(solute_index))
                elif type == "inhibition":
                    string = "( 1 / (1 + (S[{}] / {})) )"
                    string = string.format(str(solute_index), param)
                else:
                    string = "0.0"
                
                #insert multiplication between terms, then +1 to index
                string += ' * ' 
                solute_index += 1
            
            #add string to array, trim off last 3 characters which will be ' * '.
            kinetics_arr[row_index] = string[:-3]
            row_index += 1
        return kinetics_arr
                
            

class Kinetic(customtkinter.CTkFrame): #one kinetic object represents one particulate
    def __init__(self, parent, particulate, solutes, dependancy_matrix, index):
        super().__init__(parent)
        self.particulate = particulate
        self.params = particulate.getParams()
        self.solutes = solutes
        self.dependancy_matrix = dependancy_matrix
        self.index = index
        self.muMax = customtkinter.StringVar(value='0.0')
        self.initFrame()


    def initFrame(self):
        #initialize and grid elements for particulate title + muMax entry box and its label.
        name = customtkinter.CTkLabel(master=self, text="Growth of " + self.params["name"].get())
        name.grid(row = 0, column = 0)
        muMaxLabel = customtkinter.CTkLabel(master=self, text = "Mu Max")
        muMaxLabel.grid(row = 1, column = 0)
        muMaxEntry = customtkinter.CTkEntry(master=self, textvariable=self.muMax)
        muMaxEntry.grid(row = 1, column = 1)
        
        row = 2 #NEXT STEP DEBUG FILLING IN DEPENDANCY MATRIX wrong indices
        solute_index = 0
        for solute in self.solutes:
            #Make new 'Dependancy' object for each solute, store it in dependancy_matrix 
            
            self.dependancy_matrix[self.index][solute_index] = Dependancy(self, 'zero', "", row, self.muMax) #update link to matrix

            #make and grid label indicating solute name
            label = customtkinter.CTkLabel(self, text = "Dependance on: S" + str(row-1) + " (" + solute.getParams()['name'].get() + ")")
            label.grid(row = row, column = 1, pady = 3)

            row += 1
            solute_index += 1
        print("")
            

    def setMuMax(self, val):
        self.muMax = val



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
        spacer = customtkinter.CTkLabel(self.parent, text="")
        spacer.grid(row = row, column = 3, columnspan=2)


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
        return self.type, self.param.get(), self.muMax.get()
        
