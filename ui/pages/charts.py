"""
Charts/Analytics Page
Model training info, performance metrics, and algorithm comparison.
"""

import tkinter as tk
from tkinter import ttk
from .base import BasePage
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS


class ChartsPage(BasePage):
    """Analytics and charts page with dynamic algorithm comparison."""
    
    # Algorithm data - metrics for each model
    ALGORITHMS = {
        'logistic': {
            'name': 'Logistic Regression',
            'accuracy': 72.5,
            'precision': 63.9,
            'recall': 35.4,
            'f1_score': 45.5,
            'confusion_matrix': [[122, 13], [42, 23]],
            'is_best': True,
            'description': 'A linear model that predicts probability of churn using a logistic function. Best for interpretability and when features have linear relationships with the target.',
            'strengths': ['Easy to interpret', 'Fast training', 'Good for linear relationships', 'Provides probability scores'],
            'weaknesses': ['Assumes linearity', 'May underfit complex patterns'],
            'why_chosen': 'Selected as the best model due to highest accuracy (72.5%) and good balance between precision and interpretability for business decisions.',
        },
        'naive_bayes': {
            'name': 'Naive Bayes',
            'accuracy': 62.0,
            'precision': 40.4,
            'recall': 47.7,
            'f1_score': 43.8,
            'confusion_matrix': [[100, 35], [34, 31]],
            'is_best': False,
            'description': 'A probabilistic classifier based on Bayes theorem with strong independence assumptions between features.',
            'strengths': ['Very fast training', 'Works well with small data', 'Good baseline model', 'Highest recall among tested'],
            'weaknesses': ['Assumes feature independence', 'Lower accuracy', 'Poor precision'],
            'why_not': 'Not selected due to lowest accuracy (62.0%) and poor precision (40.4%), leading to many false positive churn predictions.',
        },
        'random_forest': {
            'name': 'Random Forest',
            'accuracy': 71.0,
            'precision': 58.1,
            'recall': 36.9,
            'f1_score': 45.1,
            'confusion_matrix': [[118, 17], [41, 24]],
            'is_best': False,
            'description': 'An ensemble method that builds multiple decision trees and merges their predictions for more accurate and stable results.',
            'strengths': ['Handles non-linear patterns', 'Feature importance built-in', 'Robust to overfitting', 'No feature scaling needed'],
            'weaknesses': ['Slower training', 'Less interpretable', 'Slightly lower accuracy than Logistic Regression'],
            'why_not': 'Not selected because Logistic Regression achieved slightly better accuracy (72.5% vs 71.0%) with better interpretability for business use cases.',
        }
    }
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.selected_algorithm = 'logistic'  # Default selection
        self.algo_buttons = {}
        self.setup_page()
    
    def setup_page(self):
        """Setup the analytics page."""
        # Header
        self.create_header(
            "Model Analytics",
            "Compare algorithms and understand why our model was chosen"
        )
        
        # Main content
        self.main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Algorithm selector section
        self.create_algorithm_selector()
        
        # Dynamic content area (will update based on selection)
        self.dynamic_frame = tk.Frame(self.main_frame, bg=COLORS['bg_medium'])
        self.dynamic_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Initial display
        self.update_display()
    
    def create_algorithm_selector(self):
        """Create the clickable algorithm selector cards."""
        card = tk.Frame(self.main_frame, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title row
        title_row = tk.Frame(card, bg=COLORS['bg_card'])
        title_row.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_row, text="🤖  Select Algorithm to Analyze",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            title_row, text="Click on an algorithm to see its detailed metrics",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(side=tk.RIGHT)
        
        # Algorithm buttons container
        algo_frame = tk.Frame(card, bg=COLORS['bg_card'])
        algo_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        for algo_key, algo_data in self.ALGORITHMS.items():
            self.create_algo_button(algo_frame, algo_key, algo_data)
    
    def create_algo_button(self, parent, algo_key, algo_data):
        """Create a clickable algorithm card."""
        is_selected = algo_key == self.selected_algorithm
        is_best = algo_data['is_best']
        
        # Determine colors
        if is_selected:
            bg_color = COLORS['accent']
            fg_color = COLORS['text_primary']
        else:
            bg_color = COLORS['bg_light']
            fg_color = COLORS['text_secondary']
        
        # Card frame
        card = tk.Frame(parent, bg=bg_color, cursor='hand2', padx=20, pady=12)
        card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Best badge
        if is_best:
            badge = tk.Label(
                card, text="⭐ BEST",
                font=('Segoe UI', 8, 'bold'),
                bg=COLORS['success'] if not is_selected else COLORS['warning'],
                fg=COLORS['text_primary'],
                padx=5, pady=1
            )
            badge.pack(anchor=tk.E)
        
        # Algorithm name
        name_label = tk.Label(
            card, text=algo_data['name'],
            font=FONTS['body_bold'],
            bg=bg_color,
            fg=fg_color,
            cursor='hand2'
        )
        name_label.pack(anchor=tk.W)
        
        # Accuracy
        acc_label = tk.Label(
            card, text=f"Accuracy: {algo_data['accuracy']:.1f}%",
            font=FONTS['small'],
            bg=bg_color,
            fg=fg_color if is_selected else COLORS['text_muted'],
            cursor='hand2'
        )
        acc_label.pack(anchor=tk.W)
        
        # Store references for updating
        self.algo_buttons[algo_key] = {
            'card': card,
            'name': name_label,
            'acc': acc_label,
            'badge': badge if is_best else None
        }
        
        # Bind click events
        def on_click(e, key=algo_key):
            self.select_algorithm(key)
        
        def on_enter(e, c=card, n=name_label, a=acc_label, key=algo_key):
            if key != self.selected_algorithm:
                c.config(bg=COLORS['sidebar_hover'])
                n.config(bg=COLORS['sidebar_hover'])
                a.config(bg=COLORS['sidebar_hover'])
        
        def on_leave(e, c=card, n=name_label, a=acc_label, key=algo_key):
            if key != self.selected_algorithm:
                c.config(bg=COLORS['bg_light'])
                n.config(bg=COLORS['bg_light'])
                a.config(bg=COLORS['bg_light'])
        
        for widget in [card, name_label, acc_label]:
            widget.bind('<Button-1>', on_click)
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
    
    def select_algorithm(self, algo_key):
        """Select an algorithm and update the display."""
        if algo_key == self.selected_algorithm:
            return
        
        self.selected_algorithm = algo_key
        
        # Update button styles
        for key, widgets in self.algo_buttons.items():
            is_selected = key == algo_key
            bg_color = COLORS['accent'] if is_selected else COLORS['bg_light']
            fg_color = COLORS['text_primary'] if is_selected else COLORS['text_secondary']
            
            widgets['card'].config(bg=bg_color)
            widgets['name'].config(bg=bg_color, fg=fg_color)
            widgets['acc'].config(bg=bg_color, fg=fg_color if is_selected else COLORS['text_muted'])
            
            if widgets['badge']:
                widgets['badge'].config(
                    bg=COLORS['success'] if not is_selected else COLORS['warning']
                )
        
        # Update content
        self.update_display()
    
    def update_display(self):
        """Update the dynamic content based on selected algorithm."""
        # Clear previous content
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        
        algo = self.ALGORITHMS[self.selected_algorithm]
        
        # Two columns layout
        columns_frame = tk.Frame(self.dynamic_frame, bg=COLORS['bg_medium'])
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column
        left_col = tk.Frame(columns_frame, bg=COLORS['bg_medium'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_performance_section(left_col, algo)
        self.create_confusion_matrix(left_col, algo)
        
        # Right column
        right_col = tk.Frame(columns_frame, bg=COLORS['bg_medium'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_algorithm_info(right_col, algo)
        self.create_comparison_summary(right_col)
    
    def create_performance_section(self, parent, algo):
        """Create performance metrics section for selected algorithm."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title with algorithm name
        title_frame = tk.Frame(card, bg=COLORS['bg_card'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_frame, text=f"📈  {algo['name']} Performance",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(side=tk.LEFT)
        
        if algo['is_best']:
            tk.Label(
                title_frame, text="⭐ Selected Model",
                font=FONTS['small'],
                bg=COLORS['success'],
                fg=COLORS['text_primary'],
                padx=8, pady=2
            ).pack(side=tk.RIGHT)
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Metrics with visual bars
        metrics = [
            ("Accuracy", algo['accuracy'], COLORS['success'] if algo['accuracy'] >= 70 else COLORS['warning']),
            ("Precision", algo['precision'], COLORS['success'] if algo['precision'] >= 60 else COLORS['warning']),
            ("Recall", algo['recall'], COLORS['warning'] if algo['recall'] >= 35 else COLORS['danger']),
            ("F1-Score", algo['f1_score'], COLORS['accent']),
        ]
        
        for metric, value, color in metrics:
            frame = tk.Frame(content, bg=COLORS['bg_card'])
            frame.pack(fill=tk.X, pady=5)
            
            # Label and value
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
            
            # Progress bar
            bar_frame = tk.Frame(frame, bg=COLORS['bg_light'], height=10)
            bar_frame.pack(fill=tk.X, pady=(3, 0))
            bar_frame.pack_propagate(False)
            
            bar = tk.Frame(bar_frame, bg=color, height=10)
            bar.place(relwidth=value/100, relheight=1)
    
    def create_confusion_matrix(self, parent, algo):
        """Create confusion matrix for selected algorithm."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            card, text="📊  Confusion Matrix",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        cm = algo['confusion_matrix']
        tn, fp = cm[0]
        fn, tp = cm[1]
        
        matrix_data = [
            ["", "Predicted\nStay", "Predicted\nChurn"],
            ["Actual Stay", f"{tn} ✓", str(fp)],
            ["Actual Churn", str(fn), f"{tp} ✓"],
        ]
        
        matrix_frame = tk.Frame(content, bg=COLORS['bg_light'])
        matrix_frame.pack(fill=tk.X)
        
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
                
                tk.Label(
                    row, text=cell.replace(" ✓", ""),
                    font=FONTS['small'] if is_header else FONTS['body_bold'],
                    bg=bg_color, fg=fg_color,
                    width=12, height=2,
                    relief=tk.FLAT
                ).pack(side=tk.LEFT, padx=1, pady=1)
        
        # Interpretation
        total = tn + fp + fn + tp
        correct = tn + tp
        tk.Label(
            content, text=f"\nCorrect predictions: {correct}/{total} ({correct/total*100:.1f}%)",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(anchor=tk.W, pady=(10, 0))
    
    def create_algorithm_info(self, parent, algo):
        """Create algorithm information and reasoning section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            card, text="📖  About This Algorithm",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Description
        tk.Label(
            content, text=algo['description'],
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            wraplength=350,
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Strengths
        tk.Label(
            content, text="✅ Strengths:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['success']
        ).pack(anchor=tk.W, pady=(5, 0))
        
        for strength in algo['strengths']:
            tk.Label(
                content, text=f"  • {strength}",
                font=FONTS['small'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_secondary']
            ).pack(anchor=tk.W)
        
        # Weaknesses
        tk.Label(
            content, text="⚠️ Weaknesses:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['warning']
        ).pack(anchor=tk.W, pady=(10, 0))
        
        for weakness in algo['weaknesses']:
            tk.Label(
                content, text=f"  • {weakness}",
                font=FONTS['small'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_secondary']
            ).pack(anchor=tk.W)
        
        # Why chosen / not chosen
        why_frame = tk.Frame(content, bg=COLORS['bg_light'], padx=10, pady=10)
        why_frame.pack(fill=tk.X, pady=(15, 0))
        
        if algo['is_best']:
            tk.Label(
                why_frame, text="🏆 Why This Model Was Chosen:",
                font=FONTS['body_bold'],
                bg=COLORS['bg_light'],
                fg=COLORS['success']
            ).pack(anchor=tk.W)
            
            tk.Label(
                why_frame, text=algo['why_chosen'],
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_secondary'],
                wraplength=330,
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=(5, 0))
        else:
            tk.Label(
                why_frame, text="❌ Why This Model Was Not Selected:",
                font=FONTS['body_bold'],
                bg=COLORS['bg_light'],
                fg=COLORS['danger']
            ).pack(anchor=tk.W)
            
            tk.Label(
                why_frame, text=algo['why_not'],
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_secondary'],
                wraplength=330,
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=(5, 0))
    
    def create_comparison_summary(self, parent):
        """Create quick comparison summary table."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            card, text="⚖️  All Models Comparison",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Header
        header = tk.Frame(content, bg=COLORS['bg_light'])
        header.pack(fill=tk.X, pady=(0, 5))
        
        for h, w in [("Model", 18), ("Acc", 8), ("Prec", 8), ("Rec", 8), ("F1", 8)]:
            tk.Label(
                header, text=h, width=w,
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_muted']
            ).pack(side=tk.LEFT, padx=1, pady=5)
        
        # Data rows
        for key, data in self.ALGORITHMS.items():
            is_selected = key == self.selected_algorithm
            row_bg = COLORS['accent'] if is_selected else COLORS['bg_card']
            row_fg = COLORS['text_primary'] if is_selected else COLORS['text_secondary']
            
            row = tk.Frame(content, bg=row_bg)
            row.pack(fill=tk.X, pady=1)
            
            # Name with star for best
            name_text = f"⭐ {data['name']}" if data['is_best'] else f"   {data['name']}"
            tk.Label(
                row, text=name_text, width=18, anchor=tk.W,
                font=FONTS['body_bold'] if data['is_best'] or is_selected else FONTS['body'],
                bg=row_bg,
                fg=row_fg
            ).pack(side=tk.LEFT, padx=1, pady=3)
            
            # Metrics
            for val in [data['accuracy'], data['precision'], data['recall'], data['f1_score']]:
                color = COLORS['success'] if val >= 60 else COLORS['warning'] if val >= 40 else COLORS['danger']
                if is_selected:
                    color = COLORS['text_primary']
                tk.Label(
                    row, text=f"{val:.1f}%", width=8,
                    font=FONTS['body'],
                    bg=row_bg,
                    fg=color
                ).pack(side=tk.LEFT, padx=1)
        
        # Legend
        tk.Label(
            content, text="\n⭐ = Best performing model (selected for production)",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(anchor=tk.W, pady=(10, 0))
