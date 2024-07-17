import customtkinter
import StoichiometryGrid
import Dependancy
import numpy as np


#In this file the classes ReactionFrame, Kinetics, and Dependancy are defined.

#Class for the 'Reactions' menu
class ReactionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent, params, solutes, particulates, dependancies, *args, **kwargs): #takes in pointer to parent frame, the parameters dictionary, the array of soluteObjectFrames, and the array of ParticulateObjectFrames.
        super().__init__(parent, *args, **kwargs)
        self.params = params
        self.solute_arr = solutes
        self.particulate_arr = particulates
        self.dependancy_str = dependancies

        self.init_reaction_frame()


    def force_update(self):
        self.StoichGrid.createLabels()
        

    def init_reaction_frame(self):
        #initialize and grid frame for stoichiometry 
        self.StoichFrame = customtkinter.CTkFrame(self)
        self.StoichFrame.grid(row = 1, column = 0) 
        self.initStoichGrid()

        #initialize and grid frame for kinetics 
        self.kineticsFrame = customtkinter.CTkFrame(self) #make new child frame for kinetics section
        self.kineticsFrame.grid(row=3, column = 0, pady = 20)
        self.initKinetics()

        rows = len(self.particulate_arr)
        cols = len(self.solute_arr)

        #First, handle mu_max_list. If it is None, create new list with default values.
        if self.dependancy_str is None:
            self.mu_max_list = [customtkinter.StringVar(value='0.0') for _ in range(rows)]
        else:
            comma_separated_values = self.dependancy_str[0].split(', ')
            self.mu_max_list = [customtkinter.StringVar(value = item) for item in comma_separated_values[1:]]

        #define dependancy_matrix. This will hold a 2d np array of 'Dependancy' objects, as defined at the end of this file. 
        #Rows are particulates, and columns are solutes. ex. row 1 col 2 represents the dependancy of particulate 1 on solute 2
        self.dependancy_matrix = np.empty((rows, cols), dtype=Dependancy.Dependancy)

        for r in range(rows):
            for c in range(cols):
                self.dependancy_matrix[r][c] = Dependancy.Dependancy(parent = self.kinetics[r], type = 'zero', param = '0', row = r, muMax = self.mu_max_list[r])

        if self.dependancy_str is not None:
            for line in self.dependancy_str[1:]:
                #each line represents a kinetic (dependancy). is of the format: type (monod/inhibition), particulate_index, solute_index, Ki/Km OR 'none', particulate_index, solute_index
                comma_separated_values = line.split(', ')

                type = comma_separated_values[1]
                particulate_index = comma_separated_values[2]
                solute_index = comma_separated_values[3]

                if type.lower() != 'none':
                    param = comma_separated_values[4]
                    self.dependancy_matrix[particulate_index][solute_index] = Dependancy.Dependancy(parent = self.kinetics[particulate_index], type = type, param = customtkinter.StringVar(value=param), row = particulate_index, muMax=self.mu_max_list[particulate_index])


    def initStoichGrid(self): #At the top of the reaction frame is the stoichiometry grid, which contains the yield coeffcients for our solutes/particulates
        label = customtkinter.CTkLabel(self, text= 'Stoichiometry')
        label.cget("font").configure(size=20)
        label.grid(row = 0, column = 0)       

        self.StoichGrid = StoichiometryGrid.StoichiometryGrid(self.StoichFrame, self.params, rows = len(self.particulate_arr), columns = len(self.solute_arr), solutes = self.solute_arr, particulates=self.particulate_arr)
        self.StoichGrid.grid(row = 1, column = 1) #place the stoich grid in the stoich frame


    def initKinetics(self):
        #initialize and grid label for kinetics section
        label = customtkinter.CTkLabel(self, text= 'Kinetics')
        label.cget("font").configure(size=20) #increase font size
        label.grid(row = 2, column = 0)

        #initialize and grid kinetics frame object for each particulate (kinetics object defined below)
        self.kinetics = []
        for index in range(len(self.particulate_arr)):
            par = self.particulate_arr[index]
            k = Kinetic(self.kineticsFrame, par, self.solute_arr, self.dependancy_matrix, self.mu_max_list[index],  index)
            self.kinetics.append(k)
            k.grid(row=index, column = 0)


    def add_object(self, scrollable_object_frame, is_solute):
        #update stoich grid:
        self.StoichGrid.add_object(scrollable_object_frame, is_solute)


    def delete_object(self, scrollable_object_frame, is_solute, index):
        #update stoich grid:
        self.StoichGrid.delete_object(scrollable_object_frame, is_solute, index)

    
    def get_mu_max_string(self): 
        # This function will take the 'muMax' value for all of the particulates and put it in a comma-separated string, to be put in the save file
        mu_max_string = '       #, '
        for k in self.kinetics:
            mu_max_string += k.get_mu_max()
            mu_max_string += ', '
        mu_max_string = mu_max_string[:-2] #trim off excess ', '
        mu_max_string += '\n'
        return mu_max_string


    def getKinetics(self):
        #this function is used in the saveFileBuilder to get the source terms. It builds an array of strings which look like:
        # 'mumax*(S[1]./(KmB1.+S[1])).*(S[3]./(KmB3.+S[3]))' as an example. This goes in the 'mu' variable in the particulate parameters section
        # This string is built here rather than in the SaveFileBuilder because it is more simple.
        kinetics_arr = np.full(shape=len(self.particulate_arr), fill_value='', dtype='<U256')

        #this 'comment' will contain the information of each dependancy, and this will be placed in the save file as a comment,
        # so Biofilm.jl will ignore it. This information will be used during the file loading process to populate the kinetics
        # fields. This is a workaround so that I don't have to parse the 'mu' string described in the comment at the top of this function.
        comment = '     #===Kinetics===#\n'
        comment += self.get_mu_max_string()
        row_index = 0
        for row in self.dependancy_matrix: #each row represents a particulate
            string = ""
            solute_index = 0
            non_zero_dependancy_present = False

            for solute in row:
                #get info from dependancy object 
                type, param, muMax = solute.get()
                
                #insert muMax at start of string
                if solute_index == 0:
                    string = muMax + ' * '

                #insert correct dependancy equation
                if type.strip() == "monod":
                    non_zero_dependancy_present = True

                    print('monod')
                    string += "( S[{}] / ({} + S[{}]) )"
                    string = string.format(str(solute_index), str(param), str(solute_index))

                    next_comment_line = '       #, monod, {}, {}, {}\n'
                    comment += next_comment_line.format(str(row_index), str(solute_index), str(param))

                    #insert multiplication between terms
                    string += ' * '

                elif type.strip() == "inhibition":
                    non_zero_dependancy_present = True

                    print('inhibition')
                    string += "( 1 / (1 + (S[{}] / {})) )"
                    string = string.format(str(solute_index), param)

                    next_comment_line = '       #, inhibition, {}, {}, {}\n'
                    comment += next_comment_line.format(str(row_index), str(solute_index), str(param))

                    #insert multiplication between terms,
                    string += ' * '
                
                else:
                    next_comment_line = '       #, none, {}, {}\n'
                    comment += next_comment_line.format(str(row_index), str(solute_index))

                # add +1 to index
                solute_index += 1
            
            if non_zero_dependancy_present == False:
                string += "0.0"
            else:
                #add string to array, trim off last 3 characters which will be ' * '.
                string = string[:-3]

            kinetics_arr[row_index] = string
            row_index += 1
        comment += '        #===End_Kinetics===#\n'
        print(kinetics_arr)
        return kinetics_arr, comment


    #TODO: - make it so reactionFrame takes in info on dependancies
    # - call reactionFrame with empty dependancies by default
    # - call reactionFrame with appropriate info in FileLoader.
            


class Kinetic(customtkinter.CTkFrame): #one kinetic object represents one particulate
    def __init__(self, parent, particulate, solutes, dependancy_matrix, muMax, index):
        super().__init__(parent)
        self.particulate = particulate
        self.params = particulate.getParams()
        self.solutes = solutes
        self.dependancy_matrix = dependancy_matrix
        self.index = index
        self.muMax = muMax
        self.initFrame()


    def initFrame(self):
        #initialize and grid elements for particulate title + muMax entry box and its label.
        name = customtkinter.CTkLabel(master=self, text="Growth of " + self.params["name"].get())
        name.grid(row = 0, column = 0)
        muMaxLabel = customtkinter.CTkLabel(master=self, text = "Mu Max")
        muMaxLabel.grid(row = 1, column = 0)
        muMaxEntry = customtkinter.CTkEntry(master=self, textvariable=self.muMax)
        muMaxEntry.grid(row = 1, column = 1)
        
        row = 2 
        solute_index = 0

        if self.dependancy_matrix == None:
            build_empty = True
        else:
            build_empty = False

        for solute in self.solutes:
            #Make new 'Dependancy' object for each solute, store it in dependancy_matrix 
            
            if build_empty == True:
                self.dependancy_matrix[self.index][solute_index] = Dependancy.Dependancy(self, 'zero', "", row, self.muMax) #update link to matrix
            else:

                self.dependancy_matrix[self.index][solute_index].gridEntry()

            #make and grid label indicating solute name
            label = customtkinter.CTkLabel(self, text = "Dependance on: S" + str(row-1) + " (" + solute.getParams()['name'].get() + ")")
            label.grid(row = row, column = 1, pady = 3)

            row += 1
            solute_index += 1
        #print("")
            

    def setMuMax(self, val):
        self.muMax = val

    
    def get_mu_max(self):
        return self.muMax.get()
    


