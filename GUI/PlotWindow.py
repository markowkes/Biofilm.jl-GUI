import customtkinter
import FileController

from PIL import Image

class PlotWindow(customtkinter.CTkToplevel):
    def __init__(self, tfinal, step, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.height = self.winfo_screenheight() - 200
        self.width = self.winfo_screenwidth() - 280
        self.geometry("%dx%d+0+0" % (self.width, self.height))

        self.step = .1
        self.tfinal = 1
        self.current_step = None

        self.init_window()


    def slider_event(self, value):
        #round the incoming value, floats can have rounding errors
        value = round(value, 10)

        if value != self.current_step:
            img = self.images.get('plot_'+str(value)+'.png')
            image_label = customtkinter.CTkLabel(master = self.plot_frame, image=img, text="")
            image_label.grid(row=0,column=0)
            self.current_step = value

    def init_window(self):
        self.plot_frame = customtkinter.CTkFrame(master = self)
        self.plot_frame.grid(row = 0, column = 0)
        slider = customtkinter.CTkSlider(master = self, from_=0, to=self.tfinal, width=self.width-100, height=40, number_of_steps=(self.tfinal/self.step), command=self.slider_event)
        slider.grid(row = 1, column = 0)
        self.plot_frame.grid_propagate()
        fc = FileController.FileController()
        file_names = fc.getPlotFilenames()
        self.images = {}
        for file in file_names:
            current_directory = fc.getCurrDir()
            image = Image.open(current_directory+'/Biofilm.jl-main/savePlots/'+file)
            CTKimage = customtkinter.CTkImage(light_image=image,
                                                size=(self.width, self.height-50))
            self.images[file] = CTKimage
        #set slider to 0 to start, create event to display plot for t0
        slider.set(0)
        self.slider_event(0.0)
            
        