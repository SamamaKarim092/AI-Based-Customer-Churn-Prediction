"""
Predict Page
Customer churn prediction interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base import BasePage
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS
from components.widgets import AnimatedGauge, FeatureBarChart, ModernButton

# Add src to path
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(project_dir, 'src'))

from predict import predict_churn, load_model_and_encoders, preprocess_customer_data
from explain import explain_prediction
from recommend import generate_full_recommendation


class PredictPage(BasePage):
    """Prediction page with input form and results."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.model = None
        self.encoders = None
        self.feature_names = None
        self.load_model()
        self.setup_page()
    
    def load_model(self):
        """Load the trained model."""
        try:
            self.model, self.encoders, self.feature_names = load_model_and_encoders()
        except FileNotFoundError:
            pass  # Will show error when predicting
    
    def setup_page(self):
        """Setup the prediction page."""
        # Header
        self.create_header(
            "Churn Prediction",
            "Enter customer information to predict churn probability"
        )
        
        # Main content - two columns
        main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Left column - Input form
        left_col = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        self.create_input_form(left_col)
        self.create_action_buttons(left_col)
        self.create_recommendations_panel(left_col)
        
        # Right column - Results
        right_col = tk.Frame(main_frame, bg=COLORS['bg_medium'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))
        
        self.create_gauge_panel(right_col)
        self.create_chart_panel(right_col)
    
    def create_input_form(self, parent):
        """Create the input form."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(card, bg=COLORS['bg_card'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_frame,
            text="📋  Customer Information",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W)
        
        # Form content
        form_frame = tk.Frame(card, bg=COLORS['bg_card'])
        form_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.inputs = {}
        
        # Row 1
        row1 = tk.Frame(form_frame, bg=COLORS['bg_card'])
        row1.pack(fill=tk.X, pady=5)
        
        self.create_input(row1, "Age", 'age', 'spinbox', (18, 100), 35)
        self.create_input(row1, "Gender", 'gender', 'combo', ['Male', 'Female'], 'Male')
        self.create_input(row1, "Subscription", 'subscription_type', 'combo', 
                         ['Basic', 'Standard', 'Premium'], 'Standard')
        
        # Row 2
        row2 = tk.Frame(form_frame, bg=COLORS['bg_card'])
        row2.pack(fill=tk.X, pady=5)
        
        self.create_input(row2, "Monthly ($)", 'monthly_charges', 'spinbox', (9.99, 50.00), 19.99)
        self.create_input(row2, "Tenure (mo)", 'tenure_in_months', 'spinbox', (1, 120), 12)
        self.create_input(row2, "Logins/mo", 'login_frequency', 'spinbox', (0, 100), 15)
        
        # Row 3
        row3 = tk.Frame(form_frame, bg=COLORS['bg_card'])
        row3.pack(fill=tk.X, pady=5)
        
        self.create_input(row3, "Last Login", 'last_login_days', 'spinbox', (0, 365), 5)
        self.create_input(row3, "Watch (hrs)", 'watch_time', 'spinbox', (0.0, 200.0), 20.0)
        self.create_input(row3, "Pay Fails", 'payment_failures', 'spinbox', (0, 10), 0)
        
        # Row 4
        row4 = tk.Frame(form_frame, bg=COLORS['bg_card'])
        row4.pack(fill=tk.X, pady=5)
        
        self.create_input(row4, "Support Calls", 'customer_support_calls', 'spinbox', (0, 20), 1)
    
    def create_input(self, parent, label, key, input_type, options, default):
        """Create a single input field."""
        frame = tk.Frame(parent, bg=COLORS['bg_card'])
        frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(
            frame, text=label,
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(anchor=tk.W)
        
        if input_type == 'combo':
            widget = ttk.Combobox(frame, values=options, width=14, state='readonly')
            widget.set(default)
        else:
            widget = ttk.Spinbox(frame, from_=options[0], to=options[1], width=14)
            widget.set(default)
        
        widget.pack(fill=tk.X, pady=(3, 0))
        self.inputs[key] = widget
    
    def create_action_buttons(self, parent):
        """Create action buttons."""
        btn_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Predict button
        self.predict_btn = ModernButton(
            btn_frame, "PREDICT CHURN", self.predict,
            style='primary', icon="🔮", colors=COLORS
        )
        self.predict_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Sample buttons
        ModernButton(
            btn_frame, "High Risk", self.load_high_risk,
            style='danger', icon="⚠️", colors=COLORS
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame, "Low Risk", self.load_low_risk,
            style='success', icon="✅", colors=COLORS
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            btn_frame, "Clear", self.clear_all,
            style='secondary', icon="🔄", colors=COLORS
        ).pack(side=tk.LEFT, padx=5)
    
    def create_recommendations_panel(self, parent):
        """Create recommendations display."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Title
        title_frame = tk.Frame(card, bg=COLORS['bg_card'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_frame,
            text="💡  Recommended Actions",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W)
        
        # Text display
        text_frame = tk.Frame(card, bg=COLORS['bg_card'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.recommendations_text = tk.Text(
            text_frame, wrap=tk.WORD, height=8,
            bg=COLORS['bg_light'], fg=COLORS['text_primary'],
            font=FONTS['mono_small'],
            relief=tk.FLAT, padx=10, pady=10,
            insertbackground=COLORS['text_primary']
        )
        self.recommendations_text.pack(fill=tk.BOTH, expand=True)
        self.recommendations_text.insert(tk.END, "Click 'Predict Churn' to see recommendations...")
        self.recommendations_text.config(state=tk.DISABLED)
    
    def create_gauge_panel(self, parent):
        """Create gauge display panel."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(card, bg=COLORS['bg_card'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_frame,
            text="📊  Churn Risk Score",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W)
        
        # Gauge and info container
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Gauge
        self.gauge = AnimatedGauge(content, size=180, colors={
            'bg': COLORS['bg_card'],
            'track': COLORS['bg_light'],
            'low': COLORS['success'],
            'medium': COLORS['warning'],
            'high': COLORS['danger'],
            'text': COLORS['text_primary'],
            'label': COLORS['text_secondary']
        })
        self.gauge.pack(side=tk.LEFT, padx=(10, 30))
        
        # Info panel
        info_frame = tk.Frame(content, bg=COLORS['bg_card'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.prediction_label = tk.Label(
            info_frame, text="Prediction: --",
            font=FONTS['heading'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        )
        self.prediction_label.pack(anchor=tk.W, pady=3)
        
        self.risk_label = tk.Label(
            info_frame, text="Risk Level: --",
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        )
        self.risk_label.pack(anchor=tk.W, pady=3)
        
        self.factors_label = tk.Label(
            info_frame, text="Top factors will appear here...",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted'],
            wraplength=250,
            justify=tk.LEFT
        )
        self.factors_label.pack(anchor=tk.W, pady=(10, 0))
    
    def create_chart_panel(self, parent):
        """Create chart display panel."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(card, bg=COLORS['bg_card'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_frame,
            text="📈  Feature Impact Analysis",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W)
        
        # Chart
        chart_frame = tk.Frame(card, bg=COLORS['bg_card'])
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.bar_chart = FeatureBarChart(chart_frame, width=400, height=260, colors={
            'bg': COLORS['bg_card'],
            'positive': COLORS['danger'],
            'negative': COLORS['success'],
            'text': COLORS['text_primary'],
            'label': COLORS['text_secondary'],
            'line': COLORS['border']
        })
        self.bar_chart.pack(fill=tk.BOTH, expand=True)
    
    def get_customer_data(self):
        """Get customer data from inputs."""
        try:
            return {
                'age': int(self.inputs['age'].get()),
                'gender': self.inputs['gender'].get(),
                'subscription_type': self.inputs['subscription_type'].get(),
                'monthly_charges': float(self.inputs['monthly_charges'].get()),
                'tenure_in_months': int(self.inputs['tenure_in_months'].get()),
                'login_frequency': int(self.inputs['login_frequency'].get()),
                'last_login_days': int(self.inputs['last_login_days'].get()),
                'watch_time': float(self.inputs['watch_time'].get()),
                'payment_failures': int(self.inputs['payment_failures'].get()),
                'customer_support_calls': int(self.inputs['customer_support_calls'].get())
            }
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return None
    
    def predict(self):
        """Run prediction."""
        if self.model is None:
            messagebox.showerror("Error", "Model not loaded. Please train the model first.")
            return
        
        customer_data = self.get_customer_data()
        if not customer_data:
            return
        
        try:
            # Predict
            prediction = predict_churn(customer_data, self.model, self.encoders, self.feature_names)
            
            # Explain
            features = preprocess_customer_data(customer_data, self.encoders, self.feature_names)
            explanation = explain_prediction(features, self.model, self.feature_names, customer_data)
            
            # Recommend
            recommendation = generate_full_recommendation(
                prediction['churn_probability'],
                customer_data,
                explanation['top_factors']
            )
            
            # Update UI
            self.update_results(prediction, explanation, recommendation)
            
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")
    
    def update_results(self, prediction, explanation, recommendation):
        """Update result displays."""
        # Animate gauge
        self.gauge.animate_to(prediction['churn_probability'] * 100)
        
        # Update labels
        pred_text = "Will CHURN" if prediction['prediction'] == 1 else "Will STAY"
        pred_color = COLORS['danger'] if prediction['prediction'] == 1 else COLORS['success']
        self.prediction_label.config(text=f"Prediction: {pred_text}", fg=pred_color)
        
        risk_colors = {'HIGH': COLORS['danger'], 'MODERATE': COLORS['warning'], 'LOW': COLORS['success']}
        self.risk_label.config(
            text=f"Risk Level: {prediction['risk_level']}",
            fg=risk_colors.get(prediction['risk_level'], COLORS['text_secondary'])
        )
        
        # Top factors
        if explanation['top_factors']:
            factors = [f"• {f['display_name']}" for f in explanation['top_factors'][:3]]
            self.factors_label.config(text="Top factors:\n" + "\n".join(factors))
        
        # Chart
        self.bar_chart.draw_bars(explanation['all_features'])
        
        # Recommendations
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete(1.0, tk.END)
        
        rec_text = f"{recommendation['summary']}\n\n"
        rec_text += f"Primary: {recommendation['primary_action']}\n\n"
        rec_text += "Actions:\n"
        for i, action in enumerate(recommendation['recommended_actions'][:4], 1):
            rec_text += f"  {i}. {action}\n"
        
        self.recommendations_text.insert(tk.END, rec_text)
        self.recommendations_text.config(state=tk.DISABLED)
    
    def load_high_risk(self):
        """Load high-risk sample."""
        sample = {'age': 25, 'gender': 'Male', 'subscription_type': 'Basic',
                  'monthly_charges': 12.99, 'tenure_in_months': 2, 'login_frequency': 3,
                  'last_login_days': 45, 'watch_time': 2.5, 'payment_failures': 2,
                  'customer_support_calls': 4}
        for key, value in sample.items():
            self.inputs[key].set(value)
    
    def load_low_risk(self):
        """Load low-risk sample."""
        sample = {'age': 45, 'gender': 'Female', 'subscription_type': 'Premium',
                  'monthly_charges': 29.99, 'tenure_in_months': 48, 'login_frequency': 25,
                  'last_login_days': 1, 'watch_time': 45.0, 'payment_failures': 0,
                  'customer_support_calls': 1}
        for key, value in sample.items():
            self.inputs[key].set(value)
    
    def clear_all(self):
        """Clear all inputs and results."""
        defaults = {'age': 35, 'gender': 'Male', 'subscription_type': 'Standard',
                   'monthly_charges': 19.99, 'tenure_in_months': 12, 'login_frequency': 15,
                   'last_login_days': 5, 'watch_time': 20.0, 'payment_failures': 0,
                   'customer_support_calls': 1}
        for key, value in defaults.items():
            self.inputs[key].set(value)
        
        self.gauge.reset()
        self.prediction_label.config(text="Prediction: --", fg=COLORS['text_primary'])
        self.risk_label.config(text="Risk Level: --", fg=COLORS['text_secondary'])
        self.factors_label.config(text="Top factors will appear here...")
        self.bar_chart.delete("all")
        
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.insert(tk.END, "Click 'Predict Churn' to see recommendations...")
        self.recommendations_text.config(state=tk.DISABLED)
