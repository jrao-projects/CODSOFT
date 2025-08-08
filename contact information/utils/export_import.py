import csv
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from models.database import get_all_contacts, add_contact
from models.contact import Contact

def export_contacts_csv():
    """Export all contacts to CSV file"""
    try:
        # Get all contacts
        contacts = get_all_contacts()
        
        if not contacts:
            messagebox.showwarning("No Data", "No contacts to export!")
            return
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            title="Export Contacts to CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Write to CSV
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'phone', 'email', 'company', 'position', 'address', 'birthday', 'notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for contact in contacts:
                writer.writerow({
                    'name': contact.name,
                    'phone': contact.phone,
                    'email': contact.email or '',
                    'company': contact.company or '',
                    'position': contact.position or '',
                    'address': contact.address or '',
                    'birthday': contact.birthday or '',
                    'notes': contact.notes or ''
                })
        
        messagebox.showinfo("Export Successful", f"Contacts exported to {file_path}")
        
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export contacts: {str(e)}")

def export_contacts_json():
    """Export all contacts to JSON file"""
    try:
        # Get all contacts
        contacts = get_all_contacts()
        
        if not contacts:
            messagebox.showwarning("No Data", "No contacts to export!")
            return
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            title="Export Contacts to JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Convert contacts to JSON-serializable format
        contacts_data = []
        for contact in contacts:
            contact_dict = contact.to_dict()
            # Convert binary image data to None for JSON serialization
            if contact_dict['profile_image']:
                contact_dict['profile_image'] = None  # Skip image data in JSON export
            contacts_data.append(contact_dict)
        
        # Write to JSON
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(contacts_data, jsonfile, indent=2, ensure_ascii=False)
        
        messagebox.showinfo("Export Successful", f"Contacts exported to {file_path}")
        
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export contacts: {str(e)}")

def import_contacts_csv():
    """Import contacts from CSV file"""
    try:
        # Ask user for file location
        file_path = filedialog.askopenfilename(
            title="Import Contacts from CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        imported_count = 0
        
        # Read from CSV
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Create new contact
                contact = Contact(
                    name=row.get('name', '').strip(),
                    phone=row.get('phone', '').strip(),
                    email=row.get('email', '').strip(),
                    company=row.get('company', '').strip(),
                    position=row.get('position', '').strip(),
                    address=row.get('address', '').strip(),
                    birthday=row.get('birthday', '').strip(),
                    notes=row.get('notes', '').strip()
                )
                
                # Validate required fields
                if contact.name and contact.phone:
                    add_contact(contact)
                    imported_count += 1
        
        messagebox.showinfo("Import Successful", f"Imported {imported_count} contacts from {file_path}")
        return imported_count
        
    except Exception as e:
        messagebox.showerror("Import Error", f"Failed to import contacts: {str(e)}")
        return 0

def import_contacts_json():
    """Import contacts from JSON file"""
    try:
        # Ask user for file location
        file_path = filedialog.askopenfilename(
            title="Import Contacts from JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        imported_count = 0
        
        # Read from JSON
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            contacts_data = json.load(jsonfile)
            
            for contact_dict in contacts_data:
                # Create new contact
                contact = Contact(
                    name=contact_dict.get('name', '').strip(),
                    phone=contact_dict.get('phone', '').strip(),
                    email=contact_dict.get('email', '').strip(),
                    company=contact_dict.get('company', '').strip(),
                    position=contact_dict.get('position', '').strip(),
                    address=contact_dict.get('address', '').strip(),
                    birthday=contact_dict.get('birthday', '').strip(),
                    notes=contact_dict.get('notes', '').strip()
                )
                
                # Validate required fields
                if contact.name and contact.phone:
                    add_contact(contact)
                    imported_count += 1
        
        messagebox.showinfo("Import Successful", f"Imported {imported_count} contacts from {file_path}")
        return imported_count
        
    except Exception as e:
        messagebox.showerror("Import Error", f"Failed to import contacts: {str(e)}")
        return 0

def backup_contacts():
    """Create a backup of all contacts"""
    try:
        from datetime import datetime
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"contacts_backup_{timestamp}.json"
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            title="Backup Contacts",
            initialvalue=default_filename,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Export to JSON format
        contacts = get_all_contacts()
        contacts_data = []
        
        for contact in contacts:
            contact_dict = contact.to_dict()
            # Keep image data as base64 for complete backup
            if contact_dict['profile_image']:
                import base64
                contact_dict['profile_image'] = base64.b64encode(contact_dict['profile_image']).decode('utf-8')
            contacts_data.append(contact_dict)
        
        # Write backup file
        backup_data = {
            'backup_date': datetime.now().isoformat(),
            'contact_count': len(contacts_data),
            'contacts': contacts_data
        }
        
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(backup_data, jsonfile, indent=2, ensure_ascii=False)
        
        messagebox.showinfo("Backup Successful", f"Backup created: {file_path}")
        
    except Exception as e:
        messagebox.showerror("Backup Error", f"Failed to create backup: {str(e)}")
