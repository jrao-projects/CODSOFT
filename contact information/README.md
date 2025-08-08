# 📱 Contact Manager v2.0

A modern, feature-rich contact management application built with Python and Tkinter. This application provides a beautiful, intuitive interface for managing your contacts with advanced features like data export/import, backup, and a stunning dashboard.

## ✨ Features

### 🏠 **Homepage Dashboard**
- Beautiful welcome screen with contact statistics
- Quick action buttons for common tasks
- Recent contacts preview
- Modern card-based layout with hover effects

### 👥 **Contact Management**
- Add, edit, delete contacts with ease
- Profile photo support (upload, resize, remove)
- Comprehensive contact fields:
  - Name, Phone (required)
  - Email, Company, Position
  - Address, Birthday, Notes
- Form validation for required fields

### 🔍 **Search & Navigation**
- Real-time contact search
- Search by name, phone, email, or company
- Modern navigation with Home, Contacts, and Add buttons
- Context menus with right-click actions

### 📊 **Data Management**
- **Export Options:**
  - CSV format for spreadsheet compatibility
  - JSON format for data interchange
- **Import Options:**
  - Import from CSV files
  - Import from JSON files
- **Backup & Restore:**
  - Complete backup with profile images
  - Timestamped backup files

### 🎨 **Modern UI Design**
- Beautiful gradient color scheme (purple-blue theme)
- Card-based layout with subtle shadows
- Responsive design that adapts to window size
- Smooth hover effects and modern typography
- Emoji icons for enhanced visual appeal

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Required packages (install via pip):

```bash
pip install pillow
```

### Quick Start
1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
contact information/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── contacts.db            # SQLite database (auto-created)
├── models/
│   ├── __init__.py
│   ├── contact.py         # Contact data model
│   └── database.py        # Database operations
├── ui/
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── homepage.py        # Dashboard/homepage
│   ├── contact_form.py    # Add/edit contact form
│   ├── contact_list.py    # Contact list view
│   ├── search_bar.py      # Search functionality
│   └── styles.py          # UI styling and themes
└── utils/
    ├── __init__.py
    └── export_import.py    # Data export/import utilities
```

## 🎯 How to Use

### Adding a New Contact
1. Click the "➕ Add Contact" button or use the homepage quick action
2. Fill in the required fields (Name and Phone)
3. Optionally add profile photo, email, company details, etc.
4. Click "Save" to add the contact

### Managing Contacts
- **View All:** Click "👥 Contacts" to see your contact list
- **Search:** Use the search bar to find specific contacts
- **Edit:** Double-click a contact or use the context menu
- **Delete:** Right-click and select delete, or use the contact detail view

### Data Export/Import
- **Export:** File menu → Export → Choose CSV or JSON format
- **Import:** File menu → Import → Select your data file
- **Backup:** File menu → Backup Contacts (includes profile images)

### Navigation
- **🏠 Home:** Return to the dashboard
- **👥 Contacts:** View all contacts
- **🔍 Search:** Click to focus on search functionality

## 🛠️ Technical Details

### Database
- SQLite database for reliable data storage
- Automatic database initialization
- Support for binary data (profile images)

### Architecture
- **MVC Pattern:** Clean separation of models, views, and controllers
- **Modular Design:** Each UI component is a separate, reusable class
- **Event-Driven:** Responsive UI with proper event handling

### Key Technologies
- **Python 3.7+:** Core programming language
- **Tkinter:** Native GUI framework
- **SQLite3:** Embedded database
- **Pillow (PIL):** Image processing
- **CSV/JSON:** Data export/import formats

## 🎨 Customization

### Color Scheme
The modern color palette is defined in `ui/styles.py`:
- Primary: #667eea (Modern purple-blue)
- Secondary: #764ba2 (Deep purple)
- Accent: #f093fb (Pink accent)
- Success: #48bb78 (Modern green)
- Warning: #ed8936 (Modern orange)
- Danger: #f56565 (Modern red)

### Fonts
- Header: Helvetica 16pt Bold
- Title: Helvetica 14pt Bold
- Subtitle: Helvetica 12pt Bold
- Normal: Helvetica 10pt
- Small: Helvetica 9pt

## 🔧 Troubleshooting

### Common Issues
1. **Application won't start:**
   - Ensure Python 3.7+ is installed
   - Install required dependencies: `pip install pillow`

2. **Images not displaying:**
   - Check if Pillow is properly installed
   - Ensure image files are in supported formats (JPG, PNG, GIF, BMP)

3. **Database errors:**
   - The database is created automatically
   - If issues persist, delete `contacts.db` and restart the application

### Performance Tips
- Large profile images are automatically resized for optimal performance
- The application handles thousands of contacts efficiently
- Regular backups are recommended for data safety

## 📈 Future Enhancements

Potential features for future versions:
- Cloud synchronization
- Contact groups and categories
- Advanced search filters
- Contact merge functionality
- Integration with email clients
- Mobile app companion

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📞 Support

For support or questions, please open an issue in the project repository.

---

**Enjoy managing your contacts with style! 📱✨**
