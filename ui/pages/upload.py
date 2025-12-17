"""
Upload Page
CSV/Excel file upload for batch predictions.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .base import BasePage
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS
from components.widgets import ModernButton


class UploadPage(BasePage):
    """Page for uploading CSV/Excel files."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.uploaded_file = None
        self.setup_page()
    
    def setup_page(self):
        """Setup the upload page."""
        # Header
        self.create_header(
            "Upload Data",
            "Upload CSV or Excel files for batch predictions"
        )
        
        # Main content
        main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Upload area
        self.create_upload_area(main_frame)
        
        # File info area
        self.create_file_info(main_frame)
        
        # Preview area
        self.create_preview_area(main_frame)
    
    def create_upload_area(self, parent):
        """Create the drag & drop upload area."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Drop zone
        drop_zone = tk.Frame(
            card, bg=COLORS['bg_light'],
            highlightthickness=2, highlightcolor=COLORS['border'],
            highlightbackground=COLORS['border']
        )
        drop_zone.pack(fill=tk.X, padx=20, pady=20)
        
        inner = tk.Frame(drop_zone, bg=COLORS['bg_light'])
        inner.pack(fill=tk.X, pady=40)
        
        # Icon
        tk.Label(
            inner, text="📤",
            font=('Segoe UI', 48),
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack()
        
        tk.Label(
            inner, text="Drop your CSV or Excel file here",
            font=FONTS['heading'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary']
        ).pack(pady=(10, 5))
        
        tk.Label(
            inner, text="or",
            font=FONTS['body'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack()
        
        # Browse button
        ModernButton(
            inner, "Browse Files", self.browse_file,
            style='primary', icon="📂", colors=COLORS
        ).pack(pady=15)
        
        tk.Label(
            inner, text="Supported formats: CSV, XLSX, XLS",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack()
    
    def create_file_info(self, parent):
        """Create file information display."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(card, bg=COLORS['bg_card'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_frame,
            text="📁  File Information",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W)
        
        # Info content
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.file_name_label = tk.Label(
            content, text="No file selected",
            font=FONTS['body_bold'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        )
        self.file_name_label.pack(anchor=tk.W)
        
        self.file_stats_label = tk.Label(
            content, text="Upload a file to see details",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        )
        self.file_stats_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Action buttons
        btn_frame = tk.Frame(content, bg=COLORS['bg_card'])
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.process_btn = ModernButton(
            btn_frame, "Process & Predict", self.process_file,
            style='primary', icon="🔮", colors=COLORS
        )
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.process_btn.config(state=tk.DISABLED)
        
        ModernButton(
            btn_frame, "Clear", self.clear_file,
            style='secondary', icon="🔄", colors=COLORS
        ).pack(side=tk.LEFT)
    
    def create_preview_area(self, parent):
        """Create data preview area."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(card, bg=COLORS['bg_card'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            title_frame,
            text="👁️  Data Preview",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W)
        
        # Preview text
        preview_frame = tk.Frame(card, bg=COLORS['bg_card'])
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.preview_text = tk.Text(
            preview_frame, wrap=tk.NONE, height=12,
            bg=COLORS['bg_light'], fg=COLORS['text_primary'],
            font=FONTS['mono_small'],
            relief=tk.FLAT, padx=10, pady=10
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        self.preview_text.insert(tk.END, "Upload a file to see preview...")
        self.preview_text.config(state=tk.DISABLED)
    
    def browse_file(self):
        """Open file browser dialog."""
        file_path = filedialog.askopenfilename(
            title="Select Customer Data File",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx;*.xls"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """Load and preview the selected file."""
        import pandas as pd
        
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            self.uploaded_file = {
                'path': file_path,
                'name': os.path.basename(file_path),
                'data': df
            }
            
            # Update labels
            self.file_name_label.config(
                text=f"📄 {self.uploaded_file['name']}",
                fg=COLORS['text_primary']
            )
            self.file_stats_label.config(
                text=f"Rows: {len(df)} | Columns: {len(df.columns)}"
            )
            
            # Enable process button
            self.process_btn.config(state=tk.NORMAL)
            
            # Update preview
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, df.head(10).to_string())
            self.preview_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def process_file(self):
        """Process the uploaded file for predictions."""
        if not self.uploaded_file:
            messagebox.showwarning("Warning", "Please upload a file first.")
            return
        
        import pandas as pd
        import numpy as np
        
        # Add src directory to path for imports
        src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src')
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        
        from predict import predict_churn, load_model_and_encoders
        
        df = self.uploaded_file['data'].copy()
        
        # Required columns for prediction
        required_columns = [
            'age', 'gender', 'subscription_type', 'monthly_charges', 
            'tenure_in_months', 'login_frequency', 'last_login_days', 
            'watch_time', 'payment_failures', 'customer_support_calls'
        ]
        
        # Check if all required columns exist
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            messagebox.showerror(
                "Missing Columns",
                f"The following required columns are missing:\n{', '.join(missing_cols)}"
            )
            return
        
        try:
            # Load model once
            model, encoders, feature_names = load_model_and_encoders()
            
            # Prepare result columns
            predictions = []
            probabilities = []
            risk_levels = []
            
            # Process each row
            total_rows = len(df)
            for idx, row in df.iterrows():
                customer_data = {
                    'age': row['age'],
                    'gender': row['gender'],
                    'subscription_type': row['subscription_type'],
                    'monthly_charges': row['monthly_charges'],
                    'tenure_in_months': row['tenure_in_months'],
                    'login_frequency': row['login_frequency'],
                    'last_login_days': row['last_login_days'],
                    'watch_time': row['watch_time'],
                    'payment_failures': row['payment_failures'],
                    'customer_support_calls': row['customer_support_calls']
                }
                
                result = predict_churn(customer_data, model, encoders, feature_names)
                predictions.append(result['prediction_label'])
                probabilities.append(round(result['churn_probability'] * 100, 1))
                risk_levels.append(result['risk_level'])
            
            # Add results to dataframe
            df['prediction'] = predictions
            df['churn_probability_%'] = probabilities
            df['risk_level'] = risk_levels
            
            # Store results
            self.prediction_results = df
            
            # Calculate summary
            high_risk = len(df[df['risk_level'] == 'HIGH'])
            moderate_risk = len(df[df['risk_level'] == 'MODERATE'])
            low_risk = len(df[df['risk_level'] == 'LOW'])
            churn_count = len(df[df['prediction'] == 'Churn'])
            
            # Show results window
            self.show_results_window(df, high_risk, moderate_risk, low_risk, churn_count)
            
        except Exception as e:
            messagebox.showerror("Prediction Error", f"Error during prediction:\n{str(e)}")
    
    def show_results_window(self, df, high_risk, moderate_risk, low_risk, churn_count):
        """Display prediction results in a new window."""
        results_window = tk.Toplevel(self)
        results_window.title("Batch Prediction Results")
        results_window.geometry("900x600")
        results_window.configure(bg=COLORS['bg_medium'])
        
        # Header
        header = tk.Frame(results_window, bg=COLORS['bg_card'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            header, text="🎯  Prediction Results",
            font=FONTS['heading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        tk.Label(
            header, text=f"Processed {len(df)} customers",
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(anchor=tk.W, padx=15, pady=(0, 15))
        
        # Summary stats
        stats_frame = tk.Frame(results_window, bg=COLORS['bg_medium'])
        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Create stat cards
        stats = [
            ("🔴 High Risk", high_risk, COLORS['danger']),
            ("🟡 Moderate", moderate_risk, COLORS['warning']),
            ("🟢 Low Risk", low_risk, COLORS['success']),
            ("📊 Will Churn", churn_count, COLORS['accent'])
        ]
        
        for label, value, color in stats:
            card = tk.Frame(stats_frame, bg=COLORS['bg_card'])
            card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            
            tk.Label(
                card, text=label,
                font=FONTS['small'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_secondary']
            ).pack(pady=(10, 0))
            
            tk.Label(
                card, text=str(value),
                font=('Segoe UI', 24, 'bold'),
                bg=COLORS['bg_card'],
                fg=color
            ).pack(pady=(0, 10))
        
        # Results table
        table_frame = tk.Frame(results_window, bg=COLORS['bg_card'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Treeview for results
        columns = list(df.columns)
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack scrollbars and tree
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Insert data (limit to first 100 rows for performance)
        for idx, row in df.head(100).iterrows():
            tree.insert('', tk.END, values=list(row))
        
        if len(df) > 100:
            tk.Label(
                table_frame,
                text=f"Showing first 100 of {len(df)} rows",
                font=FONTS['small'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_muted']
            ).pack(pady=(0, 10))
        
        # Export button
        btn_frame = tk.Frame(results_window, bg=COLORS['bg_medium'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        ModernButton(
            btn_frame, "Export Results to CSV", lambda: self.export_results(df),
            style='primary', icon="💾", colors=COLORS
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ModernButton(
            btn_frame, "Close", results_window.destroy,
            style='secondary', icon="✖️", colors=COLORS
        ).pack(side=tk.LEFT)
    
    def export_results(self, df):
        """Export prediction results to CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Prediction Results"
        )
        
        if file_path:
            try:
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Results exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")
    
    def clear_file(self):
        """Clear the uploaded file."""
        self.uploaded_file = None
        self.file_name_label.config(text="No file selected", fg=COLORS['text_secondary'])
        self.file_stats_label.config(text="Upload a file to see details")
        self.process_btn.config(state=tk.DISABLED)
        
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, "Upload a file to see preview...")
        self.preview_text.config(state=tk.DISABLED)
