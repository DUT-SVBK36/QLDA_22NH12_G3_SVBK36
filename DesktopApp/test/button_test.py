import os
import sys
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw

# Add root directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.button import ModernButton, ButtonFactory, initialize_button_styles
from _config.theme import Theme

class ButtonTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Button Test")
        self.root.geometry("900x700")
        
        # Initialize button styles
        initialize_button_styles()
        
        # Create a main container frame
        self.container = ctk.CTkFrame(root, fg_color=Theme.WHITE)
        self.container.pack(fill="both", expand=True)
        
        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.container, fg_color=Theme.WHITE)
        self.scrollable_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Add header
        self.create_header()
        
        # Create sections
        self.create_variants_section()
        self.create_sizes_section()
        self.create_radius_section()
        self.create_interaction_section()
        self.create_icon_section()
        
    def create_header(self):
        """Create header with title and description"""
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=Theme.WHITE)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Modern Button Component Test",
            text_color=Theme.PRIMARY_DARK,
            font=(Theme.FONT_FAMILY, Theme.FONT_2XL, "bold")
        )
        title.pack(anchor="w")
        
        description = ctk.CTkLabel(
            header_frame,
            text="This test demonstrates the various features of the ModernButton component.",
            text_color=Theme.BLACK,
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE),
            wraplength=800,
            justify="left"
        )
        description.pack(anchor="w", pady=(5, 0))
    
    def create_section(self, title):
        """Create a section with title"""
        section_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=Theme.WHITE)
        section_frame.pack(fill="x", pady=(20, 10), anchor="w")
        
        section_title = ctk.CTkLabel(
            section_frame,
            text=title,
            text_color=Theme.PRIMARY_DARK,
            font=(Theme.FONT_FAMILY, Theme.FONT_LG, "bold")
        )
        section_title.pack(anchor="w")
        
        content_frame = ctk.CTkFrame(section_frame, fg_color=Theme.WHITE)
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
        
        # Fix: Create a frame to hold all buttons
        buttons_frame = ctk.CTkFrame(content_frame, fg_color=Theme.WHITE)
        buttons_frame.pack(fill="x")
        
        for variant in variants:
            button_frame = ctk.CTkFrame(buttons_frame, fg_color=Theme.WHITE)
            button_frame.pack(side="left", padx=10, pady=5)
            
            # Create button with width parameter to fix scaling issue
            button = ModernButton(
                button_frame,
                text=variant["name"],
                command=lambda v=variant["name"]: self.show_message(f"{v} button clicked"),
                variant=variant["variant"],
                width=120  # Fixed width instead of None
            )
            button.pack(pady=5)
            
            # Add label
            label = ctk.CTkLabel(
                button_frame,
                text=variant["variant"],
                text_color=Theme.BLACK,
                font=(Theme.FONT_FAMILY, Theme.FONT_SM)
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
        
        # Fix: Create a frame to hold all buttons
        buttons_frame = ctk.CTkFrame(content_frame, fg_color=Theme.WHITE)
        buttons_frame.pack(fill="x")
        
        for size_info in sizes:
            button_frame = ctk.CTkFrame(buttons_frame, fg_color=Theme.WHITE)
            button_frame.pack(side="left", padx=10, pady=5)
            
            # Create button with width parameter
            button = ModernButton(
                button_frame,
                text=size_info["name"],
                command=lambda s=size_info["name"]: self.show_message(f"{s} button clicked"),
                size=size_info["size"],
                width=120  # Fixed width instead of None
            )
            button.pack(pady=5)
            
            # Add label
            label = ctk.CTkLabel(
                button_frame,
                text=size_info["size"],
                text_color=Theme.BLACK,
                font=(Theme.FONT_FAMILY, Theme.FONT_SM)
            )
            label.pack()
    
    def create_radius_section(self):
        """Create corner radius section"""
        content_frame = self.create_section("Corner Radius Options")
        
        description = ctk.CTkLabel(
            content_frame,
            text="CustomTkinter supports corner radius natively.",
            text_color=Theme.BLACK,
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE),
            wraplength=800,
            justify="left"
        )
        description.pack(anchor="w", pady=(0, 10))
        
        # Define corner radius options
        radius_options = [
            {"name": "No Radius", "radius": 0},
            {"name": "Small", "radius": 4},
            {"name": "Medium", "radius": 8},
            {"name": "Large", "radius": 16},
            {"name": "Pill", "radius": 22}
        ]
        
        # Fix: Create a frame to hold all buttons
        buttons_frame = ctk.CTkFrame(content_frame, fg_color=Theme.WHITE)
        buttons_frame.pack(fill="x")
        
        for radius in radius_options:
            button_frame = ctk.CTkFrame(buttons_frame, fg_color=Theme.WHITE)
            button_frame.pack(side="left", padx=10, pady=5)
            
            # Create button with width parameter
            button = ModernButton(
                button_frame,
                text=radius["name"],
                corner_radius=radius["radius"],
                width=120  # Fixed width instead of None
            )
            button.pack(pady=5)
            
            # Add label
            label = ctk.CTkLabel(
                button_frame,
                text=f"radius={radius['radius']}",
                text_color=Theme.BLACK,
                font=(Theme.FONT_FAMILY, Theme.FONT_SM)
            )
            label.pack()
    
    def create_interaction_section(self):
        """Create interactive section to demonstrate button functionality"""
        content_frame = self.create_section("Interactive Test")
        
        # Create a frame for the counter demo
        counter_frame = ctk.CTkFrame(content_frame, fg_color=Theme.WHITE)
        counter_frame.pack(pady=10, fill="x")
        
        # Counter display
        self.counter = 0
        self.counter_label = ctk.CTkLabel(
            counter_frame,
            text=f"Counter: {self.counter}",
            text_color=Theme.BLACK,
            font=(Theme.FONT_FAMILY, Theme.FONT_LG)
        )
        self.counter_label.pack(side="left", padx=(0, 20))
        
        # Increment button
        increment_button = ButtonFactory.create_primary_button(
            counter_frame,
            text="Increment",
            command=self.increment_counter,
            width=100  # Fixed width
        )
        increment_button.pack(side="left", padx=5)
        
        # Decrement button
        decrement_button = ButtonFactory.create_outline_button(
            counter_frame,
            text="Decrement",
            command=self.decrement_counter,
            width=100  # Fixed width
        )
        decrement_button.pack(side="left", padx=5)
        
        # Reset button
        reset_button = ButtonFactory.create_secondary_button(
            counter_frame,
            text="Reset",
            command=self.reset_counter,
            width=100  # Fixed width
        )
        reset_button.pack(side="left", padx=5)
        
        # Create a frame for the disabled button demo
        disabled_frame = ctk.CTkFrame(content_frame, fg_color=Theme.WHITE)
        disabled_frame.pack(pady=(20, 10), fill="x")
        
        # Disabled button demo
        self.toggle_button = ModernButton(
            disabled_frame,
            text="Enabled Button",
            command=lambda: self.show_message("Button clicked!"),
            width=120  # Fixed width
        )
        self.toggle_button.pack(side="left", padx=(0, 20))
        
        # Toggle enable/disable button
        toggle_state_button = ButtonFactory.create_dark_button(
            disabled_frame,
            text="Toggle Enabled/Disabled",
            command=self.toggle_button_state,
            width=160  # Fixed width
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
            
            # Convert for CustomTkinter
            self.icon = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(icon_size, icon_size))
            
            # Icon on left
            left_icon_button = ModernButton(
                content_frame,
                text="Left Icon",
                icon=self.icon,
                icon_position="left",
                width=120  # Fixed width
            )
            left_icon_button.pack(side="left", padx=10)
            
            # Icon on right
            right_icon_button = ModernButton(
                content_frame,
                text="Right Icon",
                icon=self.icon,
                icon_position="right",
                width=120  # Fixed width
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
            error_label = ctk.CTkLabel(
                content_frame,
                text=f"Error creating icons: {e}",
                text_color="#ff0000",
                font=(Theme.FONT_FAMILY, Theme.FONT_SM)
            )
            error_label.pack()
    
    def increment_counter(self):
        """Increment the counter and update display"""
        self.counter += 1
        self.counter_label.configure(text=f"Counter: {self.counter}")
        
    def decrement_counter(self):
        """Decrement the counter and update display"""
        self.counter -= 1
        self.counter_label.configure(text=f"Counter: {self.counter}")
        
    def reset_counter(self):
        """Reset the counter and update display"""
        self.counter = 0
        self.counter_label.configure(text=f"Counter: {self.counter}")
        
    def toggle_button_state(self):
        """Toggle the state of the demo button between enabled and disabled"""
        if self.toggle_button.cget('state') == "disabled":
            self.toggle_button.enable()
            self.toggle_button.configure(text="Enabled Button")
        else:
            self.toggle_button.disable()
            self.toggle_button.configure(text="Disabled Button")
    
    def show_message(self, message):
        """Show a message (would typically use a proper notification system)"""
        print(message)


if __name__ == "__main__":
    # Initialize CustomTkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    app = ButtonTestApp(root)
    root.mainloop()