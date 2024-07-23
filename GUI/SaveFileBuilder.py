
class SaveFileBuilder():
    def __init__(self, params, particulates, solutes, kinetics):
        self.params = params
        self.particulates_arr = particulates
        self.solutes_arr = solutes
        self.kinetics = kinetics


    def getParticulateObjectParams(self, object_arr):
        param_list = []
        items = ["name", "xto", "pbo", "rho"]
        for frame in object_arr:
            temp = frame.getParams() #get the params dictionary from the frame
            for index in range(len(items)):
                if len(param_list) <= index :
                    param_list.append([]) #append empty list
                param_list[index].append(temp[items[index]].get())
        return param_list
    

    def getSoluteObjectParams(self, object_arr):
        param_list = []
        items = ["name", "sto", "sbo", "dt", "db"]
        for frame in object_arr:
            temp = frame.getParams() #get the params dictionary from the frame
            for index in range(len(items)):
                if len(param_list) <= index :
                    param_list.append([]) #append empty list
                param_list[index].append(temp[items[index]].get())
        return param_list


    #The following 2 funcitons take lists of parameters and format them with commas between them for the save file.
    def buildStringParams(self, list):
            name_string = ""
            for name in list:
                name_string = name_string + '\"' + name + '\", ' #put quotes around strings
            name_string = name_string[:-2] #trim off trailing ', '
            return name_string


    def buildFloatParams(self, list):
            name_string = ""
            for name in list:
                name_string = name_string + str(name) + ', '
            name_string = name_string[:-2] #trim off trailing ', '
            return name_string


    def makeSaveFileContent(self):
        content = "using Biofilm \n \n #input parameters \n"

        content = content + self.getSimulationParams()
        content = content + self.getParticulateParams()
        content = content + self.getSoluteParams()
        content = content + self.getTankParams()
        content = content + self.getBiofilmParams()

        content = content + """savePlots = true,
                               makePlots = true,"""
        content = content +        """)\n\tt,zm,Xt,St,Pb,Sb,Lf,sol = BiofilmSolver(p) # Run solver
        biofilm_plot(sol,p) # Plot final results
        #biofilm_sol2csv(sol,p,filname)"""
        return content


    def getSimulationParams(self):
        content =  """p = (
            # --------------------- #
            # Simulation Parameters #
            # --------------------- #\n"""
        sim_param_string = """\t\t Title = \t \"{}\",
        \t tFinal = \t {},    #Simulation time [days]
        \t tol = \t {},   #Tolerance
        \t outPeriod = \t {}, # Time between outputs [days]\n"""
        content = content + sim_param_string.format(self.params["title"].get(), self.params["run_time"].get(), self.params["tolerance"].get(), self.params["output_period"].get())
        return content


    def buildYxs(self, yxs):
        content = ""
        for row in yxs:
            for item in row:
                content = content + str(item) + "  "
            content = content.rstrip()
            content = content + '\n\t\t\t   '
        content = content.rstrip()
        return content


    def buildSrcX(self): #TODO: this is just a placeholder
        content = ""
        for particulate in self.particulates_arr:
            content = content + "(S,X,Lf,t,z,p) -> 0.0\n\t\t\t   "
        return content
    

    def buildSrcS(self): #TODO: this is just a placeholder
        content = ""
        for particulate in self.solutes_arr:
            content = content + "(S,X,Lf,t,z,p) -> 0.0\n\t\t\t   "
        return content         

#NEXT STEP: DEBUG buildMU FUNCTION. particulate on line 110 is just 0... see emulatingCase4.jl lines 26,27

    def buildMu(self):
        kinetics, comment = self.kinetics # this is a np array of strings. length = #of particulates
        content = ""
        particulate_index = 0
        for particulate in kinetics:
            content += "\n\t\t\t(S,X,Lf,t,z,p) ->"
            content += particulate
            content += ",  #" + self.particulates_arr[particulate_index].getName()
            particulate_index +=1
        return content + '\n' + comment + '\n'


    def buildSin(self): #TODO: fill in Sin with 'inflow' equation
        content = ""
        for particulate in self.solutes_arr:
            content = content + "(t) -> 100\n\t\t\t   "
        content = content.rstrip()
        return content
    

    def getParticulateParams(self):
        content = """
            # ---------------------- #
            # Particulate Parameters #
            # ---------------------- #\n"""
        particulate_params = self.getParticulateObjectParams(self.particulates_arr)
        particulate_param_string = """
            XNames = [{}],\t\t# Particulate names
            Xto =   [{}],\t\t# Tank particulate concentration initial condition(s)
            Pbo =   [{}],\t\t# Biofilm particulates volume fraction initial condition(s) 
            rho =   [{}],\t\t# Particulate densities
            Kdet =  20000.0,\t\t# Particulates detachment coefficient
            srcX =  [{}],\t\t# Source of particulates
            mu = [{}],\n"""
        content = content + particulate_param_string.format(self.buildStringParams(particulate_params[0]), self.buildFloatParams(particulate_params[1]), self.buildFloatParams(particulate_params[2]), self.buildFloatParams(particulate_params[3]), self.buildSrcX(), self.buildMu())
        return content


    def getSoluteParams(self):
        content = """
            # ----------------- #
            # Solute Parameters #
            # ----------------- #\n"""
        solute_params = self.getSoluteObjectParams(self.solutes_arr)
        solute_param_string = """
            SNames =[{}],\t\t# Solute names
            Sin =   [{}],\t\t# Solute inflow (can be function of time)
            Sto =   [{}],\t\t# Tank solute concentration initial condition(s)
            Sbo =   [{}],\t\t# Biofilm solutes concentration initial condition(s)
            Yxs =   [{}],\t\t# Biomass yield coefficient on solute   #this should come from the reaction menu
            Dt =    [{}],\t\t# Aquious solute diffusion through tank fluid
            Db =    [{}],\t\t# Effective solute diffusion through biofilm
            srcS =  [{}],     # Source of solutes\n"""   
        content = content + solute_param_string.format(self.buildStringParams(solute_params[0]), self.buildSin(), self.buildFloatParams(solute_params[1]), self.buildFloatParams(solute_params[2]), self.buildYxs(self.params["yield_coefficients"]), self.buildFloatParams(solute_params[3]), self.buildFloatParams(solute_params[4]), self.buildSrcS())
        return content


    def getTankParams(self):
        content = """
            # --------------- #
            # Tank Parameters #
            # --------------- #\n"""
        tank_param_string = """\t\t V =\t{},\t#Volume of tank[m^3]
        \t A =\t{},\t#Surface area of biofilm [m^2]
        \t Q =\t{},\t#Flowrate through tank [m^3/d]\n"""
        content = content + tank_param_string.format(self.params["volume"].get(), self.params["surface_area"].get(), self.params["flowrate"].get(), self.params["gridpoints"].get(), self.params["initial_thickness"].get(), self.params["layer_thickness"].get())
        return content
        

    def getBiofilmParams(self):
        content = """\t\t# ------------------ #
            # Biofilm Parameters #
            # ------------------ #\n"""
        biofilm_param_string = """\t\tNz = {},          # Number of grid points in biofilm
            Lfo = {},     # Biofilm initial thickness [m]
            LL = {},      # Boundary layer thickness [m]\n"""
        content = content + biofilm_param_string.format(self.params["gridpoints"].get(), self.params["initial_thickness"].get(), self.params["layer_thickness"].get())
        return content
