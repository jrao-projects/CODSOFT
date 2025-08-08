import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
from datetime import datetime

from models.database import get_all_contacts, get_recent_contacts
from ui.styles import COLORS

class Homepage(tk.Frame):
    def __init__(self, parent, add_contact_callback, view_all_callback, search_callback):
        super().__init__(parent, bg=COLORS['background'])
        self.add_contact_callback = add_contact_callback
        self.view_all_callback = view_all_callback
        self.search_callback = search_callback
        
        # Import FONTS after styles are configured
        from ui.styles import FONTS
        
        # Create main content
        self.create_header()
        self.create_stats_section()
        self.create_quick_actions()
        self.create_recent_contacts()
        
    def create_header(self):
        from ui.styles import FONTS
        
        # Header section
        header_frame = tk.Frame(self, bg=COLORS['background'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Welcome message
        welcome_label = tk.Label(header_frame, text="Welcome to Contact Manager", 
                                font=FONTS['header'], bg=COLORS['background'], 
                                fg=COLORS['primary'])
        welcome_label.pack(pady=10)
        
        # Current date
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        date_label = tk.Label(header_frame, text=current_date, 
                             font=FONTS['normal'], bg=COLORS['background'], 
                             fg=COLORS['light_text'])
        date_label.pack()
        
    def create_stats_section(self):
        from ui.styles import FONTS
        
        # Stats section
        stats_frame = tk.Frame(self, bg=COLORS['background'])
        stats_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Stats title
        stats_title = tk.Label(stats_frame, text="Your Contacts at a Glance", 
                              font=FONTS['subtitle'], bg=COLORS['background'], 
                              fg=COLORS['text'])
        stats_title.pack(pady=(0, 15))
        
        # Stats cards container
        cards_container = tk.Frame(stats_frame, bg=COLORS['background'])
        cards_container.pack()
        
        # Get contact statistics
        contacts = get_all_contacts()
        total_contacts = len(contacts)
        contacts_with_email = len([c for c in contacts if c.email])
        contacts_with_company = len([c for c in contacts if c.company])
        contacts_with_photo = len([c for c in contacts if c.profile_image])
        
        # Create stat cards
        stats = [
            ("Total Contacts", total_contacts, COLORS['primary']),
            ("With Email", contacts_with_email, COLORS['success']),
            ("With Company", contacts_with_company, COLORS['warning']),
            ("With Photo", contacts_with_photo, COLORS['accent'])
        ]
        
        for i, (label, value, color) in enumerate(stats):
            self.create_stat_card(cards_container, label, value, color, i)
    
    def create_stat_card(self, parent, label, value, color, index):
        from ui.styles import FONTS
        
        # Card frame
        card = tk.Frame(parent, bg=COLORS['card'], relief=tk.RAISED, bd=1)
        card.pack(side=tk.LEFT, padx=10, pady=5, ipadx=20, ipady=15)
        
        # Value
        value_label = tk.Label(card, text=str(value), font=FONTS['header'], 
                              bg=COLORS['card'], fg=color)
        value_label.pack()
        
        # Label
        label_label = tk.Label(card, text=label, font=FONTS['normal'], 
                              bg=COLORS['card'], fg=COLORS['text'])
        label_label.pack()
    
    def create_quick_actions(self):
        from ui.styles import FONTS
        
        # Quick actions section
        actions_frame = tk.Frame(self, bg=COLORS['background'])
        actions_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Actions title
        actions_title = tk.Label(actions_frame, text="Quick Actions", 
                                font=FONTS['subtitle'], bg=COLORS['background'], 
                                fg=COLORS['text'])
        actions_title.pack(pady=(0, 15))
        
        # Actions container
        actions_container = tk.Frame(actions_frame, bg=COLORS['background'])
        actions_container.pack()
        
        # Action buttons
        actions = [
            ("➕ Add New Contact", self.add_contact_callback, COLORS['primary']),
            ("👥 View All Contacts", self.view_all_callback, COLORS['secondary']),
            ("🔍 Search Contacts", lambda: self.search_callback(""), COLORS['success']),
        ]
        
        for text, command, color in actions:
            btn = tk.Button(actions_container, text=text, command=command,
                           bg=color, fg='white', font=FONTS['subtitle'],
                           relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=10)
            
            # Add hover effects
            def on_enter(e, button=btn, hover_color=self.darken_color(color)):
                button.config(bg=hover_color)
            
            def on_leave(e, button=btn, original_color=color):
                button.config(bg=original_color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def create_recent_contacts(self):
        from ui.styles import FONTS
        
        # Recent contacts section
        recent_frame = tk.Frame(self, bg=COLORS['background'])
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Recent title
        recent_title = tk.Label(recent_frame, text="Recent Contacts", 
                               font=FONTS['subtitle'], bg=COLORS['background'], 
                               fg=COLORS['text'])
        recent_title.pack(pady=(0, 15))
        
        # Recent contacts container
        contacts_container = tk.Frame(recent_frame, bg=COLORS['card'], relief=tk.RAISED, bd=1)
        contacts_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Get recent contacts (last 5)
        contacts = get_all_contacts()[:5]  # Get first 5 contacts as "recent"
        
        if contacts:
            for i, contact in enumerate(contacts):
                self.create_contact_preview(contacts_container, contact, i)
        else:
            # No contacts message
            no_contacts_label = tk.Label(contacts_container, 
                                        text="No contacts yet. Add your first contact!", 
                                        font=FONTS['normal'], bg=COLORS['card'], 
                                        fg=COLORS['light_text'])
            no_contacts_label.pack(pady=50)
    
    def create_contact_preview(self, parent, contact, index):
        from ui.styles import FONTS
        
        # Contact preview frame
        preview_frame = tk.Frame(parent, bg=COLORS['card'])
        preview_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Profile image or placeholder
        image_frame = tk.Frame(preview_frame, bg=COLORS['card'])
        image_frame.pack(side=tk.LEFT, padx=(0, 15))
        
        if contact.profile_image:
            try:
                image = Image.open(io.BytesIO(contact.profile_image))
                image = image.resize((40, 40), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(image_frame, image=photo, bg=COLORS['card'])
                image_label.image = photo  # Keep reference
                image_label.pack()
            except:
                # Fallback to placeholder
                placeholder = tk.Label(image_frame, text="👤", font=FONTS['title'], 
                                     bg=COLORS['border'], fg=COLORS['light_text'],
                                     width=3, height=2)
                placeholder.pack()
        else:
            placeholder = tk.Label(image_frame, text="👤", font=FONTS['title'], 
                                 bg=COLORS['border'], fg=COLORS['light_text'],
                                 width=3, height=2)
            placeholder.pack()
        
        # Contact info
        info_frame = tk.Frame(preview_frame, bg=COLORS['card'])
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Name
        name_label = tk.Label(info_frame, text=contact.name, font=FONTS['subtitle'], 
                             bg=COLORS['card'], fg=COLORS['text'], anchor='w')
        name_label.pack(fill=tk.X)
        
        # Phone
        phone_label = tk.Label(info_frame, text=contact.phone, font=FONTS['small'], 
                              bg=COLORS['card'], fg=COLORS['light_text'], anchor='w')
        phone_label.pack(fill=tk.X)
        
        # Company (if available)
        if contact.company:
            company_label = tk.Label(info_frame, text=contact.company, font=FONTS['small'], 
                                   bg=COLORS['card'], fg=COLORS['light_text'], anchor='w')
            company_label.pack(fill=tk.X)
    
    def darken_color(self, color):
        """Darken a hex color for hover effects"""
        if color.startswith('#'):
            color = color[1:]
        
        # Convert to RGB
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Darken by 20%
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def refresh_data(self):
        """Refresh the homepage data"""
        # Clear and recreate sections
        for widget in self.winfo_children():
            widget.destroy()
        
        self.create_header()
        self.create_stats_section()
        self.create_quick_actions()
        self.create_recent_contacts()
