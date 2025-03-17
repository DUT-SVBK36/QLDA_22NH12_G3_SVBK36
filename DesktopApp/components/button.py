import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import sys
import os

# Add root directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config.theme import Theme

class ModernButton(ctk.CTkButton):
    """
    A modern-looking button component using customtkinter for better appearance.
    
    Features:
    - Rounded corners with customizable radius
    - Hover effects (lighten/darken)
    - Optional icon support
    - Different sizes (small, medium, large)
    - Various color variants based on the application theme
    """
    
    # Size presets (width, height, font_size, padding_x, padding_y)
    SIZES = {
        "xs": (120, 28, Theme.FONT_XS, 12, 4),  # Changed None to fixed width
        "sm": (120, 36, Theme.FONT_SM, 16, 6),  # Changed None to fixed width
        "md": (120, 44, Theme.FONT_BASE, 20, 8),  # Changed None to fixed width
        "lg": (120, 52, Theme.FONT_LG, 24, 10),  # Changed None to fixed width
        "xl": (120, 60, Theme.FONT_XL, 28, 12),  # Changed None to fixed width
    }
    
    # Color variants
    VARIANTS = {
        "primary": {
            "bg": Theme.PRIMARY,
            "fg": Theme.WHITE,
            "hover_bg": "#c5c0f3",  # Lighter version of PRIMARY
            "active_bg": "#a9a2f0"  # Darker version of PRIMARY
        },
        "secondary": {
            "bg": Theme.SECONDARY,
            "fg": Theme.WHITE,
            "hover_bg": "#fdc3ed",  # Lighter version of SECONDARY
            "active_bg": "#fca5e7"  # Darker version of SECONDARY
        },
        "tertiary": {
            "bg": Theme.TERTIARY,
            "fg": Theme.BLACK,
            "hover_bg": "#ffe5d9",  # Lighter version of TERTIARY
            "active_bg": "#ffd2b8"  # Darker version of TERTIARY
        },
        "quaternary": {
            "bg": Theme.QUARTERNARY,
            "fg": Theme.BLACK,
            "hover_bg": "#fcf5c8",  # Lighter version of QUATERNARY
            "active_bg": "#f8efa0"  # Darker version of QUATERNARY
        },
        "dark": {
            "bg": Theme.PRIMARY_DARK,
            "fg": Theme.WHITE,
            "hover_bg": "#3a3e5c",  # Lighter version of PRIMARY_DARK
            "active_bg": "#232538"  # Darker version of PRIMARY_DARK
        },
        "outline": {
            "bg": Theme.WHITE,
            "fg": Theme.PRIMARY,
            "hover_bg": "#f8f8ff",  # Very light purple
            "active_bg": "#f0f0ff",  # Light purple
            "border_color": Theme.PRIMARY,
            "border_width": 1
        },
        "ghost": {
            "bg": "transparent",  # Using CTk's transparent option
            "fg": Theme.PRIMARY,
            "hover_bg": "#f8f8ff",  # Very light purple
            "active_bg": "#f0f0ff",  # Light purple
            "border_color": Theme.WHITE  # Using white instead of transparent for border
        }
    }
    
    def __init__(
        self, 
        master, 
        text="Button", 
        command=None, 
        size="md", 
        variant="primary", 
        icon=None,
        icon_position="left",
        width=None,
        height=None,
        corner_radius=None,
        **kwargs
    ):
        """
        Initialize a modern button
        
        Args:
            master: The parent widget
            text: Button text
            command: Function to call when button is clicked
            size: Button size ("xs", "sm", "md", "lg", or "xl")
            variant: Button color variant ("primary", "secondary", "tertiary", "quaternary", "dark", "outline", "ghost")
            icon: Optional image to display in the button
            icon_position: Position of the icon ("left" or "right")
            width: Optional custom width (overrides size preset)
            height: Optional custom height (overrides size preset)
            corner_radius: Custom corner radius (defaults to ROUNDED_4)
            **kwargs: Additional options to pass to the Button widget
        """
        # Validate size and variant
        if size not in self.SIZES:
            size = "md"  # Default to medium
        
        if variant not in self.VARIANTS:
            variant = "primary"  # Default to primary
            
        # Store size and variant for later
        self.size = size
        self.variant_name = variant
        self.variant = self.VARIANTS[variant]
        self.corner_radius = corner_radius if corner_radius is not None else Theme.ROUNDED_4
        
        # Get size configuration
        size_config = self.SIZES[size]
        self.font_size = size_config[2]
        
        # Set dimensions
        if width is None:
            width = size_config[0]
        if height is None:
            height = size_config[1]
            
        # Determine border properties for outline variant
        border_width = self.variant.get("border_width", 0)
        border_color = self.variant.get("border_color", None)
        
        # Handle transparent background for ghost variant
        fg_color = self.variant["bg"]
        if fg_color == "transparent":
            # Use CTkButton's None value for transparent background
            fg_color = None
        
        # Prepare image and position
        self.icon = icon
        self.icon_position = icon_position
        
        # Initialize customtkinter Button
        super().__init__(
            master,
            text=text,
            command=command,
            fg_color=fg_color,  # Use fg_color variable
            text_color=self.variant["fg"],
            hover_color=self.variant["hover_bg"],
            corner_radius=self.corner_radius,
            border_width=border_width,
            border_color=border_color if border_color else self.variant.get("border_color", Theme.WHITE),
            width=width,
            height=height,
            font=(Theme.FONT_FAMILY, self.font_size),
            image=icon,
            compound="left" if icon_position == "left" else "right" if icon else None,
            **kwargs
        )
        
        # Store properties
        self.text_value = text
        
    def update_size(self, size):
        """Update the button size"""
        if size not in self.SIZES:
            return
            
        if size == self.size:
            return  # No change needed
            
        # Get new size configuration
        self.size = size
        size_config = self.SIZES[size]
        self.font_size = size_config[2]
        
        # Update button properties
        self.configure(
            font=(Theme.FONT_FAMILY, self.font_size),
            height=size_config[1]
        )
        
    def configure(self, **kw):
        """Update button configuration"""
        # Handle special configurations
        if "text" in kw:
            self.text_value = kw["text"]
            
        if "icon" in kw:
            self.icon = kw.pop("icon")
            if self.icon:
                compound = "left" if self.icon_position == "left" else "right"
                super().configure(image=self.icon, compound=compound)
            else:
                super().configure(image=None, compound=None)
                
        if "icon_position" in kw:
            self.icon_position = kw.pop("icon_position")
            if self.icon:
                compound = "left" if self.icon_position == "left" else "right"
                super().configure(compound=compound)
                
        if "variant" in kw:
            variant = kw.pop("variant")
            if variant in self.VARIANTS:
                self.variant_name = variant
                self.variant = self.VARIANTS[variant]
                
                # Handle transparent background
                if self.variant["bg"] == "transparent":
                    kw["fg_color"] = None  # None means transparent in CustomTkinter
                else:
                    kw["fg_color"] = self.variant["bg"]
                
                kw["text_color"] = self.variant["fg"]
                kw["hover_color"] = self.variant["hover_bg"]
                
                # Handle border for outline variant
                if "border_width" in self.variant:
                    kw["border_width"] = self.variant["border_width"]
                    kw["border_color"] = self.variant.get("border_color", Theme.WHITE)
                else:
                    kw["border_width"] = 0
        
        # Pass remaining configs to CTkButton
        super().configure(**kw)
    
    def disable(self):
        """Disable the button"""
        self.configure(state="disabled")
    
    def enable(self):
        """Enable the button"""
        self.configure(state="normal")
        

class ButtonFactory:
    """Factory class to create different button styles easily"""
    
    @staticmethod
    def create_primary_button(master, text, command=None, size="md", **kwargs):
        """Create a primary button"""
        return ModernButton(master, text=text, command=command, size=size, variant="primary", **kwargs)
    
    @staticmethod
    def create_secondary_button(master, text, command=None, size="md", **kwargs):
        """Create a secondary button"""
        return ModernButton(master, text=text, command=command, size=size, variant="secondary", **kwargs)
        
    @staticmethod
    def create_tertiary_button(master, text, command=None, size="md", **kwargs):
        """Create a tertiary button"""
        return ModernButton(master, text=text, command=command, size=size, variant="tertiary", **kwargs)
        
    @staticmethod
    def create_quaternary_button(master, text, command=None, size="md", **kwargs):
        """Create a quaternary button"""
        return ModernButton(master, text=text, command=command, size=size, variant="quaternary", **kwargs)
    
    @staticmethod
    def create_dark_button(master, text, command=None, size="md", **kwargs):
        """Create a dark button"""
        return ModernButton(master, text=text, command=command, size=size, variant="dark", **kwargs)
    
    @staticmethod
    def create_outline_button(master, text, command=None, size="md", **kwargs):
        """Create an outline button"""
        return ModernButton(master, text=text, command=command, size=size, variant="outline", **kwargs)
    
    @staticmethod
    def create_ghost_button(master, text, command=None, size="md", **kwargs):
        """Create a ghost button"""
        return ModernButton(master, text=text, command=command, size=size, variant="ghost", **kwargs)


# Function to set CustomTkinter appearance mode
def initialize_button_styles():
    """Initialize button appearance mode for the application"""
    # Set the appearance mode and default color theme
    ctk.set_appearance_mode("light")  # Options: "light", "dark", "system"
    ctk.set_default_color_theme("blue")  # Options: "blue", "dark-blue", "green"