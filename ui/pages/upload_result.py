"""
Upload Result Page
Displays batch prediction results from uploaded data with filtering.
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
    """Page for displaying batch prediction results with filtering."""
    
    # ROI Constants (De Caigny et al., 2018 profit-driven framework)
    CLV_BENEFIT = 450   # $ saved per correctly retained churner
    CAMPAIGN_COST = 50  # $ spent per retention campaign (false alarm cost)
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.result_data = None
        self.filtered_data = None
        self.current_filter = "All"
        self.stat_cards = {}
        self.tree = None
        self.setup_page()
    
    def setup_page(self):
        """Setup the upload result page."""
        # Header
        self.create_header(
            "Data Results",
            "Batch prediction results from uploaded data"
        )
        
        # Main content
        self.main_frame = tk.Frame(self.content, bg=COLORS['bg_medium'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Summary section
        self.summary_card = tk.Frame(self.main_frame, bg=COLORS['bg_card'])
        self.summary_card.pack(fill=tk.X, pady=(0, 15))
        
        # Title row with filter info
        title_row = tk.Frame(self.summary_card, bg=COLORS['bg_card'])
        title_row.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        tk.Label(
            title_row, text="📊  Prediction Summary",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent']
        ).pack(side=tk.LEFT)
        
        self.filter_label = tk.Label(
            title_row, text="Click on a card to filter results",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        )
        self.filter_label.pack(side=tk.RIGHT)
        
        # Stats container
        self.stats_frame = tk.Frame(self.summary_card, bg=COLORS['bg_card'])
        self.stats_frame.pack(fill=tk.X, padx=20, pady=(5, 15))
        
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
        
        # ROI Business Impact section
        self.roi_card = tk.Frame(self.main_frame, bg=COLORS['bg_card'])
        self.roi_card.pack(fill=tk.X, pady=(0, 15))
        self.roi_card.pack_forget()  # Hidden until results are loaded
        
        self.roi_content = tk.Frame(self.roi_card, bg=COLORS['bg_card'])
        self.roi_content.pack(fill=tk.X, padx=20, pady=15)
        
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
        self.filtered_data = df
        self.current_filter = "All"
        
        # Clear previous stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        self.stat_cards = {}
        
        # Create clickable stat cards
        stats = [
            ("All", "👥 All Customers", len(df), COLORS['text_primary']),
            ("HIGH", "🔴 High Risk", high_risk, COLORS['danger']),
            ("MODERATE", "🟡 Moderate Risk", moderate_risk, COLORS['warning']),
            ("LOW", "🟢 Low Risk", low_risk, COLORS['success']),
        ]
        
        for filter_key, label, value, color in stats:
            card = self.create_clickable_card(
                self.stats_frame, filter_key, label, value, color
            )
            self.stat_cards[filter_key] = card
        
        # Churn stats (non-clickable)
        churn_pct = (churn_count / len(df)) * 100 if len(df) > 0 else 0
        
        churn_frame = tk.Frame(self.stats_frame, bg=COLORS['bg_light'], padx=15, pady=10)
        churn_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        tk.Label(
            churn_frame, text="📊 Predicted Churn",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack()
        
        tk.Label(
            churn_frame, text=str(churn_count),
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['accent']
        ).pack()
        
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
        
        # Highlight "All" card as selected by default
        self.highlight_selected_card("All")
        
        # Update table with ALL data
        self.create_results_table(df)
        
        # Build ROI Business Impact card
        self._build_roi_card(high_risk, moderate_risk)
        
        # Enable export button
        self.export_btn.config(state=tk.NORMAL)
    
    def create_clickable_card(self, parent, filter_key, label, value, color):
        """Create a clickable stat card for filtering."""
        card = tk.Frame(parent, bg=COLORS['bg_light'], padx=15, pady=10, cursor='hand2')
        card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        label_widget = tk.Label(
            card, text=label,
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted'],
            cursor='hand2'
        )
        label_widget.pack()
        
        value_widget = tk.Label(
            card, text=str(value),
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['bg_light'],
            fg=color,
            cursor='hand2'
        )
        value_widget.pack()
        
        # Bind click events
        def on_click(e, fk=filter_key):
            self.apply_filter(fk)
        
        def on_enter(e, c=card, lw=label_widget, vw=value_widget):
            c.config(bg=COLORS['sidebar_hover'])
            lw.config(bg=COLORS['sidebar_hover'])
            vw.config(bg=COLORS['sidebar_hover'])
        
        def on_leave(e, c=card, lw=label_widget, vw=value_widget, fk=filter_key):
            bg = COLORS['accent'] if fk == self.current_filter else COLORS['bg_light']
            c.config(bg=bg)
            lw.config(bg=bg)
            vw.config(bg=bg)
        
        for widget in [card, label_widget, value_widget]:
            widget.bind('<Button-1>', on_click)
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
        
        return {
            'frame': card,
            'label': label_widget,
            'value': value_widget,
            'color': color
        }
    
    def _build_roi_card(self, high_risk, moderate_risk):
        """Build the ROI Business Impact card."""
        # Clear previous content
        for widget in self.roi_content.winfo_children():
            widget.destroy()
        
        # Show the card
        self.roi_card.pack(fill=tk.X, pady=(0, 15))
        # Re-order: make sure it appears after summary_card and before table_card
        self.roi_card.pack_configure(after=self.summary_card)
        
        # Title row
        title_row = tk.Frame(self.roi_content, bg=COLORS['bg_card'])
        title_row.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            title_row, text="💰  ROI Business Impact",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['success']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            title_row, text="De Caigny et al. (2018) profit-driven framework",
            font=FONTS['small'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_muted']
        ).pack(side=tk.RIGHT)
        
        # ROI calculation
        high_profit = high_risk * (self.CLV_BENEFIT - self.CAMPAIGN_COST)
        mod_profit = moderate_risk * (self.CLV_BENEFIT - self.CAMPAIGN_COST)
        total_profit = high_profit + mod_profit
        total_campaign_cost = (high_risk + moderate_risk) * self.CAMPAIGN_COST
        total_clv_saved = (high_risk + moderate_risk) * self.CLV_BENEFIT
        
        # Cards row
        cards_row = tk.Frame(self.roi_content, bg=COLORS['bg_card'])
        cards_row.pack(fill=tk.X, pady=(0, 10))
        
        # Total ROI card (big, prominent)
        total_card = tk.Frame(cards_row, bg=COLORS['bg_light'], padx=20, pady=12)
        total_card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 8))
        
        tk.Label(
            total_card, text="🏆 Total Potential Profit",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack()
        
        tk.Label(
            total_card, text=f"${total_profit:,}",
            font=('Segoe UI', 28, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['success']
        ).pack()
        
        tk.Label(
            total_card, text=f"if all {high_risk + moderate_risk} at-risk customers are retained",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack()
        
        # High Risk ROI card
        high_card = tk.Frame(cards_row, bg=COLORS['bg_light'], padx=15, pady=12)
        high_card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)
        
        tk.Label(
            high_card, text="🔴 High Risk Customers",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['danger']
        ).pack()
        
        tk.Label(
            high_card, text=f"${high_profit:,}",
            font=('Segoe UI', 22, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['danger']
        ).pack()
        
        tk.Label(
            high_card, text=f"{high_risk} customers × ${self.CLV_BENEFIT - self.CAMPAIGN_COST} net",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack()
        
        # Moderate Risk ROI card
        mod_card = tk.Frame(cards_row, bg=COLORS['bg_light'], padx=15, pady=12)
        mod_card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)
        
        tk.Label(
            mod_card, text="🟡 Moderate Risk Customers",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['warning']
        ).pack()
        
        tk.Label(
            mod_card, text=f"${mod_profit:,}",
            font=('Segoe UI', 22, 'bold'),
            bg=COLORS['bg_light'],
            fg=COLORS['warning']
        ).pack()
        
        tk.Label(
            mod_card, text=f"{moderate_risk} customers × ${self.CLV_BENEFIT - self.CAMPAIGN_COST} net",
            font=FONTS['small'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_muted']
        ).pack()
        
        # Formula breakdown row
        formula_frame = tk.Frame(self.roi_content, bg=COLORS['bg_light'], padx=15, pady=10)
        formula_frame.pack(fill=tk.X)
        
        formula_parts = [
            ("CLV Saved:", f"${total_clv_saved:,}", COLORS['success']),
            ("Campaign Cost:", f"-${total_campaign_cost:,}", COLORS['danger']),
            ("Net Profit:", f"${total_profit:,}", COLORS['success']),
            ("Formula:", f"ROI = ({high_risk + moderate_risk} × ${self.CLV_BENEFIT}) − ({high_risk + moderate_risk} × ${self.CAMPAIGN_COST})", COLORS['text_secondary']),
        ]
        
        for label_text, value_text, color in formula_parts:
            part = tk.Frame(formula_frame, bg=COLORS['bg_light'])
            part.pack(side=tk.LEFT, expand=True, padx=5)
            
            tk.Label(
                part, text=label_text,
                font=FONTS['small'],
                bg=COLORS['bg_light'],
                fg=COLORS['text_muted']
            ).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Label(
                part, text=value_text,
                font=('Segoe UI', 10, 'bold'),
                bg=COLORS['bg_light'],
                fg=color
            ).pack(side=tk.LEFT)
    
    def highlight_selected_card(self, filter_key):
        """Highlight the selected filter card."""
        for key, card_info in self.stat_cards.items():
            if key == filter_key:
                # Selected
                card_info['frame'].config(bg=COLORS['accent'])
                card_info['label'].config(bg=COLORS['accent'], fg=COLORS['text_primary'])
                card_info['value'].config(bg=COLORS['accent'])
            else:
                # Not selected
                card_info['frame'].config(bg=COLORS['bg_light'])
                card_info['label'].config(bg=COLORS['bg_light'], fg=COLORS['text_muted'])
                card_info['value'].config(bg=COLORS['bg_light'])
    
    def apply_filter(self, filter_key):
        """Apply filter to show only customers of selected risk level."""
        self.current_filter = filter_key
        
        if self.result_data is None:
            return
        
        # Filter data
        if filter_key == "All":
            self.filtered_data = self.result_data
            self.filter_label.config(text="Showing: All Customers")
        else:
            self.filtered_data = self.result_data[self.result_data['risk_level'] == filter_key]
            risk_name = {"HIGH": "High Risk", "MODERATE": "Moderate Risk", "LOW": "Low Risk"}.get(filter_key, filter_key)
            self.filter_label.config(text=f"Showing: {risk_name} Customers Only")
        
        # Update card highlighting
        self.highlight_selected_card(filter_key)
        
        # Update table
        self.create_results_table(self.filtered_data)
    
    def create_results_table(self, df):
        """Create the results table with ALL data."""
        # Clear previous table
        for widget in self.table_container.winfo_children():
            widget.destroy()
        
        # Update rows label
        total = len(self.result_data) if self.result_data is not None else 0
        self.rows_label.config(text=f"Showing {len(df)} of {total} rows")
        
        # Create treeview
        columns = list(df.columns)
        self.tree = ttk.Treeview(self.table_container, columns=columns, show='headings', height=18)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            # Adjust width based on column name
            if col in ['customerID', 'gender', 'SeniorCitizen']:
                width = 90
            elif col in ['prediction', 'risk_level']:
                width = 100
            elif col == 'churn_probability_%':
                width = 130
            elif col in ['MonthlyCharges', 'TotalCharges', 'PaymentMethod']:
                width = 120
            else:
                width = 95
            self.tree.column(col, width=width, anchor=tk.CENTER)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(self.table_container, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack scrollbars and tree
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Insert ALL data (no limit)
        for idx, row in df.iterrows():
            self.tree.insert('', tk.END, values=list(row))
    
    def export_results(self):
        """Export prediction results to CSV."""
        if self.filtered_data is None:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        # Ask if user wants filtered or all data
        export_data = self.filtered_data
        filename_suffix = ""
        
        if self.current_filter != "All" and len(self.result_data) != len(self.filtered_data):
            result = messagebox.askyesnocancel(
                "Export Options",
                f"You have a filter applied ({self.current_filter}).\n\n"
                f"• Click 'Yes' to export filtered data ({len(self.filtered_data)} rows)\n"
                f"• Click 'No' to export all data ({len(self.result_data)} rows)\n"
                f"• Click 'Cancel' to cancel export"
            )
            if result is None:
                return
            elif result:
                export_data = self.filtered_data
                filename_suffix = f"_{self.current_filter.lower()}_only"
            else:
                export_data = self.result_data
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Prediction Results",
            initialfile=f"prediction_results{filename_suffix}"
        )
        
        if file_path:
            try:
                export_data.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Results exported successfully!\n\n{len(export_data)} rows saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")
    
    def go_to_upload(self):
        """Navigate to upload page."""
        self.controller.show_page('upload')
    
    def on_show(self):
        """Called when page is shown."""
        pass
