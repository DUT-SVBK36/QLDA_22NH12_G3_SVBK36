import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

# Add root directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.button import ModernButton, ButtonFactory
from _config.theme import Theme

class ButtonTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Button Test")
        self.root.geometry("900x700")
        self.root.configure(bg=Theme.WHITE)
        
        # Create a main container frame
        self.container = tk.Frame(root, bg=Theme.WHITE)
        self.container.pack(fill="both", expand=True)
        
        # Create canvas with scrollbar for scrolling
        self.canvas = tk.Canvas(self.container, bg=Theme.WHITE, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create main frame with padding inside the canvas
        self.main_frame = tk.Frame(self.canvas, bg=Theme.WHITE, padx=30, pady=30)
        
        # Create window in the canvas to contain the main frame
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configure canvas to scroll with mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Add header
        self.create_header()
        
        # Create sections
        self.create_variants_section()
        self.create_sizes_section()
        self.create_radius_section()
        self.create_interaction_section()
        self.create_icon_section()
        
        # Update window and canvas scrollregion after layout
        self.main_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
        # Bind canvas resize event
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def _on_canvas_resize(self, event):
        """Handle canvas resize to adjust the inner frame width"""
        # Update the width of the window to fill the canvas
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        
    def create_header(self):
        """Create header with title and description"""
        header_frame = tk.Frame(self.main_frame, bg=Theme.WHITE)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(
            header_frame,
            text="Modern Button Component Test",
            font=Theme.get_font(Theme.FONT_2XL, "bold"),
            fg=Theme.PRIMARY_DARK,
            bg=Theme.WHITE
        )
        title.pack(anchor="w")
        
        description = tk.Label(
            header_frame,
            text="This test demonstrates the various features of the ModernButton component.",
            font=Theme.get_font(Theme.FONT_BASE),
            fg=Theme.BLACK,
            bg=Theme.WHITE,
            wraplength=800,
            justify="left"
        )
        description.pack(anchor="w", pady=(5, 0))
    
    def create_section(self, title):
        """Create a section with title"""
        section_frame = tk.Frame(self.main_frame, bg=Theme.WHITE)
        section_frame.pack(fill="x", pady=(20, 10), anchor="w")
        
        section_title = tk.Label(
            section_frame,
            text=title,
            font=Theme.get_font(Theme.FONT_LG, "bold"),
            fg=Theme.PRIMARY_DARK,
            bg=Theme.WHITE
        )
        section_title.pack(anchor="w")
        
        content_frame = tk.Frame(section_frame, bg=Theme.WHITE)
        content_frame.pack(fill="x", pady=(10, 0))
        
        return content_frame
    
    def create_variants_section(self):
        """Create button variants section"""
        content_frame = self.create_section("Button Variants")
        
        # Create buttons for each variant
        variants = [
            {"name": "Primary", "variant": "primary"},
            {"name": "Secondary", "variant": "secondary"},
            {"name": "Tertiary", "variant": "tertiary"},
            {"name": "Quaternary", "variant": "quaternary"},
            {"name": "Dark", "variant": "dark"},
            {"name": "Outline", "variant": "outline"},
            {"name": "Ghost", "variant": "ghost"}
        ]
        
        for variant in variants:
            button_frame = tk.Frame(content_frame, bg=Theme.WHITE)
            button_frame.pack(side="left", padx=10, pady=5)
            
            # Create button
            button = ModernButton(
                button_frame,
                text=variant["name"],
                command=lambda v=variant["name"]: self.show_message(f"{v} button clicked"),
                variant=variant["variant"]
            )
            button.pack(pady=5)
            
            # Add label
            label = tk.Label(
                button_frame,
                text=variant["variant"],
                font=Theme.get_font(Theme.FONT_BASE-2),
                fg=Theme.BLACK,
                bg=Theme.WHITE
            )
            label.pack()
    
    def create_sizes_section(self):
        """Create button sizes section"""
        content_frame = self.create_section("Button Sizes")
        
        sizes = [
            {"name": "Extra Small", "size": "xs"},
            {"name": "Small", "size": "sm"},
            {"name": "Medium", "size": "md"},
            {"name": "Large", "size": "lg"},
            {"name": "Extra Large", "size": "xl"}
        ]
        
        for size_info in sizes:
            button_frame = tk.Frame(content_frame, bg=Theme.WHITE)
            button_frame.pack(side="left", padx=10, pady=5)
            
            # Create button
            button = ModernButton(
                button_frame,
                text=size_info["name"],
                command=lambda s=size_info["name"]: self.show_message(f"{s} button clicked"),
                size=size_info["size"]
            )
            button.pack(pady=5)
            
            # Add label
            label = tk.Label(
                button_frame,
                text=size_info["size"],
                font=Theme.get_font(Theme.FONT_BASE-2),
                fg=Theme.BLACK,
                bg=Theme.WHITE
            )
            label.pack()
    
    def create_radius_section(self):
        """Create corner radius section"""
        content_frame = self.create_section("Corner Radius Options")
        
        # Define corner radius options
        radius_options = [
            {"name": "No Radius", "radius": 0},
            {"name": "Small", "radius": 4},
            {"name": "Medium", "radius": 8},
            {"name": "Large", "radius": 16},
            {"name": "Pill", "radius": 22}
        ]
        
        for radius in radius_options:
            button_frame = tk.Frame(content_frame, bg=Theme.WHITE)
            button_frame.pack(side="left", padx=10, pady=5)
            
            # Create button
            button = ModernButton(
                button_frame,
                text=radius["name"],
                corner_radius=radius["radius"]
            )
            button.pack(pady=5)
            
            # Add label
            label = tk.Label(
                button_frame,
                text=f"radius={radius['radius']}",
                font=Theme.get_font(Theme.FONT_BASE-2),
                fg=Theme.BLACK,
                bg=Theme.WHITE
            )
            label.pack()
    
    def create_interaction_section(self):
        """Create interactive section to demonstrate button functionality"""
        content_frame = self.create_section("Interactive Test")
        
        # Create a frame for the counter demo
        counter_frame = tk.Frame(content_frame, bg=Theme.WHITE)
        counter_frame.pack(pady=10, fill="x")
        
        # Counter display
        self.counter = 0
        self.counter_label = tk.Label(
            counter_frame,
            text=f"Counter: {self.counter}",
            font=Theme.get_font(Theme.FONT_LG),
            bg=Theme.WHITE,
            fg=Theme.BLACK
        )
        self.counter_label.pack(side="left", padx=(0, 20))
        
        # Increment button
        increment_button = ButtonFactory.create_primary_button(
            counter_frame,
            text="Increment",
            command=self.increment_counter
        )
        increment_button.pack(side="left", padx=5)
        
        # Decrement button
        decrement_button = ButtonFactory.create_outline_button(
            counter_frame,
            text="Decrement",
            command=self.decrement_counter
        )
        decrement_button.pack(side="left", padx=5)
        
        # Reset button
        reset_button = ButtonFactory.create_secondary_button(
            counter_frame,
            text="Reset",
            command=self.reset_counter
        )
        reset_button.pack(side="left", padx=5)
        
        # Create a frame for the disabled button demo
        disabled_frame = tk.Frame(content_frame, bg=Theme.WHITE)
        disabled_frame.pack(pady=(20, 10), fill="x")
        
        # Disabled button demo
        self.toggle_button = ModernButton(
            disabled_frame,
            text="Enabled Button",
            command=lambda: self.show_message("Button clicked!")
        )
        self.toggle_button.pack(side="left", padx=(0, 20))
        
        # Toggle enable/disable button
        toggle_state_button = ButtonFactory.create_dark_button(
            disabled_frame,
            text="Toggle Enabled/Disabled",
            command=self.toggle_button_state
        )
        toggle_state_button.pack(side="left")
    
    def create_icon_section(self):
        """Create section to demonstrate buttons with icons"""
        content_frame = self.create_section("Buttons with Icons")
        
        try:
            # Create a simple icon for demonstration
            icon_size = 16
            icon_image = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(icon_image)
            
            # Draw a simple shape
            draw.rectangle([0, 0, icon_size, icon_size], outline=(100, 100, 255))
            draw.line([0, 0, icon_size, icon_size], fill=(100, 100, 255), width=2)
            draw.line([0, icon_size, icon_size, 0], fill=(100, 100, 255), width=2)
            
            self.icon = ImageTk.PhotoImage(icon_image)
            
            # Icon on left
            left_icon_button = ModernButton(
                content_frame,
                text="Left Icon",
                icon=self.icon,
                icon_position="left"
            )
            left_icon_button.pack(side="left", padx=10)
            
            # Icon on right
            right_icon_button = ModernButton(
                content_frame,
                text="Right Icon",
                icon=self.icon,
                icon_position="right"
            )
            right_icon_button.pack(side="left", padx=10)
            
            # Icon only (smaller button)
            icon_only_button = ModernButton(
                content_frame,
                text="",
                icon=self.icon,
                width=44,
                height=44
            )
            icon_only_button.pack(side="left", padx=10)
            
        except Exception as e:
            error_label = tk.Label(
                content_frame,
                text=f"Error creating icons: {e}",
                bg=Theme.WHITE,
                fg="red"
            )
            error_label.pack()
    
    def increment_counter(self):
        """Increment the counter and update display"""
        self.counter += 1
        self.counter_label.config(text=f"Counter: {self.counter}")
        
    def decrement_counter(self):
        """Decrement the counter and update display"""
        self.counter -= 1
        self.counter_label.config(text=f"Counter: {self.counter}")
        
    def reset_counter(self):
        """Reset the counter and update display"""
        self.counter = 0
        self.counter_label.config(text=f"Counter: {self.counter}")
        
    def toggle_button_state(self):
        """Toggle the state of the demo button between enabled and disabled"""
        if self.toggle_button.state == "disabled":
            self.toggle_button.enable()
            self.toggle_button.configure(text="Enabled Button")
        else:
            self.toggle_button.disable()
            self.toggle_button.configure(text="Disabled Button")
    
    def show_message(self, message):
        """Show a message (would typically use a proper notification system)"""
        print(message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonTestApp(root)
    root.mainloop()