import sqlite3
import os
from pathlib import Path
from models.contact import Contact

DB_PATH = os.path.join(Path(__file__).parent.parent, 'contacts.db')

def initialize_database():
    """Create the database and tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create contacts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        address TEXT,
        notes TEXT,
        company TEXT,
        position TEXT,
        birthday TEXT,
        profile_image BLOB
    )
    ''')
    
    conn.commit()
    conn.close()

def add_contact(contact):
    """Add a new contact to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO contacts (name, phone, email, address, notes, company, position, birthday, profile_image)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (contact.name, contact.phone, contact.email, contact.address, 
          contact.notes, contact.company, contact.position, contact.birthday, contact.profile_image))
    
    contact_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return contact_id

def get_all_contacts():
    """Retrieve all contacts from the database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contacts ORDER BY name')
    rows = cursor.fetchall()
    
    contacts = []
    for row in rows:
        contact = Contact(
            id=row['id'],
            name=row['name'],
            phone=row['phone'],
            email=row['email'],
            address=row['address'],
            notes=row['notes'],
            company=row['company'],
            position=row['position'],
            birthday=row['birthday'],
            profile_image=row['profile_image']
        )
        contacts.append(contact)
    
    conn.close()
    return contacts

def get_recent_contacts(limit=5):
    """Get the most recently added contacts"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contacts ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    
    contacts = []
    for row in rows:
        contact = Contact(
            id=row['id'],
            name=row['name'],
            phone=row['phone'],
            email=row['email'],
            address=row['address'],
            notes=row['notes'],
            company=row['company'],
            position=row['position'],
            birthday=row['birthday'],
            profile_image=row['profile_image']
        )
        contacts.append(contact)
    
    conn.close()
    return contacts

def get_contact_by_id(contact_id):
    """Retrieve a specific contact by ID"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    row = cursor.fetchone()
    
    if row:
        contact = Contact(
            id=row['id'],
            name=row['name'],
            phone=row['phone'],
            email=row['email'],
            address=row['address'],
            notes=row['notes'],
            company=row['company'],
            position=row['position'],
            birthday=row['birthday'],
            profile_image=row['profile_image']
        )
        conn.close()
        return contact
    
    conn.close()
    return None

def update_contact(contact):
    """Update an existing contact in the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE contacts
    SET name = ?, phone = ?, email = ?, address = ?, notes = ?, 
        company = ?, position = ?, birthday = ?, profile_image = ?
    WHERE id = ?
    ''', (contact.name, contact.phone, contact.email, contact.address, 
          contact.notes, contact.company, contact.position, contact.birthday, 
          contact.profile_image, contact.id))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0

def delete_contact(contact_id):
    """Delete a contact from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0

def search_contacts(query):
    """Search for contacts by name, phone, email, or company"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    search_term = f"%{query}%"
    cursor.execute('''
    SELECT * FROM contacts 
    WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR company LIKE ?
    ORDER BY name
    ''', (search_term, search_term, search_term, search_term))
    
    rows = cursor.fetchall()
    
    contacts = []
    for row in rows:
        contact = Contact(
            id=row['id'],
            name=row['name'],
            phone=row['phone'],
            email=row['email'],
            address=row['address'],
            notes=row['notes'],
            company=row['company'],
            position=row['position'],
            birthday=row['birthday'],
            profile_image=row['profile_image']
        )
        contacts.append(contact)
    
    conn.close()
    return contacts

def get_recent_contacts(limit=5):
    """Get the most recently added contacts"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contacts ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    
    contacts = []
    for row in rows:
        contact = Contact(
            id=row['id'],
            name=row['name'],
            phone=row['phone'],
            email=row['email'],
            address=row['address'],
            notes=row['notes'],
            company=row['company'],
            position=row['position'],
            birthday=row['birthday'],
            profile_image=row['profile_image']
        )
        contacts.append(contact)
    
    conn.close()
    return contacts