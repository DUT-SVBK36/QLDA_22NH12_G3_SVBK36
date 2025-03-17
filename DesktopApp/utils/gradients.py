"""
Gradient utility module for creating gradient effects in tkinter applications.
Provides functions to create linear and radial gradients for widgets, canvases, and SVG elements.
"""

import tkinter as tk
import math
from typing import List, Tuple, Union, Literal
from PIL import Image, ImageDraw, ImageTk

# Type aliases for clarity
Color = str  # Hex color string e.g. "#FF0000"
Point = Tuple[int, int]  # (x, y) coordinate
GradientType = Literal["linear", "radial"]

class Gradient:
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color string."""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    @staticmethod
    def interpolate_color(color1: Color, color2: Color, factor: float) -> Color:
        """Interpolate between two colors with given factor (0-1)."""
        rgb1 = Gradient.hex_to_rgb(color1)
        rgb2 = Gradient.hex_to_rgb(color2)
        
        # Linear interpolation between the RGB values
        result_rgb = tuple(
            int(rgb1[i] + factor * (rgb2[i] - rgb1[i]))
            for i in range(3)
        )
        
        return Gradient.rgb_to_hex(result_rgb)
    
    @staticmethod
    def create_linear_gradient_image(
        width: int, 
        height: int, 
        colors: List[Color], 
        direction: Literal["horizontal", "vertical", "diagonal"] = "horizontal",
        stops: List[float] = None
    ) -> ImageTk.PhotoImage:
        """
        Create a linear gradient image.
        
        Args:
            width: Width of the image
            height: Height of the image
            colors: List of colors (hex strings)
            direction: Direction of gradient ("horizontal", "vertical", or "diagonal")
            stops: Optional list of stop positions (0-1) for each color. If None, evenly distributed.
        
        Returns:
            An ImageTk.PhotoImage object with the gradient
        """
        img = Image.new("RGB", (width, height), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        
        # Set default stops if not provided
        if stops is None:
            stops = [i / (len(colors) - 1) for i in range(len(colors))]
        
        # Ensure stops are in range [0, 1]
        stops = [max(0, min(s, 1)) for s in stops]
        
        # For each row/column, calculate color based on position
        for y in range(height):
            for x in range(width):
                # Calculate position factor based on direction
                if direction == "horizontal":
                    factor = x / (width - 1) if width > 1 else 0
                elif direction == "vertical":
                    factor = y / (height - 1) if height > 1 else 0
                elif direction == "diagonal":
                    # Normalize distance along diagonal
                    factor = (x + y) / (width + height - 2) if (width + height - 2) > 0 else 0
                
                # Find segment and local factor
                segment_index = 0
                for i in range(len(stops) - 1):
                    if stops[i] <= factor <= stops[i + 1]:
                        segment_index = i
                        break
                
                start, end = stops[segment_index], stops[segment_index + 1]
                local_factor = (factor - start) / (end - start) if end > start else 0
                
                # Interpolate color
                color = Gradient.interpolate_color(
                    colors[segment_index],
                    colors[segment_index + 1],
                    local_factor
                )
                
                draw.point((x, y), fill=color)
        
        return ImageTk.PhotoImage(img)
    
    @staticmethod
    def create_radial_gradient_image(
        width: int, 
        height: int, 
        colors: List[Color], 
        center: Point = None,
        stops: List[float] = None
    ) -> ImageTk.PhotoImage:
        """
        Create a radial gradient image.
        
        Args:
            width: Width of the image
            height: Height of the image
            colors: List of colors (hex strings)
            center: Center point of the gradient. If None, use center of image.
            stops: Optional list of stop positions (0-1) for each color. If None, evenly distributed.
        
        Returns:
            An ImageTk.PhotoImage object with the gradient
        """
        img = Image.new("RGB", (width, height), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        
        # Default center is middle of image
        if center is None:
            center = (width // 2, height // 2)
        
        # Maximum distance is from center to any corner
        max_distance = math.sqrt(max(
            (center[0]**2 + center[1]**2),
            ((width - center[0])**2 + center[1]**2),
            (center[0]**2 + (height - center[1])**2),
            ((width - center[0])**2 + (height - center[1])**2)
        ))
        
        # Set default stops if not provided
        if stops is None:
            stops = [i / (len(colors) - 1) for i in range(len(colors))]
        
        # Ensure stops are in range [0, 1]
        stops = [max(0, min(s, 1)) for s in stops]
        
        # For each pixel, calculate color based on distance from center
        for y in range(height):
            for x in range(width):
                # Calculate distance factor (0 at center, 1 at max distance)
                distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
                factor = min(distance / max_distance, 1.0)
                
                # Find segment and local factor
                segment_index = 0
                for i in range(len(stops) - 1):
                    if stops[i] <= factor <= stops[i + 1]:
                        segment_index = i
                        break
                
                start, end = stops[segment_index], stops[segment_index + 1]
                local_factor = (factor - start) / (end - start) if end > start else 0
                
                # Interpolate color
                color = Gradient.interpolate_color(
                    colors[segment_index],
                    colors[segment_index + 1],
                    local_factor
                )
                
                draw.point((x, y), fill=color)
        
        return ImageTk.PhotoImage(img)

    @staticmethod
    def apply_gradient_to_widget(
        widget: tk.Widget, 
        colors: List[Color], 
        gradient_type: GradientType = "linear",
        direction: Literal["horizontal", "vertical", "diagonal"] = "horizontal",
        center: Point = None,
        stops: List[float] = None
    ) -> None:
        """
        Apply gradient to a tkinter widget.
        
        Args:
            widget: The tkinter widget
            colors: List of colors (hex strings)
            gradient_type: Type of gradient ("linear" or "radial")
            direction: For linear gradients, the direction
            center: For radial gradients, the center point
            stops: Optional list of stop positions (0-1) for each color
        """
        if not hasattr(widget, "winfo_width") or not hasattr(widget, "winfo_height"):
            raise ValueError("Widget must be a tkinter widget with winfo_width and winfo_height methods")
        
        # Ensure widget has been mapped to the screen
        if widget.winfo_width() == 1 and widget.winfo_height() == 1:
            # Widget not mapped yet, schedule this function to run after widget is mapped
            widget.update_idletasks()
        
        width = widget.winfo_width()
        height = widget.winfo_height()
        
        if width <= 1 or height <= 1:
            # Still not properly sized, use requested width/height
            width = widget.winfo_reqwidth()
            height = widget.winfo_reqheight()
        
        # Create gradient image
        if gradient_type == "linear":
            gradient_img = Gradient.create_linear_gradient_image(
                width, height, colors, direction, stops
            )
        else:  # radial
            gradient_img = Gradient.create_radial_gradient_image(
                width, height, colors, center, stops
            )
        
        # Create a label with the gradient as background
        gradient_label = tk.Label(widget, image=gradient_img, borderwidth=0)
        gradient_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Keep references to prevent garbage collection
        widget.gradient_img = gradient_img
        widget.gradient_label = gradient_label
        
        # Move all other children above the gradient
        widget.gradient_label.lower()

    @staticmethod
    def apply_gradient_to_canvas(
        canvas: tk.Canvas, 
        colors: List[Color], 
        gradient_type: GradientType = "linear",
        direction: Literal["horizontal", "vertical", "diagonal"] = "horizontal",
        center: Point = None,
        stops: List[float] = None
    ) -> int:
        """
        Apply gradient to a tkinter canvas as a background.
        
        Args:
            canvas: The tkinter canvas
            colors: List of colors (hex strings)
            gradient_type: Type of gradient ("linear" or "radial")
            direction: For linear gradients, the direction
            center: For radial gradients, the center point
            stops: Optional list of stop positions (0-1) for each color
        
        Returns:
            The ID of the image item on the canvas
        """
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            # Still not properly sized, use requested width/height
            width = canvas.winfo_reqwidth()
            height = canvas.winfo_reqheight()
        
        # Create gradient image
        if gradient_type == "linear":
            gradient_img = Gradient.create_linear_gradient_image(
                width, height, colors, direction, stops
            )
        else:  # radial
            gradient_img = Gradient.create_radial_gradient_image(
                width, height, colors, center, stops
            )
        
        # Add image to canvas
        img_id = canvas.create_image(0, 0, image=gradient_img, anchor=tk.NW)
        
        # Keep reference to prevent garbage collection
        canvas.gradient_img = gradient_img
        
        # Move to back
        canvas.tag_lower(img_id)
        
        return img_id

    @staticmethod
    def create_gradient_svg(
        width: int,
        height: int, 
        colors: List[Color], 
        gradient_type: GradientType = "linear",
        direction: Literal["horizontal", "vertical", "diagonal"] = "horizontal",
        center: Point = None,
        stops: List[float] = None,
        id_name: str = "gradient1"
    ) -> str:
        """
        Create an SVG gradient definition that can be used in SVG elements.
        
        Args:
            width: Width of the SVG context
            height: Height of the SVG context
            colors: List of colors (hex strings)
            gradient_type: Type of gradient ("linear" or "radial")
            direction: For linear gradients, the direction
            center: For radial gradients, the center point
            stops: Optional list of stop positions (0-1) for each color
            id_name: ID to use for the gradient definition
        
        Returns:
            SVG gradient definition as a string
        """
        # Set default stops if not provided
        if stops is None:
            stops = [i / (len(colors) - 1) for i in range(len(colors))]
        
        # Ensure stops are in range [0, 1]
        stops = [max(0, min(s, 1)) for s in stops]
        
        svg = "<defs>\n"
        
        if gradient_type == "linear":
            # Set x1, y1, x2, y2 based on direction
            if direction == "horizontal":
                x1, y1, x2, y2 = "0%", "0%", "100%", "0%"
            elif direction == "vertical":
                x1, y1, x2, y2 = "0%", "0%", "0%", "100%"
            else:  # diagonal
                x1, y1, x2, y2 = "0%", "0%", "100%", "100%"
                
            svg += f'<linearGradient id="{id_name}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">\n'
            
            # Add stops
            for i, (color, stop) in enumerate(zip(colors, stops)):
                svg += f'<stop offset="{stop * 100}%" stop-color="{color}" />\n'
                
            svg += '</linearGradient>\n'
        else:  # radial
            # Default center is middle
            cx = "50%" if center is None else f"{center[0] / width * 100}%"
            cy = "50%" if center is None else f"{center[1] / height * 100}%"
            
            svg += f'<radialGradient id="{id_name}" cx="{cx}" cy="{cy}" r="100%" fx="{cx}" fy="{cy}">\n'
            
            # Add stops
            for i, (color, stop) in enumerate(zip(colors, stops)):
                svg += f'<stop offset="{stop * 100}%" stop-color="{color}" />\n'
                
            svg += '</radialGradient>\n'
            
        svg += "</defs>\n"
        return svg

    @staticmethod
    def modify_svg_with_gradient(
        svg_content: str,
        colors: List[Color], 
        target_fill: str = None,
        target_stroke: str = None,
        gradient_type: GradientType = "linear",
        direction: Literal["horizontal", "vertical", "diagonal"] = "horizontal",
        id_name: str = "gradient1"
    ) -> str:
        """
        Modify an SVG file by replacing fill or stroke colors with gradients.
        
        Args:
            svg_content: SVG file content as string
            colors: List of colors (hex strings) for the gradient
            target_fill: Fill color to replace with gradient, or None to replace all fills
            target_stroke: Stroke color to replace with gradient, or None to replace all strokes
            gradient_type: Type of gradient ("linear" or "radial")
            direction: For linear gradients, the direction
            id_name: ID to use for the gradient definition
        
        Returns:
            Modified SVG content as string
        """
        import re
        
        # Parse SVG to extract width and height
        width_match = re.search(r'width="(\d+)"', svg_content)
        height_match = re.search(r'height="(\d+)"', svg_content)
        
        width = int(width_match.group(1)) if width_match else 100
        height = int(height_match.group(1)) if height_match else 100
        
        # Create gradient definition
        gradient_def = Gradient.create_gradient_svg(
            width, height, colors, gradient_type, direction, None, None, id_name
        )
        
        # Add gradient definition after the SVG tag
        svg_with_defs = re.sub(
            r'(<svg[^>]*>)', 
            r'\1\n' + gradient_def, 
            svg_content
        )
        
        # Replace fill attributes
        if target_fill is not None:
            svg_with_defs = re.sub(
                r'fill="' + target_fill + r'"', 
                r'fill="url(#' + id_name + r')"', 
                svg_with_defs
            )
        
        # Replace stroke attributes
        if target_stroke is not None:
            svg_with_defs = re.sub(
                r'stroke="' + target_stroke + r'"', 
                r'stroke="url(#' + id_name + r')"', 
                svg_with_defs
            )
        
        return svg_with_defs

