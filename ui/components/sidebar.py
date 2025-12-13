"""
Sidebar Component
Navigation sidebar with hover effects and page switching.
"""

import tkinter as tk
from theme import COLORS, FONTS, SIZES, ICONS, apply_button_hover


class Sidebar(tk.Frame):
    """Modern sidebar navigation component."""
    
    def __init__(self, parent, on_page_change, **kwargs):
        super().__init__(parent, bg=COLORS['sidebar_bg'], **kwargs)
        self.on_page_change = on_page_change
        self.current_page = 'home'
        self.menu_items = []
        
        self.setup_sidebar()
    
    def setup_sidebar(self):
        """Setup the sidebar layout."""
        # Logo/Brand section
        brand_frame = tk.Frame(self, bg=COLORS['sidebar_bg'])
        brand_frame.pack(fill=tk.X, padx=15, pady=20)
        
        logo_label = tk.Label(
            brand_frame,
            text="🤖 ChurnAI",
            font=('Segoe UI', 18, 'bold'),
            bg=COLORS['sidebar_bg'],
            fg=COLORS['accent']
        )
        logo_label.pack(anchor=tk.W)
        
        version_label = tk.Label(
            brand_frame,
            text="v1.0.0",
            font=FONTS['tiny'],
            bg=COLORS['sidebar_bg'],
            fg=COLORS['text_muted']
        )
        version_label.pack(anchor=tk.W)
        
        # Separator
        separator = tk.Frame(self, bg=COLORS['border'], height=1)
        separator.pack(fill=tk.X, padx=15, pady=10)
        
        # Navigation section header
        nav_header = tk.Label(
            self,
            text="NAVIGATION",
            font=FONTS['sidebar_header'],
            bg=COLORS['sidebar_bg'],
            fg=COLORS['text_muted']
        )
        nav_header.pack(anchor=tk.W, padx=20, pady=(10, 5))
        
        # Menu items
        menu_config = [
            ('home', ICONS['home'], 'Dashboard'),
            ('predict', ICONS['predict'], 'Predict'),
            ('upload', ICONS['upload'], 'Upload Data'),
            ('charts', ICONS['chart'], 'Analytics'),
            ('report', ICONS['report'], 'Reports'),
        ]
        
        for page_id, icon, label in menu_config:
            self.create_menu_item(page_id, icon, label)
        
        # Bottom section
        bottom_frame = tk.Frame(self, bg=COLORS['sidebar_bg'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        # Separator
        separator2 = tk.Frame(bottom_frame, bg=COLORS['border'], height=1)
        separator2.pack(fill=tk.X, padx=15, pady=10)
        
        # Settings at bottom
        self.create_menu_item('settings', ICONS['settings'], 'Settings', parent=bottom_frame)
    
    def create_menu_item(self, page_id, icon, label, parent=None):
        """Create a single menu item with hover effect."""
        container = parent if parent else self
        
        # Determine if this is the active item
        is_active = page_id == self.current_page
        bg_color = COLORS['sidebar_active'] if is_active else COLORS['sidebar_bg']
        fg_color = COLORS['text_primary'] if is_active else COLORS['text_secondary']
        
        # Create frame for menu item
        item_frame = tk.Frame(
            container,
            bg=bg_color,
            cursor='hand2'
        )
        item_frame.pack(fill=tk.X, padx=10, pady=2)
        
        # Inner padding frame
        inner_frame = tk.Frame(item_frame, bg=bg_color)
        inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Icon
        icon_label = tk.Label(
            inner_frame,
            text=icon,
            font=('Segoe UI', 14),
            bg=bg_color,
            fg=fg_color
        )
        icon_label.pack(side=tk.LEFT)
        
        # Label
        text_label = tk.Label(
            inner_frame,
            text=label,
            font=FONTS['sidebar_item_active'] if is_active else FONTS['sidebar_item'],
            bg=bg_color,
            fg=fg_color
        )
        text_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Store reference
        self.menu_items.append({
            'id': page_id,
            'frame': item_frame,
            'inner': inner_frame,
            'icon': icon_label,
            'text': text_label
        })
        
        # Bind hover effects
        def on_enter(e, f=item_frame, i=inner_frame, il=icon_label, tl=text_label):
            if page_id != self.current_page:
                f.config(bg=COLORS['sidebar_hover'])
                i.config(bg=COLORS['sidebar_hover'])
                il.config(bg=COLORS['sidebar_hover'])
                tl.config(bg=COLORS['sidebar_hover'])
        
        def on_leave(e, f=item_frame, i=inner_frame, il=icon_label, tl=text_label):
            if page_id != self.current_page:
                f.config(bg=COLORS['sidebar_bg'])
                i.config(bg=COLORS['sidebar_bg'])
                il.config(bg=COLORS['sidebar_bg'])
                tl.config(bg=COLORS['sidebar_bg'])
        
        def on_click(e, pid=page_id):
            self.set_active(pid)
            self.on_page_change(pid)
        
        # Bind to all elements
        for widget in [item_frame, inner_frame, icon_label, text_label]:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', on_click)
    
    def set_active(self, page_id):
        """Set the active menu item."""
        self.current_page = page_id
        
        for item in self.menu_items:
            is_active = item['id'] == page_id
            bg_color = COLORS['sidebar_active'] if is_active else COLORS['sidebar_bg']
            fg_color = COLORS['text_primary'] if is_active else COLORS['text_secondary']
            
            item['frame'].config(bg=bg_color)
            item['inner'].config(bg=bg_color)
            item['icon'].config(bg=bg_color, fg=fg_color)
            item['text'].config(
                bg=bg_color, 
                fg=fg_color,
                font=FONTS['sidebar_item_active'] if is_active else FONTS['sidebar_item']
            )
