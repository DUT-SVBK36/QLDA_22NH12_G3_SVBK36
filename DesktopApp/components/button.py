import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import sys
import os

# Add root directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config.theme import Theme

class ModernButton(tk.Canvas):
    """
    A modern-looking button component with rounded corners, hover effects,
    and customizable appearance based on application theme.
    
    Features:
    - Rounded corners with customizable radius
    - Hover effects (lighten/darken)
    - Optional icon support
    - Different sizes (small, medium, large)
    - Various color variants based on the application theme
    """
    
    # Size presets (width, height, font_size, padding_x, padding_y)
    SIZES = {
        "xs": (None, 28, Theme.FONT_BASE-4, 12, 4),
        "sm": (None, 36, Theme.FONT_BASE-2, 16, 6),
        "md": (None, 44, Theme.FONT_BASE, 20, 8),
        "lg": (None, 52, Theme.FONT_BASE+2, 24, 10),
        "xl": (None, 60, Theme.FONT_BASE+4, 28, 12),
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
            "bg": "",  # Transparent
            "fg": Theme.PRIMARY,
            "hover_bg": "#f8f8ff",  # Very light purple
            "active_bg": "#f0f0ff",  # Light purple
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
            icon: Optional PhotoImage to display in the button
            icon_position: Position of the icon ("left" or "right")
            width: Optional custom width (overrides size preset)
            height: Optional custom height (overrides size preset)
            corner_radius: Custom corner radius (defaults to ROUNDED_4)
            **kwargs: Additional options to pass to the Canvas widget
        """
        # Get size configuration
        if size not in self.SIZES:
            size = "md"  # Default to medium
        
        size_config = self.SIZES[size]
        btn_width = width or size_config[0]
        btn_height = height or size_config[1]
        font_size = size_config[2]
        padding_x = size_config[3]
        padding_y = size_config[4]
        
        # Calculate width if not explicitly provided
        if not btn_width:
            # Estimate text width (approximate calculation)
            text_width = len(text) * (font_size * 0.6)
            icon_width = 0
            if icon:
                # Add space for icon and padding
                icon_width = btn_height - (2 * padding_y)
                
            btn_width = int(text_width + (2 * padding_x) + icon_width + (icon_width > 0) * padding_x)
        
        # Set corner radius based on height if not specified
        self.corner_radius = corner_radius if corner_radius is not None else Theme.ROUNDED_4
        
        # Get color configuration
        if variant not in self.VARIANTS:
            variant = "primary"  # Default to primary
        
        self.variant = self.VARIANTS[variant]
        self.border_width = self.variant.get("border_width", 0)
        self.border_color = self.variant.get("border_color", "")
        
        # Store properties
        self.btn_width = btn_width
        self.btn_height = btn_height
        self.text = text
        self.command = command
        self.icon = icon
        self.icon_position = icon_position
        self.font = Theme.get_font(font_size)
        self.state = "normal"
        
        # Set up canvas with correct dimensions
        kwargs["highlightthickness"] = 0
        kwargs["bd"] = 0
        try:
            kwargs["bg"] = master["bg"]
        except (AttributeError, TypeError, tk.TclError):
            kwargs["bg"] = Theme.WHITE
        
        super().__init__(
            master, 
            width=btn_width,
            height=btn_height,
            **kwargs
        )
        
        # Initialize button appearance
        self.redraw()
        
        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        
    def redraw(self):
        """Redraw the button with current state"""
        # Clear canvas
        self.delete("all")
        
        # Determine background color based on state
        if self.state == "hover":
            bg_color = self.variant["hover_bg"]
        elif self.state == "active":
            bg_color = self.variant["active_bg"]
        else:
            bg_color = self.variant["bg"]
        
        # Draw rounded rectangle
        if bg_color:  # Only draw if we have a background (ghost buttons may not)
            # Create rounded rectangle 
            self.create_rounded_rectangle(
                0, 0, 
                self.btn_width, self.btn_height,
                self.corner_radius, 
                fill=bg_color,
                outline=self.border_color if self.border_width > 0 else "",
                width=self.border_width
            )
        
        # Calculate positions for text and icon
        if self.icon:
            # Size the icon to fit within the button height with padding
            icon_size = self.btn_height - 16  # Adjust as needed
            
            if self.icon_position == "left":
                icon_x = 10  # Left padding
                text_x = icon_x + icon_size + 8  # Space between icon and text
            else:  # right
                text_x = 10  # Left padding
                icon_x = self.btn_width - 10 - icon_size  # Right padding
            
            # Draw icon centered vertically
            icon_y = (self.btn_height - icon_size) // 2
            self.create_image(icon_x, icon_y, anchor="nw", image=self.icon)
            
            # Draw text
            text_anchor = "w" if self.icon_position == "left" else "e"
        else:
            # Center text
            text_x = self.btn_width // 2
            text_anchor = "center"
        
        # Draw text
        if text_anchor == "center":
            self.create_text(
                self.btn_width // 2,
                self.btn_height // 2,
                text=self.text, 
                fill=self.variant["fg"],
                font=self.font,
                anchor=text_anchor
            )
        else:
            self.create_text(
                text_x,
                self.btn_height // 2,
                text=self.text, 
                fill=self.variant["fg"],
                font=self.font,
                anchor=text_anchor
            )
    
    def on_enter(self, event):
        """Handle mouse enter event"""
        self.state = "hover"
        self.redraw()
        
    def on_leave(self, event):
        """Handle mouse leave event"""
        self.state = "normal"
        self.redraw()
        
    def on_press(self, event):
        """Handle mouse press event"""
        self.state = "active"
        self.redraw()
        
    def on_release(self, event):
        """Handle mouse release event"""
        # Check if mouse is still within the button
        if 0 <= event.x <= self.btn_width and 0 <= event.y <= self.btn_height:
            if self.command:
                self.command()
            self.state = "hover"  # Return to hover state
        else:
            self.state = "normal"  # Return to normal state if released outside button
        self.redraw()
        
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle on the canvas"""
        points = [
            # Top left
            x1, y1 + radius,
            x1, y1,
            x1 + radius, y1,
            
            # Top right
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            
            # Bottom right
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            
            # Bottom left
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
        ]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def configure(self, **kwargs):
        """Update button configuration"""
        update_needed = False
        
        if "text" in kwargs:
            self.text = kwargs.pop("text")
            update_needed = True
            
        if "command" in kwargs:
            self.command = kwargs.pop("command")
            
        if "icon" in kwargs:
            self.icon = kwargs.pop("icon")
            update_needed = True
            
        if "state" in kwargs:
            state = kwargs.pop("state")
            if state == "disabled":
                self.state = "disabled"
                update_needed = True
            elif state == "normal" and self.state == "disabled":
                self.state = "normal"
                update_needed = True
                
        if update_needed:
            self.redraw()
            
        # Pass remaining configs to canvas
        super().configure(**kwargs)
    
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
        return ModernButton(master, text, command, size, "primary", **kwargs)
    
    @staticmethod
    def create_secondary_button(master, text, command=None, size="md", **kwargs):
        """Create a secondary button"""
        return ModernButton(master, text, command, size, "secondary", **kwargs)
        
    @staticmethod
    def create_tertiary_button(master, text, command=None, size="md", **kwargs):
        """Create a tertiary button"""
        return ModernButton(master, text, command, size, "tertiary", **kwargs)
        
    @staticmethod
    def create_quaternary_button(master, text, command=None, size="md", **kwargs):
        """Create a quaternary button"""
        return ModernButton(master, text, command, size, "quaternary", **kwargs)
    
    @staticmethod
    def create_dark_button(master, text, command=None, size="md", **kwargs):
        """Create a dark button"""
        return ModernButton(master, text, command, size, "dark", **kwargs)
    
    @staticmethod
    def create_outline_button(master, text, command=None, size="md", **kwargs):
        """Create an outline button"""
        return ModernButton(master, text, command, size, "outline", **kwargs)
    
    @staticmethod
    def create_ghost_button(master, text, command=None, size="md", **kwargs):
        """Create a ghost button"""
        return ModernButton(master, text, command, size, "ghost", **kwargs)
