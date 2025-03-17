import sys
import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# Add root directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config.theme import Theme
from utils.gradients import Gradient
from components.side_bar import SideBar

class TestController:
    """
    Test controller to simulate navigation between screens
    """
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.current_frame = None
        self.frames = {}
    
    def create_test_frames(self):
        """Create test frames for each navigation item"""
        frame_configs = {
            "dashboard": {
                "title": "Dashboard Screen",
                "gradient_colors": [Theme.TERTIARY, Theme.QUARTERNARY]
            },
            "monitor": {
                "title": "Monitor Screen",
                "gradient_colors": [Theme.TERTIARY, Theme.QUARTERNARY]
            },
            "settings": {
                "title": "Settings Screen",
                "gradient_colors": [Theme.TERTIARY, Theme.QUARTERNARY]
            }
        }
        
        for name, config in frame_configs.items():
            # Create frame with customtkinter
            frame = ctk.CTkFrame(
                self.content_frame,
                fg_color=Theme.WHITE,
                corner_radius=0
            )
            frame.pack_propagate(False)
            
            # We need to make the frame visible briefly to get its dimensions
            frame.pack(fill="both", expand=True)
            self.content_frame.update_idletasks()
            
            # Get the width and height of the frame
            width = frame.winfo_width()
            height = frame.winfo_height()
            
            # For customtkinter, we can set the background directly
            # Apply app background from Theme
            Theme.set_app_background(frame)
            
            # Hide the frame for now (will be shown when selected)
            frame.pack_forget()
            
            # Add a title - use a frame to make it stand out from the gradient
            title_frame = ctk.CTkFrame(
                frame,
                fg_color=Theme.WHITE,
                corner_radius=0
            )
            title_frame.pack(pady=(30, 0), padx=20, anchor="nw", fill="x")
            
            # Title label
            title = ctk.CTkLabel(
                title_frame, 
                text=config["title"],
                font=Theme.get_font(Theme.FONT_2XL, "bold"),
                text_color=Theme.PRIMARY_DARK,
                fg_color=Theme.WHITE,
                padx=10,
                pady=10
            )
            title.pack(anchor="w")
            
            # Add content with a semi-transparent background
            content_frame = ctk.CTkFrame(
                frame,
                fg_color=Theme.WHITE,
                corner_radius=0
            )
            content_frame.pack(pady=20, padx=20, anchor="nw", fill="x")
            
            content = ctk.CTkLabel(
                content_frame,
                text=f"This is the {name} screen content area.\n\n" +
                     "The background is using the app background image from Theme.set_app_background().\n\n" +
                     "This approach lets us have proper backgrounds while still using customtkinter widgets " +
                     "for the interface components.",
                font=Theme.get_font(Theme.FONT_LG),
                text_color=Theme.BLACK,
                fg_color=Theme.WHITE,
                wraplength=500,
                padx=15,
                pady=15
            )
            content.pack(anchor="nw")
            
            # Store the frame
            self.frames[name] = frame
    
    def show_frame(self, name):
        """Show the selected frame and hide others"""
        print(f"Switching to {name} screen")
        
        # Hide current frame
        if self.current_frame and self.current_frame in self.frames:
            self.frames[self.current_frame].pack_forget()
        
        # Show new frame
        if name in self.frames:
            self.frames[name].pack(fill="both", expand=True)
            self.current_frame = name


class SideBarTester:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_layout()
    
    def setup_window(self):
        """Set up the test window"""
        self.root.title("SideBar Component Test")
        
        # Set window size (16:9 ratio)
        self.width = 1024
        self.height = 576
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        
        # Set window position and size
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.minsize(800, 450)
        
    def create_layout(self):
        """Create the test layout"""
        # Main container
        main_container = ctk.CTkFrame(
            self.root, 
            fg_color=Theme.WHITE,
            corner_radius=0
        )
        main_container.pack(fill="both", expand=True)
        
        # Left side - Test information
        info_frame = ctk.CTkFrame(
            main_container, 
            fg_color=Theme.WHITE, 
            corner_radius=0,
            width=300
        )
        info_frame.pack(side="left", fill="y")
        info_frame.pack_propagate(False)
        
        # Test title
        title = ctk.CTkLabel(
            info_frame, 
            text="SideBar Component Test",
            font=Theme.get_font(Theme.FONT_XL, "bold"),
            text_color=Theme.PRIMARY_DARK,
            fg_color=Theme.WHITE
        )
        title.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Test description
        description = """
        This test demonstrates the SideBar navigation component.
        
        Features being tested:
        • Fixed width sidebar (64px)
        • Logo display at the top
        • Navigation icons with hover effects
        • Selected state with highlight bar
        • Navigation between screens
        
        Try clicking the different icons to navigate between screens.
        """
        
        desc_label = ctk.CTkLabel(
            info_frame,
            text=description,
            font=Theme.get_font(Theme.FONT_BASE),
            text_color=Theme.BLACK,
            fg_color=Theme.WHITE,
            wraplength=260,
            justify="left"
        )
        desc_label.pack(pady=10, padx=20, anchor="w")
        
        # Add event log section
        log_title = ctk.CTkLabel(
            info_frame,
            text="Event Log:",
            font=Theme.get_font(Theme.FONT_BASE, "bold"),
            text_color=Theme.PRIMARY_DARK,
            fg_color=Theme.WHITE
        )
        log_title.pack(pady=(20, 5), padx=20, anchor="w")
        
        # Log text area with scrollbar - using CTkTextbox
        self.log_text = ctk.CTkTextbox(
            info_frame,
            height=200,
            width=260,
            font=Theme.get_font(12),
            fg_color="#f9fafb",
            text_color=Theme.BLACK,
            wrap="word",
            activate_scrollbars=True
        )
        self.log_text.pack(pady=5, padx=20, fill="both", expand=True)
        
        # Add clear log button
        clear_btn = ctk.CTkButton(
            info_frame,
            text="Clear Log",
            command=lambda: self.log_text.delete("1.0", tk.END),
            font=Theme.get_font(Theme.FONT_BASE),
            text_color=Theme.WHITE,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_DARK
        )
        clear_btn.pack(pady=(5, 10), padx=20, anchor="e")
        
        # Redirect print statements to the log
        self.setup_print_redirect()
        
        # Separator - CTk doesn't have built-in separators, so create a thin frame
        separator = ctk.CTkFrame(
            main_container,
            width=1,
            fg_color=Theme.BLACK,
            corner_radius=0
        )
        separator.pack(side="left", fill="y")
        
        # Right side - Component test area with dark background for contrast
        test_frame = ctk.CTkFrame(
            main_container, 
            fg_color=Theme.PRIMARY_DARK,
            corner_radius=0
        )
        test_frame.pack(side="left", fill="both", expand=True)
        
        # Create content frame for test controller
        self.content_frame = ctk.CTkFrame(
            test_frame, 
            fg_color=Theme.WHITE,
            corner_radius=0
        )
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Create test controller to handle navigation
        self.controller = TestController(self.content_frame)
        self.controller.create_test_frames()
        
        # Create the sidebar component
        self.sidebar = SideBar(test_frame, controller=self.controller)
        self.sidebar.pack(side="left", fill="y")
        
        # Show default screen
        self.controller.show_frame("dashboard")
        
        # Log startup information
        print("SideBar test application started")
        print("Try clicking on the sidebar icons to navigate between screens")
        
    def setup_print_redirect(self):
        """Redirect print statements to the log text widget"""
        class PrintRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget
            
            def write(self, string):
                self.text_widget.insert("end", string)
                self.text_widget.see("end")  # Auto-scroll to end
            
            def flush(self):
                pass
        
        # Redirect stdout to our text widget
        self.original_stdout = sys.stdout
        sys.stdout = PrintRedirector(self.log_text)
    
    def on_closing(self):
        """Restore stdout and close application"""
        # Restore original stdout
        sys.stdout = self.original_stdout
        self.root.destroy()


def main():
    try:
        # Set appearance mode and default color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Initialize customtkinter window
        root = ctk.CTk()
        
        # Create the application
        app = SideBarTester(root)
        
        # Handle window close properly
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Start the application
        root.mainloop()
    except Exception as e:
        # If we get here, restore stdout before printing the error
        if 'app' in locals() and hasattr(app, 'original_stdout'):
            sys.stdout = app.original_stdout
        print(f"Error in SideBar test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()