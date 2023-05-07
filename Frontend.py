from tkinter import HORIZONTAL, filedialog, ttk, Tk, PhotoImage, RIDGE, Canvas, GROOVE
from PIL import Image, ImageTk
import cv2
import numpy as np

CANVA_WIDTH = 400
CANVA_HEIGHT = 300

class FrontEnd:
    def __init__(self, master):
        self.master = master
        self.modified = False

        """
        self.frame_header = ttk.Frame(self.master)
        self.frame_header.pack()

        # logo
        self.logo = cv2.imread("icon.png")
        self.logo = cv2.cvtColor(self.logo, cv2.COLOR_BGR2RGB)
        self.logo = cv2.resize(self.logo, (50, 50))
        self.logo = Image.fromarray(self.logo)
        self.logo = ImageTk.PhotoImage(self.logo)


        # Header
        ttk.Label(self.frame_header, image=self.logo).grid(row=0, column=0, rowspan=2)
        ttk.Label(self.frame_header, text = "Photoshop", 
                  font=("Helvetica", 18)).grid(row=0, column=2, columnspan=1)
        ttk.Label(self.frame_header, text = "Version 1.0", 
                  font=("Helvetica", 10)).grid(row=1, column=1, columnspan=3)
        """
        

        # Menu
        self.frame_menu = ttk.Frame(self.master)
        self.frame_menu.pack()
        self.frame_menu.config(relief=RIDGE, padding=(50, 15))

        ttk.Button(self.frame_menu, text="Upload an image", 
                   command=self.upload_image).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        self.crop_button = ttk.Button(self.frame_menu, text="Crop Image",
                   command=self.crop_image)
        self.crop_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="sw")

        self.hist_button = ttk.Button(self.frame_menu, text="Histogram",
                   command=self.histogram)
        self.hist_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="sw")

        self.fourier_button = ttk.Button(self.frame_menu, text="Fourier Transform",
                   command=self.fourier_transform)
        self.fourier_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="sw")

        self.draw_button = ttk.Button(self.frame_menu, text="Draw on image",
                   command=self.draw_on_image)
        self.draw_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        
        self.filter_button = ttk.Button(self.frame_menu, text="Apply filter",
                   command=self.filter_action)
        self.filter_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="sw")

        self.save_button = ttk.Button(self.frame_menu, text="Save as",
                   command=self.save_as)
        self.save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        
        # Image
        self.canvas = Canvas(self.frame_menu, width=CANVA_WIDTH, height=CANVA_HEIGHT, bg="gray")
        self.canvas.grid(row=0, column=2, rowspan=10)
        
        
        # Footer
        self.apply_and_cancel = ttk.Frame(self.master)
        self.apply_and_cancel.pack()
        self.apply_button = ttk.Button(self.apply_and_cancel, text="Apply",
                                command=self.apply_action)
        self.apply_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="sw")
        
        self.revert_button = ttk.Button(self.apply_and_cancel, text="Revert All Changes",
                     command=self.revert_all_change)
        self.revert_button.grid(row=0, column=1, columnspan=1, padx=5, pady=5, sticky="sw")

        self.cancel_button = ttk.Button(self.apply_and_cancel, text="Cancel",
                   command=self.cancel)
        self.cancel_button.grid(row=0, column=2, columnspan=1, padx=5, pady=5, sticky="sw")
        
        # disable buttons
        self.crop_button.config(state="disabled")
        self.hist_button.config(state="disabled")
        self.fourier_button.config(state="disabled")
        self.draw_button.config(state="disabled")
        self.filter_button.config(state="disabled")
        self.save_button.config(state="disabled")
        self.apply_button.config(state="disabled")
        self.revert_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
        

        
    def upload_image(self):

        # clear canvas and reset all frames
        self.canvas.delete("all")
        
        self.filename = filedialog.askopenfilename()
        self.original_image = cv2.imread(self.filename)
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

        # filter_image for processing
        self.filter_image = self.original_image.copy()

        # enable buttons
        self.crop_button.config(state="normal")
        self.hist_button.config(state="normal")
        self.fourier_button.config(state="normal")
        self.draw_button.config(state="normal")
        self.filter_button.config(state="normal")
        self.save_button.config(state="normal")

        # reset all frames
        try:
            self.frame_menu.pack_forget()
            self.frame_menu.pack()
        except:
            pass

        try:
            self.apply_and_cancel.pack_forget()
            self.apply_and_cancel.pack()
        except:
            pass

        try:
            self.side_frame.pack_forget()
            self.side_frame.pack()
        except:
            pass

        self.display_action(self.filter_image)

    def display_action(self, image):
        if self.modified:
            self.apply_button.config(state="normal")
            self.revert_button.config(state="normal")
            self.cancel_button.config(state="normal")

        # resize image to fit the canvas
        new_width = CANVA_WIDTH
        new_height = int(image.shape[0] * (new_width / image.shape[1]))

        if new_height > CANVA_HEIGHT:
            new_height = CANVA_HEIGHT
            new_width = int(image.shape[1] * (new_height / image.shape[0]))
        self.display_image = cv2.resize(image, (new_width, new_height))


        self.display_image = Image.fromarray(self.display_image)
        self.display_image = ImageTk.PhotoImage(self.display_image)
        
        pos_x = int((CANVA_WIDTH - self.display_image.width()) / 2)
        pos_y = int((CANVA_HEIGHT - self.display_image.height()) / 2)

        self.canvas.create_image(pos_x, pos_y, image=self.display_image, anchor="nw")


    def crop_image(self):
        self.refresh_side_frame()

        # create a new window to get user input
        window = Tk()

        # Set the window size
        window.geometry("400x300")

        # Set the window position
        # The format for geometry string is "width x height + x_offset + y_offset"
        window.geometry("400x300+200+100")

       # Create a Label widget and grid it on the first row, first column
        label = ttk.Label(window, text="Enter starting X:")
        label.grid(row=0, column=0)

        # Create an Entry widget and grid it on the first row, second column
        input_box = ttk.Entry(window)
        input_box.grid(row=0, column=1)



        # Create a second Label widget and grid it on the second row, first column
        label2 = ttk.Label(window, text="Enter starting Y:")
        label2.grid(row=1, column=0)

        # Create a second Entry widget and grid it on the second row, second column
        input_box2 = ttk.Entry(window)
        input_box2.grid(row=1, column=1)


        label3 = ttk.Label(window, text= "Enter width:")
        label3.grid(row=2, column=0)
        input_box3 = ttk.Entry(window)
        input_box3.grid(row=2, column=1)



        
        label4 = ttk.Label(window, text="Enter height:")
        label4.grid(row=3, column=0)
        input_box4 = ttk.Entry(window)
        input_box4.grid(row=3, column=1)

        submit_button = ttk.Button(window, text="Submit", command=lambda: self.crop_image_callback(input_box.get(), input_box2.get(), input_box3.get(), input_box4.get(), window))
        submit_button.grid(row=4, column=1)

        # Center the Label and Entry widgets horizontally
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)


        pass

    def crop_image_callback(self, x, y, width, height, window):
        new_x = int(x)
        new_y = int(y)
        new_width = int(width)
        new_height = int(height)
        self.modified = True
        
        image_width = self.filter_image.shape[0]
        image_height = self.filter_image.shape[1]

        if new_x + new_width > image_width or new_y + new_height > image_height or new_x < 0 or new_y < 0 or new_width < 0 or new_height < 0:
            print(f"WRONG INPUT. PLEASE INSERT AGAIN")
            window.destroy()
        else:
            self.filter_image = self.filter_image[new_x:new_width, new_y:new_height] 
            self.display_action(self.filter_image)
            window.destroy()


    def histogram(self):
        pass

    def fourier_transform(self):
        self.modified = True

        self.editing_image = cv2.cvtColor(self.filter_image, cv2.COLOR_BGR2GRAY)

        dft = cv2.dft(np.float32(self.editing_image), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

        self.editing_image = magnitude_spectrum
        self.display_action(self.editing_image)


    def draw_on_image(self):
        pass

    def filter_action(self):
        self.refresh_side_frame()
        ttk.Button(self.side_frame, text="Grayscale", 
                   command=self.grayscale).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Blur",
                   command=self.blur_action).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Negative",
                   command=self.negative).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Sharpen",
                   command=self.sharpen).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Gamma Correction",
                   command=self.stylisation).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Sketch Effect",
                   command=self.sketch_effect).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Emboss",
                   command=self.emboss).grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
        ttk.Button(self.side_frame, text="Sepia",
                   command=self.sepia).grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="sw")
    

    def grayscale(self):
        # check if the image is already grayscale
        if len(self.filter_image.shape) == 2:
            return

        self.editing_image = cv2.cvtColor(self.filter_image, cv2.COLOR_BGR2GRAY)

        self.modified = True
        self.display_action(self.editing_image)

    def blur_action(self):
        self.refresh_side_frame()

        ttk.Label(self.side_frame, text='Average Blur').grid(row=0, column=2, padx=5, sticky="sw")
        self.average_slider = ttk.Scale(self.side_frame, from_=1, to=100, orient=HORIZONTAL, 
                                        command=self.average_blur).grid(row=0, column=3, padx=5, sticky="sw")
        
        
    def average_blur(self, value):
        value = float(value)
        value = int(value)
        if value % 2 == 0:
            value += 1

        self.editing_image = self.filter_image.copy()
        self.editing_image = cv2.blur(self.editing_image, (value, value))

        self.modified = True
        self.display_action(self.editing_image)

    def negative(self):
        pass

    def sharpen(self):
        pass

    def look_up_table(self , image, gamma):
    # build a lookup table mapping the pixel values [0,255] to their adjusted gamma values
        table = np.array(np.power(np.arange(0, 256) / 255.0, gamma) * 255.0, dtype=np.uint8)

    # apply gamma correction using the lookup table
        return cv2.LUT(image, table)
    

    # gamma correction using lookup table 
    def stylisation(self):
        self.modified = True
        window = Tk()

        window.title("Slider")
        # create the slider
        slider = ttk.Scale(window , from_=0, to = 5, orient= HORIZONTAL, length=200)
        slider.pack()


        # Create a label to display the slider value
        value_label = ttk.Label(window)
        value_label.pack()

        def get_slider_value():
            slider_value = slider.get()
            value_label.config(text=f"Slider value: {slider_value:.2f}")
            self.filter_image = self.look_up_table(self.filter_image, slider_value)
            self.display_action(self.filter_image)

        button = ttk.Button(window, text="Get Slider Value", command=get_slider_value)
        button.pack()
    
    def sketch_effect(self):
        pass

    def emboss(self):
        pass

    def sepia(self):
        pass



    def save_as(self):
        pass

    def apply_action(self):
        self.filter_image = self.editing_image.copy()
        self.refresh_side_frame()

        self.display_action(self.filter_image)
        
    def cancel(self):
        self.editing_image = self.filter_image.copy()
        self.refresh_side_frame()
        self.display_action(self.editing_image)

    def revert_all_change(self):
        self.filter_image = self.original_image.copy()
        self.refresh_side_frame()
        self.display_action(self.filter_image)

    def refresh_side_frame(self):
        try:
            self.side_frame.grid_forget()
        except:
            pass

        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")
        self.display_action(self.filter_image)
        self.side_frame = ttk.Frame(self.frame_menu)
        self.side_frame.grid(row=0, column=11, rowspan=10)
        self.side_frame.config(relief=GROOVE, padding=(50, 15))
