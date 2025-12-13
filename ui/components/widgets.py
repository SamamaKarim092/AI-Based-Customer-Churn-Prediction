"""
Common UI Widgets
Reusable UI components for the application.
"""

import tkinter as tk
from tkinter import ttk
import math


class AnimatedGauge(tk.Canvas):
    """Animated circular gauge for displaying percentages."""
    
    def __init__(self, parent, size=180, colors=None, **kwargs):
        bg_color = colors.get('bg', '#1c2128') if colors else '#1c2128'
        super().__init__(parent, width=size, height=size, 
                        bg=bg_color, highlightthickness=0, **kwargs)
        self.size = size
        self.center = size // 2
        self.radius = size // 2 - 20
        self.current_value = 0
        self.target_value = 0
        self.animation_id = None
        self.colors = colors or {
            'bg': '#1c2128',
            'track': '#21262d',
            'low': '#3fb950',
            'medium': '#d29922',
            'high': '#f85149',
            'text': '#f0f6fc',
            'label': '#8b949e'
        }
        
        self.draw_gauge(0)
    
    def draw_gauge(self, value):
        """Draw the gauge with the given value (0-100)."""
        self.delete("all")
        
        # Background arc (track)
        self.create_arc(
            20, 20, self.size - 20, self.size - 20,
            start=135, extent=270,
            style=tk.ARC, width=12,
            outline=self.colors['track']
        )
        
        # Determine color based on value
        if value >= 70:
            color = self.colors['high']
            label = "HIGH RISK"
        elif value >= 40:
            color = self.colors['medium']
            label = "MODERATE"
        else:
            color = self.colors['low']
            label = "LOW RISK"
        
        # Value arc
        extent = (value / 100) * 270
        if extent > 0:
            self.create_arc(
                20, 20, self.size - 20, self.size - 20,
                start=135, extent=-extent,
                style=tk.ARC, width=12,
                outline=color
            )
        
        # Center percentage text
        self.create_text(
            self.center, self.center - 8,
            text=f"{value:.1f}%",
            font=('Segoe UI', 22, 'bold'),
            fill=color
        )
        
        # Risk label
        self.create_text(
            self.center, self.center + 22,
            text=label,
            font=('Segoe UI', 10, 'bold'),
            fill=self.colors['label']
        )
    
    def animate_to(self, target_value):
        """Animate the gauge to the target value."""
        self.target_value = target_value
        if self.animation_id:
            self.after_cancel(self.animation_id)
        self.animate_step()
    
    def animate_step(self):
        """Single animation step with easing."""
        diff = self.target_value - self.current_value
        if abs(diff) < 0.3:
            self.current_value = self.target_value
            self.draw_gauge(self.current_value)
            return
        
        # Smooth easing
        step = diff * 0.12
        self.current_value += step
        self.draw_gauge(self.current_value)
        
        self.animation_id = self.after(16, self.animate_step)
    
    def reset(self):
        """Reset gauge to 0."""
        if self.animation_id:
            self.after_cancel(self.animation_id)
        self.current_value = 0
        self.target_value = 0
        self.draw_gauge(0)


class FeatureBarChart(tk.Canvas):
    """Horizontal bar chart for feature importance - Enhanced version."""
    
    def __init__(self, parent, width=420, height=320, colors=None, **kwargs):
        bg_color = colors.get('bg', '#1c2128') if colors else '#1c2128'
        super().__init__(parent, width=width, height=height,
                        bg=bg_color, highlightthickness=0, **kwargs)
        self.chart_width = width
        self.chart_height = height
        self.colors = colors or {
            'bg': '#1c2128',
            'positive': '#f85149',
            'negative': '#3fb950',
            'text': '#f0f6fc',
            'label': '#8b949e',
            'line': '#30363d'
        }
        
        # Draw empty state
        self.draw_empty()
    
    def draw_empty(self):
        """Draw empty state."""
        self.delete("all")
        self.create_text(
            self.chart_width // 2, self.chart_height // 2,
            text="Click 'Predict' to see feature impacts",
            fill=self.colors.get('label', '#8b949e'),
            font=('Segoe UI', 10)
        )
    
    def draw_bars(self, features, title="Feature Impact on Churn"):
        """Draw horizontal bars for feature importance."""
        self.delete("all")
        
        if not features:
            self.draw_empty()
            return
        
        # Calculate dimensions
        padding_top = 45
        padding_bottom = 50
        padding_left = 130
        padding_right = 60
        
        available_height = self.chart_height - padding_top - padding_bottom
        num_features = min(len(features), 8)
        bar_height = min(28, (available_height - (num_features - 1) * 6) // num_features)
        bar_spacing = 6
        
        bar_area_width = self.chart_width - padding_left - padding_right
        center_x = padding_left + bar_area_width // 2
        
        # Title
        self.create_text(
            self.chart_width // 2, 20,
            text=title,
            fill=self.colors.get('text', '#f0f6fc'),
            font=('Segoe UI', 12, 'bold')
        )
        
        # Find max value for scaling
        max_abs_value = max(abs(f['shap_value']) for f in features[:num_features])
        if max_abs_value == 0:
            max_abs_value = 1
        
        # Draw center line first (behind bars)
        line_top = padding_top - 5
        line_bottom = padding_top + num_features * (bar_height + bar_spacing)
        self.create_line(
            center_x, line_top, center_x, line_bottom,
            fill=self.colors.get('line', '#30363d'), width=2, dash=(4, 2)
        )
        
        # Draw bars
        for i, feature in enumerate(features[:num_features]):
            y = padding_top + i * (bar_height + bar_spacing)
            
            # Get full display name
            display_name = feature.get('display_name', feature.get('feature', 'Unknown'))
            
            # Draw feature label
            self.create_text(
                padding_left - 10, y + bar_height // 2,
                text=display_name,
                anchor=tk.E,
                fill=self.colors.get('label', '#8b949e'),
                font=('Segoe UI', 9)
            )
            
            # Calculate bar width (scaled)
            bar_pct = abs(feature['shap_value']) / max_abs_value
            max_bar_width = (bar_area_width // 2) - 10
            bar_width = max(bar_pct * max_bar_width, 4)  # Minimum 4px
            
            # Determine color and direction
            shap_val = feature['shap_value']
            if shap_val > 0:
                # Positive = increases churn (red)
                color = self.colors.get('positive', '#f85149')
                x1 = center_x + 2
                x2 = center_x + 2 + bar_width
                value_x = x2 + 8
                text_anchor = tk.W
            else:
                # Negative = decreases churn (green)
                color = self.colors.get('negative', '#3fb950')
                x1 = center_x - 2 - bar_width
                x2 = center_x - 2
                value_x = x1 - 8
                text_anchor = tk.E
            
            # Draw rounded bar
            radius = min(4, bar_height // 2 - 2)
            self._draw_rounded_rect(x1, y + 2, x2, y + bar_height - 2, radius, color)
            
            # Draw value label
            value_text = f"{shap_val:+.2f}"
            self.create_text(
                value_x, y + bar_height // 2,
                text=value_text,
                anchor=text_anchor,
                fill=color,
                font=('Segoe UI', 9, 'bold')
            )
        
        # Draw legend at bottom
        legend_y = self.chart_height - 25
        legend_center = self.chart_width // 2
        
        # Increases churn (left)
        self.create_rectangle(
            legend_center - 140, legend_y - 5,
            legend_center - 130, legend_y + 5,
            fill=self.colors.get('positive', '#f85149'), outline=''
        )
        self.create_text(
            legend_center - 125, legend_y,
            text="Increases Churn",
            anchor=tk.W,
            fill=self.colors.get('label', '#8b949e'),
            font=('Segoe UI', 9)
        )
        
        # Decreases churn (right)
        self.create_rectangle(
            legend_center + 30, legend_y - 5,
            legend_center + 40, legend_y + 5,
            fill=self.colors.get('negative', '#3fb950'), outline=''
        )
        self.create_text(
            legend_center + 45, legend_y,
            text="Decreases Churn",
            anchor=tk.W,
            fill=self.colors.get('label', '#8b949e'),
            font=('Segoe UI', 9)
        )
    
    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, color):
        """Draw a rounded rectangle."""
        # Simple rounded rectangle using polygon
        if x2 < x1:
            x1, x2 = x2, x1
        
        width = x2 - x1
        if width < radius * 2:
            radius = width // 2
        
        # Draw as simple rectangle if too small for rounding
        if radius < 2:
            self.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
            return
        
        # Create rounded rectangle with arcs and rectangles
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline='')
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline='')
        self.create_oval(x1, y1, x1 + radius * 2, y1 + radius * 2, fill=color, outline='')
        self.create_oval(x2 - radius * 2, y1, x2, y1 + radius * 2, fill=color, outline='')
        self.create_oval(x1, y2 - radius * 2, x1 + radius * 2, y2, fill=color, outline='')
        self.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, fill=color, outline='')


class Card(tk.Frame):
    """Card container with title."""
    
    def __init__(self, parent, title="", icon="", colors=None, **kwargs):
        bg_color = colors.get('card', '#1c2128') if colors else '#1c2128'
        super().__init__(parent, bg=bg_color, **kwargs)
        self.colors = colors or {
            'card': '#1c2128',
            'accent': '#58a6ff',
            'text': '#f0f6fc',
            'border': '#30363d'
        }
        
        # Title bar
        if title:
            title_frame = tk.Frame(self, bg=bg_color)
            title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
            
            title_text = f"{icon}  {title}" if icon else title
            tk.Label(
                title_frame,
                text=title_text,
                font=('Segoe UI', 12, 'bold'),
                bg=bg_color,
                fg=self.colors['accent']
            ).pack(anchor=tk.W)
        
        # Content frame
        self.content = tk.Frame(self, bg=bg_color)
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))


class StatCard(tk.Frame):
    """Statistics display card."""
    
    def __init__(self, parent, title, value, subtitle="", icon="", color=None, colors=None, **kwargs):
        # Map colors from theme to widget colors
        if colors:
            bg_color = colors.get('bg_card', colors.get('card', '#1c2128'))
            text_color = colors.get('text_primary', colors.get('text', '#f0f6fc'))
            label_color = colors.get('text_secondary', colors.get('label', '#8b949e'))
            accent_color = colors.get('accent', '#58a6ff')
        else:
            bg_color = '#1c2128'
            text_color = '#f0f6fc'
            label_color = '#8b949e'
            accent_color = '#58a6ff'
        
        super().__init__(parent, bg=bg_color, padx=20, pady=15, **kwargs)
        
        self.bg_color = bg_color
        self.text_color = text_color
        self.label_color = label_color
        self.accent_color = accent_color
        
        value_color = color if color else self.text_color
        
        # Icon and title row
        header = tk.Frame(self, bg=bg_color)
        header.pack(fill=tk.X)
        
        if icon:
            tk.Label(
                header, text=icon,
                font=('Segoe UI', 16),
                bg=bg_color, fg=self.label_color
            ).pack(side=tk.LEFT)
        
        tk.Label(
            header, text=title,
            font=('Segoe UI', 10),
            bg=bg_color, fg=self.label_color
        ).pack(side=tk.LEFT, padx=(8 if icon else 0, 0))
        
        # Value
        self.value_label = tk.Label(
            self, text=value,
            font=('Segoe UI', 28, 'bold'),
            bg=bg_color, fg=value_color
        )
        self.value_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Subtitle
        if subtitle:
            tk.Label(
                self, text=subtitle,
                font=('Segoe UI', 9),
                bg=bg_color, fg=self.label_color
            ).pack(anchor=tk.W)
    
    def update_value(self, value, color=None):
        """Update the displayed value."""
        self.value_label.config(text=value)
        if color:
            self.value_label.config(fg=color)


class ModernButton(tk.Button):
    """Modern styled button with hover effects."""
    
    def __init__(self, parent, text, command=None, style='primary', icon="", colors=None, **kwargs):
        # Map colors from theme
        if colors:
            primary = colors.get('accent', colors.get('primary', '#58a6ff'))
            primary_hover = colors.get('accent_hover', colors.get('primary_hover', '#79b8ff'))
            secondary = colors.get('bg_light', colors.get('secondary', '#21262d'))
            secondary_hover = colors.get('sidebar_hover', colors.get('secondary_hover', '#30363d'))
            danger = colors.get('danger', '#f85149')
            danger_hover = colors.get('danger_light', colors.get('danger_hover', '#ff7b72'))
            success = colors.get('success', '#3fb950')
            success_hover = colors.get('success_light', colors.get('success_hover', '#56d364'))
            text_color = colors.get('text_primary', colors.get('text', '#ffffff'))
        else:
            primary = '#58a6ff'
            primary_hover = '#79b8ff'
            secondary = '#21262d'
            secondary_hover = '#30363d'
            danger = '#f85149'
            danger_hover = '#ff7b72'
            success = '#3fb950'
            success_hover = '#56d364'
            text_color = '#ffffff'
        
        # Determine colors based on style
        if style == 'primary':
            bg = primary
            bg_hover = primary_hover
            fg = text_color
        elif style == 'danger':
            bg = danger
            bg_hover = danger_hover
            fg = text_color
        elif style == 'success':
            bg = success
            bg_hover = success_hover
            fg = text_color
        else:  # secondary
            bg = secondary
            bg_hover = secondary_hover
            fg = text_color
        
        self.bg_normal = bg
        self.bg_hover = bg_hover
        
        button_text = f"{icon}  {text}" if icon else text
        
        super().__init__(
            parent,
            text=button_text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=bg_hover,
            activeforeground=fg,
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=10,
            **kwargs
        )
        
        # Bind hover effects
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, e):
        self.config(bg=self.bg_hover)
    
    def _on_leave(self, e):
        self.config(bg=self.bg_normal)
