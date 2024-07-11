import re
import numpy as np
import SoluteObjectFrame
import ParticulateObjectFrame
import customtkinter
import Dependancy

class FileLoader():
    def __init__(self, file_content):
        self.file_content = file_content
        file_parameters = self.parse_parameters(file_content)

        #print(file_parameters)


    # Define a function to parse the parameters string and return them as a dictionary
    def parse_parameters(self, param_string):
        #parse file using regular expression -
        key_value_pattern = re.compile(r"(\w+)\s*=\s*((\[[^\]]*\])|([^,\n(]+))")
        parameters = {}

        # Find all key-value pairs in the string
        matches = key_value_pattern.findall(param_string)

        # Iterate over matches and assign values to corresponding variables
        for match in matches:

            # Add the key-value pair to the parameters dictionary, removing the characters: \n, \t, [, ], "
            parameters[match[0]] = match[1].replace('\n', '').replace('\t', '').replace('[', '').replace(']', '').replace('\"', '')

        self.file_params = parameters

        return parameters
    

    def parse_kinetics_comment(self, solute_count, particulate_count, reaction_frame):
        #Create matrix of correct dimensions (solute_count x particulate_count) where all values are None
        dependancy_matrix = np.full(shape=(solute_count, particulate_count), fill_value=None, dtype=Dependancy.Dependancy)
        mu_max_list = None

        start = self.file_content.find("===Kinetics===", 900)
        if start == -1:
            print("note: cannot find '===Kinetics===' comment in save file.")
            return dependancy_matrix, mu_max_list

        end = self.file_content.find("===End_Kinetics===", start)
        if end == -1:
            print("note: cannot find '===End_Kinetics===' comment in save file.")
            return dependancy_matrix, mu_max_list
        
        # get a substring which is only the kinetics comment
        substring = self.file_content[start:end]
        # split into list of lines
        lines = substring.splitlines()
        for line in lines:
            #each line represents a kinetic (dependancy). is of the format: type (monod/inhibition), particulate_index, solute_index, Ki/Km OR 'none', particulate_index, solute_index
            comma_separated_values = line.split(', ')

            #the first line will be a list of mu maxs, as strings, and the first item in the string will just be a '#' so Julia doesn't read it.
            if mu_max_list == None:
                mu_max_list = [int(item) for item in comma_separated_values[1:]]
                continue #skip to next loop iteration

            type = comma_separated_values[1]
            particulate_index = comma_separated_values[2]
            solute_index = comma_separated_values[3]

            if type.lower() == 'none':
                dependancy_matrix[particulate_index][solute_index] = Dependancy.Dependancy(parent=reaction_frame, type = type, param = customtkinter.StringVar(), row = particulate_index, muMax=mu_max_list[particulate_index])
            else:
                param = comma_separated_values[4]
                dependancy_matrix[particulate_index][solute_index] = Dependancy.Dependancy(parent=reaction_frame, type = type, param = customtkinter.StringVar(value=param), row = particulate_index, muMax=mu_max_list[particulate_index])
        
        return dependancy_matrix, mu_max_list



    def saveDataToStructures(self, params, solutes_scrollable_object_frame, particulates_scrollable_object_frame, reaction_frame):
        #This function will...
        solute_objects = []
        particulate_objects = []

        #take basic parameters from the file and put them in the params dict that will be used by Main. 
        #.set() is used because the params dict holds stringVars, not strings. 
        params["title"].set(self.file_params["Title"])
        params["run_time"].set(self.file_params["tFinal"])
        params["tolerance"].set(self.file_params["tol"])
        params["output_period"].set(self.file_params["outPeriod"])
        params["kdet"].set(self.file_params["Kdet"])
        params["volume"].set(self.file_params["V"])
        params["surface_area"].set(self.file_params["A"])
        params["flowrate"].set(self.file_params["Q"])
        params["gridpoints"].set(self.file_params["Nz"])
        params["initial_thickness"].set(self.file_params["Lfo"])
        params["layer_thickness"].set(self.file_params["LL"])

        #get array params:
        #particulate params:
        XNames = self.file_params["XNames"].split(", ") 
        Xto = self.file_params["Xto"].split(", ")
        Pbo = self.file_params["Pbo"].split(", ")
        rho = self.file_params["rho"].split(", ")
        #get srcX
        srcX = self.file_params["srcX"].split("(S,X,Lf,t,z,p) ->")
        edited_srcX = []
        for term in srcX:
            if term != '':
                edited_srcX.append(term.strip())
        #get mu (first make sure comments are taken out)

        #solute params:
        SNames = self.file_params["SNames"].split(", ")
        #get Sin
        Sin = self.file_params["Sin"].split("(t) ->")
        edited_Sin = []
        for term in Sin:
            if term != '':
                edited_Sin.append(term.strip())
        Sto = self.file_params["Sto"].split(", ")
        Sbo = self.file_params["Sbo"].split(", ")
        Yxs = self.file_params["Yxs"].split() #this needs to be reshaped
        Dt = self.file_params["Dt"].split(", ")
        Db = self.file_params["Db"].split(", ")
        #get srcS

        #get makeplots, saveplots, default these to false if not in file

        #reshape Yxs:
        Yxs = np.array(Yxs) #make into numpy array
        row_count = len(XNames)
        col_count = len(SNames)
        Yxs = np.reshape(a = Yxs, newshape=(row_count, col_count))

        #Make solute objects with correct parameters, place in 'solute_objects' list to be returned
        for solute_index in range(col_count):
            frame_params = {"name": customtkinter.StringVar(value = SNames[solute_index]),
                            "sto": customtkinter.StringVar(value = Sto[solute_index]),
                            "sbo": customtkinter.StringVar(value = Sbo[solute_index]),
                            "dt": customtkinter.StringVar(value = Dt[solute_index]),
                            "db": customtkinter.StringVar(value = Db[solute_index]),
                            "Sin": edited_Sin[solute_index]}
            new_frame = SoluteObjectFrame.ObjectFrame(solutes_scrollable_object_frame, frame_params, solute_index) 
            solute_objects.append(new_frame)

        #make particulate objects with correct parameters, place in 'particulate_objects' list to be returned
        for particulate_index in range(row_count):
            frame_params = {"name": customtkinter.StringVar(value = XNames[particulate_index]),
                            "xto": customtkinter.StringVar(value = Xto[particulate_index]),
                            "pbo": customtkinter.StringVar(value = Pbo[particulate_index]),
                            "rho": customtkinter.StringVar(value = rho[particulate_index]),
                            "srcX": edited_srcX[particulate_index]} #TODO: this srcX is not being used currently, this would be in the interactions part of reaction menus
            new_frame = ParticulateObjectFrame.ObjectFrame(particulates_scrollable_object_frame, frame_params, particulate_index) 
            particulate_objects.append(new_frame)

        dependancy_matrix, mu_max_list = self.parse_kinetics_comment(solute_count=col_count, particulate_count=row_count, reaction_frame=reaction_frame)

        return solute_objects, particulate_objects, Yxs, dependancy_matrix, mu_max_list


    
        


