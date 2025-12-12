"""
Theme and Styles Module
Centralized color scheme and styling for the application.
"""

# Color Palette - Dark Modern Theme
COLORS = {
    # Background colors
    'bg_dark': '#0d1117',
    'bg_medium': '#161b22',
    'bg_light': '#21262d',
    'bg_card': '#1c2128',
    
    # Sidebar colors
    'sidebar_bg': '#0d1117',
    'sidebar_hover': '#21262d',
    'sidebar_active': '#1f6feb',
    
    # Accent colors
    'accent': '#58a6ff',
    'accent_hover': '#79b8ff',
    'accent_dark': '#1f6feb',
    
    # Status colors
    'success': '#3fb950',
    'success_light': '#56d364',
    'warning': '#d29922',
    'warning_light': '#e3b341',
    'danger': '#f85149',
    'danger_light': '#ff7b72',
    
    # Text colors
    'text_primary': '#f0f6fc',
    'text_secondary': '#8b949e',
    'text_muted': '#6e7681',
    
    # Border colors
    'border': '#30363d',
    'border_light': '#484f58',
    
    # Chart colors
    'chart_positive': '#f85149',
    'chart_negative': '#3fb950',
    'chart_neutral': '#8b949e'
}

# Font configurations
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 16, 'bold'),
    'subheading': ('Segoe UI', 13, 'bold'),
    'body': ('Segoe UI', 11),
    'body_bold': ('Segoe UI', 11, 'bold'),
    'small': ('Segoe UI', 10),
    'tiny': ('Segoe UI', 9),
    'mono': ('Consolas', 11),
    'mono_small': ('Consolas', 10),
    
    # Sidebar fonts
    'sidebar_item': ('Segoe UI', 11),
    'sidebar_item_active': ('Segoe UI', 11, 'bold'),
    'sidebar_header': ('Segoe UI', 9)
}

# Sizing
SIZES = {
    'sidebar_width': 220,
    'sidebar_collapsed': 60,
    'padding': 15,
    'padding_small': 10,
    'padding_large': 20,
    'border_radius': 8,
    'icon_size': 20,
    'button_height': 40,
    'input_height': 35
}

# Icons (using Unicode/Emoji)
ICONS = {
    'home': '🏠',
    'predict': '🔮',
    'upload': '📤',
    'chart': '📊',
    'report': '📄',
    'settings': '⚙️',
    'menu': '☰',
    'close': '✕',
    'check': '✓',
    'warning': '⚠️',
    'error': '❌',
    'success': '✅',
    'info': 'ℹ️',
    'arrow_right': '→',
    'arrow_left': '←',
    'user': '👤',
    'refresh': '🔄',
    'download': '📥',
    'search': '🔍'
}


def apply_button_hover(button, normal_bg, hover_bg, normal_fg='white', hover_fg='white'):
    """Apply hover effects to a button."""
    def on_enter(e):
        button.config(bg=hover_bg, fg=hover_fg)
    
    def on_leave(e):
        button.config(bg=normal_bg, fg=normal_fg)
    
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)


def create_hover_frame(parent, normal_bg, hover_bg):
    """Create a frame with hover effect."""
    import tkinter as tk
    
    frame = tk.Frame(parent, bg=normal_bg)
    
    def on_enter(e):
        frame.config(bg=hover_bg)
        for child in frame.winfo_children():
            try:
                child.config(bg=hover_bg)
            except:
                pass
    
    def on_leave(e):
        frame.config(bg=normal_bg)
        for child in frame.winfo_children():
            try:
                child.config(bg=normal_bg)
            except:
                pass
    
    frame.bind('<Enter>', on_enter)
    frame.bind('<Leave>', on_leave)
    
    return frame
