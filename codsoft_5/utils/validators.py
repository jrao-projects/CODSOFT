import re

def validate_name(name):
    """Validate contact name"""
    if not name or not name.strip():
        return False, "Name is required"
    
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters"
    
    return True, ""

def validate_phone(phone):
    """Validate phone number"""
    if not phone or not phone.strip():
        return False, "Phone number is required"
    
    # Remove all non-digit characters
    cleaned = re.sub(r'[^\d]', '', phone)
    
    if len(cleaned) < 10:
        return False, "Phone number must be at least 10 digits"
    
    return True, ""

def validate_email(email):
    """Validate email address"""
    if not email:
        return True, ""  # Email is optional
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, ""

def validate_birthday(birthday):
    """Validate birthday date"""
    if not birthday:
        return True, ""  # Birthday is optional
    
    try:
        from datetime import datetime
        datetime.strptime(birthday, '%Y-%m-%d')
        return True, ""
    except ValueError:
        return False, "Invalid date format (use YYYY-MM-DD)"