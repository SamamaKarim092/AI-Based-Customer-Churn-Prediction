"""
Customer Churn Prediction UI - Enhanced Version
Modern Tkinter-based desktop application with charts, gauges, and animations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
import math
import threading

# Add src directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.insert(0, os.path.join(project_dir, 'src'))

from predict import predict_churn, load_model_and_encoders, preprocess_customer_data
from explain import explain_prediction, load_model_and_data
from recommend import generate_full_recommendation

# Try to import matplotlib for charts
try:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Charts will be disabled.")


# Color scheme
COLORS = {
    'bg_dark': '#1a1a2e',
    'bg_medium': '#16213e',
    'bg_light': '#0f3460',
    'accent': '#e94560',
    'accent_light': '#ff6b6b',
    'success': '#00d9a0',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'text_primary': '#ffffff',
    'text_secondary': '#a0a0a0',
    'card_bg': '#1f2940',
    'border': '#2d3748'
}


class AnimatedGauge(tk.Canvas):
    """Animated circular gauge for displaying churn probability."""
    
    def __init__(self, parent, size=200, **kwargs):
        super().__init__(parent, width=size, height=size, 
                        bg=COLORS['card_bg'], highlightthickness=0, **kwargs)
        self.size = size
        self.center = size // 2
        self.radius = size // 2 - 20
        self.current_value = 0
        self.target_value = 0
        self.animation_id = None
        
        self.draw_gauge(0)
    
    def draw_gauge(self, value):
        """Draw the gauge with the given value (0-100)."""
        self.delete("all")
        
        # Background arc
        self.create_arc(
            20, 20, self.size - 20, self.size - 20,
            start=135, extent=270,
            style=tk.ARC, width=15,
            outline=COLORS['bg_light']
        )
        
        # Determine color based on value
        if value >= 70:
            color = COLORS['danger']
        elif value >= 40:
            color = COLORS['warning']
        else:
            color = COLORS['success']
        
        # Value arc
        extent = (value / 100) * 270
        self.create_arc(
            20, 20, self.size - 20, self.size - 20,
            start=135, extent=-extent,
            style=tk.ARC, width=15,
            outline=color
        )
        
        # Center text
        self.create_text(
            self.center, self.center - 10,
            text=f"{value:.1f}%",
            font=('Helvetica', 24, 'bold'),
            fill=color
        )
        
        # Label
        risk_label = "HIGH RISK" if value >= 70 else ("MODERATE" if value >= 40 else "LOW RISK")
        self.create_text(
            self.center, self.center + 25,
            text=risk_label,
            font=('Helvetica', 12, 'bold'),
            fill=COLORS['text_secondary']
        )
    
    def animate_to(self, target_value):
        """Animate the gauge to the target value."""
        self.target_value = target_value
        if self.animation_id:
            self.after_cancel(self.animation_id)
        self.animate_step()
    
    def animate_step(self):
        """Single animation step."""
        diff = self.target_value - self.current_value
        if abs(diff) < 0.5:
            self.current_value = self.target_value
            self.draw_gauge(self.current_value)
            return
        
        # Smooth easing
        step = diff * 0.1
        self.current_value += step
        self.draw_gauge(self.current_value)
        
        self.animation_id = self.after(20, self.animate_step)
    
    def reset(self):
        """Reset gauge to 0."""
        self.current_value = 0
        self.target_value = 0
        self.draw_gauge(0)


class FeatureBarChart(tk.Canvas):
    """Horizontal bar chart for feature importance."""
    
    def __init__(self, parent, width=400, height=250, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=COLORS['card_bg'], highlightthickness=0, **kwargs)
        self.chart_width = width
        self.chart_height = height
    
    def draw_bars(self, features):
        """Draw horizontal bars for feature importance."""
        self.delete("all")
        
        if not features:
            self.create_text(
                self.chart_width // 2, self.chart_height // 2,
                text="No data to display",
                fill=COLORS['text_secondary'],
                font=('Helvetica', 12)
            )
            return
        
        # Title
        self.create_text(
            self.chart_width // 2, 15,
            text="Feature Impact on Churn",
            fill=COLORS['text_primary'],
            font=('Helvetica', 11, 'bold')
        )
        
        max_abs_value = max(abs(f['shap_value']) for f in features) if features else 1
        bar_height = 22
        start_y = 40
        label_width = 130
        bar_area_width = self.chart_width - label_width - 60
        
        for i, feature in enumerate(features[:8]):  # Show top 8
            y = start_y + i * (bar_height + 5)
            
            # Feature name
            display_name = feature['display_name'][:15]
            self.create_text(
                label_width - 5, y + bar_height // 2,
                text=display_name,
                anchor=tk.E,
                fill=COLORS['text_secondary'],
                font=('Helvetica', 9)
            )
            
            # Bar
            bar_width = (abs(feature['shap_value']) / max_abs_value) * (bar_area_width / 2)
            bar_x = label_width + bar_area_width // 2
            
            if feature['shap_value'] > 0:
                color = COLORS['danger']
                self.create_rectangle(
                    bar_x, y + 2,
                    bar_x + bar_width, y + bar_height - 2,
                    fill=color, outline=''
                )
            else:
                color = COLORS['success']
                self.create_rectangle(
                    bar_x - bar_width, y + 2,
                    bar_x, y + bar_height - 2,
                    fill=color, outline=''
                )
            
            # Value label
            value_text = f"{feature['shap_value']:+.2f}"
            text_x = bar_x + bar_width + 5 if feature['shap_value'] > 0 else bar_x - bar_width - 5
            anchor = tk.W if feature['shap_value'] > 0 else tk.E
            self.create_text(
                text_x, y + bar_height // 2,
                text=value_text,
                anchor=anchor,
                fill=color,
                font=('Helvetica', 8, 'bold')
            )
        
        # Center line
        center_x = label_width + bar_area_width // 2
        self.create_line(
            center_x, 35, center_x, start_y + 8 * (bar_height + 5),
            fill=COLORS['border'], width=1
        )
        
        # Legend
        self.create_rectangle(10, self.chart_height - 25, 20, self.chart_height - 15, 
                             fill=COLORS['danger'], outline='')
        self.create_text(25, self.chart_height - 20, text="Increases Churn", 
                        anchor=tk.W, fill=COLORS['text_secondary'], font=('Helvetica', 8))
        
        self.create_rectangle(150, self.chart_height - 25, 160, self.chart_height - 15, 
                             fill=COLORS['success'], outline='')
        self.create_text(165, self.chart_height - 20, text="Decreases Churn", 
                        anchor=tk.W, fill=COLORS['text_secondary'], font=('Helvetica', 8))


class ChurnPredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Customer Churn Prediction System")
        self.root.geometry("1200x800")
        self.root.minsize(1100, 700)
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Style configuration
        self.setup_styles()
        
        # Load model on startup
        self.model = None
        self.encoders = None
        self.feature_names = None
        self.load_model()
        
        # Setup UI
        self.setup_ui()
        
        # Animation state
        self.pulse_state = 0
    
    def setup_styles(self):
        """Configure ttk styles for modern look."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Dark.TFrame', background=COLORS['bg_dark'])
        style.configure('Card.TFrame', background=COLORS['card_bg'])
        style.configure('Dark.TLabel', background=COLORS['bg_dark'], 
                       foreground=COLORS['text_primary'])
        style.configure('Card.TLabel', background=COLORS['card_bg'], 
                       foreground=COLORS['text_primary'])
        style.configure('Secondary.TLabel', background=COLORS['card_bg'], 
                       foreground=COLORS['text_secondary'])
        
        # Button styles
        style.configure('Accent.TButton', 
                       background=COLORS['accent'],
                       foreground='white',
                       padding=(20, 10),
                       font=('Helvetica', 10, 'bold'))
        style.map('Accent.TButton',
                 background=[('active', COLORS['accent_light'])])
        
        style.configure('Secondary.TButton',
                       background=COLORS['bg_light'],
                       foreground='white',
                       padding=(15, 8))
        
        # Entry style
        style.configure('Dark.TEntry',
                       fieldbackground=COLORS['bg_light'],
                       foreground=COLORS['text_primary'],
                       insertcolor=COLORS['text_primary'])
        
        style.configure('Dark.TCombobox',
                       fieldbackground=COLORS['bg_light'],
                       background=COLORS['bg_light'],
                       foreground=COLORS['text_primary'])
        
        style.configure('Dark.TSpinbox',
                       fieldbackground=COLORS['bg_light'],
                       background=COLORS['bg_light'],
                       foreground=COLORS['text_primary'])
        
        # LabelFrame
        style.configure('Card.TLabelframe', 
                       background=COLORS['card_bg'],
                       foreground=COLORS['text_primary'])
        style.configure('Card.TLabelframe.Label',
                       background=COLORS['card_bg'],
                       foreground=COLORS['accent'],
                       font=('Helvetica', 11, 'bold'))
    
    def load_model(self):
        """Load the trained model and encoders."""
        try:
            self.model, self.encoders, self.feature_names = load_model_and_encoders()
        except FileNotFoundError as e:
            messagebox.showerror("Model Not Found", 
                                str(e) + "\n\nPlease run train_model.py first.")
            self.root.destroy()
            return
    
    def setup_ui(self):
        """Setup the main UI components."""
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_frame)
        
        # Content area with two columns
        content_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Left column - Input
        left_frame = ttk.Frame(content_frame, style='Dark.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_input_section(left_frame)
        self.create_action_buttons(left_frame)
        self.create_recommendations_section(left_frame)
        
        # Right column - Results & Charts
        right_frame = ttk.Frame(content_frame, style='Dark.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_gauge_section(right_frame)
        self.create_chart_section(right_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create the header section."""
        header_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title with icon
        title_label = tk.Label(
            header_frame,
            text="🤖  AI Customer Churn Prediction System",
            font=('Helvetica', 20, 'bold'),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary']
        )
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle = tk.Label(
            header_frame,
            text="Predict • Explain • Recommend",
            font=('Helvetica', 11),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_secondary']
        )
        subtitle.pack(side=tk.RIGHT, padx=10)
    
    def create_input_section(self, parent):
        """Create the input fields section."""
        # Card frame
        card = tk.Frame(parent, bg=COLORS['card_bg'], padx=20, pady=15)
        card.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        tk.Label(
            card, text="📋 Customer Information",
            font=('Helvetica', 12, 'bold'),
            bg=COLORS['card_bg'], fg=COLORS['accent']
        ).grid(row=0, column=0, columnspan=6, sticky=tk.W, pady=(0, 15))
        
        self.inputs = {}
        
        # Row 1
        self.create_input_field(card, "Age", 'age', 1, 0, 'spinbox', (18, 100), 35)
        self.create_input_field(card, "Gender", 'gender', 1, 2, 'combo', ['Male', 'Female'], 'Male')
        self.create_input_field(card, "Subscription", 'subscription_type', 1, 4, 'combo', 
                               ['Basic', 'Standard', 'Premium'], 'Standard')
        
        # Row 2
        self.create_input_field(card, "Monthly ($)", 'monthly_charges', 2, 0, 'spinbox', (9.99, 50.00), 19.99)
        self.create_input_field(card, "Tenure (mo)", 'tenure_in_months', 2, 2, 'spinbox', (1, 120), 12)
        self.create_input_field(card, "Logins/mo", 'login_frequency', 2, 4, 'spinbox', (0, 100), 15)
        
        # Row 3
        self.create_input_field(card, "Last Login", 'last_login_days', 3, 0, 'spinbox', (0, 365), 5)
        self.create_input_field(card, "Watch (hrs)", 'watch_time', 3, 2, 'spinbox', (0.0, 200.0), 20.0)
        self.create_input_field(card, "Pay Fails", 'payment_failures', 3, 4, 'spinbox', (0, 10), 0)
        
        # Row 4
        self.create_input_field(card, "Support Calls", 'customer_support_calls', 4, 0, 'spinbox', (0, 20), 1)
    
    def create_input_field(self, parent, label, key, row, col, input_type, options, default):
        """Create a single input field."""
        tk.Label(
            parent, text=label + ":",
            font=('Helvetica', 9),
            bg=COLORS['card_bg'], fg=COLORS['text_secondary']
        ).grid(row=row, column=col, sticky=tk.E, padx=(10, 5), pady=8)
        
        if input_type == 'combo':
            widget = ttk.Combobox(parent, values=options, width=12, state='readonly')
            widget.set(default)
        else:
            widget = ttk.Spinbox(parent, from_=options[0], to=options[1], width=12)
            widget.set(default)
        
        widget.grid(row=row, column=col + 1, sticky=tk.W, padx=5, pady=8)
        self.inputs[key] = widget
    
    def create_action_buttons(self, parent):
        """Create action buttons."""
        btn_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Predict button (large, accent color)
        self.predict_btn = tk.Button(
            btn_frame, text="🔮  PREDICT CHURN",
            font=('Helvetica', 12, 'bold'),
            bg=COLORS['accent'], fg='white',
            activebackground=COLORS['accent_light'],
            activeforeground='white',
            relief=tk.FLAT, cursor='hand2',
            padx=30, pady=12,
            command=self.predict
        )
        self.predict_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Sample buttons
        sample_frame = tk.Frame(btn_frame, bg=COLORS['bg_dark'])
        sample_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            sample_frame, text="⚠️ High Risk",
            font=('Helvetica', 9),
            bg=COLORS['danger'], fg='white',
            relief=tk.FLAT, cursor='hand2',
            padx=15, pady=8,
            command=self.load_high_risk_sample
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            sample_frame, text="✅ Low Risk",
            font=('Helvetica', 9),
            bg=COLORS['success'], fg='white',
            relief=tk.FLAT, cursor='hand2',
            padx=15, pady=8,
            command=self.load_low_risk_sample
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            sample_frame, text="🔄 Clear",
            font=('Helvetica', 9),
            bg=COLORS['bg_light'], fg='white',
            relief=tk.FLAT, cursor='hand2',
            padx=15, pady=8,
            command=self.clear_all
        ).pack(side=tk.LEFT, padx=2)
    
    def create_recommendations_section(self, parent):
        """Create recommendations display."""
        card = tk.Frame(parent, bg=COLORS['card_bg'], padx=20, pady=15)
        card.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        tk.Label(
            card, text="💡 Recommended Actions",
            font=('Helvetica', 12, 'bold'),
            bg=COLORS['card_bg'], fg=COLORS['accent']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.recommendations_text = tk.Text(
            card, wrap=tk.WORD, height=12,
            bg=COLORS['bg_medium'], fg=COLORS['text_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT, padx=10, pady=10,
            insertbackground=COLORS['text_primary']
        )
        self.recommendations_text.pack(fill=tk.BOTH, expand=True)
        self.recommendations_text.config(state=tk.DISABLED)
    
    def create_gauge_section(self, parent):
        """Create the gauge display section."""
        card = tk.Frame(parent, bg=COLORS['card_bg'], padx=20, pady=15)
        card.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            card, text="📊 Churn Risk Score",
            font=('Helvetica', 12, 'bold'),
            bg=COLORS['card_bg'], fg=COLORS['accent']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        gauge_frame = tk.Frame(card, bg=COLORS['card_bg'])
        gauge_frame.pack(fill=tk.X)
        
        # Gauge
        self.gauge = AnimatedGauge(gauge_frame, size=180)
        self.gauge.pack(side=tk.LEFT, padx=(20, 30))
        
        # Info panel
        info_frame = tk.Frame(gauge_frame, bg=COLORS['card_bg'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.prediction_label = tk.Label(
            info_frame, text="Prediction: --",
            font=('Helvetica', 14, 'bold'),
            bg=COLORS['card_bg'], fg=COLORS['text_primary']
        )
        self.prediction_label.pack(anchor=tk.W, pady=5)
        
        self.risk_label = tk.Label(
            info_frame, text="Risk Level: --",
            font=('Helvetica', 12),
            bg=COLORS['card_bg'], fg=COLORS['text_secondary']
        )
        self.risk_label.pack(anchor=tk.W, pady=5)
        
        # Factor summary
        self.factor_summary = tk.Label(
            info_frame, text="Top factors will appear here...",
            font=('Helvetica', 10),
            bg=COLORS['card_bg'], fg=COLORS['text_secondary'],
            wraplength=300, justify=tk.LEFT
        )
        self.factor_summary.pack(anchor=tk.W, pady=(15, 5))
    
    def create_chart_section(self, parent):
        """Create the chart display section."""
        card = tk.Frame(parent, bg=COLORS['card_bg'], padx=20, pady=15)
        card.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        tk.Label(
            card, text="📈 Feature Impact Analysis",
            font=('Helvetica', 12, 'bold'),
            bg=COLORS['card_bg'], fg=COLORS['accent']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.bar_chart = FeatureBarChart(card, width=450, height=280)
        self.bar_chart.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self, parent):
        """Create status bar."""
        self.status_var = tk.StringVar(value="Ready. Enter customer data and click 'Predict Churn'.")
        status_bar = tk.Label(
            parent, textvariable=self.status_var,
            font=('Helvetica', 9),
            bg=COLORS['bg_medium'], fg=COLORS['text_secondary'],
            anchor=tk.W, padx=10, pady=5
        )
        status_bar.pack(fill=tk.X, pady=(15, 0))
    
    def get_customer_data(self):
        """Collect customer data from input fields."""
        try:
            data = {
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
            return data
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input value: {e}")
            return None
    
    def predict(self):
        """Run prediction on current customer data."""
        self.status_var.set("🔄 Running prediction...")
        self.predict_btn.config(state=tk.DISABLED, text="⏳ Processing...")
        self.root.update()
        
        # Get customer data
        customer_data = self.get_customer_data()
        if customer_data is None:
            self.status_var.set("❌ Error: Invalid input data")
            self.predict_btn.config(state=tk.NORMAL, text="🔮  PREDICT CHURN")
            return
        
        try:
            # Get prediction
            prediction = predict_churn(customer_data, self.model, self.encoders, self.feature_names)
            
            # Get explanation
            features = preprocess_customer_data(customer_data, self.encoders, self.feature_names)
            explanation = explain_prediction(features, self.model, self.feature_names, customer_data)
            
            # Get recommendation
            recommendation = generate_full_recommendation(
                prediction['churn_probability'], 
                customer_data, 
                explanation['top_factors']
            )
            
            # Update UI with animation
            self.update_results(prediction, explanation, recommendation)
            
            risk_emoji = "🔴" if prediction['risk_level'] == 'HIGH' else ("🟡" if prediction['risk_level'] == 'MODERATE' else "🟢")
            self.status_var.set(f"✅ Prediction complete! {risk_emoji} Risk Level: {prediction['risk_level']}")
            
        except Exception as e:
            messagebox.showerror("Prediction Error", f"Error during prediction: {str(e)}")
            self.status_var.set("❌ Error during prediction")
        
        self.predict_btn.config(state=tk.NORMAL, text="🔮  PREDICT CHURN")
    
    def update_results(self, prediction, explanation, recommendation):
        """Update all result displays."""
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
        
        # Factor summary
        if explanation['top_factors']:
            factors = [f"• {f['display_name']}" for f in explanation['top_factors'][:3]]
            self.factor_summary.config(text="Top factors:\n" + "\n".join(factors))
        
        # Update bar chart
        self.bar_chart.draw_bars(explanation['all_features'])
        
        # Update recommendations
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete(1.0, tk.END)
        
        rec_text = f"{'='*50}\n"
        rec_text += f"STATUS: {recommendation['summary']}\n"
        rec_text += f"{'='*50}\n\n"
        rec_text += f"PRIMARY ACTION:\n   ➤ {recommendation['primary_action']}\n\n"
        rec_text += "RECOMMENDED ACTIONS:\n"
        for i, action in enumerate(recommendation['recommended_actions'][:5], 1):
            rec_text += f"   {i}. {action}\n"
        
        self.recommendations_text.insert(tk.END, rec_text)
        self.recommendations_text.config(state=tk.DISABLED)
    
    def clear_all(self):
        """Clear all inputs and results."""
        # Reset inputs
        self.inputs['age'].set(35)
        self.inputs['gender'].set('Male')
        self.inputs['subscription_type'].set('Standard')
        self.inputs['monthly_charges'].set(19.99)
        self.inputs['tenure_in_months'].set(12)
        self.inputs['login_frequency'].set(15)
        self.inputs['last_login_days'].set(5)
        self.inputs['watch_time'].set(20.0)
        self.inputs['payment_failures'].set(0)
        self.inputs['customer_support_calls'].set(1)
        
        # Reset displays
        self.gauge.reset()
        self.prediction_label.config(text="Prediction: --", fg=COLORS['text_primary'])
        self.risk_label.config(text="Risk Level: --", fg=COLORS['text_secondary'])
        self.factor_summary.config(text="Top factors will appear here...")
        self.bar_chart.delete("all")
        
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.config(state=tk.DISABLED)
        
        self.status_var.set("🔄 Cleared. Enter new customer data.")
    
    def load_high_risk_sample(self):
        """Load sample high-risk customer."""
        self.inputs['age'].set(25)
        self.inputs['gender'].set('Male')
        self.inputs['subscription_type'].set('Basic')
        self.inputs['monthly_charges'].set(12.99)
        self.inputs['tenure_in_months'].set(2)
        self.inputs['login_frequency'].set(3)
        self.inputs['last_login_days'].set(45)
        self.inputs['watch_time'].set(2.5)
        self.inputs['payment_failures'].set(2)
        self.inputs['customer_support_calls'].set(4)
        self.status_var.set("⚠️ Loaded high-risk sample. Click 'Predict Churn' to analyze.")
    
    def load_low_risk_sample(self):
        """Load sample low-risk customer."""
        self.inputs['age'].set(45)
        self.inputs['gender'].set('Female')
        self.inputs['subscription_type'].set('Premium')
        self.inputs['monthly_charges'].set(29.99)
        self.inputs['tenure_in_months'].set(48)
        self.inputs['login_frequency'].set(25)
        self.inputs['last_login_days'].set(1)
        self.inputs['watch_time'].set(45.0)
        self.inputs['payment_failures'].set(0)
        self.inputs['customer_support_calls'].set(1)
        self.status_var.set("✅ Loaded low-risk sample. Click 'Predict Churn' to analyze.")


def main():
    """Run the application."""
    root = tk.Tk()
    
    # Set window icon if available
    try:
        root.iconbitmap('')
    except:
        pass
    
    app = ChurnPredictionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
