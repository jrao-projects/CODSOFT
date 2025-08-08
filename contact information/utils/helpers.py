import re
from datetime import datetime

def format_phone_number(phone):
    """Format phone number for display"""
    # Remove all non-digit characters
    cleaned = re.sub(r'[^\d]', '', phone)
    
    # Format based on length
    if len(cleaned) == 10:
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    elif len(cleaned) == 11 and cleaned[0] == '1':
        return f"+1 ({cleaned[1:4]}) {cleaned[4:7]}-{cleaned[7:]}"
    else:
        return phone  # Return original if can't format

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    # Remove all non-digit characters
    cleaned = re.sub(r'[^\d]', '', phone)
    return len(cleaned) >= 10

def format_date(date_string):
    """Format date string for display"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return date_string  # Return original if can't format

def export_contacts_to_csv(contacts, file_path):
    """Export contacts to CSV file"""
    import csv
    
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['name', 'phone', 'email', 'address', 'company', 
                     'position', 'birthday', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact.to_dict())

def import_contacts_from_csv(file_path):
    """Import contacts from CSV file"""
    import csv
    from models.contact import Contact
    
    contacts = []
    
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            contact = Contact(
                name=row.get('name', ''),
                phone=row.get('phone', ''),
                email=row.get('email', ''),
                address=row.get('address', ''),
                company=row.get('company', ''),
                position=row.get('position', ''),
                birthday=row.get('birthday', ''),
                notes=row.get('notes', '')
            )
            contacts.append(contact)
    
    return contacts