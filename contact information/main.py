import tkinter as tk
from ui.main_window import MainWindow
from models.database import initialize_database

def main():
    # Initialize the database
    initialize_database()
    
    # Create the main window
    root = tk.Tk()
    app = MainWindow(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()