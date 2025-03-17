import os
import sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config.theme import Theme

class SideBar(ctk.CTkFrame):
    """
    Side navigation bar component that provides access to main application screens.
    
    Features:
    - Fixed width of 64px
    - App logo at the top
    - Navigation icons for different screens
    - Visual feedback on hover and selection
    """
    
    def __init__(self, parent, controller=None, **kwargs):
        """
        Initialize the sidebar.
        
        Args:
            parent: Parent widget
            controller: Application controller to handle navigation
            **kwargs: Additional arguments for the Frame widget
        """
        # Set width and background color
        kwargs["width"] = 64
        kwargs["fg_color"] = Theme.PRIMARY_DARK
        kwargs["corner_radius"] = 0
        
        # Initialize as CTkFrame
        super().__init__(parent, **kwargs)
        
        # Keep reference to controller for navigation
        self.controller = controller
        
        # Load and prepare assets
        self.load_assets()
        
        # Create layout
        self.create_layout()
        
        # Track selected item
        self.selected_item = None
        self.tooltip_window = None
        self.select_item("dashboard")  # Select dashboard by default

    def load_assets(self):
        """Load and prepare all required images for the sidebar"""
        self.assets = {}
        
        # Load logo from png file
        logo_path = os.path.join(Theme.ASSETS_PATH, "img", "Logo.png")
        if os.path.exists(logo_path):
            try:
                original_logo = Image.open(logo_path)
                
                # Get original dimensions
                orig_width, orig_height = original_logo.size
                
                # Determine target size with "contain" strategy (maintain aspect ratio)
                logo_size = 48  # Maximum size in either dimension
                
                # Calculate scale factor to fit within logo_size while preserving aspect ratio
                scale = min(logo_size / orig_width, logo_size / orig_height)
                
                # Calculate new dimensions
                new_width = int(orig_width * scale)
                new_height = int(orig_height * scale)
                
                # Resize the image with LANCZOS resampling for better quality
                resized_logo = original_logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create a new blank image with the target size
                final_logo = Image.new("RGBA", (logo_size, logo_size), (0, 0, 0, 0))
                
                # Paste the resized image into the center of the blank image
                paste_x = (logo_size - new_width) // 2
                paste_y = (logo_size - new_height) // 2
                final_logo.paste(resized_logo, (paste_x, paste_y))
                
                self.assets["logo"] = ImageTk.PhotoImage(final_logo)
            except Exception as e:
                print(f"Error loading logo: {e}")
                self.assets["logo"] = None
        
        # Define icon mappings using PNG files from img directory
        icon_files = {
            "dashboard": {
                "normal": "dashboard.png",
                "hover": "dashboard-hover.png",
                "selected": "dashboard-active.png"
            },
            "monitor": {
                "normal": "monitor.png",
                "hover": "monitor-hover.png",
                "selected": "monitor-active.png"
            },
            "settings": {
                "normal": "settings.png",
                "hover": "settings-hover.png",
                "selected": "settings-active.png"
            }
        }
        
        # Load icon images from PNG files
        for name, files in icon_files.items():
            # Load normal icon
            normal_path = os.path.join(Theme.ASSETS_PATH, "img", files["normal"])
            if os.path.exists(normal_path):
                try:
                    icon = Image.open(normal_path)
                    icon_size = 24
                    icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                    self.assets[name] = ImageTk.PhotoImage(icon)
                    print(f"Successfully loaded {name} icon from: {normal_path}")
                except Exception as e:
                    print(f"Error loading normal icon {name}: {e}")
                    self.assets[name] = self.create_placeholder_icon(name, Theme.WHITE)
            else:
                print(f"Icon file not found: {normal_path}")
                self.assets[name] = self.create_placeholder_icon(name, Theme.WHITE)
            
            # Load hover icon
            hover_path = os.path.join(Theme.ASSETS_PATH, "img", files["hover"])
            if os.path.exists(hover_path):
                try:
                    icon = Image.open(hover_path)
                    icon_size = 24
                    icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                    self.assets[f"{name}_hover"] = ImageTk.PhotoImage(icon)
                    print(f"Successfully loaded {name}_hover icon from: {hover_path}")
                except Exception as e:
                    print(f"Error loading hover icon {name}: {e}")
                    self.assets[f"{name}_hover"] = self.create_placeholder_icon(name, Theme.SECONDARY)
            else:
                print(f"Hover icon file not found: {hover_path}")
                self.assets[f"{name}_hover"] = self.create_placeholder_icon(name, Theme.SECONDARY)
            
            # Load selected icon
            selected_path = os.path.join(Theme.ASSETS_PATH, "img", files["selected"])
            if os.path.exists(selected_path):
                try:
                    icon = Image.open(selected_path)
                    icon_size = 24
                    icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                    self.assets[f"{name}_selected"] = ImageTk.PhotoImage(icon)
                    print(f"Successfully loaded {name}_selected icon from: {selected_path}")
                except Exception as e:
                    print(f"Error loading selected icon {name}: {e}")
                    self.assets[f"{name}_selected"] = self.create_placeholder_icon(name, Theme.PRIMARY)
            else:
                print(f"Selected icon file not found: {selected_path}")
                self.assets[f"{name}_selected"] = self.create_placeholder_icon(name, Theme.PRIMARY)

    def create_placeholder_icon(self, name, color):
        """Create a simple colored icon placeholder"""
        icon_size = 24
        icon = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
        
        # Extract RGB values from hex color
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # Draw a simple shape based on the icon name
        from PIL import ImageDraw
        draw = ImageDraw.Draw(icon)
        
        if name == "dashboard":
            # Draw a simple pie chart
            draw.pieslice([2, 2, icon_size-2, icon_size-2], 0, 270, fill=(r, g, b))
        elif name == "monitor":
            # Draw a simple compass
            draw.ellipse([2, 2, icon_size-2, icon_size-2], outline=(r, g, b), width=2)
            draw.line([icon_size//2, 4, icon_size//2, icon_size//2], fill=(r, g, b), width=2)
            draw.line([icon_size//2, icon_size//2, icon_size-4, icon_size-4], fill=(r, g, b), width=2)
        elif name == "settings":
            # Draw a gear icon
            draw.ellipse([8, 8, icon_size-8, icon_size-8], outline=(r, g, b), width=2)
            for i in range(0, 360, 45):
                import math
                angle_rad = i * math.pi / 180
                x1 = int(icon_size/2 + 6 * math.cos(angle_rad))
                y1 = int(icon_size/2 + 6 * math.sin(angle_rad))
                x2 = int(icon_size/2 + 14 * math.cos(angle_rad))
                y2 = int(icon_size/2 + 14 * math.sin(angle_rad))
                draw.line([x1, y1, x2, y2], fill=(r, g, b), width=2)
        else:
            # Generic icon
            draw.rectangle([4, 4, icon_size-4, icon_size-4], outline=(r, g, b), width=2)
        
        return ImageTk.PhotoImage(icon)
    
    def create_layout(self):
        """Create the sidebar layout with logo and navigation options"""
        # Make the frame full height
        self.pack_propagate(False)
        
        # Logo at the top with some padding
        if self.assets.get("logo"):
            self.logo_label = ctk.CTkLabel(
                self, 
                image=self.assets["logo"],
                text="",  # No text, just the image
                fg_color="transparent"
            )
            self.logo_label.pack(pady=(20, 40))  # Padding at top and bottom
        
        # Create navigation options container
        self.nav_container = ctk.CTkFrame(
            self,
            fg_color=Theme.PRIMARY_DARK,
            corner_radius=0
        )
        self.nav_container.pack(fill="x", expand=False)
        
        # Create navigation options
        self.nav_items = {}
        
        # Dashboard option
        self.nav_items["dashboard"] = self.create_nav_item(
            "dashboard", "Dashboard"
        )
        
        # Monitor option
        self.nav_items["monitor"] = self.create_nav_item(
            "monitor", "Monitor"
        )
        
        # Settings option (at the bottom)
        self.settings_container = ctk.CTkFrame(
            self,
            fg_color=Theme.PRIMARY_DARK,
            corner_radius=0
        )
        self.settings_container.pack(side="bottom", fill="x", pady=20)
        
        self.nav_items["settings"] = self.create_nav_item(
            "settings", "Settings", parent=self.settings_container
        )

    def create_nav_item(self, name, tooltip, parent=None):
        """
        Create a navigation item with icon and tooltip
        
        Args:
            name: Icon name and identifier
            tooltip: Text to show on hover
            parent: Parent container (defaults to nav_container)
        """
        if parent is None:
            parent = self.nav_container
        
        # Create frame for this navigation item
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=Theme.PRIMARY_DARK,  # Normal state color
            width=64,
            height=64,
            corner_radius=0
        )
        item_frame.pack(pady=5)
        item_frame.pack_propagate(False)
        
        # Create the icon label
        icon_label = ctk.CTkLabel(
            item_frame,
            image=self.assets.get(name),
            text="",  # No text, just the image
            fg_color="transparent"
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create tooltip
        if tooltip:
            def show_tooltip(event):
                # Only show tooltip if not currently selected
                if self.selected_item != name:
                    # Hide any existing tooltip
                    self.hide_tooltip()
                    
                    # Create tooltip window
                    x = event.widget.winfo_rootx() + 70
                    y = event.widget.winfo_rooty() + 20
                    
                    self.tooltip_window = ctk.CTkToplevel(event.widget)
                    self.tooltip_window.wm_overrideredirect(True)
                    self.tooltip_window.wm_geometry(f"+{x}+{y}")
                    self.tooltip_window.attributes("-topmost", True)
                    self.tooltip_window.configure(fg_color=Theme.PRIMARY_DARK)
                    
                    label = ctk.CTkLabel(
                        self.tooltip_window, 
                        text=tooltip, 
                        font=Theme.get_font(Theme.FONT_SM),
                        text_color=Theme.WHITE,
                        fg_color=Theme.PRIMARY_DARK,
                        padx=6,
                        pady=2
                    )
                    label.pack()
            
            def hide_tooltip(_=None):
                if self.tooltip_window:
                    self.tooltip_window.destroy()
                    self.tooltip_window = None
            
            # Use lambda to make sure the tooltip functions get proper event parameter
            item_frame.bind("<Enter>", lambda e: show_tooltip(e))
            item_frame.bind("<Leave>", lambda e: hide_tooltip(e))
        
        # Bind event handlers for hover and click
        icon_frame_hover_in = lambda e: self._on_hover(name, icon_label, True)
        icon_frame_hover_out = lambda e: self._on_hover(name, icon_label, False)
        click_handler = lambda e, n=name: self.select_item(n)
        
        # Bind hover events to frame
        item_frame.bind("<Enter>", icon_frame_hover_in)
        item_frame.bind("<Leave>", icon_frame_hover_out)
        item_frame.bind("<Button-1>", click_handler)
        
        # Also bind click event to icon label to ensure it responds to clicks directly on the icon
        icon_label.bind("<Button-1>", click_handler)
        
        # Make the cursor change to a hand when hovering over the icon or frame for better UX
        item_frame.configure(cursor="hand2")
        icon_label.configure(cursor="hand2")
        
        # Store components for later access
        return {
            "frame": item_frame,
            "icon": icon_label,
            "name": name
        }
    
    def _on_hover(self, name, icon_label, is_hover):
        """Handle hover effects for navigation items"""
        # Skip hover effect for selected item
        if self.selected_item == name:
            return
            
        if is_hover:
            # Show hover effect - use hover icon
            icon_label.configure(image=self.assets.get(f"{name}_hover"))
        else:
            # Remove hover effect - restore normal icon
            icon_label.configure(image=self.assets.get(name))
    
    def hide_tooltip(self):
        """Hide the tooltip if it exists"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
    
    def select_item(self, name):
        """Select a navigation item and update UI accordingly"""
        # Deselect previous item if any
        if self.selected_item and self.selected_item in self.nav_items:
            prev_item = self.nav_items[self.selected_item]
            prev_item["icon"].configure(image=self.assets.get(self.selected_item))
            prev_item["frame"].configure(fg_color=Theme.PRIMARY_DARK)
        
        # Select new item
        if name in self.nav_items:
            # Update selected item
            self.selected_item = name
            
            # Get item components
            item = self.nav_items[name]
            
            # Update icon to selected state
            item["icon"].configure(image=self.assets.get(f"{name}_selected"))
            
            # Update frame background to indicate selection
            # With customtkinter, we change fg_color instead of using styles
            item["frame"].configure(fg_color=Theme.PRIMARY_DARK)
            
            # Handle navigation if controller is provided
            if self.controller and hasattr(self.controller, "show_frame"):
                self.controller.show_frame(name)
            
            # Hide any tooltip
            self.hide_tooltip()
        
        return self.selected_item