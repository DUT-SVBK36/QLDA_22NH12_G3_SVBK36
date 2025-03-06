import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import sys
import os

# Assuming these imports work with your project structure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _config.theme import Theme
from components.button import ButtonFactory, ModernButton

class Dashboard(tk.Frame):
    def __init__(self, parent, **kwargs):
        kwargs["bg"] = Theme.QUARTERNARY
        super().__init__(parent, **kwargs)
        
        # Set up responsive grid
        self.columnconfigure(0, weight=1)
        
        # Track display mode (normal or compact)
        self.is_compact = False
        self.font_scale_factor = 1.0
        
        # Store widget references for responsive updates
        self.responsive_widgets = {
            'headers': [],
            'normal_text': [],
            'small_text': []
        }
        
        # Create the dashboard layout
        self.create_welcome_section()
        self.create_stats_section()
        self.create_charts_section()
        
        # Bind resize event to handle responsive updates
        self.bind("<Configure>", self.on_resize)
        
    def on_resize(self, event):
        """Handle resize events to adapt the UI to different screen sizes"""
        width = event.width
        
        # Determine if we should switch to compact mode
        is_compact = width < 900
        font_scale = self.calculate_font_scale(width)
        layout_changed = False
        
        # Check if compact status changed
        if hasattr(self, 'is_compact') and self.is_compact != is_compact:
            self.is_compact = is_compact
            self.update_layout_for_size(is_compact)
            layout_changed = True
            
        # Check if font scale changed significantly
        if abs(font_scale - self.font_scale_factor) > 0.05:  # Only update if change is significant
            self.font_scale_factor = font_scale
            self.update_font_sizes()
            layout_changed = True
            
        # If layout changed, update matplotlib charts for new size
        if layout_changed and hasattr(self, 'charts_frame'):
            self.after(100, self.update_chart_sizes)  # Delay to let layout settle
    
    def calculate_font_scale(self, width):
        """Calculate a font scaling factor based on window width"""
        # Base width for 100% scale
        base_width = 1200
        
        # Calculate scale factor (min 0.7, max 1.2)
        scale = max(0.7, min(1.2, width / base_width))
        
        return scale
    
    def update_font_sizes(self):
        """Update font sizes of responsive widgets based on scale factor"""
        # Update header fonts
        for widget_info in self.responsive_widgets['headers']:
            widget = widget_info['widget']
            base_size = widget_info['base_size']
            new_size = int(base_size * self.font_scale_factor)
            widget.configure(font=Theme.get_font(new_size, widget_info.get('weight', 'bold')))
            
        # Update normal text fonts
        for widget_info in self.responsive_widgets['normal_text']:
            widget = widget_info['widget']
            base_size = widget_info['base_size']
            new_size = int(base_size * self.font_scale_factor)
            widget.configure(font=Theme.get_font(new_size, widget_info.get('weight', 'normal')))
            
        # Update small text fonts
        for widget_info in self.responsive_widgets['small_text']:
            widget = widget_info['widget']
            base_size = widget_info['base_size']
            new_size = int(base_size * self.font_scale_factor)
            widget.configure(font=Theme.get_font(new_size, widget_info.get('weight', 'normal')))
    
    def register_responsive_widget(self, widget, category, base_size, weight='normal'):
        """Register a widget for responsive font sizing"""
        self.responsive_widgets[category].append({
            'widget': widget,
            'base_size': base_size,
            'weight': weight
        })
        return widget
    
    def update_layout_for_size(self, is_compact):
        """Update layout based on available width"""
        if is_compact:
            # Compact layout adjustments
            if hasattr(self, 'charts_frame'):
                for widget in self.charts_frame.grid_slaves():
                    # Stack charts vertically in compact mode
                    if int(widget.grid_info()['column']) == 1:
                        widget.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
                        
            # Make stats section stack vertically in very compact mode
            if hasattr(self, 'stats_frame') and self.winfo_width() < 600:
                for i, widget in enumerate(self.stats_frame.grid_slaves()):
                    widget.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
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
    
    def update_chart_sizes(self):
        """Update chart sizes after resize"""
        if hasattr(self, 'charts_frame'):
            for widget in self.charts_frame.grid_slaves():
                if hasattr(widget, 'canvas'):
                    widget.canvas.draw()  # Redraw the canvas to fit new size
    
    def create_welcome_section(self):
        """Create the welcome section at the top of the dashboard"""
        welcome_frame = tk.Frame(self, bg=Theme.WHITE, padx=20, pady=15)
        welcome_frame.grid(row=0, column=0, sticky="ew")
        welcome_frame.columnconfigure(0, weight=1)
        
        # Welcome title (responsive font)
        welcome_label = self.register_responsive_widget(
            tk.Label(
                welcome_frame, 
                text="Welcome back, Resolved",
                font=Theme.get_font(Theme.FONT_BASE+12, weight="bold"),
                bg=Theme.WHITE, 
                fg=Theme.BLACK
            ),
            'headers',
            Theme.FONT_BASE+12,
            'bold'
        )
        welcome_label.grid(row=0, column=0, sticky="w")
        
        # Stats subtitle (responsive font)
        stats_label = self.register_responsive_widget(
            tk.Label(
                welcome_frame, 
                text="Check your daily stats here",
                font=Theme.get_font(Theme.FONT_BASE),
                bg=Theme.WHITE, 
                fg=Theme.BLACK
            ),
            'normal_text',
            Theme.FONT_BASE
        )
        stats_label.grid(row=1, column=0, sticky="w")
        
    def create_stats_section(self):
        """Create the three stat boxes: Progress, Streak, and Monitoring"""
        stats_frame = tk.Frame(self, bg=Theme.WHITE, padx=15, pady=10)
        stats_frame.grid(row=1, column=0, sticky="ew")
        
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
        progress_frame = tk.Frame(
            parent,
            bg=Theme.WHITE,
            highlightbackground=Theme.LIGHT_GRAY,
            highlightthickness=1,
            padx=15,
            pady=15,
            borderwidth=0
        )
        progress_frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        
        # Title (responsive font)
        progress_title = self.register_responsive_widget(
            tk.Label(
                progress_frame,
                text="Progress",
                font=Theme.get_font(Theme.FONT_BASE+4, weight="bold"),
                bg=Theme.WHITE,
                fg=Theme.BLACK
            ),
            'headers',
            Theme.FONT_BASE+4,
            'bold'
        )
        progress_title.pack(anchor="w", pady=(0, 10))
        
        # Progress circle - Using a Canvas for this
        circle_size = 100
        circle_frame = tk.Frame(progress_frame, bg=Theme.WHITE)
        circle_frame.pack(anchor="center")
        
        # Create canvas for the progress circle
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
        
        # Progress text in the middle (responsive)
        progress_text = progress_canvas.create_text(
            circle_size/2, 
            circle_size/2,
            text="30",
            font=Theme.get_font(Theme.FONT_BASE+8, weight="bold"),
            fill=Theme.BLACK
        )
        
        # Store reference for responsive updates
        progress_canvas.progress_text = progress_text
        self.responsive_widgets['headers'].append({
            'widget': progress_canvas,
            'base_size': Theme.FONT_BASE+8,
            'weight': 'bold',
            'text_id': progress_text,
            'is_canvas': True
        })
        
        # Today's goal text
        goal_frame = tk.Frame(circle_frame, bg=Theme.WHITE)
        goal_frame.pack(side="left", padx=15)
        
        goal_title = self.register_responsive_widget(
            tk.Label(
                goal_frame,
                text="Today's goal:",
                font=Theme.get_font(Theme.FONT_BASE+2, weight="bold"),
                bg=Theme.WHITE,
                fg=Theme.BLACK
            ),
            'normal_text',
            Theme.FONT_BASE+2,
            'bold'
        )
        goal_title.pack(anchor="w")
        
        goal_value = self.register_responsive_widget(
            tk.Label(
                goal_frame,
                text="Correct posture 45%",
                font=Theme.get_font(Theme.FONT_BASE),
                bg=Theme.WHITE,
                fg=Theme.BLACK
            ),
            'normal_text',
            Theme.FONT_BASE
        )
        goal_value.pack(anchor="w")
        
    def create_streak_box(self, parent, column):
        """Create the streak box"""
        streak_frame = tk.Frame(
            parent,
            bg=Theme.WHITE,
            highlightbackground=Theme.LIGHT_GRAY,
            highlightthickness=1,
            padx=15,
            pady=15,
            borderwidth=0
        )
        streak_frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        
        # Title (responsive)
        streak_title = self.register_responsive_widget(
            tk.Label(
                streak_frame,
                text="Streak",
                font=Theme.get_font(Theme.FONT_BASE+4, weight="bold"),
                bg=Theme.WHITE,
                fg=Theme.BLACK
            ),
            'headers',
            Theme.FONT_BASE+4,
            'bold'
        )
        streak_title.pack(anchor="w", pady=(0, 15))
        
        # Current streak value (responsive)
        streak_value = self.register_responsive_widget(
            tk.Label(
                streak_frame,
                text="256",
                font=Theme.get_font(40, weight="bold"),
                bg=Theme.WHITE,
                fg=Theme.BLACK
            ),
            'headers',
            40,
            'bold'
        )
        streak_value.pack(anchor="w")
        
        # Streak description (responsive)
        streak_desc = self.register_responsive_widget(
            tk.Label(
                streak_frame,
                text="days since your first journey",
                font=Theme.get_font(Theme.FONT_BASE),
                bg=Theme.WHITE,
                fg=Theme.BLACK
            ),
            'normal_text',
            Theme.FONT_BASE
        )
        streak_desc.pack(anchor="w")
        
    def create_monitoring_box(self, parent, column):
        """Create the monitoring box with buttons"""
        monitoring_frame = tk.Frame(
            parent,
            bg=Theme.WHITE,
            highlightbackground=Theme.LIGHT_GRAY,
            highlightthickness=1,
            padx=15,
            pady=15,
            borderwidth=0
        )
        monitoring_frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        
        # Title (responsive)
        monitoring_title = self.register_responsive_widget(
            tk.Label(
                monitoring_frame,
                text="Monitoring",
                font=Theme.get_font(Theme.FONT_BASE+4, weight="bold"),
                bg=Theme.WHITE,
                fg=Theme.BLACK
            ),
            'headers',
            Theme.FONT_BASE+4,
            'bold'
        )
        monitoring_title.pack(anchor="w", pady=(0, 10))
        
        # Recent session info
        session_frame = tk.Frame(monitoring_frame, bg=Theme.WHITE)
        session_frame.pack(fill="x", pady=(0, 15))
        
        # Clock icon (using a placeholder circle)
        clock_canvas = tk.Canvas(
            session_frame,
            width=20,
            height=20,
            bg=Theme.WHITE,
            highlightthickness=0
        )
        clock_canvas.pack(side="left")
        clock_canvas.create_oval(2, 2, 18, 18, outline=Theme.BLACK, width=1)
        clock_canvas.create_line(10, 10, 10, 5, fill=Theme.BLACK, width=1)
        clock_canvas.create_line(10, 10, 14, 12, fill=Theme.BLACK, width=1)
        
        # Session text (responsive)
        session_text = self.register_responsive_widget(
            tk.Label(
                session_frame,
                text=f"Recent Session: Thu 03/02/2025 - 15:00",
                font=Theme.get_font(Theme.FONT_SM),
                bg=Theme.WHITE,
                fg=Theme.BLACK,
                padx=5
            ),
            'normal_text',
            Theme.FONT_XS
        )
        session_text.pack(side="left")
        
        # Button frame
        button_frame = tk.Frame(monitoring_frame, bg=Theme.WHITE)
        button_frame.pack(fill="x")
        
        # Start monitoring button
        start_btn = ButtonFactory.create_dark_button(
            button_frame,
            text="Start monitoring",
            command=self.start_monitoring,
            size="sm" if self.is_compact else "md"
        )
        start_btn.pack(side="left", padx=(0, 10))
        
        # View history button
        history_btn = ButtonFactory.create_outline_button(
            button_frame,
            text="View History",
            command=self.view_history,
            size="sm" if self.is_compact else "md"
        )
        history_btn.pack(side="left")
        
        # Store button references for responsive updates
        self.start_btn = start_btn
        self.history_btn = history_btn

    # Rest of the code (create_charts_section and create_weekly_chart) with responsive updates...
    def create_charts_section(self):
        """Create the weekly and 7-week progress charts"""
        charts_frame = tk.Frame(self, bg=Theme.WHITE, padx=15, pady=10)
        charts_frame.grid(row=2, column=0, sticky="nsew")
        
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
        chart_frame = tk.Frame(
            parent,
            bg=Theme.WHITE,
            highlightbackground=Theme.LIGHT_GRAY,
            highlightthickness=1,
            padx=15,
            pady=15,
            borderwidth=0
        )
        chart_frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        chart_frame.columnconfigure(0, weight=1)
        chart_frame.rowconfigure(1, weight=1)
        
        # Chart title (responsive)
        title_label = self.register_responsive_widget(
            tk.Label(
                chart_frame,
                text=title,
                font=Theme.get_font(Theme.FONT_BASE+2, weight="bold"),
                bg=Theme.WHITE,
                fg=Theme.BLACK
            ),
            'headers',
            Theme.FONT_BASE+2,
            'bold'
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Create frame for the chart to allow responsive resizing
        chart_container = tk.Frame(chart_frame, bg=Theme.WHITE)
        chart_container.grid(row=1, column=0, sticky="nsew")
        
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
        
        # Adjust font sizes based on current scale
        if hasattr(self, 'font_scale_factor'):
            for text in ax.get_xticklabels() + ax.get_yticklabels():
                text.set_fontsize(8 * self.font_scale_factor)
        
        # To make chart responsive, we need to create a special frame that will resize the chart
        chart_display = tk.Frame(chart_container, bg=Theme.WHITE)
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
            
    def update_button_sizes(self):
        """Update button sizes based on current mode"""
        if hasattr(self, 'start_btn') and hasattr(self, 'history_btn'):
            size = "xs" if self.is_compact and self.font_scale_factor < 0.85 else "sm" if self.is_compact else "md"
            
            # These methods would need to be implemented in ModernButton
            if hasattr(self.start_btn, 'update_size'):
                self.start_btn.update_size(size)
                self.history_btn.update_size(size)