import customtkinter as ctk
import sys
import os

# Add root directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from _config.theme import Theme
from components.side_bar import SideBar
from screens.dashboard import Dashboard

# Import other screens as they are created
from screens.monitor.choosing import Choosing
from screens.monitor.detect.remote_camera import RemoteCamera
from screens.monitor.detect.own_camera import OwnCamera
# from screens.settings import Settings
# from screens.auth import Auth

class BPDApp(ctk.CTk):
    """
    Main application controller class
    
    Handles:
    - Window creation
    - Screen navigation
    - Authentication state
    """
    
    def __init__(self, *args, **kwargs):
        # Set appearance mode before initializing
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        super().__init__(*args, **kwargs)
        
        # Configure main window
        self.title("BPD Application")
        self.geometry("1366x768")
        self.minsize(1000, 600)
        self._set_appearance_mode("light")
        
        # Initialize frames dictionary before creating sidebar
        self.frames = {}
        
        # Setup application container
        self.setup_container()
        
        # Initialize screens
        self.setup_frames()
        
        # Set initial screen
        self.show_frame("dashboard")
        
        # Apply background from Theme
        self.apply_background()
    
    def apply_background(self):
        """Apply the app background from Theme"""
        # Set the background image to the main container
        self.bg_label = Theme.set_app_background(self.main_container)
        
        # Ensure the background is behind other widgets
        if self.bg_label:
            self.bg_label.lower()
    
    def setup_container(self):
        """Setup the main container and sidebar"""
        # Main container with weight configuration for responsiveness
        self.main_container = ctk.CTkFrame(self, fg_color=Theme.WHITE, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        
        # Make the main container responsive with grid
        self.main_container.columnconfigure(1, weight=1)  # Content area grows
        self.main_container.rowconfigure(0, weight=1)     # Full height
        
        # Create sidebar - fixed width
        self.sidebar = SideBar(self.main_container, controller=self)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        # Create content area - expandable
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Make the content area responsive
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
    
    def setup_frames(self):
        """Initialize all screen frames"""
        # Dashboard screen
        dashboard_frame = Dashboard(self.content_frame)
        dashboard_frame.controller = self  # Set controller reference for navigation
        self.frames["dashboard"] = dashboard_frame
        
        choosing_frame = Choosing(self.content_frame, self)
        self.frames["monitor"] = choosing_frame

        remote_camera_frame = RemoteCamera(self.content_frame, self)
        self.frames["remote_camera"] = remote_camera_frame

        own_camera_frame = OwnCamera(self.content_frame, self)
        self.frames["own_camera"] = own_camera_frame
        # Add other screens as they are created
        # monitor_frame = Monitor(self.content_frame, self)
        # self.frames["monitor"] = monitor_frame
        #
        # settings_frame = Settings(self.content_frame, self)
        # self.frames["settings"] = settings_frame
        #
        # auth_frame = Auth(self.content_frame, self)
        # self.frames["auth"] = auth_frame
    
    def show_frame(self, frame_name):
        """Show the specified frame and hide others"""
        print(f"Showing frame: {frame_name}")
        
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_forget() if hasattr(frame, 'grid_info') else frame.pack_forget()
        
        # Show the requested frame
        if frame_name in self.frames:
            # Use grid for better responsiveness
            self.frames[frame_name].grid(row=0, column=0, sticky="nsew")
            print(f"Frame '{frame_name}' is now visible")
        else:
            print(f"Frame '{frame_name}' not found in available frames: {list(self.frames.keys())}")
    
    def go_to_monitor(self):
        """Navigate to the monitor screen"""
        self.show_frame("monitor")
    
    def go_to_settings(self):
        """Navigate to the settings screen"""
        self.show_frame("settings")

if __name__ == "__main__":
    app = BPDApp()
    app.mainloop()