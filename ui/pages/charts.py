"""
Charts/Analytics Page
Model training info, performance metrics, and data visualizations.
"""

import tkinter as tk
from tkinter import ttk
from .base import BasePage
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS


class ChartsPage(BasePage):
    """Analytics and charts page with model information."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.setup_page()
    
    def setup_page(self):
        """Setup the analytics page."""
        # Header
        self.create_header(
            "Model Analytics",
            "Training details, performance metrics, and data insights"
        )
        
        # Main content
        main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Model Info Section
        self.create_model_info_section(main_frame)
        
        # Two columns layout
        columns_frame = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        columns_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Left column - Model Performance & Comparison
        left_col = tk.Frame(columns_frame, bg=COLORS['bg_medium'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_model_performance(left_col)
        self.create_model_comparison(left_col)
        
        # Right column - Feature Importance & Data Stats
        right_col = tk.Frame(columns_frame, bg=COLORS['bg_medium'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_feature_importance(right_col)
        self.create_data_statistics(right_col)
    
    def create_model_info_section(self, parent):
        """Create the model training information section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            card, text="🤖  Model Training Information",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # Info cards container
        info_frame = tk.Frame(card, bg=COLORS['bg_card'])
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Model info items
        info_items = [
            ("🎯", "Model Type", "Logistic Regression", COLORS['accent']),
            ("📊", "Training Data", "1,000 customers", COLORS['success']),
            ("🔢", "Features", "10 features", COLORS['warning']),
            ("📅", "Train Date", "December 2025", COLORS['text_secondary']),
            ("⚡", "Train/Test Split", "80% / 20%", COLORS['accent']),
            ("🎲", "Random State", "42", COLORS['text_muted']),
        ]
        
        # Create 3 items per row
        for i in range(0, len(info_items), 3):
            row = tk.Frame(info_frame, bg=COLORS['bg_card'])
            row.pack(fill=tk.X, pady=5)
            
            for icon, label, value, color in info_items[i:i+3]:
                item_frame = tk.Frame(row, bg=COLORS['bg_light'], padx=15, pady=10)
                item_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
                
                # Icon and label
                header_frame = tk.Frame(item_frame, bg=COLORS['bg_light'])
                header_frame.pack(fill=tk.X)
                
                tk.Label(
                    header_frame, text=f"{icon} {label}",
                    font=FONTS['small'],
                    bg=COLORS['bg_light'],
                    fg=COLORS['text_muted']
                ).pack(anchor=tk.W)
                
                tk.Label(
                    item_frame, text=value,
                    font=FONTS['body_bold'],
                    bg=COLORS['bg_light'],
                    fg=color
                ).pack(anchor=tk.W, pady=(2, 0))
        
        # Algorithms tested
        algo_frame = tk.Frame(card, bg=COLORS['bg_card'])
        algo_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(
            algo_frame, text="Algorithms Tested:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(side=tk.LEFT)
        
        algorithms = ["Logistic Regression ✓", "Naive Bayes", "Random Forest"]
        for algo in algorithms:
            is_selected = "✓" in algo
            tk.Label(
                algo_frame, text=algo.replace(" ✓", ""),
                font=FONTS['small'],
                bg=COLORS['accent'] if is_selected else COLORS['bg_light'],
                fg=COLORS['text_primary'] if is_selected else COLORS['text_muted'],
                padx=10, pady=3
            ).pack(side=tk.LEFT, padx=5)
    
    def create_model_performance(self, parent):
        """Create model performance metrics section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            card, text="📈  Performance Metrics",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Main metrics with visual bars
        metrics = [
            ("Accuracy", 72.5, COLORS['success'], "Overall correct predictions"),
            ("Precision", 63.9, COLORS['warning'], "Correct churn predictions"),
            ("Recall", 35.4, COLORS['warning'], "Churners correctly identified"),
            ("F1-Score", 45.5, COLORS['accent'], "Balance of precision & recall"),
        ]
        
        for metric, value, color, desc in metrics:
            frame = tk.Frame(content, bg=COLORS['bg_card'])
            frame.pack(fill=tk.X, pady=5)
            
            # Metric label
            label_frame = tk.Frame(frame, bg=COLORS['bg_card'])
            label_frame.pack(fill=tk.X)
            
            tk.Label(
                label_frame, text=metric, width=12, anchor=tk.W,
                font=FONTS['body_bold'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_primary']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                label_frame, text=f"{value:.1f}%",
                font=FONTS['heading'],
                bg=COLORS['bg_card'],
                fg=color
            ).pack(side=tk.LEFT, padx=10)
            
            tk.Label(
                label_frame, text=desc,
                font=FONTS['small'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_muted']
            ).pack(side=tk.RIGHT)
            
            # Progress bar
            bar_frame = tk.Frame(frame, bg=COLORS['bg_light'], height=8)
            bar_frame.pack(fill=tk.X, pady=(3, 0))
            bar_frame.pack_propagate(False)
            
            bar = tk.Frame(bar_frame, bg=color, height=8)
            bar.place(relwidth=value/100, relheight=1)
        
        # Confusion Matrix
        tk.Label(
            content, text="\n📊 Confusion Matrix",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(10, 5))
        
        matrix_frame = tk.Frame(content, bg=COLORS['bg_light'])
        matrix_frame.pack(fill=tk.X, pady=5)
        
        # Create matrix grid
        matrix_data = [
            ["", "Predicted\nStay", "Predicted\nChurn"],
            ["Actual Stay", "122 ✓", "13"],
            ["Actual Churn", "42", "23 ✓"],
        ]
        
        for i, row_data in enumerate(matrix_data):
            row = tk.Frame(matrix_frame, bg=COLORS['bg_light'])
            row.pack(fill=tk.X)
            for j, cell in enumerate(row_data):
                is_header = i == 0 or j == 0
                is_correct = "✓" in cell
                
                if is_correct:
                    bg_color = COLORS['success']
                    fg_color = COLORS['text_primary']
                elif is_header:
                    bg_color = COLORS['bg_light']
                    fg_color = COLORS['text_secondary']
                else:
                    bg_color = COLORS['danger']
                    fg_color = COLORS['text_primary']
                
                cell_label = tk.Label(
                    row, text=cell.replace(" ✓", ""),
                    font=FONTS['small'] if is_header else FONTS['body_bold'],
                    bg=bg_color, fg=fg_color,
                    width=12, height=2,
                    relief=tk.FLAT
                )
                cell_label.pack(side=tk.LEFT, padx=1, pady=1)
    
    def create_model_comparison(self, parent):
        """Create model comparison table."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            card, text="⚖️  Model Comparison",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Comparison data
        models = [
            ("Logistic Regression", 72.5, 63.9, 35.4, 45.5, True),
            ("Random Forest", 71.0, 58.1, 36.9, 45.1, False),
            ("Naive Bayes", 62.0, 40.4, 47.7, 43.8, False),
        ]
        
        # Header
        header = tk.Frame(content, bg=COLORS['bg_light'])
        header.pack(fill=tk.X, pady=(0, 5))
        
        headers = ["Model", "Accuracy", "Precision", "Recall", "F1-Score"]
        widths = [20, 10, 10, 10, 10]
        
        for h, w in zip(headers, widths):
            tk.Label(
                header, text=h, width=w,
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_muted']
            ).pack(side=tk.LEFT, padx=2, pady=5)
        
        # Data rows
        for model, acc, prec, rec, f1, is_best in models:
            row = tk.Frame(content, bg=COLORS['bg_card'])
            row.pack(fill=tk.X, pady=2)
            
            # Model name
            name_text = f"⭐ {model}" if is_best else f"   {model}"
            tk.Label(
                row, text=name_text, width=20, anchor=tk.W,
                font=FONTS['body_bold'] if is_best else FONTS['body'],
                bg=COLORS['bg_card'],
                fg=COLORS['accent'] if is_best else COLORS['text_secondary']
            ).pack(side=tk.LEFT, padx=2)
            
            # Metrics
            for val in [acc, prec, rec, f1]:
                color = COLORS['success'] if val >= 60 else COLORS['warning'] if val >= 40 else COLORS['danger']
                tk.Label(
                    row, text=f"{val:.1f}%", width=10,
                    font=FONTS['body'],
                    bg=COLORS['bg_card'],
                    fg=color
                ).pack(side=tk.LEFT, padx=2)
    
    def create_feature_importance(self, parent):
        """Create feature importance display."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            card, text="🎯  Feature Importance",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(
            content, text="Impact on churn prediction (based on model coefficients):",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Feature importance bars
        features = [
            ("Last Login Days", 0.25, COLORS['danger'], "↑ Higher = More churn risk"),
            ("Payment Failures", 0.20, COLORS['danger'], "↑ More failures = Higher risk"),
            ("Login Frequency", 0.15, COLORS['warning'], "↓ Lower = Higher risk"),
            ("Watch Time", 0.12, COLORS['warning'], "↓ Less engagement = Risk"),
            ("Tenure (months)", 0.10, COLORS['success'], "↓ New customers churn more"),
            ("Support Calls", 0.08, COLORS['text_secondary'], "Variable impact"),
            ("Monthly Charges", 0.05, COLORS['text_muted'], "Minor impact"),
            ("Age", 0.03, COLORS['text_muted'], "Minor impact"),
            ("Subscription Type", 0.02, COLORS['text_muted'], "Minimal impact"),
        ]
        
        for feature, importance, color, insight in features:
            self.create_importance_bar(content, feature, importance, color, insight)
    
    def create_importance_bar(self, parent, label, value, color, insight):
        """Create a single importance bar with insight."""
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
        bar = tk.Frame(bar_container, bg=color, height=16)
        bar.place(relwidth=value, relheight=1)
        
        # Value
        tk.Label(
            frame, text=f"{value*100:.0f}%", width=5,
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=color
        ).pack(side=tk.LEFT)
    
    def create_data_statistics(self, parent):
        """Create data statistics section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            card, text="📋  Dataset Statistics",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Stats items
        stats = [
            ("Total Records", "1,001", COLORS['accent']),
            ("Training Set", "800", COLORS['success']),
            ("Test Set", "200", COLORS['warning']),
            ("Churn Rate", "32.5%", COLORS['danger']),
            ("Stay Rate", "67.5%", COLORS['success']),
            ("Avg Age", "44 years", COLORS['text_secondary']),
            ("Avg Tenure", "25 months", COLORS['text_secondary']),
            ("Avg Monthly", "$19.50", COLORS['text_secondary']),
        ]
        
        for label, value, color in stats:
            row = tk.Frame(content, bg=COLORS['bg_card'])
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(
                row, text=label, width=15, anchor=tk.W,
                font=FONTS['body'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_secondary']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=value,
                font=FONTS['body_bold'],
                bg=COLORS['bg_card'],
                fg=color
            ).pack(side=tk.LEFT)
        
        # Class distribution
        tk.Label(
            content, text="\n📊 Target Distribution:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(10, 5))
        
        dist_frame = tk.Frame(content, bg=COLORS['bg_light'], height=30)
        dist_frame.pack(fill=tk.X, pady=5)
        dist_frame.pack_propagate(False)
        
        # Stay portion (67.5%)
        stay_bar = tk.Frame(dist_frame, bg=COLORS['success'])
        stay_bar.place(relwidth=0.675, relheight=1, relx=0)
        tk.Label(
            stay_bar, text="Stay: 67.5%",
            font=FONTS['small'],
            bg=COLORS['success'],
            fg=COLORS['text_primary']
        ).pack(expand=True)
        
        # Churn portion (32.5%)
        churn_bar = tk.Frame(dist_frame, bg=COLORS['danger'])
        churn_bar.place(relwidth=0.325, relheight=1, relx=0.675)
        tk.Label(
            churn_bar, text="Churn: 32.5%",
            font=FONTS['small'],
            bg=COLORS['danger'],
            fg=COLORS['text_primary']
        ).pack(expand=True)
