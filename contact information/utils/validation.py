import re
from tkinter import messagebox

class ContactValidator:
    """Comprehensive validation for contact form fields"""
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate phone number: must be exactly 10 digits
        Returns: (is_valid, error_message)
        """
        if not phone:
            return False, "Phone number is required!"
        
        # Remove any spaces, dashes, or parentheses
        clean_phone = re.sub(r'[^\d]', '', phone)
        
        if len(clean_phone) != 10:
            return False, "Phone number must be exactly 10 digits!"
        
        if not clean_phone.isdigit():
            return False, "Phone number must contain only numbers!"
        
        return True, ""
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format (optional field)
        Returns: (is_valid, error_message)
        """
        if not email:  # Email is optional
            return True, ""
        
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return False, "Please enter a valid email address!"
        
        return True, ""
    
    @staticmethod
    def validate_name(name):
        """
        Validate name: required, only letters and spaces, 2-50 characters
        Returns: (is_valid, error_message)
        """
        if not name:
            return False, "Name is required!"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, "Name must be at least 2 characters long!"
        
        if len(name) > 50:
            return False, "Name must be less than 50 characters!"
        
        # Allow letters, spaces, apostrophes, and hyphens
        if not re.match(r"^[a-zA-Z\s'-]+$", name):
            return False, "Name can only contain letters, spaces, apostrophes, and hyphens!"
        
        return True, ""
    
    @staticmethod
    def validate_company(company):
        """
        Validate company name (optional field)
        Returns: (is_valid, error_message)
        """
        if not company:  # Company is optional
            return True, ""
        
        company = company.strip()
        
        if len(company) > 100:
            return False, "Company name must be less than 100 characters!"
        
        return True, ""
    
    @staticmethod
    def validate_position(position):
        """
        Validate position/job title (optional field)
        Returns: (is_valid, error_message)
        """
        if not position:  # Position is optional
            return True, ""
        
        position = position.strip()
        
        if len(position) > 50:
            return False, "Position must be less than 50 characters!"
        
        return True, ""
    
    @staticmethod
    def validate_address(address):
        """
        Validate address (optional field)
        Returns: (is_valid, error_message)
        """
        if not address:  # Address is optional
            return True, ""
        
        address = address.strip()
        
        if len(address) > 200:
            return False, "Address must be less than 200 characters!"
        
        return True, ""
    
    @staticmethod
    def validate_birthday(birthday):
        """
        Validate birthday format (optional field): DD/MM/YYYY or DD-MM-YYYY
        Returns: (is_valid, error_message)
        """
        if not birthday:  # Birthday is optional
            return True, ""
        
        birthday = birthday.strip()
        
        # Accept DD/MM/YYYY or DD-MM-YYYY format
        date_pattern = r'^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$'
        match = re.match(date_pattern, birthday)
        
        if not match:
            return False, "Birthday must be in DD/MM/YYYY or DD-MM-YYYY format!"
        
        day, month, year = map(int, match.groups())
        
        # Basic date validation
        if month < 1 or month > 12:
            return False, "Invalid month in birthday!"
        
        if day < 1 or day > 31:
            return False, "Invalid day in birthday!"
        
        if year < 1900 or year > 2024:
            return False, "Invalid year in birthday!"
        
        # More detailed day validation based on month
        days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if day > days_in_month[month - 1]:
            return False, "Invalid day for the given month!"
        
        return True, ""
    
    @staticmethod
    def validate_notes(notes):
        """
        Validate notes (optional field)
        Returns: (is_valid, error_message)
        """
        if not notes:  # Notes are optional
            return True, ""
        
        notes = notes.strip()
        
        if len(notes) > 500:
            return False, "Notes must be less than 500 characters!"
        
        return True, ""
    
    @staticmethod
    def validate_all_fields(contact_data):
        """
        Validate all contact fields at once
        Returns: (is_valid, error_messages_list)
        """
        errors = []
        
        # Validate each field
        validators = [
            ('name', ContactValidator.validate_name),
            ('phone', ContactValidator.validate_phone),
            ('email', ContactValidator.validate_email),
            ('company', ContactValidator.validate_company),
            ('position', ContactValidator.validate_position),
            ('address', ContactValidator.validate_address),
            ('birthday', ContactValidator.validate_birthday),
            ('notes', ContactValidator.validate_notes)
        ]
        
        for field_name, validator in validators:
            field_value = contact_data.get(field_name, '')
            is_valid, error_msg = validator(field_value)
            
            if not is_valid:
                errors.append(f"{field_name.title()}: {error_msg}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def format_phone(phone):
        """
        Format phone number for consistent storage
        Returns: formatted phone number (10 digits only)
        """
        if not phone:
            return ""
        
        # Remove all non-digit characters
        clean_phone = re.sub(r'[^\d]', '', phone)
        return clean_phone
    
    @staticmethod
    def format_email(email):
        """
        Format email for consistent storage
        Returns: lowercase email
        """
        if not email:
            return ""
        
        return email.strip().lower()
    
    @staticmethod
    def format_name(name):
        """
        Format name for consistent storage
        Returns: properly capitalized name
        """
        if not name:
            return ""
        
        # Capitalize each word properly
        return ' '.join(word.capitalize() for word in name.strip().split())
    
    @staticmethod
    def show_validation_errors(errors):
        """
        Display validation errors to the user
        """
        if errors:
            error_message = "Please fix the following errors:\n\n" + "\n".join(f"• {error}" for error in errors)
            messagebox.showerror("Validation Error", error_message)
            return False
        return True
