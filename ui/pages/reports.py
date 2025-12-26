"""
Reports Page
PDF report generation interface using prediction results.
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from .base import BasePage
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS, ICONS
from components.widgets import ModernButton


class ReportsPage(BasePage):
    """Page for generating PDF reports from prediction results."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.generated_reports = []
        self.setup_page()
    
    def setup_page(self):
        """Setup the reports page."""
        # Header
        self.create_header(
            "Reports",
            "Generate and export PDF reports from prediction results"
        )
        
        # Main content
        main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Data status banner
        self.create_data_status(main_frame)
        
        # Report types
        self.create_report_options(main_frame)
        
        # Report settings
        self.create_report_settings(main_frame)
        
        # Recent reports
        self.create_recent_reports(main_frame)
    
    def create_data_status(self, parent):
        """Create data status banner."""
        self.status_card = tk.Frame(parent, bg=COLORS['bg_light'])
        self.status_card.pack(fill=tk.X, pady=(0, 15))
        
        self.status_inner = tk.Frame(self.status_card, bg=COLORS['bg_light'], padx=20, pady=15)
        self.status_inner.pack(fill=tk.X)
        
        self.status_icon = tk.Label(
            self.status_inner, text="⚠️",
            font=('Segoe UI', 16),
            bg=COLORS['bg_light'],
            fg=COLORS['warning']
        )
        self.status_icon.pack(side=tk.LEFT)
        
        self.status_text = tk.Label(
            self.status_inner,
            text="No prediction data available. Upload a file and run predictions first.",
            font=FONTS['body'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_secondary']
        )
        self.status_text.pack(side=tk.LEFT, padx=(10, 0))
        
        self.goto_upload_btn = ModernButton(
            self.status_inner, "Go to Upload", self.go_to_upload,
            style='secondary', icon="📤", colors=COLORS
        )
        self.goto_upload_btn.pack(side=tk.RIGHT)
    
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
            ("📊 Summary Report", "Executive overview with risk distribution, key metrics, and recommendations", "summary"),
            ("👥 Customer Analysis", "Detailed breakdown of customers grouped by risk level", "customer"),
            ("📈 Model Performance", "ML model metrics, confusion matrix, and feature importance", "model"),
            ("📋 Batch Predictions", "Complete prediction results table for all customers", "batch"),
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
            ("Include detailed customer data (larger file)", self.include_details),
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
        
        self.generate_btn = ModernButton(
            btn_frame, "Generate & Save PDF", self.generate_report,
            style='primary', icon="📄", colors=COLORS
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ModernButton(
            btn_frame, "Preview Report", self.preview_report,
            style='secondary', icon="👁️", colors=COLORS
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
        
        self.reports_container = tk.Frame(card, bg=COLORS['bg_card'])
        self.reports_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Placeholder for recent reports
        self.no_reports_label = tk.Label(
            self.reports_container,
            text="No reports generated yet.\n\nSelect a report type above and click 'Generate & Save PDF' to create your first report.",
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted'],
            justify=tk.CENTER
        )
        self.no_reports_label.pack(expand=True)
    
    def get_prediction_data(self):
        """Get prediction data from upload_result page."""
        upload_result_page = self.controller.pages.get('upload_result')
        if upload_result_page and upload_result_page.result_data is not None:
            return upload_result_page.result_data
        return None
    
    def update_data_status(self):
        """Update the data status banner based on available prediction data."""
        data = self.get_prediction_data()
        
        if data is not None:
            # Data available
            self.status_card.config(bg=COLORS['success'])
            self.status_inner.config(bg=COLORS['success'])
            self.status_icon.config(text="✓", bg=COLORS['success'], fg=COLORS['text_primary'])
            self.status_text.config(
                text=f"Prediction data available: {len(data)} customers ready for report generation.",
                bg=COLORS['success'],
                fg=COLORS['text_primary']
            )
            self.goto_upload_btn.pack_forget()
            self.generate_btn.config(state=tk.NORMAL)
        else:
            # No data
            self.status_card.config(bg=COLORS['bg_light'])
            self.status_inner.config(bg=COLORS['bg_light'])
            self.status_icon.config(text="⚠️", bg=COLORS['bg_light'], fg=COLORS['warning'])
            self.status_text.config(
                text="No prediction data available. Upload a file and run predictions first.",
                bg=COLORS['bg_light'],
                fg=COLORS['text_secondary']
            )
            self.goto_upload_btn.pack(side=tk.RIGHT)
            self.generate_btn.config(state=tk.DISABLED)
    
    def on_show(self):
        """Called when page is shown."""
        self.update_data_status()
    
    def go_to_upload(self):
        """Navigate to upload page."""
        self.controller.show_page('upload')
    
    def preview_report(self):
        """Show preview of what will be in the report."""
        data = self.get_prediction_data()
        if data is None:
            messagebox.showwarning("No Data", "Please upload and process data first.")
            return
        
        report_type = self.selected_report.get()
        report_names = {
            'summary': 'Summary Report',
            'customer': 'Customer Analysis Report',
            'model': 'Model Performance Report',
            'batch': 'Batch Predictions Report'
        }
        
        # Calculate stats for preview
        total = len(data)
        high_risk = len(data[data['risk_level'] == 'HIGH'])
        moderate_risk = len(data[data['risk_level'] == 'MODERATE'])
        low_risk = len(data[data['risk_level'] == 'LOW'])
        churn_count = len(data[data['prediction'] == 'Churn'])
        churn_rate = (churn_count / total * 100) if total > 0 else 0
        
        preview_text = f"""
Report Preview: {report_names.get(report_type, 'Report')}

📊 Data Summary:
• Total Customers: {total}
• High Risk: {high_risk} ({high_risk/total*100:.1f}%)
• Moderate Risk: {moderate_risk} ({moderate_risk/total*100:.1f}%)
• Low Risk: {low_risk} ({low_risk/total*100:.1f}%)
• Predicted Churn: {churn_count} ({churn_rate:.1f}%)

📄 Report will include:
• Charts: {'Yes' if self.include_charts.get() else 'No'}
• Recommendations: {'Yes' if self.include_recommendations.get() else 'No'}
• Detailed Data: {'Yes' if self.include_details.get() else 'No'}

Click 'Generate & Save PDF' to create the report.
        """
        
        messagebox.showinfo("Report Preview", preview_text.strip())
    
    def generate_report(self):
        """Generate the selected report."""
        data = self.get_prediction_data()
        if data is None:
            messagebox.showwarning("No Data", "Please upload and process data first.")
            return
        
        report_type = self.selected_report.get()
        report_names = {
            'summary': 'Summary_Report',
            'customer': 'Customer_Analysis_Report',
            'model': 'Model_Performance_Report',
            'batch': 'Batch_Predictions_Report'
        }
        
        # Ask for save location
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"ChurnAI_{report_names.get(report_type, 'Report')}_{timestamp}"
        
        file_path = filedialog.asksaveasfilename(
            title="Save Report as PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=default_filename
        )
        
        if not file_path:
            return
        
        try:
            # Import report generator
            ui_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, ui_dir)
            from report_generator import ChurnReportGenerator
            
            # Create generator with settings
            generator = ChurnReportGenerator(
                data, 
                include_charts=self.include_charts.get(),
                include_recommendations=self.include_recommendations.get()
            )
            
            # Generate appropriate report
            if report_type == 'summary':
                generator.generate_summary_report(file_path)
            elif report_type == 'customer':
                generator.generate_customer_analysis_report(file_path)
            elif report_type == 'model':
                generator.generate_model_performance_report(file_path)
            elif report_type == 'batch':
                generator.generate_batch_predictions_report(file_path)
            
            # Add to recent reports
            self.add_recent_report(report_type, file_path)
            
            # Success message
            messagebox.showinfo(
                "Report Generated",
                f"Report saved successfully!\n\nFile: {os.path.basename(file_path)}\nLocation: {os.path.dirname(file_path)}"
            )
            
            # Ask to open
            if messagebox.askyesno("Open Report", "Would you like to open the report now?"):
                os.startfile(file_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{str(e)}")
    
    def add_recent_report(self, report_type, file_path):
        """Add a report to the recent reports list."""
        report_names = {
            'summary': '📊 Summary Report',
            'customer': '👥 Customer Analysis',
            'model': '📈 Model Performance',
            'batch': '📋 Batch Predictions'
        }
        
        self.generated_reports.insert(0, {
            'type': report_type,
            'name': report_names.get(report_type, 'Report'),
            'path': file_path,
            'time': datetime.now().strftime("%I:%M %p")
        })
        
        # Keep only last 5
        self.generated_reports = self.generated_reports[:5]
        
        # Update display
        self.update_recent_reports()
    
    def update_recent_reports(self):
        """Update the recent reports display."""
        # Clear container
        for widget in self.reports_container.winfo_children():
            widget.destroy()
        
        if not self.generated_reports:
            self.no_reports_label = tk.Label(
                self.reports_container,
                text="No reports generated yet.",
                font=FONTS['body'],
                bg=COLORS['bg_card'],
                fg=COLORS['text_muted']
            )
            self.no_reports_label.pack(expand=True)
            return
        
        for report in self.generated_reports:
            row = tk.Frame(self.reports_container, bg=COLORS['bg_light'])
            row.pack(fill=tk.X, pady=3)
            
            inner = tk.Frame(row, bg=COLORS['bg_light'], padx=10, pady=8)
            inner.pack(fill=tk.X)
            
            tk.Label(
                inner, text=report['name'],
                font=FONTS['body_bold'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_primary']
            ).pack(side=tk.LEFT)
            
            tk.Label(
                inner, text=f"Generated at {report['time']}",
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_muted']
            ).pack(side=tk.LEFT, padx=(10, 0))
            
            # Open button
            def open_report(path=report['path']):
                try:
                    os.startfile(path)
                except:
                    messagebox.showerror("Error", f"Could not open file:\n{path}")
            
            open_btn = tk.Label(
                inner, text="📂 Open",
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['accent'],
                cursor='hand2'
            )
            open_btn.pack(side=tk.RIGHT)
            open_btn.bind('<Button-1>', lambda e, p=report['path']: open_report(p))
