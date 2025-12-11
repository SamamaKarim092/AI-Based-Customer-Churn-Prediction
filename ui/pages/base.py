"""
Base Page Class
Common functionality for all pages with scrollable content.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import COLORS, FONTS


class ScrollableFrame(tk.Frame):
    """A scrollable frame container."""
    
    def __init__(self, parent, bg_color=None, **kwargs):
        super().__init__(parent, bg=bg_color or COLORS['bg_medium'], **kwargs)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self,
            bg=bg_color or COLORS['bg_medium'],
            highlightthickness=0
        )
        
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )
        
        # Create inner frame for content
        self.inner_frame = tk.Frame(
            self.canvas,
            bg=bg_color or COLORS['bg_medium']
        )
        
        # Configure canvas scrolling
        self.inner_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        )
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.inner_frame,
            anchor=tk.NW
        )
        
        # Configure canvas to expand with frame
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Configure canvas scroll
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack widgets
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mouse wheel
        self.inner_frame.bind('<Enter>', self._bind_mousewheel)
        self.inner_frame.bind('<Leave>', self._unbind_mousewheel)
    
    def _on_canvas_configure(self, event):
        """Update inner frame width when canvas resizes."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def _bind_mousewheel(self, event):
        """Bind mouse wheel to scroll."""
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
    
    def _unbind_mousewheel(self, event):
        """Unbind mouse wheel."""
        self.canvas.unbind_all('<MouseWheel>')
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')


class BasePage(tk.Frame):
    """Base class for all pages with scrollable content."""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, bg=COLORS['bg_medium'], **kwargs)
        self.controller = controller
        self.colors = COLORS
        self.fonts = FONTS
        
        # Create scrollable container
        self.scrollable = ScrollableFrame(self, bg_color=COLORS['bg_medium'])
        self.scrollable.pack(fill=tk.BOTH, expand=True)
        
        # Content should be added to self.content
        self.content = self.scrollable.inner_frame
    
    def create_header(self, title, subtitle=""):
        """Create a page header."""
        header = tk.Frame(self.content, bg=self.colors['bg_medium'])
        header.pack(fill=tk.X, padx=30, pady=(25, 20))
        
        tk.Label(
            header,
            text=title,
            font=self.fonts['title'],
            bg=self.colors['bg_medium'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W)
        
        if subtitle:
            tk.Label(
                header,
                text=subtitle,
                font=self.fonts['body'],
                bg=self.colors['bg_medium'],
                fg=self.colors['text_secondary']
            ).pack(anchor=tk.W, pady=(5, 0))
        
        return header
    
    def create_card(self, parent, title="", icon=""):
        """Create a card container."""
        card = tk.Frame(parent, bg=self.colors['bg_card'])
        
        if title:
            title_frame = tk.Frame(card, bg=self.colors['bg_card'])
            title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
            
            title_text = f"{icon}  {title}" if icon else title
            tk.Label(
                title_frame,
                text=title_text,
                font=self.fonts['subheading'],
                bg=self.colors['bg_card'],
                fg=self.colors['accent']
            ).pack(anchor=tk.W)
        
        content = tk.Frame(card, bg=self.colors['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        return card, content
    
    def on_show(self):
        """Called when page is shown. Override in subclasses."""
        pass
    
    def on_hide(self):
        """Called when page is hidden. Override in subclasses."""
        pass
