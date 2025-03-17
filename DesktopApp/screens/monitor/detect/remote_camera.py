import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from components.button import ButtonFactory
from _config.theme import Theme

class RemoteCamera(ctk.CTkFrame):
    def __init__(self, parent, controller=None, **kwargs):
        super().__init__(parent, fg_color=Theme.QUARTERNARY, **kwargs)
        self.controller = controller

        self.create_title_section()

        # Container chính chứa hai cột
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)

        self.create_camera_section()
        self.create_control_section()

        self.create_back_button()

        # Biến camera
        self.cap = None
        self.update_video()

    def create_title_section(self):
        """Tạo phần tiêu đề riêng biệt trên cùng"""
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(72, 12))

        self.title_label = ctk.CTkLabel(
            title_frame, text="Start your posture monitoring session",
            font=(Theme.FONT_FAMILY, Theme.FONT_3XL, "bold"), text_color=Theme.BLACK
        )
        self.title_label.pack()

        self.desc_label = ctk.CTkLabel(
            title_frame, text="Adjust your position and posture for better sitting",
            font=(Theme.FONT_FAMILY, Theme.FONT_XL), text_color=Theme.BLACK
        )
        self.desc_label.pack(pady=(12, 0))

    def create_camera_section(self):
        self.camera_frame = ctk.CTkFrame(
            self.container, fg_color=Theme.WHITE, width=448, height=293,
            corner_radius=Theme.ROUNDED_7,
            border_width=3,
            border_color=Theme.BLACK
            )
        self.camera_frame.grid(row=0, column=0, padx=(0, 10), pady=20, sticky="ne")

        self.camera_label = ctk.CTkLabel(self.camera_frame, text="No Camera Feed", width=448, height=293)
        self.camera_label.pack()

    def create_control_section(self):
        """Tạo phần điều khiển"""
        control_frame = ctk.CTkFrame(self.container, fg_color="transparent", width=468, height=278)
        control_frame.grid(row=0, column=1, padx=(10, 0), pady=20, sticky="nw")

        address_label = ctk.CTkLabel(
            control_frame, text="Enter your camera address here", anchor="w",
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE), text_color=Theme.BLACK
        )
        address_label.pack(fill="x",pady=(0,10))

        self.address_entry = ctk.CTkEntry(
            control_frame, 
            placeholder_text="Your camera address", 
            width=400, height=45,
            border_width=2,
            border_color=Theme.BLACK
        )
        self.address_entry.pack(pady=(0, 15))

        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(anchor="w") 

        self.connect_button = ButtonFactory.create_tertiary_button(
            button_frame, 
            "Connect", 
            command=self.connect_camera, 
            corner_radius=Theme.ROUNDED_8
        )
        self.connect_button.pack(side="left", padx=(0, 10))

        self.status_button = ButtonFactory.create_quaternary_button(
            button_frame, 
            "Status Check", 
            command=self.check_status,
            corner_radius=Theme.ROUNDED_8
        )
        self.status_button.pack(side="left")

        duration_label = ctk.CTkLabel(
            control_frame, text="Duration", anchor="w",
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE), text_color=Theme.BLACK
        )
        duration_label.pack(fill="x", pady=(10, 0))

        self.time_selection = ctk.CTkComboBox(
        control_frame,
        values=["1 min", "2 min", "5 min", "10 min"],
        width=155,
        height=40,
        font=(Theme.FONT_FAMILY, Theme.FONT_BASE),
        dropdown_font=(Theme.FONT_FAMILY, Theme.FONT_L),
        state="readonly",
        fg_color=Theme.WHITE,
        text_color=Theme.BLACK,  
        dropdown_fg_color=Theme.WHITE,  
        dropdown_text_color=Theme.BLACK,  
        border_width=2,  
        border_color=Theme.BLACK,  
        corner_radius=Theme.ROUNDED_3,  
        button_color=Theme.WHITE, 
    )

        self.time_selection.pack(pady=(0, 12), anchor="w")  

        self.start_button = ButtonFactory.create_dark_button(control_frame, "Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=(0, 20), anchor="w")

    def create_back_button(self):
        """Tạo nút Go Back và đặt trong container với grid"""
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
        self.back_button.grid(row=1, column=0, columnspan=2, pady=(20, 20))  

    def update_video(self):
        """Cập nhật luồng video từ camera"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (468, 293))
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.camera_label.configure(image=img)
                self.camera_label.image = img
        self.after(30, self.update_video)

    def connect_camera(self):
        """Kết nối đến camera theo địa chỉ"""
        address = self.address_entry.get()
        if not address:
            print("Enter a camera address!")
            return

        self.cap = cv2.VideoCapture(address)
        if not self.cap.isOpened():
            print("Failed to connect to camera.")

    def check_status(self):
        """Kiểm tra trạng thái kết nối camera"""
        if self.cap and self.cap.isOpened():
            print("Camera is connected!")
        else:
            print("No active camera connection.")

    def start_monitoring(self):
        """Bắt đầu theo dõi tư thế"""
        print("Monitoring started...")

    def go_back(self):
        """Quay lại màn hình trước"""
        if self.controller:
            self.controller.show_frame("monitor")
