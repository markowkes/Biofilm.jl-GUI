import re
import numpy as np
import SoluteObjectFrame
import ParticulateObjectFrame
import customtkinter

class FileLoader():
    def __init__(self, file_content):
        file_parameters = self.parse_parameters(file_content)
        print(file_parameters)


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


    def saveDataToStructures(self, params):
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
        #get mu (first make sure comments are taken out)
            #solute params:
        SNames = self.file_params["SNames"].split(", ")
        #get Sin
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
        for solute_index in col_count:
            frame_params = {"name": customtkinter.StringVar(value = SNames[solute_index]),
                            "sto": customtkinter.StringVar(value = Sto[solute_index]),
                            "sbo": customtkinter.StringVar(value = Sbo[solute_index]),
                            "dt": customtkinter.StringVar(value = Dt[solute_index]),
                            "db": customtkinter.StringVar(value = Db[solute_index])}
            new_frame = SoluteObjectFrame.ObjectFrame(None, frame_params, solute_index) #Problem! the 'None' here is the master, which should really be the scrollable object frame
            solute_objects.append(new_frame)

        #make particulate objects with correct parameters, place in 'particulate_objects' list to be returned
        for particulate_index in row_count:
            frame_params = {"name": customtkinter.StringVar(value = XNames[particulate_index]),
                            "xto": customtkinter.StringVar(value = Xto[particulate_index]),
                            "pbo": customtkinter.StringVar(value = Pbo[particulate_index]),
                            "rho": customtkinter.StringVar(value = rho[particulate_index])}
            new_frame = ParticulateObjectFrame.ObjectFrame(None, frame_params, particulate_index) #Problem! the 'None' here is the master, which should really be the scrollable object frame
            particulate_objects.append(new_frame)

        return solute_objects, particulate_objects, Yxs


    
        


