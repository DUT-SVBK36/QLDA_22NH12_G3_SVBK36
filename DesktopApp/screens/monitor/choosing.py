import customtkinter as ctk
from components.camera_option import CameraOptionButton
from _config.theme import Theme
from utils.model_loader import load_model_and_encoder

class Choosing(ctk.CTkFrame):
    def __init__(self, parent, controller=None, **kwargs):
        super().__init__(
            parent,
            fg_color=Theme.QUARTERNARY,
            corner_radius=0,
            **kwargs
        )
        self.controller = controller

       
        
        self.create_layout()
    
    def create_layout(self):
        """Tạo bố cục chính của màn hình chọn camera."""
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.create_title_section()
        self.create_option_section()
        self.create_back_button()
    
    def create_title_section(self):
        """Tạo phần tiêu đề của giao diện."""
        self.title_label = ctk.CTkLabel(
            self.container, text="Choose your device", 
            font=(Theme.FONT_FAMILY, Theme.FONT_3XL, "bold"), text_color=Theme.BLACK
        )
        self.title_label.pack(pady=(24, 5))
        
        self.desc_label = ctk.CTkLabel(
            self.container, text="Select your own camera option below to continue", 
            font=(Theme.FONT_FAMILY, Theme.FONT_XL), text_color=Theme.BLACK
        )
        self.desc_label.pack(pady=(0, 24))
    
    def create_option_section(self):
        """Tạo phần chứa các nút chọn camera."""
        self.option_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.option_frame.pack(pady=(0,24))
        
        self.remote_camera_button = CameraOptionButton(
            self.option_frame, "Using Remote Camera", "assets/img/remote_camera.png", self.use_remote_camera
        )
        self.remote_camera_button.grid(row=0, column=0, padx=24)
        
        self.own_camera_button = CameraOptionButton(
            self.option_frame, "Using Your Own Camera", "assets/img/own_camera.png", self.use_own_camera
        )
        self.own_camera_button.grid(row=0, column=1, padx=24)
    
    def create_back_button(self):
        self.back_button = ctk.CTkButton(
            self.container,
            text="Go Back",
            fg_color="transparent",  
            hover_color=Theme.LIGHT_PURPLE,  
            text_color=Theme.PRIMARY_DARK,  
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE, "underline"),  
            width=0, height=0,  
            command=self.go_back
        )
        self.back_button.pack(pady=(20, 20))
    
    def use_remote_camera(self):
        if self.controller:
            self.controller.show_frame("remote_camera")
    
    def use_own_camera(self):
        if self.controller:
            self.controller.show_frame("own_camera")
    
    def go_back(self):
        if self.controller:
            self.controller.show_frame("dashboard")