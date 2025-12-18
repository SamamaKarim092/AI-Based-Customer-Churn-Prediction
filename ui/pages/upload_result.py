"""
Upload Result Page
Displays batch prediction results from uploaded data.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .base import BasePage
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS
from components.widgets import ModernButton


class UploadResultPage(BasePage):
    """Page for displaying batch prediction results."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.result_data = None
        self.setup_page()
    
    def setup_page(self):
        """Setup the upload result page."""
        # Header
        self.create_header(
            "Prediction Results",
            "Batch prediction results from uploaded data"
        )
        
        # Main content
        self.main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Summary section
        self.summary_card = tk.Frame(self.main_frame, bg=COLORS['bg_card'])
        self.summary_card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            self.summary_card, text="📊  Prediction Summary",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # Stats container
        self.stats_frame = tk.Frame(self.summary_card, bg=COLORS['bg_card'])
        self.stats_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Initial message when no data
        self.no_data_label = tk.Label(
            self.stats_frame,
            text="No prediction results yet.\nUpload a file and click 'Process & Predict' to see results.",
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted'],
            justify=tk.CENTER
        )
        self.no_data_label.pack(pady=20)
        
        # Results table section
        self.table_card = tk.Frame(self.main_frame, bg=COLORS['bg_card'])
        self.table_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Table title
        self.table_title_frame = tk.Frame(self.table_card, bg=COLORS['bg_card'])
        self.table_title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(
            self.table_title_frame, text="📋  Detailed Results",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(side=tk.LEFT)
        
        self.rows_label = tk.Label(
            self.table_title_frame, text="",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        )
        self.rows_label.pack(side=tk.RIGHT)
        
        # Table container
        self.table_container = tk.Frame(self.table_card, bg=COLORS['bg_card'])
        self.table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Action buttons
        self.btn_frame = tk.Frame(self.main_frame, bg=COLORS['bg_medium'])
        self.btn_frame.pack(fill=tk.X)
        
        self.export_btn = ModernButton(
            self.btn_frame, "Export Results to CSV", self.export_results,
            style='primary', icon="💾", colors=COLORS
        )
        self.export_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.export_btn.config(state=tk.DISABLED)
        
        ModernButton(
            self.btn_frame, "Upload New File", self.go_to_upload,
            style='secondary', icon="📤", colors=COLORS
        ).pack(side=tk.LEFT)
    
    def set_results(self, df, high_risk, moderate_risk, low_risk, churn_count):
        """Set the prediction results to display."""
        self.result_data = df
        
        # Clear previous stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Create stat cards
        stats = [
            ("🔴 High Risk", high_risk, COLORS['danger']),
            ("🟡 Moderate Risk", moderate_risk, COLORS['warning']),
            ("🟢 Low Risk", low_risk, COLORS['success']),
            ("📊 Predicted Churn", churn_count, COLORS['accent']),
            ("👥 Total Processed", len(df), COLORS['text_primary']),
        ]
        
        for label, value, color in stats:
            card = tk.Frame(self.stats_frame, bg=COLORS['bg_light'], padx=15, pady=10)
            card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            
            tk.Label(
                card, text=label,
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_muted']
            ).pack()
            
            tk.Label(
                card, text=str(value),
                font=('Segoe UI', 24, 'bold'),
                bg=COLORS['bg_light'],
                fg=color
            ).pack()
        
        # Churn percentage
        churn_pct = (churn_count / len(df)) * 100 if len(df) > 0 else 0
        pct_frame = tk.Frame(self.stats_frame, bg=COLORS['bg_light'], padx=15, pady=10)
        pct_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        tk.Label(
            pct_frame, text="📈 Churn Rate",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack()
        
        tk.Label(
            pct_frame, text=f"{churn_pct:.1f}%",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['danger'] if churn_pct > 30 else COLORS['warning'] if churn_pct > 15 else COLORS['success']
        ).pack()
        
        # Update table
        self.create_results_table(df)
        
        # Enable export button
        self.export_btn.config(state=tk.NORMAL)
    
    def create_results_table(self, df):
        """Create the results table with data."""
        # Clear previous table
        for widget in self.table_container.winfo_children():
            widget.destroy()
        
        # Update rows label
        self.rows_label.config(text=f"Showing {min(100, len(df))} of {len(df)} rows")
        
        # Create treeview
        columns = list(df.columns)
        tree = ttk.Treeview(self.table_container, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            # Adjust width based on column name
            if col in ['customer_id', 'age', 'churn']:
                width = 80
            elif col in ['prediction', 'risk_level']:
                width = 100
            elif col == 'churn_probability_%':
                width = 120
            else:
                width = 100
            tree.column(col, width=width, anchor=tk.CENTER)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(self.table_container, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(self.table_container, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack scrollbars and tree
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Insert data (limit to 100 rows for performance)
        for idx, row in df.head(100).iterrows():
            tree.insert('', tk.END, values=list(row))
    
    def export_results(self):
        """Export prediction results to CSV."""
        if self.result_data is None:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Prediction Results"
        )
        
        if file_path:
            try:
                self.result_data.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Results exported successfully!\n\nFile saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")
    
    def go_to_upload(self):
        """Navigate to upload page."""
        self.controller.show_page('upload')
    
    def on_show(self):
        """Called when page is shown."""
        # If no data, show message
        if self.result_data is None:
            pass  # Keep showing the no data message
