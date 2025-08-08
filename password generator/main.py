import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import string
import secrets
import json
import os
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont
from datetime import datetime, timedelta
import math
import base64
import hashlib
import re
import time
# Try to import pyperclip, but make it optional
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecurePass Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Set icon (if available)
        try:
            self.root.iconbitmap("password_icon.ico")
        except:
            pass
        
        # Initialize variables
        self.password_history = []
        self.settings = {
            'length': 16,
            'uppercase': True,
            'lowercase': True,
            'numbers': True,
            'symbols': True,
            'exclude_similar': False,
            'exclude_ambiguous': False,
            'custom_chars': '',
            'exclude_chars': '',
            'quantity': 1,
            'pronounceable': False,
            'passphrase': False,
            'theme': 'dark',
            'strength_indicator': True,
            'copy_on_generate': False,
            'auto_save': False,
            'save_history': True,
            'max_history': 20
        }
        
        # Character sets
        self.uppercase_chars = string.ascii_uppercase
        self.lowercase_chars = string.ascii_lowercase
        self.number_chars = string.digits
        self.symbol_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.similar_chars = "il1Lo0O"
        self.ambiguous_chars = "{}[]()/\\\"'`~,;.<>"
        
        # Load settings and history
        self.load_settings()
        self.load_history()
        
        # Create style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure theme
        self.configure_theme()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create UI
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Bind events
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Start animation loop
        self.animate_background()
        
        # Check if clipboard is available
        if not CLIPBOARD_AVAILABLE:
            messagebox.showwarning("Clipboard Not Available", 
                                 "The pyperclip module is not installed. Clipboard functionality will be disabled.\n\n" +
                                 "To enable clipboard features, install pyperclip:\n" +
                                 "pip install pyperclip")
    
    def configure_theme(self):
        theme = self.settings['theme']
        
        if theme == 'dark':
            bg_color = "#1e1e2e"
            secondary_bg = "#2d2d44"
            accent = "#6c5ce7"
            text_color = "#dfe6e9"
            accent_text = "#fd79a8"
            success = "#00b894"
            warning = "#fdcb6e"
            danger = "#e17055"
            button_bg = "#6c5ce7"
            button_hover = "#5f3dc4"
        else:  # light theme
            bg_color = "#f5f6fa"
            secondary_bg = "#dfe6e9"
            accent = "#6c5ce7"
            text_color = "#2d3436"
            accent_text = "#e84393"
            success = "#00b894"
            warning = "#fdcb6e"
            danger = "#e17055"
            button_bg = "#6c5ce7"
            button_hover = "#5f3dc4"
        
        # Configure root
        self.root.configure(bg=bg_color)
        
        # Configure styles
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TButton', 
                            font=('Arial', 10, 'bold'), 
                            background=button_bg, 
                            foreground='white',
                            borderwidth=0,
                            focuscolor='none',
                            padding=8)
        self.style.map('TButton', 
                      background=[('active', button_hover)],
                      foreground=[('active', 'white')])
        self.style.configure('Generate.TButton', 
                            font=('Arial', 12, 'bold'), 
                            background=accent, 
                            foreground='white',
                            borderwidth=0,
                            focuscolor='none',
                            padding=12)
        self.style.map('Generate.TButton', 
                      background=[('active', button_hover)],
                      foreground=[('active', 'white')])
        self.style.configure('TLabel', 
                            background=bg_color, 
                            foreground=text_color, 
                            font=('Arial', 10))
        self.style.configure('Title.TLabel', 
                            font=('Arial', 20, 'bold'), 
                            foreground=accent_text)
        self.style.configure('Header.TLabel', 
                            font=('Arial', 14, 'bold'), 
                            foreground=accent_text)
        self.style.configure('Card.TFrame', 
                            background=secondary_bg, 
                            relief=tk.RAISED, 
                            borderwidth=1)
        self.style.configure('TScale', 
                            background=bg_color, 
                            troughcolor=secondary_bg,
                            borderwidth=0,
                            lightcolor=button_bg,
                            darkcolor=button_hover)
        self.style.configure('TCheckbutton', 
                            background=bg_color, 
                            foreground=text_color,
                            font=('Arial', 10))
        self.style.configure('TCombobox', 
                            fieldbackground=secondary_bg,
                            background=secondary_bg,
                            foreground=text_color,
                            arrowcolor=text_color,
                            borderwidth=1,
                            focuscolor='none')
        self.style.map('TCombobox', 
                      fieldbackground=[('readonly', secondary_bg)],
                      selectbackground=[('readonly', button_bg)],
                      selectforeground=[('readonly', 'white')])
        
        # Store colors for later use
        self.colors = {
            'bg': bg_color,
            'secondary_bg': secondary_bg,
            'accent': accent,
            'text': text_color,
            'accent_text': accent_text,
            'success': success,
            'warning': warning,
            'danger': danger,
            'button_bg': button_bg,
            'button_hover': button_hover
        }
    
    def create_header(self):
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo and title
        logo_frame = ttk.Frame(header_frame)
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        self.logo_canvas = tk.Canvas(logo_frame, width=60, height=60, highlightthickness=0, bg=self.colors['bg'])
        self.logo_canvas.pack()
        self.draw_logo()
        
        title_text = "SecurePass Generator"
        title_label = ttk.Label(header_frame, text=title_text, style='Title.TLabel')
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Theme toggle button
        theme_btn = ttk.Button(header_frame, text="🌓 Toggle Theme", 
                              command=self.toggle_theme)
        theme_btn.pack(side=tk.RIGHT, padx=10)
    
    def draw_logo(self):
        canvas = self.logo_canvas
        canvas.delete("all")
        
        # Draw a lock icon
        # Lock body
        canvas.create_rectangle(15, 25, 45, 50, fill=self.colors['accent'], outline="")
        # Lock shackle
        canvas.create_arc(20, 15, 40, 35, start=0, extent=180, style=tk.ARC, 
                         outline=self.colors['accent'], width=4)
        # Keyhole
        canvas.create_oval(27, 32, 33, 38, fill=self.colors['bg'], outline="")
        canvas.create_rectangle(28, 38, 32, 45, fill=self.colors['bg'], outline="")
    
    def create_main_content(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Generator tab
        self.generator_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.generator_tab, text="Generator")
        
        # History tab
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="History")
        
        # Settings tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Create content for each tab
        self.create_generator_tab()
        self.create_history_tab()
        self.create_settings_tab()
    
    def create_generator_tab(self):
        # Create a scrollable frame for the generator tab
        self.generator_canvas = tk.Canvas(self.generator_tab, bg=self.colors['bg'], highlightthickness=0)
        generator_scrollbar = ttk.Scrollbar(self.generator_tab, orient="vertical", command=self.generator_canvas.yview)
        self.generator_canvas.configure(yscrollcommand=generator_scrollbar.set)
        
        generator_scrollbar.pack(side="right", fill="y")
        self.generator_canvas.pack(side="left", fill="both", expand=True)
        
        # Create a frame inside the canvas
        self.generator_frame = ttk.Frame(self.generator_canvas)
        self.generator_canvas.create_window((0, 0), window=self.generator_frame, anchor="nw")
        
        # Update scrollregion when frame size changes
        self.generator_frame.bind("<Configure>", self.update_generator_scrollregion)
        
        # Main container for generator
        gen_container = ttk.Frame(self.generator_frame)
        gen_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a prominent generate button at the top
        generate_btn_frame = ttk.Frame(gen_container)
        generate_btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.generate_btn = ttk.Button(generate_btn_frame, text="🔑 GENERATE PASSWORD 🔑", 
                                      style='Generate.TButton', command=self.generate_password)
        self.generate_btn.pack(pady=10)
        
        # Left panel - Options
        left_panel = ttk.Frame(gen_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Options card
        options_card = ttk.Frame(left_panel, style='Card.TFrame')
        options_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Password length
        length_frame = ttk.Frame(options_card)
        length_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(length_frame, text="Password Length:", style='Header.TLabel').pack(anchor=tk.W)
        
        length_control_frame = ttk.Frame(length_frame)
        length_control_frame.pack(fill=tk.X, pady=5)
        
        self.length_var = tk.IntVar(value=self.settings['length'])
        self.length_slider = ttk.Scale(length_control_frame, from_=4, to=128, 
                                      variable=self.length_var, orient=tk.HORIZONTAL)
        self.length_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.length_label = ttk.Label(length_control_frame, text=str(self.settings['length']))
        self.length_label.pack(side=tk.LEFT, padx=10)
        
        self.length_slider.config(command=self.update_length_label)
        
        # Character options
        char_options_frame = ttk.Frame(options_card)
        char_options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(char_options_frame, text="Character Options:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        self.uppercase_var = tk.BooleanVar(value=self.settings['uppercase'])
        uppercase_check = ttk.Checkbutton(char_options_frame, text="Uppercase Letters (A-Z)", 
                                         variable=self.uppercase_var)
        uppercase_check.pack(anchor=tk.W, pady=2)
        
        self.lowercase_var = tk.BooleanVar(value=self.settings['lowercase'])
        lowercase_check = ttk.Checkbutton(char_options_frame, text="Lowercase Letters (a-z)", 
                                         variable=self.lowercase_var)
        lowercase_check.pack(anchor=tk.W, pady=2)
        
        self.numbers_var = tk.BooleanVar(value=self.settings['numbers'])
        numbers_check = ttk.Checkbutton(char_options_frame, text="Numbers (0-9)", 
                                       variable=self.numbers_var)
        numbers_check.pack(anchor=tk.W, pady=2)
        
        self.symbols_var = tk.BooleanVar(value=self.settings['symbols'])
        symbols_check = ttk.Checkbutton(char_options_frame, text="Symbols (!@#$%^&*)", 
                                       variable=self.symbols_var)
        symbols_check.pack(anchor=tk.W, pady=2)
        
        # Advanced options
        advanced_frame = ttk.Frame(options_card)
        advanced_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(advanced_frame, text="Advanced Options:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        self.exclude_similar_var = tk.BooleanVar(value=self.settings['exclude_similar'])
        exclude_similar_check = ttk.Checkbutton(advanced_frame, text="Exclude Similar Characters (i, l, 1, L, o, 0, O)", 
                                               variable=self.exclude_similar_var)
        exclude_similar_check.pack(anchor=tk.W, pady=2)
        
        self.exclude_ambiguous_var = tk.BooleanVar(value=self.settings['exclude_ambiguous'])
        exclude_ambiguous_check = ttk.Checkbutton(advanced_frame, text="Exclude Ambiguous Characters ({ } [ ] ( ) / \\ ' \" ` ~ , ; : . < >)", 
                                                 variable=self.exclude_ambiguous_var)
        exclude_ambiguous_check.pack(anchor=tk.W, pady=2)
        
        # Custom characters
        custom_frame = ttk.Frame(options_card)
        custom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(custom_frame, text="Custom Characters:", style='Header.TLabel').pack(anchor=tk.W)
        
        custom_entry_frame = ttk.Frame(custom_frame)
        custom_entry_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(custom_entry_frame, text="Include only:").pack(side=tk.LEFT)
        self.custom_chars_var = tk.StringVar(value=self.settings['custom_chars'])
        custom_chars_entry = ttk.Entry(custom_entry_frame, textvariable=self.custom_chars_var)
        custom_chars_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        exclude_entry_frame = ttk.Frame(custom_frame)
        exclude_entry_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(exclude_entry_frame, text="Exclude:").pack(side=tk.LEFT)
        self.exclude_chars_var = tk.StringVar(value=self.settings['exclude_chars'])
        exclude_chars_entry = ttk.Entry(exclude_entry_frame, textvariable=self.exclude_chars_var)
        exclude_chars_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Password type
        type_frame = ttk.Frame(options_card)
        type_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(type_frame, text="Password Type:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        self.password_type_var = tk.StringVar(value="random")
        random_radio = ttk.Radiobutton(type_frame, text="Random Password", 
                                      variable=self.password_type_var, value="random")
        random_radio.pack(anchor=tk.W, pady=2)
        
        self.pronounceable_var = tk.BooleanVar(value=self.settings['pronounceable'])
        pronounceable_radio = ttk.Radiobutton(type_frame, text="Pronounceable Password", 
                                            variable=self.password_type_var, value="pronounceable",
                                            command=self.toggle_pronounceable)
        pronounceable_radio.pack(anchor=tk.W, pady=2)
        
        self.passphrase_var = tk.BooleanVar(value=self.settings['passphrase'])
        passphrase_radio = ttk.Radiobutton(type_frame, text="Passphrase (Multiple Words)", 
                                          variable=self.password_type_var, value="passphrase",
                                          command=self.toggle_passphrase)
        passphrase_radio.pack(anchor=tk.W, pady=2)
        
        # Quantity
        quantity_frame = ttk.Frame(options_card)
        quantity_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(quantity_frame, text="Quantity:", style='Header.TLabel').pack(anchor=tk.W)
        
        quantity_control_frame = ttk.Frame(quantity_frame)
        quantity_control_frame.pack(fill=tk.X, pady=5)
        
        self.quantity_var = tk.IntVar(value=self.settings['quantity'])
        self.quantity_slider = ttk.Scale(quantity_control_frame, from_=1, to=50, 
                                       variable=self.quantity_var, orient=tk.HORIZONTAL)
        self.quantity_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.quantity_label = ttk.Label(quantity_control_frame, text=str(self.settings['quantity']))
        self.quantity_label.pack(side=tk.LEFT, padx=10)
        
        self.quantity_slider.config(command=self.update_quantity_label)
        
        # Right panel - Results
        right_panel = ttk.Frame(gen_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Results card
        results_card = ttk.Frame(right_panel, style='Card.TFrame')
        results_card.pack(fill=tk.BOTH, expand=True)
        
        # Password display
        password_frame = ttk.Frame(results_card)
        password_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(password_frame, text="Generated Password:", style='Header.TLabel').pack(anchor=tk.W)
        
        self.password_display_frame = ttk.Frame(password_frame)
        self.password_display_frame.pack(fill=tk.X, pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.password_display_frame, textvariable=self.password_var, 
                                       font=('Courier', 12), state='readonly')
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        copy_btn = ttk.Button(self.password_display_frame, text="📋 Copy", 
                             command=self.copy_password)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Disable copy button if clipboard not available
        if not CLIPBOARD_AVAILABLE:
            copy_btn.config(state='disabled')
        
        # Strength indicator
        if self.settings['strength_indicator']:
            strength_frame = ttk.Frame(results_card)
            strength_frame.pack(fill=tk.X, padx=10, pady=10)
            
            ttk.Label(strength_frame, text="Password Strength:", style='Header.TLabel').pack(anchor=tk.W)
            
            self.strength_canvas = tk.Canvas(strength_frame, height=20, highlightthickness=0, 
                                           bg=self.colors['secondary_bg'])
            self.strength_canvas.pack(fill=tk.X, pady=5)
            
            self.strength_label = ttk.Label(strength_frame, text="No password generated")
            self.strength_label.pack()
        
        # QR code - SMALLER SIZE
        qr_frame = ttk.Frame(results_card)
        qr_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(qr_frame, text="QR Code:", style='Header.TLabel').pack(anchor=tk.W)
        
        # Create a frame for QR code
        qr_container = ttk.Frame(qr_frame)
        qr_container.pack(fill=tk.X, pady=5)
        
        # Create canvas with smaller size (200x200)
        self.qr_canvas = tk.Canvas(qr_container, width=200, height=200, 
                                  highlightthickness=0, bg=self.colors['secondary_bg'])
        self.qr_canvas.pack()
        
        # Password details
        details_frame = ttk.Frame(results_card)
        details_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(details_frame, text="Password Details:", style='Header.TLabel').pack(anchor=tk.W)
        
        self.details_text = tk.Text(details_frame, height=8, width=40, wrap=tk.WORD, 
                                   font=('Courier', 10), state='disabled')
        self.details_text.pack(fill=tk.X, pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(results_card)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        save_btn = ttk.Button(action_frame, text="💾 Save Password", 
                             command=self.save_password)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(action_frame, text="🔄 New Password", 
                                command=self.generate_password)
        refresh_btn.pack(side=tk.LEFT, padx=5)
    
    def update_generator_scrollregion(self, event=None):
        """Update the scrollregion of the generator canvas"""
        self.generator_canvas.configure(scrollregion=self.generator_canvas.bbox("all"))
    
    def create_history_tab(self):
        # Main container for history
        hist_container = ttk.Frame(self.history_tab)
        hist_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toolbar
        toolbar = ttk.Frame(hist_container)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(toolbar, text="Password History", style='Header.TLabel').pack(side=tk.LEFT, padx=10)
        
        clear_btn = ttk.Button(toolbar, text="🗑️ Clear History", 
                              command=self.clear_history)
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        export_btn = ttk.Button(toolbar, text="📤 Export History", 
                               command=self.export_history)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        # History list
        history_card = ttk.Frame(hist_container, style='Card.TFrame')
        history_card.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for history
        tree_frame = ttk.Frame(history_card)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_tree = ttk.Treeview(tree_frame, columns=('password', 'length', 'strength', 'date'), 
                                        show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.history_tree.yview)
        
        self.history_tree.heading('password', text='Password')
        self.history_tree.heading('length', text='Length')
        self.history_tree.heading('strength', text='Strength')
        self.history_tree.heading('date', text='Date')
        
        self.history_tree.column('password', width=200)
        self.history_tree.column('length', width=80)
        self.history_tree.column('strength', width=100)
        self.history_tree.column('date', width=150)
        
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click to copy password
        self.history_tree.bind("<Double-1>", self.copy_history_password)
        
        # Populate history
        self.populate_history()
    
    def create_settings_tab(self):
        # Main container for settings
        settings_container = ttk.Frame(self.settings_tab)
        settings_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings
        general_card = ttk.Frame(settings_container, style='Card.TFrame')
        general_card.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(general_card, text="General Settings", style='Header.TLabel').pack(anchor=tk.W, padx=10, pady=10)
        
        # Theme
        theme_frame = ttk.Frame(general_card)
        theme_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=5)
        
        self.theme_var = tk.StringVar(value=self.settings['theme'])
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                  values=['dark', 'light'], state='readonly')
        theme_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        
        # Copy on generate
        self.copy_on_generate_var = tk.BooleanVar(value=self.settings['copy_on_generate'])
        copy_check = ttk.Checkbutton(general_card, text="Copy to clipboard on generate", 
                                    variable=self.copy_on_generate_var,
                                    command=self.update_copy_setting)
        copy_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Disable if clipboard not available
        if not CLIPBOARD_AVAILABLE:
            copy_check.config(state='disabled')
        
        # Auto save
        self.auto_save_var = tk.BooleanVar(value=self.settings['auto_save'])
        auto_save_check = ttk.Checkbutton(general_card, text="Auto save generated passwords", 
                                        variable=self.auto_save_var,
                                        command=self.update_auto_save_setting)
        auto_save_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Save history
        self.save_history_var = tk.BooleanVar(value=self.settings['save_history'])
        save_history_check = ttk.Checkbutton(general_card, text="Save password history", 
                                           variable=self.save_history_var,
                                           command=self.update_save_history_setting)
        save_history_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Max history
        history_frame = ttk.Frame(general_card)
        history_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(history_frame, text="Max history entries:").pack(side=tk.LEFT, padx=5)
        
        self.max_history_var = tk.IntVar(value=self.settings['max_history'])
        max_history_spin = ttk.Spinbox(history_frame, from_=5, to=100, textvariable=self.max_history_var, 
                                      width=5, command=self.update_max_history)
        max_history_spin.pack(side=tk.LEFT, padx=5)
        
        # Password policies
        policy_card = ttk.Frame(settings_container, style='Card.TFrame')
        policy_card.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(policy_card, text="Password Policies", style='Header.TLabel').pack(anchor=tk.W, padx=10, pady=10)
        
        # Minimum length
        min_length_frame = ttk.Frame(policy_card)
        min_length_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(min_length_frame, text="Minimum length:").pack(side=tk.LEFT, padx=5)
        
        self.min_length_var = tk.IntVar(value=8)
        min_length_spin = ttk.Spinbox(min_length_frame, from_=4, to=32, textvariable=self.min_length_var, 
                                     width=5)
        min_length_spin.pack(side=tk.LEFT, padx=5)
        
        # Require uppercase
        self.require_uppercase_var = tk.BooleanVar(value=False)
        require_uppercase_check = ttk.Checkbutton(policy_card, text="Require at least one uppercase letter", 
                                                 variable=self.require_uppercase_var)
        require_uppercase_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Require lowercase
        self.require_lowercase_var = tk.BooleanVar(value=False)
        require_lowercase_check = ttk.Checkbutton(policy_card, text="Require at least one lowercase letter", 
                                                 variable=self.require_lowercase_var)
        require_lowercase_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Require number
        self.require_number_var = tk.BooleanVar(value=False)
        require_number_check = ttk.Checkbutton(policy_card, text="Require at least one number", 
                                              variable=self.require_number_var)
        require_number_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Require symbol
        self.require_symbol_var = tk.BooleanVar(value=False)
        require_symbol_check = ttk.Checkbutton(policy_card, text="Require at least one symbol", 
                                             variable=self.require_symbol_var)
        require_symbol_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Save button
        save_btn = ttk.Button(settings_container, text="💾 Save Settings", 
                             command=self.save_settings)
        save_btn.pack(pady=10)
    
    def create_footer(self):
        footer_frame = ttk.Frame(self.main_container)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        footer_text = "SecurePass Generator © 2023 | Your passwords are never stored or transmitted"
        footer_label = ttk.Label(footer_frame, text=footer_text, style='Stats.TLabel')
        footer_label.pack()
    
    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))
    
    def update_quantity_label(self, value):
        self.quantity_label.config(text=str(int(float(value))))
    
    def toggle_pronounceable(self):
        self.pronounceable_var.set(True)
        self.passphrase_var.set(False)
    
    def toggle_passphrase(self):
        self.pronounceable_var.set(False)
        self.passphrase_var.set(True)
    
    def toggle_theme(self):
        if self.settings['theme'] == 'dark':
            self.settings['theme'] = 'light'
        else:
            self.settings['theme'] = 'dark'
        
        self.theme_var.set(self.settings['theme'])
        self.configure_theme()
        self.save_settings()
    
    def change_theme(self, event):
        self.settings['theme'] = self.theme_var.get()
        self.configure_theme()
        self.save_settings()
    
    def update_copy_setting(self):
        self.settings['copy_on_generate'] = self.copy_on_generate_var.get()
        self.save_settings()
    
    def update_auto_save_setting(self):
        self.settings['auto_save'] = self.auto_save_var.get()
        self.save_settings()
    
    def update_save_history_setting(self):
        self.settings['save_history'] = self.save_history_var.get()
        self.save_settings()
    
    def update_max_history(self):
        self.settings['max_history'] = self.max_history_var.get()
        self.save_settings()
    
    def generate_password(self):
        password_type = self.password_type_var.get()
        
        if password_type == "random":
            password = self.generate_random_password()
        elif password_type == "pronounceable":
            password = self.generate_pronounceable_password()
        elif password_type == "passphrase":
            password = self.generate_passphrase()
        else:
            password = self.generate_random_password()
        
        self.password_var.set(password)
        
        # Copy to clipboard if enabled
        if self.settings['copy_on_generate'] and CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        
        # Calculate strength
        strength = self.calculate_strength(password)
        self.update_strength_indicator(strength)
        
        # Update details
        self.update_password_details(password)
        
        # Generate QR code
        self.generate_qr_code(password)
        
        # Save to history if enabled
        if self.settings['save_history']:
            self.add_to_history(password, len(password), strength)
        
        # Auto save if enabled
        if self.settings['auto_save']:
            self.save_password_to_file(password)
    
    def generate_random_password(self):
        length = self.length_var.get()
        quantity = self.quantity_var.get()
        
        # Build character set
        char_set = ""
        
        if self.custom_chars_var.get():
            # Use only custom characters
            char_set = self.custom_chars_var.get()
        else:
            # Use standard character sets based on options
            if self.uppercase_var.get():
                char_set += self.uppercase_chars
            if self.lowercase_var.get():
                char_set += self.lowercase_chars
            if self.numbers_var.get():
                char_set += self.number_chars
            if self.symbols_var.get():
                char_set += self.symbol_chars
            
            # Apply exclusions
            if self.exclude_similar_var.get():
                for char in self.similar_chars:
                    char_set = char_set.replace(char, "")
            
            if self.exclude_ambiguous_var.get():
                for char in self.ambiguous_chars:
                    char_set = char_set.replace(char, "")
            
            if self.exclude_chars_var.get():
                for char in self.exclude_chars_var.get():
                    char_set = char_set.replace(char, "")
        
        # Ensure character set is not empty
        if not char_set:
            char_set = string.ascii_letters + string.digits
        
        # Generate password
        password = ''.join(secrets.choice(char_set) for _ in range(length))
        
        # Apply password policies if enabled
        password = self.apply_password_policies(password)
        
        return password
    
    def generate_pronounceable_password(self):
        length = self.length_var.get()
        
        # Syllables for pronounceable passwords
        syllables = [
            'ba', 'be', 'bi', 'bo', 'bu', 'by',
            'ca', 'ce', 'ci', 'co', 'cu', 'cy',
            'da', 'de', 'di', 'do', 'du', 'dy',
            'fa', 'fe', 'fi', 'fo', 'fu', 'fy',
            'ga', 'ge', 'gi', 'go', 'gu', 'gy',
            'ha', 'he', 'hi', 'ho', 'hu', 'hy',
            'ja', 'je', 'ji', 'jo', 'ju', 'jy',
            'ka', 'ke', 'ki', 'ko', 'ku', 'ky',
            'la', 'le', 'li', 'lo', 'lu', 'ly',
            'ma', 'me', 'mi', 'mo', 'mu', 'my',
            'na', 'ne', 'ni', 'no', 'nu', 'ny',
            'pa', 'pe', 'pi', 'po', 'pu', 'py',
            'qa', 'qe', 'qi', 'qo', 'qu', 'qy',
            'ra', 're', 'ri', 'ro', 'ru', 'ry',
            'sa', 'se', 'si', 'so', 'su', 'sy',
            'ta', 'te', 'ti', 'to', 'tu', 'ty',
            'va', 've', 'vi', 'vo', 'vu', 'vy',
            'wa', 'we', 'wi', 'wo', 'wu', 'wy',
            'xa', 'xe', 'xi', 'xo', 'xu', 'xy',
            'ya', 'ye', 'yi', 'yo', 'yu', 'yy',
            'za', 'ze', 'zi', 'zo', 'zu', 'zy'
        ]
        
        # Generate password from syllables
        password = ""
        while len(password) < length:
            syllable = secrets.choice(syllables)
            password += syllable
        
        # Trim to exact length
        password = password[:length]
        
        # Capitalize some letters for complexity
        password_chars = list(password)
        for i in range(len(password_chars)):
            if i % 3 == 0 and password_chars[i].isalpha():
                password_chars[i] = password_chars[i].upper()
        
        # Add some numbers and symbols if requested
        if self.numbers_var.get() and len(password) > 3:
            num_pos = secrets.randint(1, len(password) - 2)
            password_chars[num_pos] = secrets.choice(self.number_chars)
        
        if self.symbols_var.get() and len(password) > 3:
            sym_pos = secrets.randint(1, len(password) - 2)
            password_chars[sym_pos] = secrets.choice(self.symbol_chars)
        
        password = ''.join(password_chars)
        
        # Apply password policies if enabled
        password = self.apply_password_policies(password)
        
        return password
    
    def generate_passphrase(self):
        # Common words for passphrase
        words = [
            'apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew',
            'kiwi', 'lemon', 'mango', 'nectarine', 'orange', 'papaya', 'quince', 'raspberry',
            'strawberry', 'tangerine', 'watermelon', 'blueberry', 'coconut', 'dragonfruit',
            'guava', 'jackfruit', 'lime', 'melon', 'olive', 'peach', 'pear', 'plum',
            'pineapple', 'pomegranate', 'apricot', 'avocado', 'blackberry', 'cantaloupe',
            'carambola', 'clementine', 'durian', 'grapefruit', 'jujube', 'kumquat',
            'lychee', 'mandarin', 'mulberry', 'nance', 'pomelo', 'rambutan', 'salak',
            'sapodilla', 'soursop', 'starfruit', 'tamarind', 'ugli', 'voavanga', 'yangmei',
            'zucchini', 'acorn', 'almond', 'anise', 'artichoke', 'arugula', 'asparagus',
            'aubergine', 'bamboo', 'bean', 'beet', 'broccoli', 'brussels', 'cabbage',
            'carrot', 'cauliflower', 'celery', 'chard', 'chickpea', 'chive', 'cocoa',
            'coffee', 'collard', 'corn', 'cucumber', 'currant', 'dill', 'eggplant',
            'endive', 'fennel', 'garlic', 'ginger', 'kale', 'kohlrabi', 'leek',
            'lentil', 'lettuce', 'mushroom', 'mustard', 'okra', 'onion', 'oregano',
            'parsley', 'parsnip', 'pea', 'pepper', 'potato', 'pumpkin', 'radish',
            'rhubarb', 'rutabaga', 'sage', 'scallion', 'shallot', 'sorrel', 'soybean',
            'spinach', 'squash', 'taro', 'thyme', 'tomato', 'turnip', 'vanilla',
            'watercress', 'yam', 'zucchini', 'basil', 'caper', 'cardamom', 'cassava',
            'chicory', 'cinnamon', 'clove', 'coriander', 'cumin', 'curry', 'dandelion',
            'fennel', 'fenugreek', 'flax', 'galangal', 'ginseng', 'horseradish',
            'juniper', 'lavender', 'lemongrass', 'licorice', 'marjoram', 'marshmallow',
            'mustard', 'nutmeg', 'oregano', 'paprika', 'parsley', 'peppermint',
            'poppy', 'rosemary', 'saffron', 'sage', 'salt', 'savory', 'sesame',
            'spearmint', 'tarragon', 'thyme', 'turmeric', 'vanilla', 'wasabi'
        ]
        
        # Determine number of words based on length
        num_words = max(3, min(10, self.length_var.get() // 4))
        
        # Generate passphrase
        passphrase_words = []
        for _ in range(num_words):
            word = secrets.choice(words)
            passphrase_words.append(word)
        
        # Join with separators
        separators = ['-', '_', '.', '']
        separator = secrets.choice(separators)
        passphrase = separator.join(passphrase_words)
        
        # Capitalize first letter of each word
        passphrase = ' '.join(word.capitalize() for word in passphrase_words)
        
        # Add numbers and symbols if requested
        if self.numbers_var.get():
            passphrase += str(secrets.randint(0, 99))
        
        if self.symbols_var.get():
            passphrase += secrets.choice(self.symbol_chars)
        
        # Apply password policies if enabled
        passphrase = self.apply_password_policies(passphrase)
        
        return passphrase
    
    def apply_password_policies(self, password):
        # Apply minimum length policy
        if len(password) < self.min_length_var.get():
            # Add random characters to meet minimum length
            needed_length = self.min_length_var.get() - len(password)
            additional_chars = ''.join(secrets.choice(string.ascii_letters + string.digits) 
                                     for _ in range(needed_length))
            password += additional_chars
        
        # Apply character requirements
        password_chars = list(password)
        
        # Ensure at least one uppercase letter
        if self.require_uppercase_var.get() and not any(c.isupper() for c in password_chars):
            pos = secrets.randint(0, len(password_chars) - 1)
            password_chars[pos] = password_chars[pos].upper()
        
        # Ensure at least one lowercase letter
        if self.require_lowercase_var.get() and not any(c.islower() for c in password_chars):
            pos = secrets.randint(0, len(password_chars) - 1)
            password_chars[pos] = password_chars[pos].lower()
        
        # Ensure at least one number
        if self.require_number_var.get() and not any(c.isdigit() for c in password_chars):
            pos = secrets.randint(0, len(password_chars) - 1)
            password_chars[pos] = secrets.choice(self.number_chars)
        
        # Ensure at least one symbol
        if self.require_symbol_var.get() and not any(c in self.symbol_chars for c in password_chars):
            pos = secrets.randint(0, len(password_chars) - 1)
            password_chars[pos] = secrets.choice(self.symbol_chars)
        
        return ''.join(password_chars)
    
    def calculate_strength(self, password):
        # Calculate password strength based on various factors
        score = 0
        
        # Length contributes to score
        score += min(len(password) * 4, 40)
        
        # Character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in self.symbol_chars for c in password)
        
        variety = sum([has_upper, has_lower, has_digit, has_symbol])
        score += variety * 10
        
        # Entropy calculation
        pool_size = 0
        if has_upper:
            pool_size += 26
        if has_lower:
            pool_size += 26
        if has_digit:
            pool_size += 10
        if has_symbol:
            pool_size += len(self.symbol_chars)
        
        if pool_size > 0:
            entropy = len(password) * math.log2(pool_size)
            score += min(entropy, 40)
        
        # Common patterns reduce score
        common_patterns = [
            r'123', r'abc', r'qwe', r'asd', r'zxc',
            r'password', r'admin', r'login', r'welcome',
            r'qwerty', r'letmein', r'access', r'master'
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, password, re.IGNORECASE):
                score -= 10
        
        # Repeated characters reduce score
        for i in range(len(password) - 1):
            if password[i] == password[i+1]:
                score -= 2
        
        # Sequential characters reduce score
        for i in range(len(password) - 2):
            if (ord(password[i+1]) == ord(password[i]) + 1 and 
                ord(password[i+2]) == ord(password[i]) + 2):
                score -= 5
        
        # Determine strength level
        if score < 40:
            return "Very Weak", self.colors['danger']
        elif score < 60:
            return "Weak", self.colors['warning']
        elif score < 80:
            return "Medium", self.colors['warning']
        elif score < 100:
            return "Strong", self.colors['success']
        else:
            return "Very Strong", self.colors['success']
    
    def update_strength_indicator(self, strength):
        strength_text, strength_color = strength
        
        # Update strength label
        self.strength_label.config(text=f"Password Strength: {strength_text}", foreground=strength_color)
        
        # Update strength bar
        self.strength_canvas.delete("all")
        
        # Calculate width based on strength
        if strength_text == "Very Weak":
            width = 20
        elif strength_text == "Weak":
            width = 40
        elif strength_text == "Medium":
            width = 60
        elif strength_text == "Strong":
            width = 80
        else:  # Very Strong
            width = 100
        
        # Draw strength bar
        canvas_width = self.strength_canvas.winfo_width()
        if canvas_width > 1:  # Canvas has been rendered
            bar_width = int(canvas_width * width / 100)
            self.strength_canvas.create_rectangle(0, 0, bar_width, 20, 
                                               fill=strength_color, outline="")
    
    def update_password_details(self, password):
        # Enable text widget for editing
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)
        
        # Calculate details
        length = len(password)
        entropy = self.calculate_entropy(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in self.symbol_chars for c in password)
        
        # Create details text
        details = f"Length: {length} characters\n"
        details += f"Entropy: {entropy:.2f} bits\n"
        details += f"Character Types:\n"
        details += f"  Uppercase: {'Yes' if has_upper else 'No'}\n"
        details += f"  Lowercase: {'Yes' if has_lower else 'No'}\n"
        details += f"  Numbers: {'Yes' if has_digit else 'No'}\n"
        details += f"  Symbols: {'Yes' if has_symbol else 'No'}\n"
        
        # Add time to crack estimate
        time_to_crack = self.estimate_crack_time(entropy)
        details += f"\nEstimated time to crack: {time_to_crack}"
        
        # Insert details
        self.details_text.insert(1.0, details)
        
        # Disable text widget again
        self.details_text.config(state='disabled')
    
    def calculate_entropy(self, password):
        # Calculate password entropy
        pool_size = 0
        
        if any(c.isupper() for c in password):
            pool_size += 26
        if any(c.islower() for c in password):
            pool_size += 26
        if any(c.isdigit() for c in password):
            pool_size += 10
        if any(c in self.symbol_chars for c in password):
            pool_size += len(self.symbol_chars)
        
        if pool_size == 0:
            return 0
        
        return len(password) * math.log2(pool_size)
    
    def estimate_crack_time(self, entropy):
        # Estimate time to crack based on entropy
        # Assuming 100 billion guesses per second (high-end GPU)
        guesses_per_second = 100000000000
        total_guesses = 2 ** entropy
        
        seconds = total_guesses / guesses_per_second
        
        if seconds < 1:
            return "Instantly"
        elif seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds / 60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds / 3600:.1f} hours"
        elif seconds < 31536000:
            return f"{seconds / 86400:.1f} days"
        elif seconds < 31536000000:
            return f"{seconds / 31536000:.1f} years"
        else:
            return "Billions of years"
    
    def generate_qr_code(self, password):
        # Clear previous QR code
        self.qr_canvas.delete("all")
        
        try:
            # Generate QR code with smaller box size
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,  # Reduced box size for smaller QR code
                border=2,
            )
            qr.add_data(password)
            qr.make(fit=True)
            
            # Create image with white background
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Resize to fit canvas (180x180 to leave a small border)
            canvas_size = 180
            img = img.resize((canvas_size, canvas_size), Image.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Clear canvas and display QR code centered
            self.qr_canvas.delete("all")
            # Position at center of 200x200 canvas
            self.qr_canvas.create_image(100, 100, image=photo)  
            self.qr_canvas.image = photo  # Keep a reference
            
            # Draw a border around the QR code
            self.qr_canvas.create_rectangle(5, 5, 195, 195, outline=self.colors['accent'], width=1)
            
        except Exception as e:
            print(f"Error generating QR code: {e}")
            # Display error message if QR code generation fails
            self.qr_canvas.create_text(100, 100, text="QR Code\nUnavailable", 
                                      fill=self.colors['text'], font=('Arial', 10))
    
    def copy_password(self):
        password = self.password_var.get()
        if password:
            if CLIPBOARD_AVAILABLE:
                pyperclip.copy(password)
                messagebox.showinfo("Copied", "Password copied to clipboard!")
            else:
                # Fallback method using Tkinter's clipboard
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                messagebox.showinfo("Copied", "Password copied to clipboard (using fallback method)!")
    
    def copy_history_password(self, event):
        # Get selected item
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            password = item['values'][0]
            
            # Copy to clipboard
            if CLIPBOARD_AVAILABLE:
                pyperclip.copy(password)
                messagebox.showinfo("Copied", "Password copied to clipboard!")
            else:
                # Fallback method using Tkinter's clipboard
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                messagebox.showinfo("Copied", "Password copied to clipboard (using fallback method)!")
    
    def save_password(self):
        password = self.password_var.get()
        if password:
            self.save_password_to_file(password)
    
    def save_password_to_file(self, password):
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Password"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(f"Generated Password: {password}\n")
                    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Length: {len(password)}\n")
                    
                    # Add additional details
                    strength, _ = self.calculate_strength(password)
                    f.write(f"Strength: {strength}\n")
                    f.write(f"Entropy: {self.calculate_entropy(password):.2f} bits\n")
                
                messagebox.showinfo("Saved", f"Password saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save password: {str(e)}")
    
    def add_to_history(self, password, length, strength):
        # Add password to history
        history_entry = {
            'password': password,
            'length': length,
            'strength': strength[0],  # Just the text part
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.password_history.append(history_entry)
        
        # Limit history size
        if len(self.password_history) > self.settings['max_history']:
            self.password_history = self.password_history[-self.settings['max_history']:]
        
        # Save history
        self.save_history()
        
        # Update history display
        self.populate_history()
    
    def populate_history(self):
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add history items
        for entry in self.password_history:
            self.history_tree.insert('', tk.END, values=(
                entry['password'],
                entry['length'],
                entry['strength'],
                entry['date']
            ))
    
    def clear_history(self):
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the password history?"):
            self.password_history = []
            self.save_history()
            self.populate_history()
    
    def export_history(self):
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Password History"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    # Write header
                    f.write("Password,Length,Strength,Date\n")
                    
                    # Write history entries
                    for entry in self.password_history:
                        f.write(f"{entry['password']},{entry['length']},{entry['strength']},{entry['date']}\n")
                
                messagebox.showinfo("Exported", f"Password history exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export history: {str(e)}")
    
    def save_settings(self):
        # Update settings from UI
        self.settings['length'] = self.length_var.get()
        self.settings['uppercase'] = self.uppercase_var.get()
        self.settings['lowercase'] = self.lowercase_var.get()
        self.settings['numbers'] = self.numbers_var.get()
        self.settings['symbols'] = self.symbols_var.get()
        self.settings['exclude_similar'] = self.exclude_similar_var.get()
        self.settings['exclude_ambiguous'] = self.exclude_ambiguous_var.get()
        self.settings['custom_chars'] = self.custom_chars_var.get()
        self.settings['exclude_chars'] = self.exclude_chars_var.get()
        self.settings['quantity'] = self.quantity_var.get()
        self.settings['pronounceable'] = self.pronounceable_var.get()
        self.settings['passphrase'] = self.passphrase_var.get()
        self.settings['theme'] = self.theme_var.get()
        self.settings['copy_on_generate'] = self.copy_on_generate_var.get()
        self.settings['auto_save'] = self.auto_save_var.get()
        self.settings['save_history'] = self.save_history_var.get()
        self.settings['max_history'] = self.max_history_var.get()
        
        # Save to file
        try:
            with open('password_generator_settings.json', 'w') as f:
                json.dump(self.settings, f, indent=2)
            
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def load_settings(self):
        try:
            with open('password_generator_settings.json', 'r') as f:
                loaded_settings = json.load(f)
                self.settings.update(loaded_settings)
        except FileNotFoundError:
            # Use default settings
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
    
    def save_history(self):
        # Save password history
        try:
            with open('password_generator_history.json', 'w') as f:
                json.dump(self.password_history, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save history: {str(e)}")
    
    def load_history(self):
        try:
            with open('password_generator_history.json', 'r') as f:
                self.password_history = json.load(f)
                
                # Limit history size
                if len(self.password_history) > self.settings['max_history']:
                    self.password_history = self.password_history[-self.settings['max_history']:]
        except FileNotFoundError:
            # No history file
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load history: {str(e)}")
    
    def on_window_resize(self, event):
        # Handle window resize events
        if event.widget == self.root:
            # Update strength indicator if visible
            if hasattr(self, 'strength_canvas') and self.strength_canvas.winfo_width() > 1:
                password = self.password_var.get()
                if password:
                    strength = self.calculate_strength(password)
                    self.update_strength_indicator(strength)
    
    def animate_background(self):
        # Simple background animation
        self.root.after(100, self.animate_background)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()