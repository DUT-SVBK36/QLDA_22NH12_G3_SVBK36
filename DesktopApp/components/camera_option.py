import customtkinter as ctk
from PIL import Image, ImageTk
import os
from _config.theme import Theme
class CameraOptionButton(ctk.CTkButton):
    def __init__(self, master, text, icon_path, command=None, **kwargs):
        """
        Nút chọn camera với biểu tượng và mô tả.
        
        Args:
            master: Widget cha
            text: Nội dung hiển thị trên nút
            icon_path: Đường dẫn tới hình ảnh biểu tượng
            command: Hàm thực thi khi bấm nút
            **kwargs: Các tùy chọn bổ sung cho CTkButton
        """
        self.icon_image = None
        if os.path.exists(icon_path):
            self.icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(96, 96))
        
        super().__init__(
            master,
            text=text,
            image=self.icon_image,
            compound="top",
            width=280,
            height=238,
            fg_color=Theme.WHITE,
            text_color= Theme.BLACK,
            corner_radius=15,
            font=(Theme.FONT_FAMILY, 16),
            hover_color=Theme.LIGHT_PURPLE,
            command=command,
            **kwargs
        )
