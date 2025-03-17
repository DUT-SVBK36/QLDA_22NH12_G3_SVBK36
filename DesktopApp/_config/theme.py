"""
Global theme configuration for tkinter application based on tailwindcss config.
This module provides consistent styling across the application.
"""
import os
import tkinter as tk
from _config.font_manager import FontManager

# Register fonts when theme is imported
FontManager.register_fonts()

class Theme:
    # Colors
    PRIMARY = "#b7b1f2"
    PRIMARY_DARK = "#2b2e4a"
    SECONDARY = "#fdb7ea"
    TERTIARY = "#ffdccc"
    QUARTERNARY = "#fbf3b9"
    WHITE = "#ffffff"
    BLACK = "#000000"
    LIGHT_GRAY = "#E5E5E5"
    LIGHT_PURPLE = "#E0DBFF"

    # Font sizes (in pixels, assuming 16px = 1rem)
    FONT_XS = 12         # 0.75rem
    FONT_SM = 14         # 0.875rem
    FONT_BASE = 16       # 1rem
    FONT_L =18
    FONT_LG = 22         # 1.375rem
    FONT_XL = 24         # 1.5rem
    FONT_2XL = 30        # 1.875rem
    FONT_3XL = 36        # 2.25rem
    
    # Font families
    FONT_FAMILY = FontManager.DEFAULT_FONT_FAMILY
    
    # Border radius values (in pixels, assuming 16px = 1rem)
    ROUNDED_0 = 0        # 0rem
    ROUNDED_1 = 4        # 0.25rem
    ROUNDED_2 = 5        # 0.3125rem
    ROUNDED_3 = 6        # 0.375rem
    ROUNDED_4 = 8        # 0.5rem
    ROUNDED_5 = 16       # 1rem
    ROUNDED_6 = 25       # 1.5625rem
    ROUNDED_7 = 62       # ~3.85rem
    ROUNDED_8 = 999      # 62.4375rem (essentially pill-shaped)
    
    # Assets paths
    ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    APP_BG_PATH = os.path.join(ASSETS_PATH, "img", "app-bg.png")
    
    # Cached loaded images
    _app_bg_image = None
    
    @classmethod
    def get_app_bg_image(cls):
        """Load and cache the app background image"""
        if cls._app_bg_image is None:
            try:
                cls._app_bg_image = tk.PhotoImage(file=cls.APP_BG_PATH)
            except Exception as e:
                print(f"Error loading background image: {e}")
                return None
        return cls._app_bg_image
    
    @classmethod
    def get_font(cls, size=None, weight="normal"):
        """Get a properly configured font tuple with fallbacks"""
        if size is None:
            size = cls.FONT_BASE
        return FontManager.get_font(cls.FONT_FAMILY, size, weight)
    
    # Common styles as dictionaries for easier application
    @staticmethod
    def button_primary():
        return {
            "bg": Theme.PRIMARY,
            "fg": Theme.WHITE,
            "font": Theme.get_font(Theme.FONT_BASE),
            "borderwidth": 0,
            "relief": "flat",
            "padx": 16,
            "pady": 8,
        }
    
    @staticmethod
    def button_secondary():
        return {
            "bg": Theme.SECONDARY,
            "fg": Theme.WHITE,
            "font": Theme.get_font(Theme.FONT_BASE),
            "borderwidth": 0,
            "relief": "flat",
            "padx": 16, 
            "pady": 8,
        }
    
    @staticmethod
    def entry_default():
        return {
            "bg": Theme.WHITE,
            "fg": Theme.BLACK,
            "font": Theme.get_font(Theme.FONT_BASE),
            "borderwidth": 1,
            "relief": "solid",
            "insertbackground": Theme.BLACK,  # cursor color
        }
    
    @staticmethod
    def label_default():
        return {
            "bg": Theme.WHITE,
            "fg": Theme.BLACK,
            "font": Theme.get_font(Theme.FONT_BASE),
            "padx": 4,
            "pady": 4,
        }
    
    @staticmethod
    def frame_default():
        return {
            "bg": Theme.WHITE,
            "borderwidth": 0,
        }
    
    @staticmethod
    def apply_style(widget, style_dict):
        """Apply a style dictionary to a widget"""
        for key, value in style_dict.items():
            try:
                widget[key] = value
            except Exception:
                # Some widgets might not support all styling options
                pass

    @staticmethod
    def set_app_background(window):
        """Set application background image to a window or frame"""
        bg_image = Theme.get_app_bg_image()
        if bg_image:
            bg_label = tk.Label(window, image=bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            # Keep reference to prevent garbage collection
            window.bg_image = bg_image
            window.bg_label = bg_label
            return bg_label
        return None

# Helper function for creating rounded corners (requires PIL/Pillow)
def create_rounded_rectangle(width, height, radius, fill_color):
    """
    Creates a rounded rectangle image that can be used with tkinter
    
    Requires: from PIL import Image, ImageDraw, ImageTk
    Usage: 
        img = create_rounded_rectangle(200, 100, Theme.ROUNDED_4, Theme.PRIMARY)
        label = tk.Label(root, image=img, borderwidth=0)
        label.image = img  # Keep a reference
    """
    try:
        from PIL import Image, ImageDraw, ImageTk
        
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw rounded rectangle
        draw.rounded_rectangle([(0, 0), (width, height)], radius, fill=fill_color)
        
        return ImageTk.PhotoImage(img)
    except ImportError:
        print("PIL/Pillow is required for rounded corners. Please install with: pip install pillow")
        return None