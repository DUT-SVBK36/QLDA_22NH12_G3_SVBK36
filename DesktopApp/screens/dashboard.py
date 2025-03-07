import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import sys
import os

# Assuming these imports work with your project structure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config.theme import Theme
from components.button import ButtonFactory, ModernButton, initialize_button_styles

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        # Initialize customtkinter appearance if not done already
        initialize_button_styles()
        
        # Use Theme colors but adapt to customtkinter's parameters
        super().__init__(
            parent,
            fg_color=Theme.QUARTERNARY,
            corner_radius=0,
            **kwargs
        )
        
        # Set up responsive grid
        self.columnconfigure(0, weight=1)
        
        # Track display mode (normal or compact)
        self.is_compact = False
        
        # Create the dashboard layout
        self.create_welcome_section()
        self.create_stats_section()
        self.create_charts_section()
        
        # Bind resize event to handle responsive layout updates only
        self.bind("<Configure>", self.on_resize)
        
    def on_resize(self, event):
        """Handle resize events to adapt layout to different screen sizes"""
        width = event.width
        
        # Determine if we should switch to compact mode
        is_compact = width < 900
        very_compact = width < 600
        
        # Check if compact status changed
        if hasattr(self, 'is_compact') and self.is_compact != is_compact:
            self.is_compact = is_compact
            self.update_layout_for_size(is_compact, very_compact)
            
            # Update chart sizes when layout changes
            self.after(100, self.update_chart_sizes)  # Delay to let layout settle
    
    def update_layout_for_size(self, is_compact, very_compact=False):
        """Update layout based on available width"""
        if is_compact:
            # Compact layout adjustments
            if hasattr(self, 'charts_frame'):
                for widget in self.charts_frame.grid_slaves():
                    # Stack charts vertically in compact mode
                    if int(widget.grid_info()['column']) == 1:
                        widget.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
                        
            # Make stats section stack vertically in very compact mode
            if very_compact and hasattr(self, 'stats_frame'):
                for i, widget in enumerate(self.stats_frame.grid_slaves()):
                    widget.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
                    
            # Update button sizes if needed
            if hasattr(self, 'start_btn') and hasattr(self, 'history_btn'):
                size = "xs" if very_compact else "sm"
                if hasattr(self.start_btn, 'update_size'):
                    self.start_btn.update_size(size)
                    self.history_btn.update_size(size)
        else:
            # Regular layout adjustments
            if hasattr(self, 'charts_frame'):
                for widget in self.charts_frame.grid_slaves():
                    # Restore original position if it's the second chart
                    if int(widget.grid_info()['row']) == 1:
                        widget.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
                        
            # Restore horizontal stats layout
            if hasattr(self, 'stats_frame'):
                for i, widget in enumerate(reversed(self.stats_frame.grid_slaves())):
                    widget.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
                    
            # Update button sizes
            if hasattr(self, 'start_btn') and hasattr(self, 'history_btn'):
                if hasattr(self.start_btn, 'update_size'):
                    self.start_btn.update_size("md")
                    self.history_btn.update_size("md")
    
    def update_chart_sizes(self):
        """Update chart sizes after resize"""
        if hasattr(self, 'charts_frame'):
            for widget in self.charts_frame.grid_slaves():
                if hasattr(widget, 'canvas'):
                    widget.canvas.draw()  # Redraw the canvas to fit new size
    
    def create_welcome_section(self):
        """Create the welcome section at the top of the dashboard"""
        welcome_frame = ctk.CTkFrame(
            self, 
            fg_color=Theme.WHITE,
            corner_radius=Theme.ROUNDED_4
        )
        welcome_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        welcome_frame.columnconfigure(0, weight=1)
        
        # Welcome title with fixed font size
        welcome_label = ctk.CTkLabel(
            welcome_frame, 
            text="Welcome back, Resolved",
            font=(Theme.FONT_FAMILY, Theme.FONT_2XL, "bold"),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        welcome_label.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 0))
        
        # Stats subtitle with fixed font size
        stats_label = ctk.CTkLabel(
            welcome_frame, 
            text="Check your daily stats here",
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        stats_label.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))
        
    def create_stats_section(self):
        """Create the three stat boxes: Progress, Streak, and Monitoring"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=10)
        
        # Configure columns to create three equal sections
        stats_frame.columnconfigure(0, weight=1, uniform="stats")
        stats_frame.columnconfigure(1, weight=1, uniform="stats")
        stats_frame.columnconfigure(2, weight=1, uniform="stats")
        
        # Configure row for compact mode
        stats_frame.rowconfigure(0, weight=1)
        stats_frame.rowconfigure(1, weight=1)
        stats_frame.rowconfigure(2, weight=1)
        
        # 1. Progress Box
        self.create_progress_box(stats_frame, 0)
        
        # 2. Streak Box
        self.create_streak_box(stats_frame, 1)
        
        # 3. Monitoring Box
        self.create_monitoring_box(stats_frame, 2)
        
        # Store reference for responsive layout
        self.stats_frame = stats_frame
        
    def create_progress_box(self, parent, column):
        """Create the progress circle box"""
        # Main frame for the progress section
        progress_frame = ctk.CTkFrame(
            parent,
            fg_color=Theme.WHITE,
            corner_radius=Theme.ROUNDED_4,
            border_width=1,
            border_color=Theme.LIGHT_GRAY
        )
        progress_frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        
        # Title with fixed font size
        progress_title = ctk.CTkLabel(
            progress_frame,
            text="Progress",
            font=(Theme.FONT_FAMILY, Theme.FONT_XL, "bold"),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        progress_title.pack(anchor="w", pady=(15, 10), padx=15)
        
        # Progress circle - Using a Canvas for this
        circle_size = 100
        circle_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        circle_frame.pack(anchor="center")
        
        # Create canvas for the progress circle (using tk.Canvas as ctk has no direct equivalent)
        progress_canvas = tk.Canvas(
            circle_frame,
            width=circle_size,
            height=circle_size,
            bg=Theme.WHITE,
            highlightthickness=0
        )
        progress_canvas.pack(side="left")
        
        # Draw the progress circle (45% complete)
        # Background circle (light color)
        progress_canvas.create_oval(
            5, 5, circle_size-5, circle_size-5,
            outline=Theme.LIGHT_PURPLE,
            width=8,
            fill=Theme.WHITE
        )
        
        # Progress arc (calculated for 45%)
        progress_canvas.create_arc(
            5, 5, circle_size-5, circle_size-5,
            start=90, extent=-(45/100*360),
            outline=Theme.PRIMARY,
            width=8,
            style="arc"
        )
        
        # Progress text in the middle with fixed font size
        progress_text = progress_canvas.create_text(
            circle_size/2, 
            circle_size/2,
            text="30",
            font=(Theme.FONT_FAMILY, Theme.FONT_XL, "bold"),
            fill=Theme.BLACK
        )
        
        # Today's goal text
        goal_frame = ctk.CTkFrame(circle_frame, fg_color="transparent")
        goal_frame.pack(side="left", padx=15)
        
        goal_title = ctk.CTkLabel(
            goal_frame,
            text="Today's goal:",
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE, "bold"),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        goal_title.pack(anchor="w")
        
        goal_value = ctk.CTkLabel(
            goal_frame,
            text="Correct posture 45%",
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        goal_value.pack(anchor="w")
        
    def create_streak_box(self, parent, column):
        """Create the streak box"""
        streak_frame = ctk.CTkFrame(
            parent,
            fg_color=Theme.WHITE,
            corner_radius=Theme.ROUNDED_4,
            border_width=1,
            border_color=Theme.LIGHT_GRAY
        )
        streak_frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        
        # Title with fixed font size
        streak_title = ctk.CTkLabel(
            streak_frame,
            text="Streak",
            font=(Theme.FONT_FAMILY, Theme.FONT_XL, "bold"),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        streak_title.pack(anchor="w", pady=(15, 15), padx=15)
        
        # Current streak value with fixed font size
        streak_value = ctk.CTkLabel(
            streak_frame,
            text="256",
            font=(Theme.FONT_FAMILY, Theme.FONT_2XL, "bold"),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        streak_value.pack(anchor="w", padx=15)
        
        # Streak description with fixed font size
        streak_desc = ctk.CTkLabel(
            streak_frame,
            text="days since your first journey",
            font=(Theme.FONT_FAMILY, Theme.FONT_BASE),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        streak_desc.pack(anchor="w", padx=15, pady=(0, 15))
        
    def create_monitoring_box(self, parent, column):
        """Create the monitoring box with buttons"""
        monitoring_frame = ctk.CTkFrame(
            parent,
            fg_color=Theme.WHITE,
            corner_radius=Theme.ROUNDED_4,
            border_width=1,
            border_color=Theme.LIGHT_GRAY
        )
        monitoring_frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        
        # Title with fixed font size
        monitoring_title = ctk.CTkLabel(
            monitoring_frame,
            text="Monitoring",
            font=(Theme.FONT_FAMILY, Theme.FONT_XL, "bold"),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        monitoring_title.pack(anchor="w", pady=(15, 10), padx=15)
        
        # Recent session info
        session_frame = ctk.CTkFrame(monitoring_frame, fg_color="transparent")
        session_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        # Session text with fixed font size (using just text for simplicity)
        session_text = ctk.CTkLabel(
            session_frame,
            text=f"⏱️ Recent Session: Thu 03/02/2025 - 15:00",
            font=(Theme.FONT_FAMILY, Theme.FONT_SM),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        session_text.pack(side="left")
        
        # Button frame
        button_frame = ctk.CTkFrame(monitoring_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Start monitoring button
        start_btn = ButtonFactory.create_dark_button(
            button_frame,
            text="Start monitoring",
            command=self.start_monitoring,
            size="md",
            corner_radius=Theme.ROUNDED_6
        )
        start_btn.pack(side="left", padx=(0, 10))
        
        # View history button
        history_btn = ButtonFactory.create_outline_button(
            button_frame,
            text="View History",
            command=self.view_history,
            size="md",
            corner_radius=Theme.ROUNDED_6
        )
        history_btn.pack(side="left")
        
        # Store button references for responsive updates
        self.start_btn = start_btn
        self.history_btn = history_btn

    def create_charts_section(self):
        """Create the weekly and 7-week progress charts"""
        charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        charts_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)
        
        # Store reference for responsive adjustments
        self.charts_frame = charts_frame
        
        # Configure columns to create two equal sections
        charts_frame.columnconfigure(0, weight=1, uniform="charts")
        charts_frame.columnconfigure(1, weight=1, uniform="charts")
        charts_frame.rowconfigure(0, weight=1)
        charts_frame.rowconfigure(1, weight=1)  # Add for compact mode
        
        # Create the weekly progress chart
        self.create_weekly_chart(charts_frame, 0, "Progress this week", "pink", 
                                ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                                [63.72, 83.16, 68.1, 47.85, 31.75, 18.77, 62.41])
        
        # Create the 7-week progress chart
        self.create_weekly_chart(charts_frame, 1, "Recent 7 weeks", "purple",
                                ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7"],
                                [63.72, 83.16, 68.1, 47.85, 31.75, 18.77, 62.41])
                                
        # Give this frame the ability to expand
        self.rowconfigure(2, weight=1)
    
    def create_weekly_chart(self, parent, column, title, color, labels, values):
        """Create a chart showing weekly progress"""
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=Theme.WHITE,
            corner_radius=Theme.ROUNDED_4,
            border_width=1,
            border_color=Theme.LIGHT_GRAY
        )
        chart_frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        chart_frame.columnconfigure(0, weight=1)
        chart_frame.rowconfigure(1, weight=1)
        
        # Chart title with fixed font size
        title_label = ctk.CTkLabel(
            chart_frame,
            text=title,
            font=(Theme.FONT_FAMILY, Theme.FONT_LG, "bold"),
            text_color=Theme.BLACK,
            fg_color="transparent"
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(15, 10), padx=15)
        
        # Create frame for the chart to allow responsive resizing
        chart_container = ctk.CTkFrame(chart_frame, fg_color="transparent")
        chart_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Create matplotlib figure for the bar chart with tight_layout for better responsiveness
        fig, ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        
        # Set color based on parameter
        bar_color = "#FF6B98" if color == "pink" else "#A594F9"
        
        # Create the bar chart
        bars = ax.bar(labels, values, color=bar_color, width=0.6)
        
        # Add data labels on top of bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{value:.2f}',
                    ha='center', va='bottom', rotation=0, fontsize=8)
            
        # Customize the chart
        ax.set_ylim(0, 100)
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlabel('')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_alpha(0.3)
        ax.spines['bottom'].set_alpha(0.3)
        
        # To make chart responsive, use ctk frame
        chart_display = ctk.CTkFrame(chart_container, fg_color="transparent")
        chart_display.pack(fill="both", expand=True)
        
        # Embed the matplotlib figure in the tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=chart_display)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Store references for dynamic resizing
        chart_frame.fig = fig
        chart_frame.canvas = canvas
        chart_frame.ax = ax
    
    # Button command functions
    def start_monitoring(self):
        """Start monitoring session"""
        print("Starting monitoring session...")
        # Add your monitoring logic here
        
    def view_history(self):
        """View monitoring history"""
        print("Viewing history...")
        if hasattr(self, 'controller') and hasattr(self.controller, 'go_to_monitor'):
            self.controller.go_to_monitor()
        else:
            print("Controller not properly initialized or missing go_to_monitor method")