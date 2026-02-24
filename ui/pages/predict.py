"""
Predict Page
Customer churn prediction interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base import BasePage
import sys
import os
import random

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
    
    # ROI Constants (De Caigny et al., 2018 profit-driven framework)
    CLV_BENEFIT = 450   # $ saved per correctly retained churner
    CAMPAIGN_COST = 50  # $ spent per false alarm (unnecessary retention offer)
    
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
        """Create the input form for Telco customer features."""
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
        
        # Form content - scrollable
        form_frame = tk.Frame(card, bg=COLORS['bg_card'])
        form_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.inputs = {}
        
        # Row 1 - Demographics
        row1 = tk.Frame(form_frame, bg=COLORS['bg_card'])
        row1.pack(fill=tk.X, pady=3)
        
        self.create_input(row1, "Gender", 'gender', 'combo', ['Male', 'Female'], 'Male')
        self.create_input(row1, "Senior Citizen", 'SeniorCitizen', 'combo', ['No', 'Yes'], 'No')
        self.create_input(row1, "Partner", 'Partner', 'combo', ['Yes', 'No'], 'No')
        self.create_input(row1, "Dependents", 'Dependents', 'combo', ['Yes', 'No'], 'No')
        
        # Row 2 - Account Info
        row2 = tk.Frame(form_frame, bg=COLORS['bg_card'])
        row2.pack(fill=tk.X, pady=3)
        
        self.create_input(row2, "Tenure (mo)", 'tenure', 'spinbox', (0, 72), 12)
        self.create_input(row2, "Contract", 'Contract', 'combo',
                         ['Month-to-month', 'One year', 'Two year'], 'Month-to-month')
        self.create_input(row2, "Monthly ($)", 'MonthlyCharges', 'spinbox', (18.0, 120.0), 50.0)
        self.create_input(row2, "Total ($)", 'TotalCharges', 'spinbox', (0.0, 9000.0), 600.0)
        
        # Row 3 - Phone & Internet
        row3 = tk.Frame(form_frame, bg=COLORS['bg_card'])
        row3.pack(fill=tk.X, pady=3)
        
        self.create_input(row3, "Phone Svc", 'PhoneService', 'combo', ['Yes', 'No'], 'Yes')
        self.create_input(row3, "Multi Lines", 'MultipleLines', 'combo',
                         ['No', 'Yes', 'No phone service'], 'No')
        self.create_input(row3, "Internet Svc", 'InternetService', 'combo',
                         ['DSL', 'Fiber optic', 'No'], 'Fiber optic')
        
        # Row 4 - Add-on Services
        row4 = tk.Frame(form_frame, bg=COLORS['bg_card'])
        row4.pack(fill=tk.X, pady=3)
        
        self.create_input(row4, "Security", 'OnlineSecurity', 'combo',
                         ['Yes', 'No', 'No internet service'], 'No')
        self.create_input(row4, "Backup", 'OnlineBackup', 'combo',
                         ['Yes', 'No', 'No internet service'], 'No')
        self.create_input(row4, "Device Prot", 'DeviceProtection', 'combo',
                         ['Yes', 'No', 'No internet service'], 'No')
        self.create_input(row4, "Tech Supp", 'TechSupport', 'combo',
                         ['Yes', 'No', 'No internet service'], 'No')
        
        # Row 5 - Streaming & Billing
        row5 = tk.Frame(form_frame, bg=COLORS['bg_card'])
        row5.pack(fill=tk.X, pady=3)
        
        self.create_input(row5, "Stream TV", 'StreamingTV', 'combo',
                         ['Yes', 'No', 'No internet service'], 'No')
        self.create_input(row5, "Stream Movie", 'StreamingMovies', 'combo',
                         ['Yes', 'No', 'No internet service'], 'No')
        self.create_input(row5, "Paperless", 'PaperlessBilling', 'combo', ['Yes', 'No'], 'Yes')
        self.create_input(row5, "Pay Method", 'PaymentMethod', 'combo',
                         ['Electronic check', 'Mailed check',
                          'Bank transfer (automatic)', 'Credit card (automatic)'],
                         'Electronic check')
    
    def create_input(self, parent, label, key, input_type, options, default):
        """Create a single input field."""
        frame = tk.Frame(parent, bg=COLORS['bg_card'])
        frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        
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
        """Create recommendations button (greyed out until prediction is made)."""
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
        
        # Button frame
        btn_frame = tk.Frame(card, bg=COLORS['bg_card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._current_recommendation = None  # store last recommendation
        
        self.view_rec_btn = tk.Button(
            btn_frame,
            text="📋  View Recommended Actions",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted'],
            activebackground=COLORS['bg_light'],
            activeforeground=COLORS['text_muted'],
            relief=tk.FLAT,
            cursor='arrow',
            padx=20, pady=12,
            state=tk.DISABLED,
            command=self._open_recommendation_dialog
        )
        self.view_rec_btn.pack(fill=tk.X)
        
        # Disabled hint
        self.rec_hint_label = tk.Label(
            btn_frame,
            text="Run a prediction first to unlock recommendations",
            font=FONTS['tiny'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        )
        self.rec_hint_label.pack(anchor=tk.W, pady=(5, 0))
    
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
        
        # ROI Impact label
        self.roi_label = tk.Label(
            info_frame, text="",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        )
        self.roi_label.pack(anchor=tk.W, pady=(10, 0))
        
        self.roi_detail_label = tk.Label(
            info_frame, text="",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted'],
            wraplength=250,
            justify=tk.LEFT
        )
        self.roi_detail_label.pack(anchor=tk.W, pady=(2, 0))
    
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
            # Map SeniorCitizen combo to int
            senior = 1 if self.inputs['SeniorCitizen'].get() == 'Yes' else 0
            
            return {
                'gender': self.inputs['gender'].get(),
                'SeniorCitizen': senior,
                'Partner': self.inputs['Partner'].get(),
                'Dependents': self.inputs['Dependents'].get(),
                'tenure': int(self.inputs['tenure'].get()),
                'PhoneService': self.inputs['PhoneService'].get(),
                'MultipleLines': self.inputs['MultipleLines'].get(),
                'InternetService': self.inputs['InternetService'].get(),
                'OnlineSecurity': self.inputs['OnlineSecurity'].get(),
                'OnlineBackup': self.inputs['OnlineBackup'].get(),
                'DeviceProtection': self.inputs['DeviceProtection'].get(),
                'TechSupport': self.inputs['TechSupport'].get(),
                'StreamingTV': self.inputs['StreamingTV'].get(),
                'StreamingMovies': self.inputs['StreamingMovies'].get(),
                'Contract': self.inputs['Contract'].get(),
                'PaperlessBilling': self.inputs['PaperlessBilling'].get(),
                'PaymentMethod': self.inputs['PaymentMethod'].get(),
                'MonthlyCharges': float(self.inputs['MonthlyCharges'].get()),
                'TotalCharges': float(self.inputs['TotalCharges'].get())
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
            explanation = explain_prediction(features, self.model, self.feature_names, customer_data, self.encoders)
            
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
        
        # Calculate and display ROI impact
        prob = prediction['churn_probability']
        if prediction['prediction'] == 1:  # Predicted to churn
            roi_value = self.CLV_BENEFIT
            self.roi_label.config(
                text=f"💰  ROI Impact: +${roi_value}",
                fg=COLORS['success']
            )
            self.roi_detail_label.config(
                text=f"Retaining this customer saves ${self.CLV_BENEFIT} in CLV\n"
                     f"Retention campaign cost: ${self.CAMPAIGN_COST}\n"
                     f"Net value: ${self.CLV_BENEFIT - self.CAMPAIGN_COST} per customer"
            )
        else:  # Predicted to stay
            self.roi_label.config(
                text=f"💰  ROI Impact: No action needed",
                fg=COLORS['text_muted']
            )
            self.roi_detail_label.config(
                text="Low risk — no retention cost required"
            )
        
        # Store recommendation and activate button
        self._current_recommendation = recommendation
        risk_level = recommendation.get('risk_level', 'LOW')
        btn_colors = {
            'HIGH': (COLORS['danger'], '#ff7b72'),
            'MODERATE': (COLORS['warning'], '#e3b341'),
            'LOW': (COLORS['success'], '#56d364'),
        }
        bg_color, hover_color = btn_colors.get(risk_level, (COLORS['accent'], COLORS['accent_hover']))
        
        self.view_rec_btn.config(
            state=tk.NORMAL,
            bg=bg_color,
            fg='#ffffff',
            activebackground=hover_color,
            activeforeground='#ffffff',
            cursor='hand2',
            text=f"📋  View {min(len(recommendation.get('factor_insights', [])), 5)} Recommended Actions  →"
        )
        # hover effect
        self.view_rec_btn.bind('<Enter>', lambda e: self.view_rec_btn.config(bg=hover_color))
        self.view_rec_btn.bind('<Leave>', lambda e: self.view_rec_btn.config(bg=bg_color))
        self.rec_hint_label.config(
            text=f"Risk: {risk_level} — Click the button above to see detailed actions",
            fg=bg_color
        )
    
    def load_high_risk(self):
        """Load random high-risk sample (month-to-month, fiber optic, no add-ons)."""
        sample = {
            'gender': random.choice(['Male', 'Female']),
            'SeniorCitizen': random.choice(['No', 'Yes']),
            'Partner': 'No',
            'Dependents': 'No',
            'tenure': random.randint(1, 6),
            'PhoneService': 'Yes',
            'MultipleLines': random.choice(['No', 'Yes']),
            'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No',
            'OnlineBackup': 'No',
            'DeviceProtection': 'No',
            'TechSupport': 'No',
            'StreamingTV': random.choice(['No', 'Yes']),
            'StreamingMovies': random.choice(['No', 'Yes']),
            'Contract': 'Month-to-month',
            'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check',
            'MonthlyCharges': round(random.uniform(65.0, 100.0), 2),
            'TotalCharges': round(random.uniform(50.0, 500.0), 2)
        }
        for key, value in sample.items():
            self.inputs[key].set(value)
    
    def load_low_risk(self):
        """Load random low-risk sample (two-year contract, DSL, with add-ons)."""
        sample = {
            'gender': random.choice(['Male', 'Female']),
            'SeniorCitizen': 'No',
            'Partner': 'Yes',
            'Dependents': 'Yes',
            'tenure': random.randint(40, 72),
            'PhoneService': 'Yes',
            'MultipleLines': 'Yes',
            'InternetService': 'DSL',
            'OnlineSecurity': 'Yes',
            'OnlineBackup': 'Yes',
            'DeviceProtection': 'Yes',
            'TechSupport': 'Yes',
            'StreamingTV': 'Yes',
            'StreamingMovies': 'Yes',
            'Contract': 'Two year',
            'PaperlessBilling': 'No',
            'PaymentMethod': random.choice(['Bank transfer (automatic)', 'Credit card (automatic)']),
            'MonthlyCharges': round(random.uniform(70.0, 100.0), 2),
            'TotalCharges': round(random.uniform(4000.0, 8000.0), 2)
        }
        for key, value in sample.items():
            self.inputs[key].set(value)
    
    def clear_all(self):
        """Clear all inputs and results."""
        defaults = {
            'gender': 'Male',
            'SeniorCitizen': 'No',
            'Partner': 'No',
            'Dependents': 'No',
            'tenure': 12,
            'PhoneService': 'Yes',
            'MultipleLines': 'No',
            'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No',
            'OnlineBackup': 'No',
            'DeviceProtection': 'No',
            'TechSupport': 'No',
            'StreamingTV': 'No',
            'StreamingMovies': 'No',
            'Contract': 'Month-to-month',
            'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check',
            'MonthlyCharges': 50.0,
            'TotalCharges': 600.0
        }
        for key, value in defaults.items():
            self.inputs[key].set(value)
        
        self.gauge.reset()
        self.prediction_label.config(text="Prediction: --", fg=COLORS['text_primary'])
        self.risk_label.config(text="Risk Level: --", fg=COLORS['text_secondary'])
        self.factors_label.config(text="Top factors will appear here...")
        self.bar_chart.draw_empty()
        self.roi_label.config(text="", fg=COLORS['accent'])
        self.roi_detail_label.config(text="")
        
        # Reset recommendation button to greyed out
        self._current_recommendation = None
        self.view_rec_btn.config(
            state=tk.DISABLED,
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted'],
            activebackground=COLORS['bg_light'],
            activeforeground=COLORS['text_muted'],
            cursor='arrow',
            text="📋  View Recommended Actions"
        )
        self.view_rec_btn.unbind('<Enter>')
        self.view_rec_btn.unbind('<Leave>')
        self.rec_hint_label.config(
            text="Run a prediction first to unlock recommendations",
            fg=COLORS['text_muted']
        )

    # ────────────────────────────────────────────────────────────────
    #  Recommendation Dialog
    # ────────────────────────────────────────────────────────────────

    def _open_recommendation_dialog(self):
        """Open a beautiful dialog showing detailed recommendations."""
        rec = self._current_recommendation
        if rec is None:
            return

        risk_level = rec.get('risk_level', 'LOW')
        risk_colors_map = {'HIGH': COLORS['danger'], 'MODERATE': COLORS['warning'], 'LOW': COLORS['success']}
        risk_color = risk_colors_map.get(risk_level, COLORS['accent'])

        # ── Create dialog window ────────────────────────────────────
        dialog = tk.Toplevel(self)
        dialog.title("Recommended Actions")
        dialog.configure(bg=COLORS['bg_dark'])
        dialog.geometry("650x700")
        dialog.resizable(True, True)
        dialog.minsize(500, 400)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # Center on screen
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 325
        y = (dialog.winfo_screenheight() // 2) - 350
        dialog.geometry(f"+{x}+{y}")

        # ── Header banner ───────────────────────────────────────────
        header = tk.Frame(dialog, bg=risk_color, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        prob_pct = rec.get('churn_probability', 0) * 100
        risk_icons = {'HIGH': '🚨', 'MODERATE': '⚠️', 'LOW': '✅'}
        icon = risk_icons.get(risk_level, '📋')

        tk.Label(
            header,
            text=f"{icon}  {risk_level} RISK  —  {prob_pct:.0f}% Churn Probability",
            font=('Segoe UI', 15, 'bold'),
            bg=risk_color, fg='#ffffff'
        ).pack(expand=True)

        # ── Primary action bar ──────────────────────────────────────
        primary_bar = tk.Frame(dialog, bg=COLORS['bg_card'])
        primary_bar.pack(fill=tk.X)

        tk.Label(
            primary_bar,
            text=f"⚡  {rec.get('primary_action', '')}",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['bg_card'], fg=COLORS['accent'],
            pady=10, padx=20, anchor=tk.W
        ).pack(fill=tk.X)

        # ── Scrollable Text widget (reliable rendering) ─────────────
        text_frame = tk.Frame(dialog, bg=COLORS['bg_dark'])
        text_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(
            text_frame,
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary'],
            font=('Segoe UI', 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=25, pady=15,
            cursor='arrow',
            yscrollcommand=scrollbar.set,
            insertbackground=COLORS['bg_dark'],
            selectbackground=COLORS['accent'],
            spacing1=2,
            spacing3=2
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        # Define text tags for styling
        text_widget.tag_configure('section_title', font=('Segoe UI', 13, 'bold'),
                                  foreground=COLORS['text_primary'], spacing1=10, spacing3=6)
        text_widget.tag_configure('top_badge', font=('Segoe UI', 9, 'bold'),
                                  foreground='#ffffff', background=risk_color)
        text_widget.tag_configure('impact_badge', font=('Segoe UI', 9),
                                  foreground=COLORS['warning'], background=COLORS['bg_light'])
        text_widget.tag_configure('action_text', font=('Segoe UI', 11),
                                  foreground=COLORS['text_primary'], lmargin1=15, lmargin2=15,
                                  spacing1=4, spacing3=2)
        text_widget.tag_configure('reason_text', font=('Segoe UI', 10),
                                  foreground=COLORS['text_secondary'], lmargin1=15, lmargin2=15,
                                  spacing3=8)
        text_widget.tag_configure('card_num', font=('Segoe UI', 10, 'bold'),
                                  foreground=COLORS['accent'])
        text_widget.tag_configure('card_num_top', font=('Segoe UI', 10, 'bold'),
                                  foreground=risk_color)
        text_widget.tag_configure('separator', font=('Segoe UI', 4),
                                  foreground=COLORS['border'])
        text_widget.tag_configure('gen_action', font=('Segoe UI', 11),
                                  foreground=COLORS['text_primary'], lmargin1=15, lmargin2=30,
                                  spacing1=4, spacing3=4)

        # ── Write content ───────────────────────────────────────────
        factor_insights = rec.get('factor_insights', [])
        # Limit to top 5 insights only
        top_insights = factor_insights[:5]

        text_widget.insert(tk.END, f"🎯  Retention Strategy ({len(top_insights)} Key Actions)\n", 'section_title')

        if top_insights:
            for i, insight in enumerate(top_insights):
                is_top = insight.get('is_top_factor', False)
                shap_pct = insight.get('shap_impact', 0)

                # Number + badges line
                num_tag = 'card_num_top' if is_top else 'card_num'
                text_widget.insert(tk.END, f"  {i+1}. ", num_tag)

                if is_top:
                    text_widget.insert(tk.END, " TOP FACTOR ", 'top_badge')
                    text_widget.insert(tk.END, "  ")

                if shap_pct > 0:
                    text_widget.insert(tk.END, f" Impact: {shap_pct:.1f}% ", 'impact_badge')

                text_widget.insert(tk.END, "\n")

                # Problem (why)
                reason_text = insight.get('reason', '')
                text_widget.insert(tk.END, f"Problem: {reason_text}\n", 'reason_text')

                # Solution (action)
                action_text = insight.get('action', '')
                text_widget.insert(tk.END, f"→ Solution: {action_text}\n", 'action_text')

                # Thin separator
                text_widget.insert(tk.END, "─" * 60 + "\n", 'separator')
        else:
            text_widget.insert(tk.END, "No specific risk factors detected for this customer.\n\n",
                               'reason_text')

        # ── ROI Business Impact section ──────────────────────────────
        text_widget.tag_configure('roi_title', font=('Segoe UI', 13, 'bold'),
                                  foreground=COLORS['success'], spacing1=12, spacing3=6)
        text_widget.tag_configure('roi_value', font=('Segoe UI', 16, 'bold'),
                                  foreground=COLORS['success'], justify='center',
                                  spacing1=6, spacing3=4)
        text_widget.tag_configure('roi_detail', font=('Segoe UI', 10),
                                  foreground=COLORS['text_secondary'], lmargin1=15, lmargin2=15,
                                  spacing1=2, spacing3=2)
        text_widget.tag_configure('roi_cite', font=('Segoe UI', 9, 'italic'),
                                  foreground=COLORS['text_muted'], lmargin1=15,
                                  spacing1=8, spacing3=4)

        text_widget.insert(tk.END, "\n💰  ROI Business Impact\n", 'roi_title')

        prob_pct_val = rec.get('churn_probability', 0) * 100
        if prob_pct_val >= 50:  # Predicted churner
            net_value = self.CLV_BENEFIT - self.CAMPAIGN_COST
            text_widget.insert(tk.END, f"      +${net_value} net value per customer\n", 'roi_value')
            text_widget.insert(tk.END, f"  • CLV saved if retained: ${self.CLV_BENEFIT}\n", 'roi_detail')
            text_widget.insert(tk.END, f"  • Retention campaign cost: ${self.CAMPAIGN_COST}\n", 'roi_detail')
            text_widget.insert(tk.END, f"  • Net ROI per customer: ${net_value}\n", 'roi_detail')
            text_widget.insert(tk.END, f"  • Formula: ROI = (TP × ${self.CLV_BENEFIT}) − (FP × ${self.CAMPAIGN_COST})\n", 'roi_detail')
            text_widget.insert(tk.END, f"  • Model-wide ROI: $132,000 (339 TPs × ${self.CLV_BENEFIT} − 411 FPs × ${self.CAMPAIGN_COST})\n", 'roi_detail')
        else:  # Low risk
            text_widget.insert(tk.END, "      $0 — No retention action needed\n", 'roi_value')
            text_widget.insert(tk.END, "  • Customer is low risk — no campaign spend required\n", 'roi_detail')
            text_widget.insert(tk.END, f"  • Unnecessary retention offer would cost ${self.CAMPAIGN_COST}\n", 'roi_detail')

        text_widget.insert(tk.END, "\n  Based on profit-driven framework (De Caigny et al., 2018)\n", 'roi_cite')

        # Make read-only
        text_widget.config(state=tk.DISABLED)

        # ── Close button ────────────────────────────────────────────
        close_frame = tk.Frame(dialog, bg=COLORS['bg_dark'])
        close_frame.pack(fill=tk.X, padx=20, pady=(5, 15))

        close_btn = tk.Button(
            close_frame,
            text="Close",
            font=('Segoe UI', 11, 'bold'),
            bg=COLORS['bg_light'], fg=COLORS['text_primary'],
            activebackground=COLORS['border_light'],
            activeforeground=COLORS['text_primary'],
            relief=tk.FLAT,
            cursor='hand2',
            padx=30, pady=8,
            command=dialog.destroy
        )
        close_btn.pack(side=tk.RIGHT)

        # Hover effect on close button
        close_btn.bind('<Enter>', lambda e: close_btn.config(bg=COLORS['border_light']))
        close_btn.bind('<Leave>', lambda e: close_btn.config(bg=COLORS['bg_light']))
