import tkinter as tk
from _config.theme import Theme

class App:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        
        # Track window resizing
        self.root.bind("<Configure>", self.on_resize)
        
        # Store initial size for aspect ratio calculations
        self.initial_width = self.width
        self.initial_height = self.height

    def setup_window(self):
        # Configure the root window
        self.root.title("BPD Desktop App")
        
        # Set 16:9 aspect ratio dimensions
        self.width = 1280
        self.height = 720
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        
        # Set initial geometry
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Set minimum size
        self.root.minsize(640, 360)  # Half of 1280x720, maintains 16:9
        
        # Allow resizing
        self.root.resizable(True, True)

    def create_widgets(self):
        # Create a master frame to maintain border and padding
        self.master_frame = tk.Frame(
            self.root,
            bg=Theme.PRIMARY_DARK,  # Border color
            padx=2,  # Border thickness
            pady=2   # Border thickness
        )
        self.master_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create inner content frame
        self.content_frame = tk.Frame(self.master_frame, bg=Theme.WHITE)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Set the background image from theme
        self.bg_label = Theme.set_app_background(self.content_frame)
        
        # Add a welcome message
        self.welcome_label = tk.Label(
            self.content_frame,
            text="16:9 Responsive Window",
            font=Theme.get_font(Theme.FONT_2XL, "bold"),
            bg=Theme.PRIMARY,
            fg=Theme.WHITE,
            padx=20,
            pady=10,
            relief="flat"
        )
        self.welcome_label.place(relx=0.5, rely=0.3, anchor="center")
        
        # Add info text
        self.info_label = tk.Label(
            self.content_frame,
            text="Resize the window while maintaining 16:9 aspect ratio",
            font=Theme.get_font(Theme.FONT_BASE),
            bg=Theme.WHITE,
            fg=Theme.BLACK
        )
        self.info_label.place(relx=0.5, rely=0.4, anchor="center")
        
        # Add resize indicator
        self.size_label = tk.Label(
            self.content_frame,
            text=f"Window size: {self.width}x{self.height}",
            font=Theme.get_font(Theme.FONT_BASE),
            bg=Theme.WHITE,
            fg=Theme.PRIMARY_DARK
        )
        self.size_label.place(relx=0.5, rely=0.5, anchor="center")

    def on_resize(self, event):
        # Only process if this is the root window
        if event.widget == self.root:
            # Get new dimensions
            new_width = event.width
            new_height = event.height
            
            # Update size label
            self.size_label.config(text=f"Window size: {new_width}x{new_height}")
            
            # Enforce 16:9 aspect ratio if significantly different
            # (allowing small deviations for window borders)
            aspect_ratio = new_width / new_height
            target_ratio = 16 / 9
            
            # Only enforce if the difference is significant (>5%)
            if abs(aspect_ratio - target_ratio) > 0.05:
                if aspect_ratio > target_ratio:
                    # Too wide, adjust height
                    adjusted_height = int(new_width / target_ratio)
                    self.root.geometry(f"{new_width}x{adjusted_height}")
                else:
                    # Too tall, adjust width
                    adjusted_width = int(new_height * target_ratio)
                    self.root.geometry(f"{adjusted_width}x{new_height}")
                
                # Prevent immediate re-triggering
                self.root.after(100, lambda: None)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()