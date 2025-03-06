import tkinter as tk
import sys
import os

# Add root directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from _config.theme import Theme
from components.side_bar import SideBar
from screens.dashboard import Dashboard
from utils.gradients import Gradient  # Import for gradient background
# Import other screens as they are created
# from screens.monitor import Monitor
# from screens.settings import Settings
# from screens.auth import Auth

class BPDApp(tk.Tk):
    """
    Main application controller class
    
    Handles:
    - Window creation
    - Screen navigation
    - Authentication state
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure main window
        self.title("BPD Application")
        self.geometry("1200x720")
        self.minsize(1000, 600)
        self.config(bg=Theme.WHITE)
        
        # Initialize frames dictionary before creating sidebar
        self.frames = {}
        
        # Setup application container
        self.setup_container()
        
        # Initialize screens
        self.setup_frames()
        
        # Set initial screen
        self.show_frame("dashboard")
        
        # Bind resize event
        self.bind("<Configure>", self.on_window_resize)
        
        # Apply gradient background after UI is set up
        self.after(100, self.apply_background_gradient)
    
    def apply_background_gradient(self):
        """Apply a vertical gradient background to the main container"""
        # Get current dimensions
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Apply vertical gradient from TERTIARY to QUARTERNARY
        Gradient.apply_gradient_to_widget(
            self.main_container,
            [Theme.TERTIARY, Theme.QUARTERNARY],
            gradient_type="linear",
            direction="vertical",
            width=width,
            height=height
        )
        
        # Store the gradient image reference to prevent garbage collection
        self.bg_gradient = self.main_container.gradient_img
    
    def on_window_resize(self, event):
        """Handle window resize event to update responsive elements"""
        # Only process resize events for the main window
        if event.widget == self:
            # Update the gradient on resize with a slight delay to avoid excessive redraws
            if hasattr(self, '_resize_timer'):
                self.after_cancel(self._resize_timer)
            self._resize_timer = self.after(100, self.apply_background_gradient)
    
    def setup_container(self):
        """Setup the main container and sidebar"""
        # Main container with weight configuration for responsiveness
        self.main_container = tk.Frame(self, bg=Theme.WHITE)
        self.main_container.pack(fill="both", expand=True)
        
        # Make the main container responsive with grid
        self.main_container.columnconfigure(1, weight=1)  # Content area grows
        self.main_container.rowconfigure(0, weight=1)     # Full height
        
        # Create sidebar - fixed width
        self.sidebar = SideBar(self.main_container, controller=self)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        # Create content area - expandable
        self.content_frame = tk.Frame(self.main_container, bg="")  # Transparent bg
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