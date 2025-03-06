"""
Font manager module for the application.
Handles font loading and registration for cross-platform compatibility.
"""
import os
import tkinter as tk
import platform
from typing import Tuple, Dict, List, Optional

class FontManager:
    """Manages font loading and registration for the application."""
    
    # Font configuration
    DEFAULT_FONT_FAMILY = "Lexend"
    
    # Font files
    ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    FONTS_DIR = os.path.join(ASSETS_PATH, "fonts")
    
    # Font variants dictionary with font filename mappings
    FONT_VARIANTS = {
        "Lexend": {
            "regular": "Lexend-Regular.ttf",
            "bold": "Lexend-Bold.ttf",
            "medium": "Lexend-Medium.ttf",
            "light": "Lexend-Light.ttf",
            "semibold": "Lexend-SemiBold.ttf",
            "thin": "Lexend-Thin.ttf",
            "black": "Lexend-Black.ttf",
            "extrabold": "Lexend-ExtraBold.ttf",
            "extralight": "Lexend-ExtraLight.ttf",
        }
    }
    
    # Registered font objects
    _registered_fonts = {}
    
    # System font fallbacks by platform
    FALLBACK_FONTS = {
        "Windows": "Arial",
        "Darwin": "SF Pro",  # macOS
        "Linux": "DejaVu Sans"
    }
    
    # Track if we've registered fonts already
    _fonts_registered = False
    
    # Temporary root window for font operations
    _temp_root = None
    
    @classmethod
    def get_font_path(cls, font_family: str, variant: str = "regular") -> Optional[str]:
        """Get the full path to a specific font file"""
        if font_family not in cls.FONT_VARIANTS:
            return None
            
        if variant not in cls.FONT_VARIANTS[font_family]:
            variant = "regular"  # Default to regular if variant not found
            
        font_filename = cls.FONT_VARIANTS[font_family][variant]
        font_path = os.path.join(cls.FONTS_DIR, font_family, font_filename)
        
        if os.path.exists(font_path):
            return font_path
        return None
    
    @classmethod
    def ensure_font_directories(cls) -> None:
        """Ensure all needed font directories exist"""
        # Create main fonts directory if it doesn't exist
        if not os.path.exists(cls.FONTS_DIR):
            os.makedirs(cls.FONTS_DIR, exist_ok=True)
            
        # Create subdirectories for each font family
        for family in cls.FONT_VARIANTS:
            family_dir = os.path.join(cls.FONTS_DIR, family)
            if not os.path.exists(family_dir):
                os.makedirs(family_dir, exist_ok=True)
    
    @classmethod
    def _ensure_root_window(cls):
        """Ensure we have a root window for font operations"""
        if cls._temp_root is None:
            # Create a temporary root window that won't be shown
            cls._temp_root = tk.Tk()
            cls._temp_root.withdraw()  # Hide the window
    
    @classmethod
    def register_fonts(cls) -> bool:
        """Register custom fonts for use in the application"""
        # Avoid registering multiple times
        if cls._fonts_registered:
            return True
            
        try:
            # Ensure font directories exist
            cls.ensure_font_directories()
            
            # Create a temporary root window if needed for font operations
            # We'll defer this until an actual font operation needs it
            
            # Mark as registered - we'll do actual registration when needed
            cls._fonts_registered = True
            return True
        except Exception as e:
            print(f"Error preparing font registration: {e}")
            return False
    
    @classmethod
    def _register_fonts_now(cls) -> bool:
        """Do the actual font registration now that we have a root window"""
        try:
            # Only import when needed
            from tkinter import font as tkfont
            
            # Ensure we have a root window
            cls._ensure_root_window()
            
            # Check if fonts are already installed in the system
            system_fonts = tkfont.families()
            
            # Check which font families we need to register
            families_to_register = []
            for family in cls.FONT_VARIANTS:
                if family not in system_fonts:
                    families_to_register.append(family)
            
            if not families_to_register:
                print("All required fonts already available in system")
                return True
            
            # Register necessary fonts based on platform
            if platform.system() == "Windows":
                cls._register_windows_fonts(families_to_register)
            else:
                # macOS and Linux method
                cls._register_fonts_with_tkfont(tkfont, families_to_register)
                
            return True
        except Exception as e:
            print(f"Error registering fonts: {e}")
            return False
    
    @classmethod
    def _register_windows_fonts(cls, families_to_register: List[str]) -> None:
        """Register fonts on Windows"""
        try:
            # Windows-specific font registration
            import ctypes
            from ctypes import wintypes
            
            # Add font resource
            FR_PRIVATE = 0x10
            AddFontResourceEx = ctypes.windll.gdi32.AddFontResourceExW
            AddFontResourceEx.restype = wintypes.BOOL
            
            fonts_added = False
            
            # Register each font file for each family
            for family in families_to_register:
                if family not in cls.FONT_VARIANTS:
                    continue
                    
                for variant in cls.FONT_VARIANTS[family]:
                    font_path = cls.get_font_path(family, variant)
                    if font_path and os.path.exists(font_path):
                        result = AddFontResourceEx(font_path, FR_PRIVATE, 0)
                        if result > 0:
                            fonts_added = True
                            print(f"Registered {family} {variant}: {font_path}")
            
            # Notify applications of font change if any fonts were added
            if fonts_added:
                HWND_BROADCAST = 0xFFFF
                WM_FONTCHANGE = 0x001D
                SendMessage = ctypes.windll.user32.SendMessageW
                SendMessage(HWND_BROADCAST, WM_FONTCHANGE, 0, 0)
                print("Windows fonts registered successfully")
        except Exception as e:
            print(f"Error registering Windows fonts: {e}")
    
    @classmethod
    def _register_fonts_with_tkfont(cls, tkfont, families_to_register: List[str]) -> None:
        """Register fonts using tkinter's font mechanism"""
        for family in families_to_register:
            if family not in cls.FONT_VARIANTS:
                continue
                
            for variant in cls.FONT_VARIANTS[family]:
                font_path = cls.get_font_path(family, variant)
                if font_path and os.path.exists(font_path):
                    try:
                        # Create a unique name for this font variant
                        font_name = f"{family}-{variant}"
                        cls._registered_fonts[font_name] = tkfont.Font(family=font_name, file=font_path)
                        print(f"Registered font: {font_name}")
                    except Exception as e:
                        print(f"Failed to register font {font_path}: {e}")
    
    @staticmethod
    def is_font_available(font_name: str) -> bool:
        """Check if a font is available in the system"""
        try:
            # Get or create the root for font operations
            FontManager._ensure_root_window()
            
            from tkinter import font as tkfont
            available_fonts = tkfont.families()
            return font_name in available_fonts
        except Exception as e:
            print(f"Error checking font availability: {e}")
            return False
    
    @classmethod
    def get_font_families(cls) -> List[str]:
        """Get list of all available font families"""
        try:
            # Get or create the root for font operations
            cls._ensure_root_window()
            
            from tkinter import font as tkfont
            return sorted(tkfont.families())
        except Exception as e:
            print(f"Error getting font families: {e}")
            return []

    @classmethod
    def get_font(cls, font_family: str = None, size: int = 12, weight: str = "normal") -> Tuple[str, int, str]:
        """
        Get a font tuple that will work with Tkinter
        
        Args:
            font_family: Font family name (e.g., "Lexend")
            size: Font size in points
            weight: Font weight ("normal", "bold", etc.)
            
        Returns:
            A font tuple (family, size, weight) for tkinter
        """
        # If this is the first time getting a font, actually register them now
        if cls._fonts_registered and not cls._temp_root:
            cls._register_fonts_now()
            
        if font_family is None:
            font_family = cls.DEFAULT_FONT_FAMILY
        
        # For system fonts, we can just return the tuple without checking
        system = platform.system()
        fallback = cls.FALLBACK_FONTS.get(system, "Arial")
        
        # If we're requesting the default font or specific font,
        # try to check if it's available
        if font_family != fallback:
            # Only check font availability if we have a root window
            if cls._temp_root:
                if cls.is_font_available(font_family):
                    return (font_family, size, weight)
        
        # Use fallback font
        return (fallback, size, weight)