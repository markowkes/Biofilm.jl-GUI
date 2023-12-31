#Scrollable solute/particulate class
import customtkinter
import ObjectFrame


class ScrollableObjectFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, frame_list, **kwargs):
        super().__init__(master, **kwargs)
        self.frame_list = frame_list
        add_frame_button = customtkinter.CTkButton(self, text = "Add New", command = self.addEmptyFrame, height=40)
        add_frame_button.grid(row = 0, column = 0, sticky = "w", ipadx = 20)
    
    def drawFrames(self):
        for i in range(0, len(self.frame_list)):
            self.frame_list[i].grid(row = i+1, column = 0, pady = 10)
        self.update()

    def drawFrame(self):
            self.frame_list[-1].grid(row = len(self.frame_list)+1, column = 0, pady = 10, sticky = "w")
            self.update()
            print(str(len(self.frame_list)))

    def deleteFrame(self, index):
        del self.frame_list[index]

    def addEmptyFrame(self):
        print("adding new frame. Frame count: " + str(len(self.frame_list)))
        new_frame = ObjectFrame.ObjectFrame(self, "", 0.0, 0.0, 0.0, 0.0, len(self.frame_list))
        new_frame.bind('<Unmap>', command = lambda event: self.deleteFrame(new_frame.index))
        self.frame_list.append(new_frame)
        self.drawFrame()
        
