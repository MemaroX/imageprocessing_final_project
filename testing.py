import cv2
import numpy as np
from tkinter import Tk, Frame, Label, Scale, Button, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from image_processing import ImageProcessing
from ttkbootstrap import Style
import os

class ImageEditorGUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.image_processing = ImageProcessing()  
        self.original_image = None
        self.processed_image = None
        self.slider = None
        self.current_filter = None
        self.threshold_slider = None
        self.filter_var = None
        self.original_filename = ""
        self.create_widgets()

    def create_widgets(self):
        # Image display label
        self.image_label = Label(self)
        self.image_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        
        # Filter label
        self.filter_label = Label(self, text='', font=("Arial", 12, "bold"))
        self.filter_label.grid(row=1, column=0, columnspan=3, pady=5, sticky="nsew")

        # Filter information box
        self.filter_info_label = Label(self, text="Filter Information", font=("Arial", 10, "bold"))
        self.filter_info_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.filter_info_text = Label(self, text="", wraplength=400, justify="left")
        self.filter_info_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Save button
        self.save_button = ttk.Button(self, text="Save Image", command=self.save_image, state="disabled")
        self.save_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Load button
        self.load_button = ttk.Button(self, text="Load Image", command=self.load_image)
        self.load_button.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # Reset button
        self.reset_button = ttk.Button(self, text="Reset to Original", command=self.reset_image, state="disabled")
        self.reset_button.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        # Apply button
        self.apply_button = ttk.Button(self, text="Apply", state="disabled", command=self.apply_filter)
        self.apply_button.grid(row=5, column=2, padx=5, pady=5, sticky="nsew")

        # Filter buttons frame
        self.filter_frame = Frame(self)
        self.filter_frame.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Create filter buttons
        self.filter_buttons = {}
        filters = [
            ("Low Pass Filter", self.image_processing.apply_low_pass_filter, "Applies a Gaussian blur to the image"),
            ("High-Pass Filter", self.image_processing.apply_hpf, "Highlights edges and fine details in the image"),
            ("Mean Filter", self.image_processing.apply_mean_filter, "Blurs the image to reduce noise and detail"),
            ("Median Filter", self.image_processing.apply_median_filter, "Removes salt-and-pepper noise from the image"),
            ("Roberts Edge", self.image_processing.apply_roberts_edge_detector, "Detects edges using Roberts operator"),
            ("Prewitt Edge", self.image_processing.apply_prewitt_edge_detector, "Detects edges using Prewitt operator"),
            ("Sobel Edge", self.image_processing.apply_sobel_edge_detector, "Detects edges using Sobel operator"),
            ("Erosion", self.image_processing.apply_erosion, "Erodes boundaries of foreground objects"),
            ("Dilation", self.image_processing.apply_dilation, "Expands boundaries of foreground objects"),
            ("Opening", self.image_processing.apply_open, "Erosion followed by dilation, useful for removing noise"),
            ("Closing", self.image_processing.apply_close, "Dilation followed by erosion, useful for closing gaps"),
            ("Hough Circle", self.image_processing.apply_hough_circle_transform, "Detects circles in the image"),
            ("Region Split and Merge", self.image_processing.apply_region_split_and_merge, "Segments the image into regions"),
            ("Thresholding", self.image_processing.apply_thresholding, "Converts image to binary based on intensity threshold"),
        ]
        for i, (name, function, description) in enumerate(filters):
            button = ttk.Button(self.filter_frame, text=name, command=lambda f=function, n=name: self.set_filter(f, n))      
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="nsew")
            self.filter_buttons[name] = (button, description)

    def reset_image(self):
        self.processed_image = self.original_image.copy()
        self.update_image_display()

    def load_image(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.bmp")])
        if filename:
            self.original_image = cv2.imread(filename)
            self.processed_image = self.original_image.copy()
            self.original_filename = os.path.basename(filename)
            self.update_image_display()
            self.apply_button.config(state="normal")
            self.reset_button.config(state="normal")
            self.save_button.config(state="normal")
    
    def set_filter(self, function, name):
        self.filter_var = function
        self.current_filter = name
        self.remove_slider()
        if function == self.image_processing.apply_thresholding:
            self.create_threshold_slider()
        elif function in [self.image_processing.apply_hpf,
                          self.image_processing.apply_mean_filter,
                          self.image_processing.apply_erosion,
                          self.image_processing.apply_dilation,
                          self.image_processing.apply_open,
                          self.image_processing.apply_close]:
            self.create_slider(1, 20, 5)

        # Update filter information
        self.filter_info_text.config(text=self.filter_buttons[name][1])
        self.filter_label.config(text=f"Current filter applied: {self.current_filter}")

    def create_slider(self, min_value, max_value, default_value):
        self.slider = Scale(self, from_=min_value, to=max_value, orient="horizontal",
                            command=self.update_filter_param)
        self.slider.set(default_value)
        self.slider.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    def create_threshold_slider(self):
        self.threshold_slider = Scale(self, from_=0, to=255, orient="horizontal",
                                      command=self.update_filter_param, resolution=1)
        self.threshold_slider.set(128)
        self.threshold_slider.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    def remove_slider(self):
        if self.slider:
            self.slider.destroy()
            self.slider = None
        if self.threshold_slider:
            self.threshold_slider.destroy()
            self.threshold_slider = None

    def update_filter_param(self, value):
        if self.filter_var in [self.image_processing.apply_hpf,
                               self.image_processing.apply_mean_filter,
                               self.image_processing.apply_erosion,
                               self.image_processing.apply_dilation,
                               self.image_processing.apply_open,
                               self.image_processing.apply_close]:
            self.image_processing.kernel_size = int(value)
        elif self.filter_var == self.image_processing.apply_region_split_and_merge:
            self.image_processing.threshold_value = int(value)

    def apply_filter(self):
        if self.filter_var and self.original_image is not None:
            if self.filter_var == self.image_processing.apply_thresholding:
                threshold_value = self.threshold_slider.get()
                self.processed_image = self.filter_var(self.original_image.copy(), threshold_value)
            else:
                self.processed_image = self.filter_var(self.original_image.copy())
            self.update_image_display()
            self.filter_label.config(text=f"Current filter applied: {self.current_filter}")

    def update_image_display(self):
        if self.processed_image is not None:
            processed_image_8bit = cv2.normalize(self.processed_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            rgb_image = cv2.cvtColor(processed_image_8bit, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_image)
            photo = ImageTk.PhotoImage(image=image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        else:
            self.reset_button.config(state='disabled')

    def save_image(self):
        if self.processed_image is not None:
            file_types = [("PNG files", "*.png"), ("JPEG files", "*.jpg")]
            default_extension = ".png" if self.original_filename.endswith(".png") else ".jpg"
            default_name = f"{self.current_filter} of {os.path.splitext(self.original_filename)[0]}{default_extension}"
            filename = filedialog.asksaveasfilename(defaultextension=default_extension,
                                                     initialfile=default_name,
                                                     filetypes=file_types)
            if filename:
                cv2.imwrite(filename, self.processed_image)

# Create the main Tkinter window
root = Tk()
root.title("Image Processing App")

# Apply ttkbootstrap style
style = Style()
style.theme_use('flatly')

# Configure resizing behavior
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create and run the GUI application
app = ImageEditorGUI(root)
app.mainloop()
