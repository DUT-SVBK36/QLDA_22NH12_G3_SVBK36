import tkinter as tk
import math
from typing import List, Tuple, Union, Literal
from PIL import Image, ImageDraw, ImageTk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gradients import Gradient
from _config.theme import Theme

# Example usage demonstration
def demo_gradients():
    root = tk.Tk()
    root.title("Gradient Demo")
    root.geometry("800x600")
    
    # Create a frame with linear gradient
    frame1 = tk.Frame(root, width=300, height=150)
    frame1.pack(pady=10)
    
    # Create a frame with radial gradient
    frame2 = tk.Frame(root, width=300, height=150)
    frame2.pack(pady=10)
    
    # Create a canvas with gradient
    canvas = tk.Canvas(root, width=300, height=150, bd=0, highlightthickness=0)
    canvas.pack(pady=10)
    
    # Create a button with gradient
    button = tk.Button(root, text="Gradient Button", width=20, height=2)
    button.pack(pady=10)
    
    # Apply gradients after widgets are packed
    root.update()
    
    # Apply gradients using available Theme colors
    Gradient.apply_gradient_to_widget(
        frame1,
        [Theme.PRIMARY, Theme.SECONDARY, Theme.TERTIARY],
        "linear",
        "horizontal"
    )
    
    Gradient.apply_gradient_to_widget(
        frame2,
        [Theme.TERTIARY, Theme.WHITE, Theme.PRIMARY],
        "radial"
    )
    
    Gradient.apply_gradient_to_canvas(
        canvas,
        [Theme.PRIMARY, Theme.SECONDARY, Theme.QUARTERNARY],
        "linear",
        "diagonal"
    )
    
    Gradient.apply_gradient_to_widget(
        button,
        [Theme.PRIMARY, Theme.SECONDARY],
        "linear",
        "vertical"
    )
    
    root.mainloop()

if __name__ == "__main__":
    demo_gradients()