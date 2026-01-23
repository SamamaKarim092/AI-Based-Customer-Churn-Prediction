"""
Home/Dashboard Page
Enhanced overview with stats, charts, and quick insights.
"""

import tkinter as tk
from .base import BasePage
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS
from components.widgets import StatCard, Card


class HomePage(BasePage):
    """Enhanced dashboard home page with overview stats and insights."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.setup_page()
    
    def setup_page(self):
        """Setup the home page layout."""
        # Header with greeting
        current_hour = datetime.now().hour
        greeting = "Good Morning" if current_hour < 12 else "Good Afternoon" if current_hour < 18 else "Good Evening"
        
        self.create_header(
            f"Dashboard",
            f"{greeting}! Welcome to the AI Customer Churn Prediction System"
        )
        
        # Main content frame
        main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Stats row
        self.create_stats_section(main_frame)
        
        # Two columns layout
        columns_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        columns_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Left column
        left_col = tk.Frame(columns_frame, bg=COLORS['bg_medium'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_quick_actions(left_col)
        self.create_churn_overview(left_col)
        
        # Right column
        right_col = tk.Frame(columns_frame, bg=COLORS['bg_medium'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_model_status(right_col)
        self.create_key_insights(right_col)
        self.create_getting_started(right_col)
    
    def create_stats_section(self, parent):
        """Create enhanced stats cards row."""
        stats_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        stats_frame.pack(fill=tk.X, pady=(0, 0))
        
        stat_cards_data = [
            ("📊 Total Customers", "5,000", "In training dataset", COLORS['accent']),
            ("⚠️ Churn Rate", "40%", "Historical average", COLORS['warning']),
            ("🎯 Model Accuracy", "75.3%", "Random Forest", COLORS['success']),
            ("🔴 High Risk", "~2,000", "Need immediate attention", COLORS['danger']),
        ]
        
        for i, (title, value, subtitle, color) in enumerate(stat_cards_data):
            self.create_stat_card(stats_frame, title, value, subtitle, color, i)
    
    def create_stat_card(self, parent, title, value, subtitle, color, index):
        """Create an enhanced stat card."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0 if index == 0 else 8, 0))
        
        content = tk.Frame(card, bg=COLORS['bg_card'], padx=20, pady=15)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            content, text=title,
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(anchor=tk.W)
        
        # Value with color bar
        value_frame = tk.Frame(content, bg=COLORS['bg_card'])
        value_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Label(
            value_frame, text=value,
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_card'],
            fg=color
        ).pack(side=tk.LEFT)
        
        # Subtitle
        tk.Label(
            content, text=subtitle,
            font=FONTS['tiny'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(anchor=tk.W, pady=(5, 0))
        
        # Bottom color accent bar
        accent_bar = tk.Frame(card, bg=color, height=3)
        accent_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_quick_actions(self, parent):
        """Create quick actions section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            card, text="⚡  Quick Actions",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Action buttons in a grid
        actions_row1 = tk.Frame(content, bg=COLORS['bg_card'])
        actions_row1.pack(fill=tk.X, pady=(0, 8))
        
        actions_row2 = tk.Frame(content, bg=COLORS['bg_card'])
        actions_row2.pack(fill=tk.X)
        
        actions = [
            ("🔮 Predict", "Single prediction", 'predict', COLORS['accent'], actions_row1),
            ("📤 Upload", "Batch process", 'upload', COLORS['success'], actions_row1),
            ("📊 Analytics", "View insights", 'charts', COLORS['warning'], actions_row2),
            ("📄 Reports", "Generate PDF", 'report', COLORS['danger'], actions_row2),
        ]
        
        for title, desc, page, color, row in actions:
            self.create_action_button(row, title, desc, page, color)
    
    def create_action_button(self, parent, title, desc, page, color):
        """Create a quick action button."""
        frame = tk.Frame(parent, bg=color, cursor='hand2')
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        content = tk.Frame(frame, bg=color, padx=15, pady=12)
        content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            content, text=title,
            font=FONTS['body_bold'],
            bg=color,
            fg=COLORS['text_primary'],
            cursor='hand2'
        ).pack(anchor=tk.W)
        
        tk.Label(
            content, text=desc,
            font=FONTS['tiny'],
            bg=color,
            fg=COLORS['text_primary'],
            cursor='hand2'
        ).pack(anchor=tk.W)
        
        def on_click(e, p=page):
            self.controller.show_page(p)
        
        for widget in [frame, content] + list(content.winfo_children()):
            widget.bind('<Button-1>', on_click)
    
    def create_churn_overview(self, parent):
        """Create churn distribution overview."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            card, text="📈  Churn Distribution Overview",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Visual distribution bar
        tk.Label(
            content, text="Customer Distribution by Risk Level:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Distribution bar
        dist_frame = tk.Frame(content, bg=COLORS['bg_light'], height=40)
        dist_frame.pack(fill=tk.X)
        dist_frame.pack_propagate(False)
        
        # Risk segments (approximate from 30% churn rate)
        # High: ~15%, Moderate: ~17.5%, Low: ~67.5%
        segments = [
            (0.15, COLORS['danger'], "High 15%"),
            (0.175, COLORS['warning'], "Med 17.5%"),
            (0.675, COLORS['success'], "Low 67.5%"),
        ]
        
        x_pos = 0
        for width, color, label in segments:
            seg = tk.Frame(dist_frame, bg=color)
            seg.place(relx=x_pos, relwidth=width, relheight=1)
            
            if width > 0.1:  # Only show label if segment is wide enough
                tk.Label(
                    seg, text=label,
                    font=('Segoe UI', 8, 'bold'),
                    bg=color,
                    fg=COLORS['text_primary']
                ).pack(expand=True)
            x_pos += width
        
        # Legend
        legend_frame = tk.Frame(content, bg=COLORS['bg_card'])
        legend_frame.pack(fill=tk.X, pady=(15, 0))
        
        legends = [
            ("🔴 High Risk", "750 customers", COLORS['danger']),
            ("🟡 Moderate Risk", "875 customers", COLORS['warning']),
            ("🟢 Low Risk", "3,375 customers", COLORS['success']),
        ]
        
        for label, count, color in legends:
            leg_item = tk.Frame(legend_frame, bg=COLORS['bg_card'])
            leg_item.pack(side=tk.LEFT, expand=True)
            
            tk.Label(
                leg_item, text=label,
                font=FONTS['small'],
                bg=COLORS['bg_card'],
                fg=color
            ).pack()
            
            tk.Label(
                leg_item, text=count,
                font=FONTS['tiny'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_muted']
            ).pack()
        
        # Key metrics
        metrics_frame = tk.Frame(content, bg=COLORS['bg_light'], padx=15, pady=10)
        metrics_frame.pack(fill=tk.X, pady=(15, 0))
        
        metrics = [
            ("Avg. Churn Probability", "30%"),
            ("Predicted Churners", "~1,500"),
            ("Retention Opportunity", "$16,250/mo"),
        ]
        
        for label, value in metrics:
            row = tk.Frame(metrics_frame, bg=COLORS['bg_light'])
            row.pack(fill=tk.X, pady=2)
            
            tk.Label(
                row, text=label,
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_secondary']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=value,
                font=FONTS['body_bold'],
                bg=COLORS['bg_light'],
                fg=COLORS['accent']
            ).pack(side=tk.RIGHT)
    
    def create_model_status(self, parent):
        """Create model status section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title row
        title_row = tk.Frame(card, bg=COLORS['bg_card'])
        title_row.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_row, text="🤖  Model Status",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(side=tk.LEFT)
        
        # Status badge
        tk.Label(
            title_row, text="● Active",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['bg_card'],
            fg=COLORS['success']
        ).pack(side=tk.RIGHT)
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Model info grid
        info = [
            ("Algorithm", "Random Forest", COLORS['accent']),
            ("Accuracy", "75.3%", COLORS['success']),
            ("Precision", "72.2%", COLORS['success']),
            ("Last Trained", "January 2026", COLORS['text_secondary']),
        ]
        
        for label, value, color in info:
            row = tk.Frame(content, bg=COLORS['bg_card'])
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(
                row, text=label + ":",
                font=FONTS['small'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_muted'],
                width=12,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=value,
                font=FONTS['body_bold'],
                bg=COLORS['bg_card'],
                fg=color
            ).pack(side=tk.LEFT)
    
    def create_key_insights(self, parent):
        """Create key insights section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            card, text="💡  Key Insights",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        insights = [
            ("📅 Last Login", "Most important churn predictor", COLORS['danger']),
            ("💳 Payment Failures", "Strong churn indicator", COLORS['warning']),
            ("📱 Login Frequency", "Lower = Higher risk", COLORS['warning']),
            ("⏱️ New Customers", "Higher churn tendency", COLORS['accent']),
        ]
        
        for icon_text, insight, color in insights:
            row = tk.Frame(content, bg=COLORS['bg_light'], padx=10, pady=8)
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(
                row, text=icon_text,
                font=FONTS['body_bold'],
                bg=COLORS['bg_light'],
                fg=color
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=f" — {insight}",
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_secondary']
            ).pack(side=tk.LEFT)
    
    def create_getting_started(self, parent):
        """Create getting started section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            card, text="🚀  Getting Started",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        steps = [
            ("1️⃣", "Predict", "Analyze individual customer churn risk"),
            ("2️⃣", "Upload", "Batch process CSV files for predictions"),
            ("3️⃣", "Analytics", "Explore model performance & insights"),
            ("4️⃣", "Reports", "Generate PDF reports to share"),
        ]
        
        for num, action, desc in steps:
            row = tk.Frame(content, bg=COLORS['bg_card'])
            row.pack(fill=tk.X, pady=4)
            
            tk.Label(
                row, text=num,
                font=('Segoe UI', 12),
                bg=COLORS['bg_card'],
                fg=COLORS['accent']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=f" {action}",
                font=FONTS['body_bold'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_primary']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=f" — {desc}",
                font=FONTS['small'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_secondary']
            ).pack(side=tk.LEFT)
