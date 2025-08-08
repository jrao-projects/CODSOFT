import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io

from models.contact import Contact
from ui.styles import COLORS
from utils.validation import ContactValidator

class ContactForm(tk.Frame):
    def __init__(self, parent, contact, save_callback, cancel_callback):
        super().__init__(parent, bg=COLORS['card'])
        self.contact = contact
        self.save_callback = save_callback
        self.cancel_callback = cancel_callback
        self.profile_image = contact.profile_image
        
        # Import FONTS after styles are configured
        from ui.styles import FONTS
        
        # Header
        self.create_header()
        
        # Content
        self.content = tk.Frame(self, bg=COLORS['card'])
        self.content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left column - Profile image
        self.left_col = tk.Frame(self.content, bg=COLORS['card'])
        self.left_col.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Profile image section
        self.create_profile_image_section()
        
        # Right column - Form fields
        self.right_col = tk.Frame(self.content, bg=COLORS['card'])
        self.right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Form fields
        self.create_form_fields()
        
        # Buttons
        self.create_buttons()
    
    def create_header(self):
        from ui.styles import FONTS
        
        header = tk.Frame(self, bg=COLORS['primary'])
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="Add Contact" if not self.contact.id else "Edit Contact",
                        font=FONTS['title'], bg=COLORS['primary'], fg='white')
        title.pack(side=tk.LEFT, padx=20, pady=15)
    
    def create_profile_image_section(self):
        from ui.styles import FONTS
        
        # Profile image frame
        image_frame = tk.Frame(self.left_col, bg=COLORS['card'], width=200, height=200)
        image_frame.pack(pady=10)
        image_frame.pack_propagate(False)
        
        # Profile image
        self.image_label = tk.Label(image_frame, bg=COLORS['border'])
        self.image_label.pack(pady=10)
        
        self.update_profile_image()
        
        # Upload button
        upload_button = tk.Button(self.left_col, text="Upload Image", command=self.upload_image,
                                bg=COLORS['primary'], fg='white', 
                                font=FONTS['normal'], relief=tk.FLAT,
                                padx=15, pady=5)
        upload_button.pack(pady=10)
        
        # Remove button
        remove_button = tk.Button(self.left_col, text="Remove Image", command=self.remove_image,
                                 bg=COLORS['danger'], fg='white', 
                                 font=FONTS['normal'], relief=tk.FLAT,
                                 padx=15, pady=5)
        remove_button.pack(pady=5)
    
    def update_profile_image(self):
        if self.profile_image:
            image = Image.open(io.BytesIO(self.profile_image))
            image = image.resize((180, 180), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference
        else:
            from ui.styles import FONTS
            self.image_label.config(image="", text="No Image", 
                                   bg=COLORS['border'], fg=COLORS['light_text'],
                                   font=FONTS['subtitle'], width=20, height=10)
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Profile Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    self.profile_image = f.read()
                self.update_profile_image()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def remove_image(self):
        self.profile_image = None
        self.update_profile_image()
    
    def create_form_fields(self):
        from ui.styles import FONTS
        
        # Create form fields
        fields = [
            ("Name", "name", self.contact.name, True),
            ("Phone", "phone", self.contact.phone, True),
            ("Email", "email", self.contact.email, False),
            ("Company", "company", self.contact.company, False),
            ("Position", "position", self.contact.position, False),
            ("Address", "address", self.contact.address, False),
            ("Birthday", "birthday", self.contact.birthday, False)
        ]
        
        self.entries = {}
        
        for i, (label_text, field_name, default_value, required) in enumerate(fields):
            # Label with validation indicator
            label_text_display = label_text + (" *" if required else " (optional)")
            label = tk.Label(self.right_col, text=label_text_display,
                           font=FONTS['subtitle'], bg=COLORS['card'], 
                           fg=COLORS['danger'] if required else COLORS['text'], anchor='w')
            label.grid(row=i, column=0, sticky='w', pady=(10, 5), padx=(0, 10))
            
            # Entry with validation styling
            entry = tk.Entry(self.right_col, font=FONTS['normal'], bg=COLORS['card'], 
                           fg=COLORS['text'], relief=tk.SOLID, borderwidth=2,
                           highlightthickness=1, highlightcolor=COLORS['primary'])
            entry.grid(row=i, column=1, sticky='ew', pady=(10, 5))
            entry.insert(0, default_value)
            
            # Add real-time validation
            self.add_real_time_validation(entry, field_name)
            
            self.entries[field_name] = entry
        
        # Notes field with validation
        notes_label = tk.Label(self.right_col, text="Notes (optional):", font=FONTS['subtitle'], 
                              bg=COLORS['card'], fg=COLORS['text'], anchor='w')
        notes_label.grid(row=len(fields), column=0, sticky='nw', pady=(10, 5), padx=(0, 10))
        
        self.notes_text = tk.Text(self.right_col, height=4, font=FONTS['normal'], 
                                 bg=COLORS['card'], fg=COLORS['text'], relief=tk.SOLID, borderwidth=2,
                                 highlightthickness=1, highlightcolor=COLORS['primary'])
        self.notes_text.grid(row=len(fields), column=1, sticky='ew', pady=(10, 5))
        self.notes_text.insert("1.0", self.contact.notes or "")
        
        # Add character counter for notes
        self.notes_counter = tk.Label(self.right_col, text="0/500 characters", 
                                     font=FONTS['small'], bg=COLORS['card'], 
                                     fg=COLORS['light_text'], anchor='e')
        self.notes_counter.grid(row=len(fields)+1, column=1, sticky='e', pady=(0, 5))
        
        # Bind notes validation
        self.notes_text.bind('<KeyRelease>', self.validate_notes_realtime)
        
        # Configure grid weights
        self.right_col.grid_columnconfigure(1, weight=1)
    
    def create_buttons(self):
        from ui.styles import FONTS
        
        button_frame = tk.Frame(self, bg=COLORS['card'])
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Save button
        save_button = tk.Button(button_frame, text="Save", command=self.save_contact,
                              bg=COLORS['primary'], fg='white', 
                              font=FONTS['normal'], relief=tk.FLAT,
                              padx=20, pady=5)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Cancel button
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel_callback,
                                bg=COLORS['light_text'], fg='white', 
                                font=FONTS['normal'], relief=tk.FLAT,
                                padx=20, pady=5)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def add_real_time_validation(self, entry, field_name):
        """Add real-time validation to form fields"""
        def validate_on_change(event=None):
            value = entry.get().strip()
            
            # Get appropriate validator
            validators = {
                'name': ContactValidator.validate_name,
                'phone': ContactValidator.validate_phone,
                'email': ContactValidator.validate_email,
                'company': ContactValidator.validate_company,
                'position': ContactValidator.validate_position,
                'address': ContactValidator.validate_address,
                'birthday': ContactValidator.validate_birthday
            }
            
            if field_name in validators:
                is_valid, error_msg = validators[field_name](value)
                
                # Update entry styling based on validation
                if value and not is_valid:
                    entry.config(highlightcolor=COLORS['danger'], highlightbackground=COLORS['danger'])
                elif value and is_valid:
                    entry.config(highlightcolor=COLORS['success'], highlightbackground=COLORS['success'])
                else:
                    entry.config(highlightcolor=COLORS['primary'], highlightbackground=COLORS['light_bg'])
        
        # Bind validation to key release events
        entry.bind('<KeyRelease>', validate_on_change)
        entry.bind('<FocusOut>', validate_on_change)
    
    def validate_notes_realtime(self, event=None):
        """Real-time validation for notes field with character counter"""
        notes = self.notes_text.get("1.0", tk.END).strip()
        char_count = len(notes)
        
        # Update character counter
        counter_text = f"{char_count}/500 characters"
        if char_count > 500:
            self.notes_counter.config(text=counter_text, fg=COLORS['danger'])
            self.notes_text.config(highlightcolor=COLORS['danger'], highlightbackground=COLORS['danger'])
        elif char_count > 450:
            self.notes_counter.config(text=counter_text, fg=COLORS['warning'])
            self.notes_text.config(highlightcolor=COLORS['warning'], highlightbackground=COLORS['light_bg'])
        else:
            self.notes_counter.config(text=counter_text, fg=COLORS['light_text'])
            self.notes_text.config(highlightcolor=COLORS['primary'], highlightbackground=COLORS['light_bg'])
    
    def save_contact(self):
        # Get values from form
        contact_data = {
            'name': self.entries['name'].get().strip(),
            'phone': self.entries['phone'].get().strip(),
            'email': self.entries['email'].get().strip(),
            'company': self.entries['company'].get().strip(),
            'position': self.entries['position'].get().strip(),
            'address': self.entries['address'].get().strip(),
            'birthday': self.entries['birthday'].get().strip(),
            'notes': self.notes_text.get("1.0", tk.END).strip()
        }
        
        # Comprehensive validation
        is_valid, errors = ContactValidator.validate_all_fields(contact_data)
        
        if not is_valid:
            ContactValidator.show_validation_errors(errors)
            return
        
        # Format data for consistent storage
        formatted_data = {
            'name': ContactValidator.format_name(contact_data['name']),
            'phone': ContactValidator.format_phone(contact_data['phone']),
            'email': ContactValidator.format_email(contact_data['email']),
            'company': contact_data['company'].strip(),
            'position': contact_data['position'].strip(),
            'address': contact_data['address'].strip(),
            'birthday': contact_data['birthday'].strip(),
            'notes': contact_data['notes'].strip()
        }
        
        # Update contact with validated and formatted data
        self.contact.name = formatted_data['name']
        self.contact.phone = formatted_data['phone']
        self.contact.email = formatted_data['email']
        self.contact.company = formatted_data['company']
        self.contact.position = formatted_data['position']
        self.contact.address = formatted_data['address']
        self.contact.birthday = formatted_data['birthday']
        self.contact.notes = formatted_data['notes']
        self.contact.profile_image = self.profile_image
        
        # Show success message with formatted data
        success_msg = f"Contact saved successfully!\n\nName: {formatted_data['name']}\nPhone: {formatted_data['phone']}"
        if formatted_data['email']:
            success_msg += f"\nEmail: {formatted_data['email']}"
        
        messagebox.showinfo("Success", success_msg)
        
        # Call save callback
        self.save_callback(self.contact)