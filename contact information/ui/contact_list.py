import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io

from models.contact import Contact
from ui.styles import COLORS

class ContactList(tk.Frame):
    def __init__(self, parent, view_callback, edit_callback, delete_callback):
        super().__init__(parent, bg=COLORS['card'])
        self.view_callback = view_callback
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        
        # Import FONTS after styles are configured
        from ui.styles import FONTS
        
        # Create custom header frame that's always visible
        self.header_frame = tk.Frame(self, bg=COLORS['primary'], height=35)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_frame.pack_propagate(False)
        
        # Create header labels that are always visible
        headers = [
            ('👤 Name', 200, 'name'),
            ('📞 Phone', 150, 'phone'), 
            ('📧 Email', 200, 'email'),
            ('🏢 Company', 150, 'company')
        ]
        
        self.header_labels = {}
        x_pos = 0
        
        for header_text, width, col_name in headers:
            label = tk.Label(self.header_frame, text=header_text, 
                           bg=COLORS['primary'], fg='white',
                           font=FONTS['subtitle'], anchor='w',
                           relief=tk.RAISED, borderwidth=1)
            label.place(x=x_pos, y=0, width=width, height=35)
            
            # Make headers clickable for sorting
            label.bind('<Button-1>', lambda e, col=col_name: self.sort_column(col, False))
            label.bind('<Enter>', lambda e, lbl=label: lbl.config(bg=COLORS['secondary']))
            label.bind('<Leave>', lambda e, lbl=label: lbl.config(bg=COLORS['primary']))
            
            self.header_labels[col_name] = label
            x_pos += width
        
        # Create treeview WITHOUT headers (since we have custom ones above)
        self.tree = ttk.Treeview(self, columns=('name', 'phone', 'email', 'company'), 
                                show='', style='Contact.Treeview')
        
        # Define columns with proper sizing to match headers
        self.tree.column('name', width=200, anchor=tk.W, minwidth=150)
        self.tree.column('phone', width=150, anchor=tk.W, minwidth=120)
        self.tree.column('email', width=200, anchor=tk.W, minwidth=150)
        self.tree.column('company', width=150, anchor=tk.W, minwidth=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # Create context menu
        self.create_context_menu()
    
    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="View", command=self.view_selected)
        self.context_menu.add_command(label="Edit", command=self.edit_selected)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        
        # Bind right-click event
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def show_context_menu(self, event):
        # Select item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def on_double_click(self, event):
        self.view_selected()
    
    def view_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            contact_id = item['values'][4]  # ID is stored as the 5th column
            contact = self.get_contact_by_id(contact_id)
            if contact:
                self.view_callback(contact)
    
    def edit_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            contact_id = item['values'][4]  # ID is stored as the 5th column
            contact = self.get_contact_by_id(contact_id)
            if contact:
                self.edit_callback(contact)
    
    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            contact_id = item['values'][4]  # ID is stored as the 5th column
            contact = self.get_contact_by_id(contact_id)
            if contact:
                self.delete_callback(contact)
    
    def get_contact_by_id(self, contact_id):
        from models.database import get_contact_by_id
        return get_contact_by_id(contact_id)
    
    def update_contacts(self, contacts):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        for contact in contacts:
            # Create a display name with profile image if available
            display_name = contact.name
            if contact.profile_image:
                # Create a small thumbnail
                image = Image.open(io.BytesIO(contact.profile_image))
                image = image.resize((16, 16), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Add to tree with image
                item = self.tree.insert('', tk.END, values=(
                    contact.name, contact.phone, contact.email or "", 
                    contact.company or "", contact.id
                ))
                
                # Store reference to image
                self.tree.set(item, 'name', contact.name)
                self.tree.images = {} if not hasattr(self.tree, 'images') else self.tree.images
                self.tree.images[contact.id] = photo
            else:
                # Add to tree without image
                self.tree.insert('', tk.END, values=(
                    contact.name, contact.phone, contact.email or "", 
                    contact.company or "", contact.id
                ))
    
    def sort_column(self, col, reverse):
        """Sort treeview contents when column header is clicked"""
        # Get all items and their values
        items = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        
        # Sort items
        items.sort(reverse=reverse)
        
        # Rearrange items in sorted positions
        for index, (val, child) in enumerate(items):
            self.tree.move(child, '', index)
        
        # Update custom header labels to show sort direction
        col_text = {
            'name': '👤 Name',
            'phone': '📞 Phone', 
            'email': '📧 Email',
            'company': '🏢 Company'
        }[col]
        
        sort_indicator = ' ▼' if reverse else ' ▲'
        
        # Reset all header labels first
        for column in ['name', 'phone', 'email', 'company']:
            if column != col:
                self.header_labels[column].config(text=col_text.get(column, column))
                # Update click binding for next sort
                self.header_labels[column].bind('<Button-1>', 
                    lambda e, c=column: self.sort_column(c, False))
        
        # Set the sorted column header with indicator
        self.header_labels[col].config(text=col_text + sort_indicator)
        # Update click binding to reverse sort next time
        self.header_labels[col].bind('<Button-1>', 
            lambda e: self.sort_column(col, not reverse))