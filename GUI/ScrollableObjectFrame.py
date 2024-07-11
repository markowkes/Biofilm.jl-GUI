#Scrollable solute/particulate class
import numpy as np

import customtkinter
import SoluteObjectFrame
import ParticulateObjectFrame


class ScrollableObjectFrame(customtkinter.CTkScrollableFrame): 
    def __init__(self, params, master, frame_list, is_solute, **kwargs):
        super().__init__(master, **kwargs)
        self.params = params
        self.is_solute = is_solute
        self.frame_list = frame_list
        add_frame_button = customtkinter.CTkButton(self, text = "Add New", command = self.addEmptyFrame, height=40)
        add_frame_button.grid(row = 0, column = 0, sticky = "w", ipadx = 20)
        if len(frame_list) > 0:
            self.loadFrames()
    

    def drawFrames(self):
        for i in range(0, len(self.frame_list)):
            self.frame_list[i].grid(row = i+1, column = 0, pady = 10)
        self.update()


    def drawFrame(self):
            self.frame_list[-1].grid(row = len(self.frame_list)+1, column = 0, pady = 10, sticky = "w")
            self.update()
            #print(str(len(self.frame_list)))


    def deleteFrame(self, index):
        self.frame_list.pop(index)


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


    def loadFrames(self, frame_list):
        self.frame_list = frame_list
        self.drawFrames()
        
