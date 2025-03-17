import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
import time

class CameraTest(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Camera Test")
        self.geometry("800x600")

        # Camera variables
        self.local_camera_active = False
        self.remote_camera_active = False
        self.camera_thread = None
        self.cap = None
        self.remote_url = "your_remote_camera_url_here"  # Replace with actual URL

        # Create frame for buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        # Create toggle buttons
        self.local_camera_button = ctk.CTkSwitch(
            self.button_frame, 
            text="Local Camera",
            command=self.toggle_local_camera
        )
        self.local_camera_button.pack(side="left", padx=10)

        self.remote_camera_button = ctk.CTkSwitch(
            self.button_frame, 
            text="Remote Camera",
            command=self.toggle_remote_camera
        )
        self.remote_camera_button.pack(side="left", padx=10)

        # Create label for video display
        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(pady=10)

    def toggle_local_camera(self):
        if self.remote_camera_active:
            self.remote_camera_button.deselect()
            self.remote_camera_active = False
            time.sleep(0.1)  # Allow time for camera to close

        self.local_camera_active = not self.local_camera_active
        if self.local_camera_active:
            self.start_camera(0)  # 0 for default webcam
        else:
            self.stop_camera()

    def toggle_remote_camera(self):
        if self.local_camera_active:
            self.local_camera_button.deselect()
            self.local_camera_active = False
            time.sleep(0.1)  # Allow time for camera to close

        self.remote_camera_active = not self.remote_camera_active
        if self.remote_camera_active:
            self.start_camera(self.remote_url)
        else:
            self.stop_camera()

    def start_camera(self, source):
        if self.camera_thread is None or not self.camera_thread.is_alive():
            self.cap = cv2.VideoCapture(source)
            self.camera_thread = threading.Thread(target=self.update_frame)
            self.camera_thread.daemon = True
            self.camera_thread.start()

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        # Clear the image and reset the label text
        self.video_label.configure(image=None, text="Camera Off")
        self.video_label.image = None

    def update_frame(self):
        while self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Convert frame to PhotoImage
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image)
                
                # Update label
                self.video_label.configure(image=photo)
                self.video_label.image = photo
            time.sleep(0.03)  # Limit frame rate

    def on_closing(self):
        self.stop_camera()
        self.quit()

if __name__ == "__main__":
    app = CameraTest()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()