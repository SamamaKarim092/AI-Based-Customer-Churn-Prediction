"""
Reports Page
PDF report generation interface.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from .base import BasePage
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS
from components.widgets import ModernButton


class ReportsPage(BasePage):
    """Page for generating PDF reports."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.setup_page()
    
    def setup_page(self):
        """Setup the reports page."""
        # Header
        self.create_header(
            "Reports",
            "Generate and export PDF reports"
        )
        
        # Main content
        main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Report types
        self.create_report_options(main_frame)
        
        # Report settings
        self.create_report_settings(main_frame)
        
        # Recent reports
        self.create_recent_reports(main_frame)
    
    def create_report_options(self, parent):
        """Create report type options."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            card, text="📄  Report Types",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # Options container
        options_frame = tk.Frame(card, bg=COLORS['bg_card'])
        options_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        report_types = [
            ("📊 Summary Report", "Overview of churn predictions and recommendations", "summary"),
            ("👥 Customer Analysis", "Detailed analysis of individual customers", "customer"),
            ("📈 Model Performance", "ML model metrics and accuracy report", "model"),
            ("📋 Batch Predictions", "Results from batch prediction processing", "batch"),
        ]
        
        self.selected_report = tk.StringVar(value="summary")
        
        for title, description, value in report_types:
            self.create_report_option(options_frame, title, description, value)
    
    def create_report_option(self, parent, title, description, value):
        """Create a single report option."""
        frame = tk.Frame(parent, bg=COLORS['bg_light'], cursor='hand2')
        frame.pack(fill=tk.X, pady=5)
        
        inner = tk.Frame(frame, bg=COLORS['bg_light'], padx=15, pady=12)
        inner.pack(fill=tk.X)
        
        # Radio button
        rb = tk.Radiobutton(
            inner, text=title,
            variable=self.selected_report,
            value=value,
            font=FONTS['body_bold'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary'],
            selectcolor=COLORS['bg_medium'],
            activebackground=COLORS['bg_light'],
            activeforeground=COLORS['text_primary']
        )
        rb.pack(anchor=tk.W)
        
        tk.Label(
            inner, text=description,
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary']
        ).pack(anchor=tk.W, padx=(20, 0))
        
        # Hover effect
        def on_enter(e):
            frame.config(bg=COLORS['sidebar_hover'])
            inner.config(bg=COLORS['sidebar_hover'])
            for child in inner.winfo_children():
                try:
                    child.config(bg=COLORS['sidebar_hover'])
                except:
                    pass
        
        def on_leave(e):
            frame.config(bg=COLORS['bg_light'])
            inner.config(bg=COLORS['bg_light'])
            for child in inner.winfo_children():
                try:
                    child.config(bg=COLORS['bg_light'])
                except:
                    pass
        
        for widget in [frame, inner]:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
    
    def create_report_settings(self, parent):
        """Create report settings section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            card, text="⚙️  Report Settings",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Options
        self.include_charts = tk.BooleanVar(value=True)
        self.include_recommendations = tk.BooleanVar(value=True)
        self.include_details = tk.BooleanVar(value=False)
        
        options = [
            ("Include visualizations and charts", self.include_charts),
            ("Include action recommendations", self.include_recommendations),
            ("Include detailed customer data", self.include_details),
        ]
        
        for text, var in options:
            cb = tk.Checkbutton(
                content, text=text,
                variable=var,
                font=FONTS['body'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_primary'],
                selectcolor=COLORS['bg_medium'],
                activebackground=COLORS['bg_card'],
                activeforeground=COLORS['text_primary']
            )
            cb.pack(anchor=tk.W, pady=3)
        
        # Generate button
        btn_frame = tk.Frame(content, bg=COLORS['bg_card'])
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        ModernButton(
            btn_frame, "Generate Report", self.generate_report,
            style='primary', icon="📄", colors=COLORS
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ModernButton(
            btn_frame, "Export as PDF", self.export_pdf,
            style='secondary', icon="📥", colors=COLORS
        ).pack(side=tk.LEFT)
    
    def create_recent_reports(self, parent):
        """Create recent reports section."""
        card = tk.Frame(parent, bg=COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            card, text="📜  Recent Reports",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        content = tk.Frame(card, bg=COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Placeholder for recent reports
        tk.Label(
            content,
            text="No reports generated yet.\n\nSelect a report type above and click 'Generate Report' to create your first report.",
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted'],
            justify=tk.CENTER
        ).pack(expand=True)
    
    def generate_report(self):
        """Generate the selected report."""
        report_type = self.selected_report.get()
        messagebox.showinfo(
            "Report Generation",
            f"Generating {report_type} report...\n\n"
            "This feature is coming soon!\n\n"
            "The report will include:\n"
            f"• Charts: {'Yes' if self.include_charts.get() else 'No'}\n"
            f"• Recommendations: {'Yes' if self.include_recommendations.get() else 'No'}\n"
            f"• Detailed data: {'Yes' if self.include_details.get() else 'No'}"
        )
    
    def export_pdf(self):
        """Export report as PDF."""
        file_path = filedialog.asksaveasfilename(
            title="Save Report as PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            messagebox.showinfo(
                "Export PDF",
                f"PDF export feature coming soon!\n\nWould save to:\n{file_path}"
            )
