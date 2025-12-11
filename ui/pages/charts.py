"""
Charts/Analytics Page
Visualizations and analytics display.
"""

import tkinter as tk
from .base import BasePage
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS


class ChartsPage(BasePage):
    """Analytics and charts page."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.setup_page()
    
    def setup_page(self):
        """Setup the charts page."""
        # Header
        self.create_header(
            "Analytics",
            "Visualizations and insights from your data"
        )
        
        # Main content
        main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Top row - Summary charts
        top_row = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        top_row.pack(fill=tk.X, pady=(0, 15))
        
        # Churn distribution chart
        self.create_pie_chart(top_row, "Churn Distribution", {
            "Stayed": 67.5,
            "Churned": 32.5
        })
        
        # Subscription distribution chart
        self.create_pie_chart(top_row, "Subscription Types", {
            "Basic": 40.8,
            "Standard": 35.1,
            "Premium": 24.1
        })
        
        # Risk distribution chart
        self.create_pie_chart(top_row, "Risk Levels", {
            "Low Risk": 45,
            "Moderate": 30,
            "High Risk": 25
        })
        
        # Bottom row - Detailed analytics
        bottom_row = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        bottom_row.pack(fill=tk.BOTH, expand=True)
        
        # Left - Feature importance
        left_card = tk.Frame(bottom_row, bg=COLORS['bg_card'])
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_feature_importance(left_card)
        
        # Right - Model metrics
        right_card = tk.Frame(bottom_row, bg=COLORS['bg_card'])
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_model_metrics(right_card)
    
    def create_pie_chart(self, parent, title, data):
        """Create a simple pie chart visualization."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Title
        tk.Label(
            card, text=title,
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # Canvas for pie chart
        canvas = tk.Canvas(
            card, width=200, height=180,
            bg=COLORS['bg_card'], highlightthickness=0
        )
        canvas.pack(pady=(0, 15))
        
        # Draw simple pie representation
        colors = [COLORS['success'], COLORS['danger'], COLORS['warning'], COLORS['accent']]
        total = sum(data.values())
        start_angle = 90
        
        center_x, center_y = 100, 80
        radius = 60
        
        for i, (label, value) in enumerate(data.items()):
            extent = (value / total) * 360
            color = colors[i % len(colors)]
            
            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=-extent,
                fill=color, outline=COLORS['bg_card'], width=2
            )
            start_angle -= extent
        
        # Legend
        legend_y = 160
        x_offset = 30
        for i, (label, value) in enumerate(data.items()):
            color = colors[i % len(colors)]
            canvas.create_rectangle(
                x_offset, legend_y - 5,
                x_offset + 10, legend_y + 5,
                fill=color, outline=''
            )
            canvas.create_text(
                x_offset + 15, legend_y,
                text=f"{label}: {value:.1f}%",
                anchor=tk.W,
                fill=COLORS['text_secondary'],
                font=('Segoe UI', 8)
            )
            x_offset += 70
    
    def create_feature_importance(self, parent):
        """Create feature importance display."""
        # Title
        tk.Label(
            parent, text="📊  Feature Importance",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(parent, bg=COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Feature importance bars
        features = [
            ("Last Login Days", 0.25, COLORS['danger']),
            ("Payment Failures", 0.20, COLORS['danger']),
            ("Login Frequency", 0.15, COLORS['warning']),
            ("Watch Time", 0.12, COLORS['warning']),
            ("Tenure", 0.10, COLORS['success']),
            ("Support Calls", 0.08, COLORS['text_muted']),
            ("Monthly Charges", 0.05, COLORS['text_muted']),
            ("Age", 0.03, COLORS['text_muted']),
            ("Subscription Type", 0.02, COLORS['text_muted']),
        ]
        
        for feature, importance, color in features:
            self.create_importance_bar(content, feature, importance, color)
    
    def create_importance_bar(self, parent, label, value, color):
        """Create a single importance bar."""
        frame = tk.Frame(parent, bg=COLORS['bg_card'])
        frame.pack(fill=tk.X, pady=3)
        
        # Label
        tk.Label(
            frame, text=label, width=18, anchor=tk.W,
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(side=tk.LEFT)
        
        # Bar container
        bar_container = tk.Frame(frame, bg=COLORS['bg_light'], height=16)
        bar_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        bar_container.pack_propagate(False)
        
        # Bar
        bar_width = int(value * 200)
        bar = tk.Frame(bar_container, bg=color, width=bar_width, height=16)
        bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Value
        tk.Label(
            frame, text=f"{value*100:.0f}%", width=5,
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=color
        ).pack(side=tk.LEFT)
    
    def create_model_metrics(self, parent):
        """Create model metrics display."""
        # Title
        tk.Label(
            parent, text="📈  Model Performance",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(parent, bg=COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Metrics
        metrics = [
            ("Accuracy", "72.5%", COLORS['success']),
            ("Precision", "63.9%", COLORS['warning']),
            ("Recall", "35.4%", COLORS['warning']),
            ("F1-Score", "45.5%", COLORS['warning']),
        ]
        
        for metric, value, color in metrics:
            self.create_metric_row(content, metric, value, color)
        
        # Confusion matrix
        tk.Label(
            content, text="\nConfusion Matrix:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(15, 5))
        
        matrix_text = """
                    Predicted
                   Stay  Churn
   Actual Stay     122    13
   Actual Churn     42    23
        """
        
        tk.Label(
            content, text=matrix_text,
            font=FONTS['mono_small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            justify=tk.LEFT
        ).pack(anchor=tk.W)
    
    def create_metric_row(self, parent, label, value, color):
        """Create a metric display row."""
        frame = tk.Frame(parent, bg=COLORS['bg_card'])
        frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            frame, text=label, width=12, anchor=tk.W,
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            frame, text=value,
            font=FONTS['heading'],
            bg=COLORS['bg_card'],
            fg=color
        ).pack(side=tk.LEFT, padx=10)
