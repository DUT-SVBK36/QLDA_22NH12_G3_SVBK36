import sys
import os
import tkinter as tk
from tkinter import ttk

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
            # Create frame with a temporary background color
            frame = tk.Frame(self.content_frame, bg=Theme.WHITE)
            frame.pack_propagate(False)
            
            # We need to make the frame visible briefly to get its dimensions
            frame.pack(fill="both", expand=True)
            self.content_frame.update_idletasks()
            
            # Apply gradient background
            Gradient.apply_gradient_to_widget(
                frame,
                config["gradient_colors"],
                gradient_type="linear",
                direction="vertical"
            )
            
            # Hide the frame for now (will be shown when selected)
            frame.pack_forget()
            
            # Store gradient images to prevent garbage collection
            frame.gradient_img = frame.gradient_img  # Reference created by apply_gradient_to_widget
            
            # Add a title - use a frame to make it stand out from the gradient
            title_frame = tk.Frame(frame, bg=Theme.WHITE, bd=1, relief="solid")
            title_frame.pack(pady=(30, 0), padx=20, anchor="nw", fill="x")
            
            title = tk.Label(
                title_frame, 
                text=config["title"],
                font=Theme.get_font(Theme.FONT_2XL, "bold"),
                bg=Theme.WHITE,
                fg=Theme.PRIMARY_DARK,
                pady=10,
                padx=10
            )
            title.pack(anchor="w")
            
            # Add content with a semi-transparent background
            content_frame = tk.Frame(frame, bg=Theme.WHITE, bd=0)
            content_frame.pack(pady=20, padx=20, anchor="nw", fill="x")
            
            content = tk.Label(
                content_frame,
                text=f"This is the {name} screen content area with a vertical gradient background.",
                font=Theme.get_font(Theme.FONT_LG),
                bg=Theme.WHITE,
                fg=Theme.BLACK,
                justify="left",
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
        main_container = tk.Frame(self.root, bg=Theme.WHITE)
        main_container.pack(fill="both", expand=True)
        
        # Left side - Test information
        info_frame = tk.Frame(main_container, bg=Theme.WHITE, width=300)
        info_frame.pack(side="left", fill="y")
        info_frame.pack_propagate(False)
        
        # Test title
        title = tk.Label(
            info_frame, 
            text="SideBar Component Test",
            font=Theme.get_font(Theme.FONT_XL, "bold"),
            bg=Theme.WHITE,
            fg=Theme.PRIMARY_DARK
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
        
        desc_label = tk.Label(
            info_frame,
            text=description,
            font=Theme.get_font(Theme.FONT_BASE),
            bg=Theme.WHITE,
            fg=Theme.BLACK,
            justify="left",
            wraplength=260
        )
        desc_label.pack(pady=10, padx=20, anchor="w")
        
        # Add event log section
        log_title = tk.Label(
            info_frame,
            text="Event Log:",
            font=Theme.get_font(Theme.FONT_BASE, "bold"),
            bg=Theme.WHITE,
            fg=Theme.PRIMARY_DARK
        )
        log_title.pack(pady=(20, 5), padx=20, anchor="w")
        
        # Log text area with scrollbar
        log_frame = tk.Frame(info_frame, bg=Theme.WHITE)
        log_frame.pack(pady=5, padx=20, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.log_text = tk.Text(
            log_frame,
            height=10,
            width=30,
            wrap="word",
            font=Theme.get_font(12),
            bg="#f9fafb",
            fg=Theme.BLACK
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        
        # Connect scrollbar to text
        scrollbar.config(command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # Redirect print statements to the log
        self.setup_print_redirect()
        
        # Separator
        separator = ttk.Separator(main_container, orient="vertical")
        separator.pack(side="left", fill="y")
        
        # Right side - Component test area with dark background for contrast
        test_frame = tk.Frame(main_container, bg=Theme.PRIMARY_DARK)
        test_frame.pack(side="left", fill="both", expand=True)
        
        # Create sidebar
        self.content_frame = tk.Frame(test_frame, bg=Theme.WHITE)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Create test controller to handle navigation
        self.controller = TestController(self.content_frame)
        self.controller.create_test_frames()
        
        # Create the sidebar component
        self.sidebar = SideBar(test_frame, controller=self.controller)
        self.sidebar.pack(side="left", fill="y")
        
        # Show default screen
        self.controller.show_frame("dashboard")
        
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
        root = tk.Tk()
        app = SideBarTester(root)
        
        # Handle window close properly
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Start the application
        root.mainloop()
    except Exception as e:
        # If we get here, restore stdout before printing the error
        if hasattr(app, 'original_stdout'):
            sys.stdout = app.original_stdout
        print(f"Error in SideBar test: {e}")


if __name__ == "__main__":
    main()