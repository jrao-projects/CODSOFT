import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import io
import os

from models.contact import Contact
from models.database import get_all_contacts, search_contacts, delete_contact
from ui.styles import configure_styles, COLORS
from ui.contact_form import ContactForm
from ui.contact_list import ContactList
from ui.search_bar import SearchBar
from ui.homepage import Homepage
from utils.export_import import export_contacts_csv, export_contacts_json, import_contacts_csv, import_contacts_json, backup_contacts

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure styles first
        configure_styles(root)
        
        # Now we can access FONTS from the styles module
        from ui.styles import FONTS
        
        # Create menu bar
        self.create_menu_bar()
        
        # Set background color
        self.root.configure(background=COLORS['background'])
        
        # Create main container
        self.main_container = tk.Frame(root, bg=COLORS['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create header
        self.create_header()
        
        # Create search bar
        self.search_bar = SearchBar(self.main_container, self.search_contacts)
        self.search_bar.pack(fill=tk.X, pady=(0, 20))
        
        # Create content area
        self.content_area = tk.Frame(self.main_container, bg=COLORS['background'])
        self.content_area.pack(fill=tk.BOTH, expand=True)
        
        # Create homepage
        self.homepage = Homepage(self.content_area, self.add_contact, self.show_all_contacts, self.focus_search)
        self.homepage.pack(fill=tk.BOTH, expand=True)
        
        # Create contact list (initially hidden)
        self.contact_list = ContactList(self.content_area, self.view_contact, self.edit_contact, self.delete_contact)
        
        # Create contact detail view (initially hidden)
        self.contact_detail = None
        
        # Current view state
        self.current_view = "homepage"
    
    def create_menu_bar(self):
        """Create modern menu bar with export/import functionality"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        
        # Export submenu
        export_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="📤 Export", menu=export_menu)
        export_menu.add_command(label="Export to CSV", command=self.export_csv)
        export_menu.add_command(label="Export to JSON", command=self.export_json)
        
        # Import submenu
        import_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="📥 Import", menu=import_menu)
        import_menu.add_command(label="Import from CSV", command=self.import_csv)
        import_menu.add_command(label="Import from JSON", command=self.import_json)
        
        file_menu.add_separator()
        file_menu.add_command(label="💾 Backup Contacts", command=self.backup_data)
        
        file_menu.add_separator()
        file_menu.add_command(label="❌ Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️ View", menu=view_menu)
        view_menu.add_command(label="🏠 Homepage", command=self.show_homepage)
        view_menu.add_command(label="👥 All Contacts", command=self.show_all_contacts)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_header(self):
        # Import FONTS here since it's now initialized
        from ui.styles import FONTS
        
        header = tk.Frame(self.main_container, bg=COLORS['primary'], height=60)
        header.pack(fill=tk.X, pady=(0, 20))
        header.pack_propagate(False)
        
        # Title
        title = tk.Label(header, text="📱 Contact Manager", font=FONTS['header'], 
                         bg=COLORS['primary'], fg='white')
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Navigation buttons
        nav_frame = tk.Frame(header, bg=COLORS['primary'])
        nav_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Home button
        home_button = tk.Button(nav_frame, text="🏠 Home", command=self.show_homepage,
                               bg=COLORS['card'], fg=COLORS['primary'], 
                               font=FONTS['normal'], relief=tk.FLAT,
                               padx=10, pady=5, cursor='hand2')
        home_button.pack(side=tk.LEFT, padx=5)
        
        # All Contacts button
        contacts_button = tk.Button(nav_frame, text="👥 Contacts", command=self.show_all_contacts,
                                   bg=COLORS['card'], fg=COLORS['primary'], 
                                   font=FONTS['normal'], relief=tk.FLAT,
                                   padx=10, pady=5, cursor='hand2')
        contacts_button.pack(side=tk.LEFT, padx=5)
        
        # Add contact button
        add_button = tk.Button(nav_frame, text="➕ Add Contact", command=self.add_contact,
                              bg=COLORS['success'], fg='white', 
                              font=FONTS['normal'], relief=tk.FLAT,
                              padx=15, pady=5, cursor='hand2')
        add_button.pack(side=tk.LEFT, padx=5)
    
    def show_homepage(self):
        """Show the homepage/dashboard"""
        # Clear the content area
        for widget in self.content_area.winfo_children():
            widget.pack_forget()
        
        # Show homepage
        self.homepage.refresh_data()
        self.homepage.pack(fill=tk.BOTH, expand=True)
        self.current_view = "homepage"
        
        # Hide search bar on homepage
        self.search_bar.pack_forget()
    
    def show_all_contacts(self):
        """Show all contacts list"""
        # Clear the content area
        for widget in self.content_area.winfo_children():
            widget.pack_forget()
        
        # Show search bar
        self.search_bar.pack_forget()
        self.search_bar.pack(fill=tk.X, pady=(0, 20), before=self.content_area)
        
        # Show contact list
        self.contact_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.current_view = "contacts"
        
        # Load contacts
        self.load_contacts()
    
    def focus_search(self):
        """Focus on search - show contacts and focus search bar"""
        self.show_all_contacts()
        # Focus the search entry
        self.search_bar.search_entry.focus_set()
    
    def load_contacts(self):
        contacts = get_all_contacts()
        self.contact_list.update_contacts(contacts)
    
    def search_contacts(self, query):
        if not query:
            self.load_contacts()
        else:
            contacts = search_contacts(query)
            self.contact_list.update_contacts(contacts)
    
    def add_contact(self):
        self.show_contact_form(Contact())
    
    def view_contact(self, contact):
        self.show_contact_detail(contact)
    
    def edit_contact(self, contact):
        self.show_contact_form(contact)
    
    def delete_contact(self, contact):
        result = messagebox.askyesno("Delete Contact", 
                                    f"Are you sure you want to delete {contact.name}?")
        if result:
            success = delete_contact(contact.id)
            if success:
                self.load_contacts()
                messagebox.showinfo("Success", "Contact deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete contact.")
    
    def show_contact_form(self, contact):
        # Clear the content area
        for widget in self.content_area.winfo_children():
            widget.pack_forget()
        
        # Hide search bar when showing form
        self.search_bar.pack_forget()
        
        # Create contact form
        self.contact_form = ContactForm(self.content_area, contact, self.save_contact, self.cancel_form)
        self.contact_form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Update current view
        self.current_view = "form"
    
    def show_contact_detail(self, contact):
        # Clear the content area
        for widget in self.content_area.winfo_children():
            widget.pack_forget()
        
        # Create contact detail view
        self.create_contact_detail(contact)
    
    def create_contact_detail(self, contact):
        # Import FONTS here since it's now initialized
        from ui.styles import FONTS
        
        # Create detail frame
        detail_frame = tk.Frame(self.content_area, bg=COLORS['card'], relief=tk.RAISED, bd=1)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with back button
        header = tk.Frame(detail_frame, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        back_button = tk.Button(header, text="← Back", command=self.back_to_list,
                               bg=COLORS['primary'], fg='white', 
                               font=FONTS['subtitle'], relief=tk.FLAT,
                               padx=10, pady=10)
        back_button.pack(side=tk.LEFT)
        
        title = tk.Label(header, text="Contact Details", font=FONTS['title'],
                        bg=COLORS['primary'], fg='white')
        title.pack(side=tk.LEFT, padx=20)
        
        # Content
        content = tk.Frame(detail_frame, bg=COLORS['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left column - Profile image and basic info
        left_col = tk.Frame(content, bg=COLORS['card'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Profile image
        image_frame = tk.Frame(left_col, bg=COLORS['card'], width=200, height=200)
        image_frame.pack(pady=10)
        image_frame.pack_propagate(False)
        
        if contact.profile_image:
            image = Image.open(io.BytesIO(contact.profile_image))
            image = image.resize((180, 180), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(image_frame, image=photo, bg=COLORS['card'])
            image_label.image = photo  # Keep a reference
            image_label.pack(pady=10)
        else:
            placeholder = tk.Label(image_frame, text="No Image", 
                                  bg=COLORS['border'], fg=COLORS['light_text'],
                                  font=FONTS['subtitle'], width=20, height=10)
            placeholder.pack(pady=10)
        
        # Basic info
        name_label = tk.Label(left_col, text=contact.name, font=FONTS['title'],
                             bg=COLORS['card'], fg=COLORS['text'])
        name_label.pack(pady=5)
        
        if contact.company:
            company_label = tk.Label(left_col, text=contact.company, font=FONTS['normal'],
                                    bg=COLORS['card'], fg=COLORS['light_text'])
            company_label.pack(pady=2)
        
        if contact.position:
            position_label = tk.Label(left_col, text=contact.position, font=FONTS['normal'],
                                     bg=COLORS['card'], fg=COLORS['light_text'])
            position_label.pack(pady=2)
        
        # Right column - Contact details
        right_col = tk.Frame(content, bg=COLORS['card'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        # Contact details
        details = [
            ("Phone", contact.phone),
            ("Email", contact.email),
            ("Address", contact.address),
            ("Birthday", contact.birthday),
            ("Notes", contact.notes)
        ]
        
        for label, value in details:
            if value:  # Only show if value exists
                detail_label = tk.Label(right_col, text=f"{label}:", font=FONTS['subtitle'],
                                       bg=COLORS['card'], fg=COLORS['text'], anchor='w')
                detail_label.pack(fill=tk.X, pady=(10, 2))
                
                value_label = tk.Label(right_col, text=value, font=FONTS['normal'],
                                      bg=COLORS['card'], fg=COLORS['light_text'], 
                                      anchor='w', wraplength=300, justify=tk.LEFT)
                value_label.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(detail_frame, bg=COLORS['card'])
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        edit_button = tk.Button(button_frame, text="Edit", command=lambda: self.edit_contact(contact),
                               bg=COLORS['primary'], fg='white', 
                               font=FONTS['normal'], relief=tk.FLAT,
                               padx=20, pady=5)
        edit_button.pack(side=tk.RIGHT, padx=5)
        
        delete_button = tk.Button(button_frame, text="Delete", command=lambda: self.delete_contact(contact),
                                 bg=COLORS['danger'], fg='white', 
                                 font=FONTS['normal'], relief=tk.FLAT,
                                 padx=20, pady=5)
        delete_button.pack(side=tk.RIGHT, padx=5)
    
    def save_contact(self, contact):
        from models.database import add_contact, update_contact
        
        if contact.id:
            success = update_contact(contact)
            if success:
                messagebox.showinfo("Success", "Contact updated successfully!")
            else:
                messagebox.showerror("Error", "Failed to update contact.")
        else:
            contact_id = add_contact(contact)
            if contact_id:
                messagebox.showinfo("Success", "Contact added successfully!")
            else:
                messagebox.showerror("Error", "Failed to add contact.")
        
        self.back_to_list()
    
    def cancel_form(self):
        self.back_to_list()
    
    # Menu callback methods
    def export_csv(self):
        """Export contacts to CSV"""
        export_contacts_csv()
        
    def export_json(self):
        """Export contacts to JSON"""
        export_contacts_json()
        
    def import_csv(self):
        """Import contacts from CSV"""
        count = import_contacts_csv()
        if count > 0:
            self.refresh_current_view()
            
    def import_json(self):
        """Import contacts from JSON"""
        count = import_contacts_json()
        if count > 0:
            self.refresh_current_view()
            
    def backup_data(self):
        """Create backup of contacts"""
        backup_contacts()
        
    def show_about(self):
        """Show about dialog"""
        about_text = """📱 Contact Manager v2.0
        
A modern, feature-rich contact management application.
        
Features:
• Beautiful homepage dashboard
• Contact management with photos
• Search and filter contacts
• Export/Import (CSV, JSON)
• Data backup and restore
• Modern, responsive UI
        
Built with Python & Tkinter
© 2024 Contact Manager"""
        
        messagebox.showinfo("About Contact Manager", about_text)
        
    def refresh_current_view(self):
        """Refresh the current view after data changes"""
        if self.current_view == "homepage":
            self.homepage.refresh_data()
        elif self.current_view == "contacts":
            self.load_contacts()
    
    def back_to_list(self):
        """Go back to contacts list or homepage based on previous view"""
        if self.current_view == "homepage":
            self.show_homepage()
        else:
            self.show_all_contacts()