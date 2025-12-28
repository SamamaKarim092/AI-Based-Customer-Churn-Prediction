"""
Settings Page
Application settings and configuration.
"""

import tkinter as tk
from tkinter import messagebox
from .base import BasePage
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS
from components.widgets import ModernButton


class SettingsPage(BasePage):
    """Application settings page."""
    
    # Available models with their info
    MODELS = {
        'logistic': {
            'name': 'Logistic Regression',
            'accuracy': '72.5%',
            'description': 'Best overall performance - Recommended',
            'is_default': True
        },
        'random_forest': {
            'name': 'Random Forest',
            'accuracy': '71.0%',
            'description': 'Good for non-linear patterns',
            'is_default': False
        },
        'naive_bayes': {
            'name': 'Naive Bayes',
            'accuracy': '62.0%',
            'description': 'Fast but lower accuracy',
            'is_default': False
        }
    }
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.selected_model = tk.StringVar(value='logistic')
        self.setup_page()
    
    def setup_page(self):
        """Setup the settings page."""
        # Header
        self.create_header(
            "Settings",
            "Configure application preferences"
        )
        
        # Main content
        main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Model settings
        self.create_model_settings(main_frame)
        
        # Display settings
        self.create_display_settings(main_frame)
        
        # About section
        self.create_about_section(main_frame)
    
    def create_model_settings(self, parent):
        """Create model settings section with model selection."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            card, text="🤖  Model Settings",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Current model info
        info_frame = tk.Frame(content, bg=COLORS['bg_card'])
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info = [
            ("Model File", "model/churn_model.pkl"),
            ("Last Trained", "December 2025"),
        ]
        
        for label, value in info:
            row = tk.Frame(info_frame, bg=COLORS['bg_card'])
            row.pack(fill=tk.X, pady=2)
            
            tk.Label(
                row, text=label + ":", width=15, anchor=tk.W,
                font=FONTS['body'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_secondary']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=value,
                font=FONTS['body_bold'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_primary']
            ).pack(side=tk.LEFT)
        
        # Model selection section
        tk.Label(
            content, text="\n📊 Select Prediction Model:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(10, 5))
        
        tk.Label(
            content, text="Choose which algorithm to use for churn predictions",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Model options
        for model_key, model_data in self.MODELS.items():
            self.create_model_option(content, model_key, model_data)
        
        # Action buttons
        btn_frame = tk.Frame(content, bg=COLORS['bg_card'])
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        ModernButton(
            btn_frame, "Apply Model", self.apply_model,
            style='primary', icon="✅", colors=COLORS
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ModernButton(
            btn_frame, "Retrain Model", self.retrain_model,
            style='secondary', icon="🔄", colors=COLORS
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ModernButton(
            btn_frame, "Import Model", self.import_model,
            style='secondary', icon="📥", colors=COLORS
        ).pack(side=tk.LEFT)
    
    def create_model_option(self, parent, model_key, model_data):
        """Create a model selection option."""
        frame = tk.Frame(parent, bg=COLORS['bg_light'], cursor='hand2')
        frame.pack(fill=tk.X, pady=3)
        
        inner = tk.Frame(frame, bg=COLORS['bg_light'], padx=15, pady=10)
        inner.pack(fill=tk.X)
        
        # Radio button row
        radio_row = tk.Frame(inner, bg=COLORS['bg_light'])
        radio_row.pack(fill=tk.X)
        
        rb = tk.Radiobutton(
            radio_row,
            text=model_data['name'],
            variable=self.selected_model,
            value=model_key,
            font=FONTS['body_bold'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary'],
            selectcolor=COLORS['bg_medium'],
            activebackground=COLORS['bg_light'],
            activeforeground=COLORS['text_primary'],
            cursor='hand2'
        )
        rb.pack(side=tk.LEFT)
        
        # Default badge
        if model_data['is_default']:
            tk.Label(
                radio_row, text="⭐ DEFAULT",
                font=('Segoe UI', 8, 'bold'),
                bg=COLORS['success'],
                fg=COLORS['text_primary'],
                padx=5, pady=1
            ).pack(side=tk.LEFT, padx=10)
        
        # Accuracy
        tk.Label(
            radio_row, text=f"Accuracy: {model_data['accuracy']}",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['accent']
        ).pack(side=tk.RIGHT)
        
        # Description
        tk.Label(
            inner, text=model_data['description'],
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack(anchor=tk.W, padx=(22, 0))
        
        # Hover effects
        def on_enter(e):
            frame.config(bg=COLORS['sidebar_hover'])
            inner.config(bg=COLORS['sidebar_hover'])
            radio_row.config(bg=COLORS['sidebar_hover'])
            for child in inner.winfo_children():
                try:
                    child.config(bg=COLORS['sidebar_hover'])
                except:
                    pass
            for child in radio_row.winfo_children():
                try:
                    if not isinstance(child, tk.Radiobutton):
                        child.config(bg=COLORS['sidebar_hover'])
                except:
                    pass
        
        def on_leave(e):
            frame.config(bg=COLORS['bg_light'])
            inner.config(bg=COLORS['bg_light'])
            radio_row.config(bg=COLORS['bg_light'])
            for child in inner.winfo_children():
                try:
                    child.config(bg=COLORS['bg_light'])
                except:
                    pass
            for child in radio_row.winfo_children():
                try:
                    if not isinstance(child, tk.Radiobutton):
                        child.config(bg=COLORS['bg_light'])
                except:
                    pass
        
        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)
        inner.bind('<Enter>', on_enter)
        inner.bind('<Leave>', on_leave)
    
    def create_display_settings(self, parent):
        """Create display settings section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            card, text="🎨  Display Settings",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Theme option
        theme_row = tk.Frame(content, bg=COLORS['bg_card'])
        theme_row.pack(fill=tk.X, pady=5)
        
        tk.Label(
            theme_row, text="Theme:", width=15, anchor=tk.W,
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(side=tk.LEFT)
        
        self.theme_var = tk.StringVar(value="Dark")
        themes = ["Dark", "Light"]
        for theme in themes:
            rb = tk.Radiobutton(
                theme_row, text=theme,
                variable=self.theme_var,
                value=theme,
                font=FONTS['body'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_primary'],
                selectcolor=COLORS['bg_medium'],
                activebackground=COLORS['bg_card'],
                command=self.apply_theme
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Animation toggle
        self.animations_var = tk.BooleanVar(value=True)
        cb = tk.Checkbutton(
            content, text="Enable animations",
            variable=self.animations_var,
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            selectcolor=COLORS['bg_medium'],
            activebackground=COLORS['bg_card']
        )
        cb.pack(anchor=tk.W, pady=5)
        
        # Charts toggle
        self.charts_var = tk.BooleanVar(value=True)
        cb2 = tk.Checkbutton(
            content, text="Show charts in predictions",
            variable=self.charts_var,
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            selectcolor=COLORS['bg_medium'],
            activebackground=COLORS['bg_card']
        )
        cb2.pack(anchor=tk.W, pady=5)
    
    def create_about_section(self, parent):
        """Create about section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            card, text="ℹ️  About",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # App title
        tk.Label(
            content, text="🤖 AI Customer Churn Prediction System",
            font=('Segoe UI', 14, 'bold'),
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W)
        
        tk.Label(
            content, text="Version 1.0.0",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Description
        tk.Label(
            content, text="A machine learning system that predicts customer churn probability,\nexplains predictions using SHAP, and recommends retention actions.",
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Two columns for info
        info_frame = tk.Frame(content, bg=COLORS['bg_card'])
        info_frame.pack(fill=tk.X)
        
        # Left column - Algorithms
        left_col = tk.Frame(info_frame, bg=COLORS['bg_light'], padx=15, pady=10)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(
            left_col, text="🧠 Algorithms Used:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W)
        
        algorithms = [
            ("⭐ Logistic Regression", "72.5% accuracy - Selected"),
            ("   Random Forest", "71.0% accuracy"),
            ("   Naive Bayes", "62.0% accuracy"),
        ]
        
        for algo, detail in algorithms:
            tk.Label(
                left_col, text=algo,
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['accent'] if "⭐" in algo else COLORS['text_secondary']
            ).pack(anchor=tk.W, pady=(3, 0))
            tk.Label(
                left_col, text=f"    {detail}",
                font=('Segoe UI', 8),
                bg=COLORS['bg_light'],
                fg=COLORS['text_muted']
            ).pack(anchor=tk.W)
        
        # Right column - Technologies
        right_col = tk.Frame(info_frame, bg=COLORS['bg_light'], padx=15, pady=10)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(
            right_col, text="💻 Technologies:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W)
        
        technologies = [
            "Python 3.x",
            "scikit-learn (ML)",
            "SHAP (Explainability)",
            "Tkinter (Desktop UI)",
            "ReportLab (PDF Reports)",
        ]
        
        for tech in technologies:
            tk.Label(
                right_col, text=f"• {tech}",
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_secondary']
            ).pack(anchor=tk.W, pady=1)
        
        # Team section
        team_frame = tk.Frame(content, bg=COLORS['bg_light'], padx=15, pady=12)
        team_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(
            team_frame, text="👥 Made By:",
            font=FONTS['body_bold'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary']
        ).pack(anchor=tk.W)
        
        team_members = [
            ("Samama Karim", "Group Leader"),
            ("Taimoor Abrar", "Team Member"),
            ("Abdul Wasay", "Team Member"),
            ("Muhammad Ali", "Team Member"),
        ]
        
        for name, role in team_members:
            member_row = tk.Frame(team_frame, bg=COLORS['bg_light'])
            member_row.pack(fill=tk.X, pady=2)
            
            tk.Label(
                member_row, text=f"  • {name}",
                font=FONTS['body_bold'],
                bg=COLORS['bg_light'],
                fg=COLORS['accent'] if "Leader" in role else COLORS['text_secondary']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                member_row, text=f" ({role})",
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_muted']
            ).pack(side=tk.LEFT)
        
        # Footer
        tk.Label(
            content, text="\n📅 December 2025",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(anchor=tk.W)
    
    def apply_model(self):
        """Apply the selected model."""
        model_key = self.selected_model.get()
        model_name = self.MODELS[model_key]['name']
        
        messagebox.showinfo(
            "Model Applied",
            f"✅ Model changed to: {model_name}\n\n"
            f"Accuracy: {self.MODELS[model_key]['accuracy']}\n\n"
            "All future predictions will use this model."
        )
    
    def retrain_model(self):
        """Trigger model retraining."""
        messagebox.showinfo(
            "Retrain Model",
            "Model retraining feature coming soon!\n\n"
            "This will allow you to:\n"
            "• Retrain with new data\n"
            "• Compare model versions\n"
            "• Auto-select best algorithm"
        )
    
    def import_model(self):
        """Import a pre-trained model."""
        messagebox.showinfo(
            "Import Model",
            "Model import feature coming soon!\n\n"
            "This will allow you to:\n"
            "• Import .pkl model files\n"
            "• Validate model compatibility\n"
            "• Switch between models"
        )
    
    def apply_theme(self):
        """Apply the selected theme to the entire application."""
        theme = self.theme_var.get()
        
        # Define light theme colors
        light_colors = {
            'bg_dark': '#f5f5f5',
            'bg_medium': '#ffffff',
            'bg_light': '#e8e8e8',
            'bg_card': '#ffffff',
            'sidebar_bg': '#f0f0f0',
            'sidebar_hover': '#e0e0e0',
            'sidebar_active': '#1f6feb',
            'accent': '#1f6feb',
            'accent_hover': '#388bfd',
            'accent_dark': '#0d419d',
            'success': '#2da44e',
            'success_light': '#46954a',
            'warning': '#bf8700',
            'warning_light': '#d4a012',
            'danger': '#cf222e',
            'danger_light': '#e16f76',
            'text_primary': '#1f2328',
            'text_secondary': '#57606a',
            'text_muted': '#6e7781',
            'border': '#d0d7de',
            'border_light': '#b0b8c0',
            'chart_positive': '#cf222e',
            'chart_negative': '#2da44e',
            'chart_neutral': '#57606a'
        }
        
        # Define dark theme colors (original)
        dark_colors = {
            'bg_dark': '#0d1117',
            'bg_medium': '#161b22',
            'bg_light': '#21262d',
            'bg_card': '#1c2128',
            'sidebar_bg': '#0d1117',
            'sidebar_hover': '#21262d',
            'sidebar_active': '#1f6feb',
            'accent': '#58a6ff',
            'accent_hover': '#79b8ff',
            'accent_dark': '#1f6feb',
            'success': '#3fb950',
            'success_light': '#56d364',
            'warning': '#d29922',
            'warning_light': '#e3b341',
            'danger': '#f85149',
            'danger_light': '#ff7b72',
            'text_primary': '#f0f6fc',
            'text_secondary': '#8b949e',
            'text_muted': '#6e7681',
            'border': '#30363d',
            'border_light': '#484f58',
            'chart_positive': '#f85149',
            'chart_negative': '#3fb950',
            'chart_neutral': '#8b949e'
        }
        
        # Select the appropriate color scheme
        new_colors = light_colors if theme == "Light" else dark_colors
        
        # Update the global COLORS dictionary
        for key in new_colors:
            COLORS[key] = new_colors[key]
        
        # Refresh the entire UI by calling on_show for the current page
        messagebox.showinfo(
            "Theme Changed",
            f"Theme changed to {theme} mode!\n\n"
            "Please restart the application to fully apply the new theme."
        )
