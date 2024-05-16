class ImageProcessingApp :
    def _init_(self, root):
        self.root = root
        self.root,title= "ImageProcessingApp"
        
        self.image_label= Label(master)
        self.image_label,pack()
        
        self.load_button = tk.Button(master, text="Load Image", command=self.load_default_image)
        self.load_button.pack()
        
        self,add_buttons_and_sliders()
 
    def load_default_image(self):
        path = "Simba.jpg"
        self.original_image= cv2.imread(path)
        self.update_image(self.original_image)
        
    def load_image(self):
        path = "Simba.jpg"
        self.original_image= cv2.imread(path)
        self.update_image(self.original_image)
        
    def update_image(self, image):
        image= cv.cvtColor(image, cv2.COLOR_BGR2RGB)
        image= Image.fromarray(image)
        
    def add_buttons_and_sliders(self):
        self.add_button("HPF",self.apply_hpf)
        self.add_sllider("Kernel Size", 1, 20, 5, self.update_hpf)
        
        
        
        
        
        
        
    def add_button(self, text, command):
        button= Button(self.master, text= text, command= command)
        button.pack()
        
    def add_slider(self, text, from_, to_, default, command):
        slider_label= Label(self.master, text= text)
        slider_label.pack()
        slider= Scale(self.master, from_= from_, to= to_ ,orient= tk.HORIZONTAL,command= add_slider)
        slider.set(default)
        slider.pack()