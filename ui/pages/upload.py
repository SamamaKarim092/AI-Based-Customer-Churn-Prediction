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
        
        messagebox.showinfo(
            "Coming Soon",
            "Batch prediction feature is coming soon!\n\n"
            "This will allow you to:\n"
            "• Process multiple customers at once\n"
            "• Export predictions to CSV/Excel\n"
            "• Generate batch reports"
        )
    
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
