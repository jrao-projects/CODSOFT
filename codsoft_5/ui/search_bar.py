import tkinter as tk
from tkinter import ttk

from ui.styles import COLORS

class SearchBar(tk.Frame):
    def __init__(self, parent, search_callback):
        super().__init__(parent, bg=COLORS['card'])
        self.search_callback = search_callback
        
        # Import FONTS after styles are configured
        from ui.styles import FONTS
        
        # Search icon (using a simple text label)
        search_icon = tk.Label(self, text="🔍", font=FONTS['title'], 
                              bg=COLORS['card'], fg=COLORS['light_text'])
        search_icon.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Search entry
        self.search_entry = tk.Entry(self, font=FONTS['normal'], 
                                    bg=COLORS['card'], fg=COLORS['text'],
                                    relief=tk.SOLID, borderwidth=1)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=10)
        
        # Search button
        search_button = tk.Button(self, text="Search", command=self.search,
                                 bg=COLORS['primary'], fg='white', 
                                 font=FONTS['normal'], relief=tk.FLAT,
                                 padx=15, pady=5)
        search_button.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Clear button
        clear_button = tk.Button(self, text="Clear", command=self.clear,
                               bg=COLORS['light_text'], fg='white', 
                               font=FONTS['normal'], relief=tk.FLAT,
                               padx=15, pady=5)
        clear_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        
        # Bind search on Enter key
        self.search_entry.bind('<Return>', lambda event: self.search())
    
    def search(self):
        query = self.search_entry.get().strip()
        self.search_callback(query)
    
    def clear(self):
        self.search_entry.delete(0, tk.END)
        self.search_callback("")