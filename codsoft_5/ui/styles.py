import tkinter as tk
from tkinter import font

# Define modern color scheme
COLORS = {
    'primary': '#6366f1',      # Indigo
    'secondary': '#8b5cf6',    # Violet
    'accent': '#06b6d4',       # Cyan
    'background': '#f8fafc',   # Light gray
    'card': '#ffffff',         # White
    'light_bg': '#f1f5f9',     # Very light gray
    'text': '#1e293b',         # Dark slate
    'light_text': '#64748b',   # Medium slate
    'border': '#e2e8f0',       # Light border
    'hover': '#f1f5f9',        # Hover background
    'success': '#10b981',      # Green for valid inputs
    'warning': '#f59e0b',      # Amber for warnings
    'danger': '#ef4444'        # Red for errors
}

# Define fonts (will be initialized later)
FONTS = {}

# Configure styles for ttk widgets
def configure_styles(root):
    global FONTS
    
    # Initialize fonts after root window is created
    FONTS = {
        'header': font.Font(family="Helvetica", size=16, weight="bold"),
        'title': font.Font(family="Helvetica", size=14, weight="bold"),
        'subtitle': font.Font(family="Helvetica", size=12, weight="bold"),
        'normal': font.Font(family="Helvetica", size=10),
        'small': font.Font(family="Helvetica", size=9)
    }
    
    style = tk.ttk.Style(root)
    
    # Configure styles for buttons
    style.configure('Primary.TButton', 
                    background=COLORS['primary'],
                    foreground='white',
                    borderwidth=0,
                    focuscolor='none',
                    font=FONTS['normal'])
    
    style.map('Primary.TButton',
              background=[('active', COLORS['secondary'])])
    
    style.configure('Success.TButton', 
                    background=COLORS['success'],
                    foreground='white',
                    borderwidth=0,
                    focuscolor='none',
                    font=FONTS['normal'])
    
    style.map('Success.TButton',
              background=[('active', '#27ae60')])
    
    style.configure('Danger.TButton', 
                    background=COLORS['danger'],
                    foreground='white',
                    borderwidth=0,
                    focuscolor='none',
                    font=FONTS['normal'])
    
    style.map('Danger.TButton',
              background=[('active', '#c0392b')])
    
    # Configure styles for frames
    style.configure('Card.TFrame', 
                    background=COLORS['card'],
                    relief='solid',
                    borderwidth=1)
    
    # Configure styles for labels
    style.configure('Header.TLabel', 
                    background=COLORS['primary'],
                    foreground='white',
                    font=FONTS['header'])
    
    style.configure('Title.TLabel', 
                    background=COLORS['card'],
                    foreground=COLORS['text'],
                    font=FONTS['title'])
    
    style.configure('Subtitle.TLabel', 
                    background=COLORS['card'],
                    foreground=COLORS['text'],
                    font=FONTS['subtitle'])
    
    style.configure('Normal.TLabel', 
                    background=COLORS['card'],
                    foreground=COLORS['text'],
                    font=FONTS['normal'])
    
    style.configure('Light.TLabel', 
                    background=COLORS['card'],
                    foreground=COLORS['light_text'],
                    font=FONTS['normal'])
    
    # Configure styles for entries
    style.configure('Normal.TEntry', 
                    fieldbackground=COLORS['card'],
                    borderwidth=1,
                    relief='solid',
                    font=FONTS['normal'])
    
    # Configure styles for treeview
    style.configure('Contact.Treeview', 
                    background=COLORS['card'],
                    foreground=COLORS['text'],
                    fieldbackground=COLORS['card'],
                    borderwidth=1,
                    relief='solid',
                    font=FONTS['normal'],
                    rowheight=30)
    
    # Force headers to always be visible (fix Windows hover-only issue)
    style.configure('Contact.Treeview.Heading', 
                    background=COLORS['primary'],
                    foreground='white',
                    font=FONTS['subtitle'],
                    relief='raised',
                    borderwidth=2,
                    anchor='w',
                    focuscolor='none')
    
    # Ensure headers stay visible (override default behavior)
    style.map('Contact.Treeview.Heading',
              background=[('!active', COLORS['primary']),
                         ('active', COLORS['secondary']),
                         ('pressed', COLORS['accent'])],
              foreground=[('!active', 'white'),
                         ('active', 'white'),
                         ('pressed', 'white')])
    
    style.map('Contact.Treeview',
              background=[('selected', COLORS['primary'])])