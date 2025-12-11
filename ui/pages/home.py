"""
Home/Dashboard Page
Overview and quick stats display.
"""

import tkinter as tk
from .base import BasePage
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS
from components.widgets import StatCard, Card


class HomePage(BasePage):
    """Dashboard home page with overview stats."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.setup_page()
    
    def setup_page(self):
        """Setup the home page layout."""
        # Header
        self.create_header(
            "Dashboard",
            "Welcome to the Customer Churn Prediction System"
        )
        
        # Stats row
        stats_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        stats_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        # Stat cards
        stat_cards_data = [
            ("Total Customers", "1,000", "In training dataset", ICONS['user'], COLORS['accent']),
            ("Churn Rate", "32.5%", "Historical average", ICONS['warning'], COLORS['warning']),
            ("Model Accuracy", "72.5%", "Current model", ICONS['chart'], COLORS['success']),
            ("High Risk", "~325", "Customers at risk", ICONS['error'], COLORS['danger']),
        ]
        
        for i, (title, value, subtitle, icon, color) in enumerate(stat_cards_data):
            card = StatCard(
                stats_frame, title, value, subtitle, icon, color,
                colors=COLORS
            )
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0 if i == 0 else 10, 0))
        
        # Content area
        content_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Left column - Quick Actions
        left_col = tk.Frame(content_frame, bg=COLORS['bg_medium'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Quick Actions Card
        actions_card, actions_content = self.create_card(left_col, "Quick Actions", ICONS['arrow_right'])
        actions_card.pack(fill=tk.X, pady=(0, 15))
        
        actions = [
            ("🔮 Make a Prediction", "Predict churn for a customer", 'predict'),
            ("📤 Upload Customer Data", "Batch process CSV files", 'upload'),
            ("📊 View Analytics", "Charts and visualizations", 'charts'),
            ("📄 Generate Report", "Export PDF report", 'report'),
        ]
        
        for title, desc, page in actions:
            self.create_action_item(actions_content, title, desc, page)
        
        # Recent Activity Card
        activity_card, activity_content = self.create_card(left_col, "Recent Activity", ICONS['refresh'])
        activity_card.pack(fill=tk.BOTH, expand=True)
        
        activities = [
            ("Model trained successfully", "2 minutes ago", COLORS['success']),
            ("Dataset loaded (1000 records)", "5 minutes ago", COLORS['accent']),
            ("Application started", "Just now", COLORS['text_secondary']),
        ]
        
        for text, time, color in activities:
            self.create_activity_item(activity_content, text, time, color)
        
        # Right column - System Info
        right_col = tk.Frame(content_frame, bg=COLORS['bg_medium'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Model Info Card
        model_card, model_content = self.create_card(right_col, "Model Information", ICONS['info'])
        model_card.pack(fill=tk.X, pady=(0, 15))
        
        model_info = [
            ("Algorithm", "Logistic Regression"),
            ("Features", "10 customer attributes"),
            ("Training Samples", "800 (80%)"),
            ("Test Samples", "200 (20%)"),
            ("Last Updated", "December 2025"),
        ]
        
        for label, value in model_info:
            self.create_info_row(model_content, label, value)
        
        # Tips Card
        tips_card, tips_content = self.create_card(right_col, "Getting Started", "💡")
        tips_card.pack(fill=tk.BOTH, expand=True)
        
        tips_text = """Welcome to the AI Customer Churn Prediction System!

This tool helps you:
• Predict which customers might leave
• Understand WHY they might churn
• Get actionable recommendations

Quick Start:
1. Go to 'Predict' to analyze a customer
2. Use 'Upload Data' for batch predictions
3. Check 'Analytics' for insights
4. Generate reports in 'Reports' section"""
        
        tk.Label(
            tips_content,
            text=tips_text,
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            justify=tk.LEFT,
            anchor=tk.NW
        ).pack(fill=tk.BOTH, expand=True)
    
    def create_action_item(self, parent, title, description, page):
        """Create an action item button."""
        frame = tk.Frame(parent, bg=COLORS['bg_card'], cursor='hand2')
        frame.pack(fill=tk.X, pady=5)
        
        inner = tk.Frame(frame, bg=COLORS['bg_light'], padx=15, pady=12)
        inner.pack(fill=tk.X)
        
        tk.Label(
            inner, text=title,
            font=FONTS['body_bold'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W)
        
        tk.Label(
            inner, text=description,
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary']
        ).pack(anchor=tk.W)
        
        # Hover effects
        def on_enter(e):
            inner.config(bg=COLORS['sidebar_hover'])
            for child in inner.winfo_children():
                child.config(bg=COLORS['sidebar_hover'])
        
        def on_leave(e):
            inner.config(bg=COLORS['bg_light'])
            for child in inner.winfo_children():
                child.config(bg=COLORS['bg_light'])
        
        def on_click(e, p=page):
            self.controller.show_page(p)
        
        for widget in [frame, inner] + list(inner.winfo_children()):
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', on_click)
    
    def create_activity_item(self, parent, text, time, color):
        """Create an activity log item."""
        frame = tk.Frame(parent, bg=COLORS['bg_card'])
        frame.pack(fill=tk.X, pady=5)
        
        # Color indicator
        indicator = tk.Frame(frame, bg=color, width=4)
        indicator.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Content
        content = tk.Frame(frame, bg=COLORS['bg_card'])
        content.pack(fill=tk.X)
        
        tk.Label(
            content, text=text,
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W)
        
        tk.Label(
            content, text=time,
            font=FONTS['tiny'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(anchor=tk.W)
    
    def create_info_row(self, parent, label, value):
        """Create an info row with label and value."""
        frame = tk.Frame(parent, bg=COLORS['bg_card'])
        frame.pack(fill=tk.X, pady=4)
        
        tk.Label(
            frame, text=label + ":",
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        tk.Label(
            frame, text=value,
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(side=tk.LEFT)
