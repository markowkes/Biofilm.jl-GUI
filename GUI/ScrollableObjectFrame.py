#Scrollable solute/particulate class
import numpy as np

import customtkinter
import SoluteObjectFrame
import ParticulateObjectFrame


class ScrollableObjectFrame(customtkinter.CTkScrollableFrame): 
    def __init__(self, params, master, frame_list, is_solute, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.params = params
        self.is_solute = is_solute
        self.frame_list = frame_list
        self.add_frame_button = customtkinter.CTkButton(self, text = "Add New", command = self.addEmptyFrame, height=40)
        self.add_frame_button.grid(row = 0, column = 0, sticky = "w", ipadx = 20)
        if len(frame_list) > 0:
            self.loadFrames()

        
    def add_reaction_frame_reference(self, reactionSF):
        self.reactionSF = reactionSF
    

    def drawFrames(self):
        for i in range(0, len(self.frame_list)):
            self.frame_list[i].grid(row = i+1, column = 0, pady = 10)
        self.update()


    def drawFrame(self):
            self.frame_list[-1].grid(row = len(self.frame_list)+1, column = 0, pady = 10, sticky = "w")
            self.update()
            #print(str(len(self.frame_list)))


    def deleteFrame(self, index):
        object = self.frame_list.pop(index)

        #update reactions menu
        self.reactionSF.delete_object(object, self.is_solute, index)

        if self.is_solute: #deleting a column
            np.delete(self.params['yield_coefficients'], index, axis=1)
        else: #deleting a row
            np.delete(self.params['yield_coefficients'], index, axis=0)
        
        #to ensure the row the objects are 'gridded' on is the same as their index, regrid all objects.
        for child in self.winfo_children():
            if child != self.add_frame_button:
                child.grid_forget()
        self.drawFrames()        


    def YxsHelper(self): #This funciton adds rows/columns of zeros to the Yxs matrix as new frames are added.
        array = self.params["yield_coefficients"]
        if self.is_solute:
            if 0 in array.shape:
                self.params["yield_coefficients"] = np.zeros((1, 1))
            elif len(self.frame_list) > 0:
                self.params["yield_coefficients"] = np.hstack((array, np.zeros((array.shape[0], 1))))
        else:             
            if 0 in array.shape:
                self.params["yield_coefficients"] = np.zeros((1, 1))
            elif len(self.frame_list) > 0:
                self.params["yield_coefficients"] = np.vstack((array, np.zeros(array.shape[1])))
        #print(self.params["yield_coefficients"].shape)


    def addEmptyFrame(self):
        #disable 'add new' button while this code is running - prevents the button from being spammed - if the button is pressed again while this function is still running there is unpredictable behavior
        self.add_frame_button.configure(state = "disabled")

        #print("adding new frame. Frame count: " + str(len(self.frame_list)))
        frame_params = {"name": customtkinter.StringVar(value=""),
                         "sto": customtkinter.StringVar(value=0.0),
                         "sbo": customtkinter.StringVar(value=0.0),
                          "dt": customtkinter.StringVar(value=0.0),
                          "db": customtkinter.StringVar(value=0.0),
                         "xto": customtkinter.StringVar(value=0.0),
                         "pbo": customtkinter.StringVar(value=0.0),
                         "rho": customtkinter.StringVar(value=0.0)}
        if self.is_solute:
            new_frame = SoluteObjectFrame.ObjectFrame(self, frame_params, index = len(self.frame_list))
        else:
            new_frame = ParticulateObjectFrame.ObjectFrame(self, frame_params, index = len(self.frame_list))
        self.YxsHelper()
        #new_frame.bind('<Unmap>', command = lambda event: self.deleteFrame(new_frame.index))
        self.frame_list.append(new_frame)
        self.drawFrame()
        
        #update the reactions menu
        self.reactionSF.add_object(new_frame, self.is_solute)

        #re-enable 'add new' button
        self.add_frame_button.configure(state = "normal")


    def loadFrames(self, frame_list):
        self.frame_list = frame_list
        self.drawFrames()


    def load_inflow(self, inflow_list):
        inflow_list = inflow_list[1:-1]
        for i, inflow in enumerate(inflow_list):
            self.frame_list[i].load_graph_frame(inflow)


    def get_inflow_params(self):
        if not self.is_solute:
            return None
        
        inflow_params = []
        for solute in self.frame_list:
            inflow_params.append(solute.get_inflow_params())
        
        return inflow_params
    

    def exit(self):
        for solute in self.frame_list:
            solute.exit()