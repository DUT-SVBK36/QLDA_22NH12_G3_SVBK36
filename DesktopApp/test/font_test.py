import sys
import os
import tkinter as tk
from tkinter import ttk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config.theme import Theme
from _config.font_manager import FontManager

"""
Test script to display and verify the different font sizes and styles
defined in the theme.py configuration.
"""

class FontTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Font Test - Theme Configuration")
        self.root.geometry("800x600")
        self.root.configure(bg=Theme.WHITE)
        
        # Handle window close event properly
        self.setup_close_handlers()
        
        try:
            # Now that we have a root window, register fonts if needed
            FontManager._register_fonts_now()
            print("Fonts registered successfully!")
        except Exception as e:
            print(f"Error registering fonts: {e}")
        
        self.create_widgets()
    
    def setup_close_handlers(self):
        """Setup handlers for proper application exit"""
        def on_closing():
            print("Application closing...")
            # Clean up any resources
            if hasattr(FontManager, '_temp_root') and FontManager._temp_root:
                try:
                    FontManager._temp_root.destroy()
                except:
                    pass
            
            # Destroy main window and exit
            self.root.destroy()
            sys.exit(0)
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        Theme.apply_style(main_frame, Theme.frame_default())
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        title = tk.Label(main_frame, text="Font Size Test", font=("Arial", 24, "bold"))  # Use system font initially
        title.configure(bg=Theme.WHITE, fg=Theme.BLACK)
        title.pack(pady=10)
        
        # Show font info
        font_info_frame = tk.Frame(main_frame, bg=Theme.WHITE)
        font_info_frame.pack(fill="x", pady=5)
        
        # Safely check font availability
        try:
            is_available = FontManager.is_font_available(Theme.FONT_FAMILY)
            font_status = f"Font '{Theme.FONT_FAMILY}' is {'available' if is_available else 'NOT available'}"
        except Exception as e:
            font_status = f"Error checking font availability: {e}"
            is_available = False
        
        font_info = tk.Label(
            font_info_frame, 
            text=font_status,
            bg=Theme.WHITE,
            fg="green" if is_available else "red",
            font=("Arial", 12)  # Use system font
        )
        font_info.pack(anchor="w", pady=5)
        
        # Font sizes test - use system fonts first
        sizes = [
            ("FONT_BASE (16px)", 16),
            ("FONT_LG (22px)", 22),
            ("FONT_XL (24px)", 24),
            ("FONT_2XL (30px)", 30),
            ("FONT_3XL (36px)", 36)
        ]
        
        for name, size in sizes:
            frame = tk.Frame(main_frame, bg=Theme.WHITE)
            frame.pack(fill="x", pady=5)
            
            # Size label
            size_label = tk.Label(
                frame, 
                text=name,
                width=20, 
                anchor="w",
                bg=Theme.WHITE,
                fg=Theme.BLACK,
                font=("Arial", 12)  # Use system font
            )
            size_label.pack(side="left", padx=10)
            
            # Try to use theme font, but fallback safely
            try:
                font_tuple = Theme.get_font(size)
            except Exception:
                font_tuple = ("Arial", size)
            
            # Example text with the font size
            example = tk.Label(
                frame, 
                text="The quick brown fox jumps over the lazy dog", 
                bg=Theme.WHITE,
                fg=Theme.BLACK,
                font=font_tuple
            )
            example.pack(side="left", padx=10)
        
        # Add a button to quit the application safely
        quit_btn = tk.Button(
            main_frame,
            text="Close",
            command=lambda: self.root.protocol("WM_DELETE_WINDOW")(),
            bg=Theme.PRIMARY,
            fg=Theme.WHITE,
            font=("Arial", 12)
        )
        quit_btn.pack(pady=20)

def main():
    try:
        # Create application
        root = tk.Tk()
        app = FontTestApp(root)
        
        # Start application mainloop
        print("Starting mainloop...")
        root.mainloop()
        
        # After mainloop exits
        print("Mainloop exited normally")
        
    except Exception as e:
        print(f"Critical error in application: {e}")
        # If we have a root window, show error in a message box
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Application error: {e}")
        except:
            pass
    
    # Make sure we exit cleanly
    print("Application exiting...")
    sys.exit(0)

if __name__ == "__main__":
    main()