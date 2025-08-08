import tkinter as tk
from tkinter import ttk, messagebox, font
import random
import os
import time
import json
from datetime import datetime
from collections import defaultdict
import threading
import math
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFilter
except ImportError:
    Image = None
    ImageTk = None
    ImageDraw = None
    ImageFilter = None

# Game variables
user_score = 0
computer_score = 0
ties = 0
total_games = 0
game_history = []
streak = 0
max_streak = 0
difficulty = 'normal'
round_limit = 0
current_round = 0
tournament_mode = False
achievements = set()
player_name = "Player"
player_avatar = "default"
settings = {
    'animations': True,
    'sound_effects': True,
    'auto_continue': False,
    'theme': 'dark',
    'particles': True,
    'confetti': True
}

# Achievement definitions
ACHIEVEMENTS = {
    'first_win': {'name': '🏆 First Victory', 'desc': 'Win your first game', 'icon': '🏆'},
    'streak_5': {'name': '🔥 Hot Streak', 'desc': 'Win 5 games in a row', 'icon': '🔥'},
    'streak_10': {'name': '⚡ Lightning Strike', 'desc': 'Win 10 games in a row', 'icon': '⚡'},
    'century': {'name': '💯 Century Club', 'desc': 'Play 100 games', 'icon': '💯'},
    'perfectionist': {'name': '✨ Perfectionist', 'desc': 'Win 10 games without losing', 'icon': '✨'},
    'rock_master': {'name': '🪨 Rock Master', 'desc': 'Win 20 games with rock', 'icon': '🪨'},
    'paper_master': {'name': '📄 Paper Master', 'desc': 'Win 20 games with paper', 'icon': '📄'},
    'scissors_master': {'name': '✂️ Scissors Master', 'desc': 'Win 20 games with scissors', 'icon': '✂️'},
    'tournament_winner': {'name': '👑 Tournament Champion', 'desc': 'Win a tournament', 'icon': '👑'},
    'speed_demon': {'name': '💨 Speed Demon', 'desc': 'Make a choice in under 2 seconds', 'icon': '💨'},
    'lucky_seven': {'name': '🍀 Lucky Seven', 'desc': 'Win 7 games with 7 choices', 'icon': '🍀'},
    'comeback': {'name': '🔄 Comeback King', 'desc': 'Win after losing 3 in a row', 'icon': '🔄'}
}

# Avatar options
AVATARS = {
    'default': {'name': 'Default', 'color': '#3498db'},
    'warrior': {'name': 'Warrior', 'color': '#e74c3c'},
    'ninja': {'name': 'Ninja', 'color': '#2ecc71'},
    'wizard': {'name': 'Wizard', 'color': '#9b59b6'},
    'robot': {'name': 'Robot', 'color': '#34495e'},
    'alien': {'name': 'Alien', 'color': '#1abc9c'}
}

# Statistics tracking
stats = defaultdict(int)
choice_stats = {'rock': 0, 'paper': 0, 'scissors': 0}
win_by_choice = {'rock': 0, 'paper': 0, 'scissors': 0}
response_times = []

# Game ASCII Art
ROCK_ART = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

PAPER_ART = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

SCISSORS_ART = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Championship")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)  # Make window resizable
        self.root.minsize(800, 600)  # Set minimum size
        
        # Set icon (if available)
        try:
            self.root.iconbitmap("rps_icon.ico")
        except:
            pass
        
        # Create particles canvas first (so it's in the background)
        self.particles_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.particles_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles based on theme
        self.configure_theme()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create title
        self.create_title()
        
        # Create main menu
        self.create_main_menu()
        
        # Load game data
        self.load_game_data()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start with main menu
        self.show_main_menu()
        
        # Start animation loop
        self.animate_particles()
        
        # Bind window resize event
        self.root.bind("<Configure>", self.on_window_resize)
    
    def on_window_resize(self, event):
        """Handle window resize events"""
        # Update particles canvas size
        self.particles_canvas.config(width=event.width, height=event.height)
        
        # Update any other elements that need resizing
        self.root.update_idletasks()
    
    def configure_theme(self):
        theme = settings['theme']
        
        if theme == 'dark':
            bg_color = "#1a1a2e"
            secondary_bg = "#16213e"
            accent = "#0f3460"
            text_color = "#ecf0f1"
            accent_text = "#e94560"
            success = "#2ecc71"
            warning = "#f39c12"
            danger = "#e74c3c"
            button_bg = "#3498db"
            button_hover = "#2980b9"
        elif theme == 'light':
            bg_color = "#f5f5f5"
            secondary_bg = "#e0e0e0"
            accent = "#3498db"
            text_color = "#2c3e50"
            accent_text = "#e74c3c"
            success = "#27ae60"
            warning = "#f1c40f"
            danger = "#e74c3c"
            button_bg = "#3498db"
            button_hover = "#2980b9"
        else:  # custom - more vibrant colors
            bg_color = "#2c3e50"
            secondary_bg = "#34495e"
            accent = "#9b59b6"  # Purple instead of blue
            text_color = "#ecf0f1"
            accent_text = "#e74c3c"
            success = "#2ecc71"
            warning = "#f1c40f"
            danger = "#e74c3c"
            button_bg = "#e74c3c"  # Red buttons for more impact
            button_hover = "#c0392b"
        
        # Configure root
        self.root.configure(bg=bg_color)
        
        # Configure styles
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TButton', 
                            font=('Arial', 12, 'bold'), 
                            background=button_bg, 
                            foreground='white',
                            borderwidth=0,
                            focuscolor='none',
                            padding=10)
        self.style.map('TButton', 
                      background=[('active', button_hover)],
                      foreground=[('active', 'white')])
        self.style.configure('TLabel', 
                            background=bg_color, 
                            foreground=text_color, 
                            font=('Arial', 12))
        self.style.configure('Title.TLabel', 
                            font=('Arial', 24, 'bold'), 
                            foreground=accent_text)
        self.style.configure('Header.TLabel', 
                            font=('Arial', 16, 'bold'), 
                            foreground=accent_text)
        self.style.configure('Stats.TLabel', 
                            font=('Arial', 11), 
                            foreground=text_color)
        self.style.configure('Game.TLabel', 
                            font=('Courier', 10), 
                            foreground=text_color)
        self.style.configure('Card.TFrame', 
                            background=secondary_bg, 
                            relief=tk.RAISED, 
                            borderwidth=2)
        
        # Store colors for later use
        self.colors = {
            'bg': bg_color,
            'secondary_bg': secondary_bg,
            'accent': accent,
            'text': text_color,
            'accent_text': accent_text,
            'success': success,
            'warning': warning,
            'danger': danger,
            'button_bg': button_bg,
            'button_hover': button_hover
        }
    
    def create_title(self):
        title_frame = ttk.Frame(self.main_container)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create a more vibrant title with gradient effect
        title_text = "🎮 ROCK PAPER SCISSORS CHAMPIONSHIP 🎮"
        title_label = ttk.Label(title_frame, text=title_text, style='Title.TLabel')
        title_label.pack(pady=10)
        
        subtitle_text = "The Ultimate Strategy Game"
        subtitle_label = ttk.Label(title_frame, text=subtitle_text, style='Stats.TLabel')
        subtitle_label.pack()
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_main_menu(self):
        self.main_menu_frame = ttk.Frame(self.main_container)
        
        # Player info card
        info_card = ttk.Frame(self.main_menu_frame, style='Card.TFrame')
        info_card.pack(fill=tk.X, pady=(0, 20), padx=10, ipady=10)
        
        # Player avatar
        avatar_frame = ttk.Frame(info_card)
        avatar_frame.pack(side=tk.LEFT, padx=20)
        
        self.avatar_canvas = tk.Canvas(avatar_frame, width=80, height=80, highlightthickness=0)
        self.avatar_canvas.pack()
        self.draw_avatar(self.avatar_canvas, player_avatar)
        
        # Player info
        info_text_frame = ttk.Frame(info_card)
        info_text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        win_rate = (user_score / total_games * 100) if total_games > 0 else 0
        info_text = f"Player: {player_name} | Wins: {user_score} | Win Rate: {win_rate:.1f}% | Streak: {streak}"
        info_label = ttk.Label(info_text_frame, text=info_text, style='Stats.TLabel')
        info_label.pack(anchor=tk.W)
        
        level_text = f"Level: {self.calculate_level()} | XP: {self.calculate_xp()}/{self.calculate_xp_to_next_level()}"
        level_label = ttk.Label(info_text_frame, text=level_text, style='Stats.TLabel')
        level_label.pack(anchor=tk.W)
        
        # Menu buttons
        buttons_frame = ttk.Frame(self.main_menu_frame)
        buttons_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Create a grid of buttons
        buttons = [
            ("🎮 Quick Play", self.quick_play),
            ("🏆 Tournament Mode", self.tournament_setup),
            ("⚙️ Game Settings", self.show_settings),
            ("👤 Player Profile", self.show_profile),
            ("📊 Statistics & Achievements", self.show_statistics),
            ("📜 Game History", self.show_history),
            ("📖 Rules & Help", self.show_rules),
            ("🔄 Reset Progress", self.reset_progress),
            ("👋 Exit Game", self.on_closing)
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = ttk.Button(buttons_frame, text=text, command=command)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Configure grid weights
            buttons_frame.grid_columnconfigure(col, weight=1)
            buttons_frame.grid_rowconfigure(row, weight=1)
        
        # Recent achievements
        if achievements:
            ach_frame = ttk.Frame(self.main_menu_frame, style='Card.TFrame')
            ach_frame.pack(fill=tk.X, pady=(20, 0), padx=10, ipady=10)
            
            ach_label = ttk.Label(ach_frame, text="🏆 Recent Achievements:", style='Header.TLabel')
            ach_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
            
            recent_achievements = list(achievements)[-3:]
            ach_container = ttk.Frame(ach_frame)
            ach_container.pack(fill=tk.X, padx=10, pady=5)
            
            for ach in recent_achievements:
                ach_item = ttk.Frame(ach_container, style='Card.TFrame')
                ach_item.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
                
                ach_icon = ttk.Label(ach_item, text=ACHIEVEMENTS[ach]['icon'], font=('Arial', 20))
                ach_icon.pack(pady=5)
                
                ach_name = ttk.Label(ach_item, text=ACHIEVEMENTS[ach]['name'], style='Stats.TLabel')
                ach_name.pack()
    
    def calculate_level(self):
        """Calculate player level based on total games and achievements"""
        base_xp = total_games * 10
        achievement_xp = len(achievements) * 50
        total_xp = base_xp + achievement_xp
        
        # Level formula: level = 1 + floor(sqrt(total_xp / 100))
        return 1 + int(math.sqrt(total_xp / 100))
    
    def calculate_xp(self):
        """Calculate current XP"""
        base_xp = total_games * 10
        achievement_xp = len(achievements) * 50
        return base_xp + achievement_xp
    
    def calculate_xp_to_next_level(self):
        """Calculate XP needed for next level"""
        current_level = self.calculate_level()
        next_level_xp = (current_level ** 2) * 100
        return next_level_xp
    
    def draw_avatar(self, canvas, avatar_type):
        """Draw player avatar on canvas"""
        canvas.delete("all")
        
        # Get avatar color
        avatar_color = AVATARS[avatar_type]['color']
        
        # Draw avatar background
        canvas.create_oval(10, 10, 70, 70, fill=avatar_color, outline="")
        
        # Draw avatar based on type
        if avatar_type == 'default':
            # Simple smiley face
            canvas.create_oval(25, 25, 35, 35, fill=self.colors['bg'], outline="")
            canvas.create_oval(45, 25, 55, 35, fill=self.colors['bg'], outline="")
            canvas.create_arc(25, 35, 55, 55, start=0, extent=180, style=tk.ARC, 
                            outline=self.colors['bg'], width=3)
        elif avatar_type == 'warrior':
            # Helmet
            canvas.create_rectangle(20, 20, 60, 40, fill=self.colors['bg'], outline="")
            canvas.create_polygon(20, 20, 40, 10, 60, 20, fill=self.colors['bg'], outline="")
            # Eyes
            canvas.create_oval(25, 25, 35, 35, fill=self.colors['bg'], outline="")
            canvas.create_oval(45, 25, 55, 35, fill=self.colors['bg'], outline="")
        elif avatar_type == 'ninja':
            # Headband
            canvas.create_rectangle(15, 30, 65, 35, fill=self.colors['bg'], outline="")
            # Eyes
            canvas.create_oval(25, 35, 35, 45, fill=self.colors['bg'], outline="")
            canvas.create_oval(45, 35, 55, 45, fill=self.colors['bg'], outline="")
        elif avatar_type == 'wizard':
            # Hat
            canvas.create_polygon(30, 15, 50, 5, 70, 15, 60, 30, 40, 30, fill=self.colors['bg'], outline="")
            # Eyes
            canvas.create_oval(25, 35, 35, 45, fill=self.colors['bg'], outline="")
            canvas.create_oval(45, 35, 55, 45, fill=self.colors['bg'], outline="")
            # Beard
            canvas.create_rectangle(30, 50, 50, 65, fill=self.colors['bg'], outline="")
        elif avatar_type == 'robot':
            # Antenna
            canvas.create_line(40, 10, 40, 20, fill=self.colors['bg'], width=3)
            canvas.create_oval(35, 5, 45, 15, fill=self.colors['bg'], outline="")
            # Eyes
            canvas.create_rectangle(25, 30, 35, 40, fill=self.colors['bg'], outline="")
            canvas.create_rectangle(45, 30, 55, 40, fill=self.colors['bg'], outline="")
            # Mouth
            canvas.create_rectangle(30, 50, 50, 55, fill=self.colors['bg'], outline="")
        elif avatar_type == 'alien':
            # Big head
            canvas.create_oval(15, 15, 65, 65, fill=avatar_color, outline="")
            # Eyes
            canvas.create_oval(20, 25, 35, 40, fill=self.colors['bg'], outline="")
            canvas.create_oval(45, 25, 60, 40, fill=self.colors['bg'], outline="")
            # Antennas
            canvas.create_line(30, 15, 25, 5, fill=self.colors['bg'], width=2)
            canvas.create_line(50, 15, 55, 5, fill=self.colors['bg'], width=2)
            canvas.create_oval(22, 3, 28, 8, fill=self.colors['bg'], outline="")
            canvas.create_oval(52, 3, 58, 8, fill=self.colors['bg'], outline="")
    
    def show_main_menu(self):
        self.hide_all_frames()
        self.main_menu_frame.pack(fill=tk.BOTH, expand=True)
    
    def hide_all_frames(self):
        for frame in self.main_container.winfo_children():
            if frame != self.main_container.winfo_children()[0]:  # Keep title frame
                frame.pack_forget()
    
    def quick_play(self):
        global tournament_mode
        tournament_mode = False
        self.show_game_screen()
    
    def tournament_setup(self):
        self.hide_all_frames()
        
        tournament_frame = ttk.Frame(self.main_container)
        tournament_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(tournament_frame, text="🏆 TOURNAMENT SETUP", style='Header.TLabel')
        title_label.pack(pady=(0, 20))
        
        info_label = ttk.Label(tournament_frame, 
                              text="Tournament Mode: Play a series of rounds with special scoring!", 
                              style='Stats.TLabel')
        info_label.pack(pady=(0, 20))
        
        # Tournament options with cards
        options_frame = ttk.Frame(tournament_frame)
        options_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        tournaments = [
            ("Quick Tournament", "5 rounds", 5),
            ("Standard Tournament", "10 rounds", 10),
            ("Championship", "20 rounds", 20),
            ("Marathon", "50 rounds", 50),
            ("Endurance", "100 rounds", 100)
        ]
        
        for i, (name, desc, rounds) in enumerate(tournaments):
            card = ttk.Frame(options_frame, style='Card.TFrame')
            card.pack(fill=tk.BOTH, expand=True, pady=10)
            
            card_content = ttk.Frame(card)
            card_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            name_label = ttk.Label(card_content, text=name, style='Header.TLabel')
            name_label.pack(anchor=tk.W)
            
            desc_label = ttk.Label(card_content, text=desc, style='Stats.TLabel')
            desc_label.pack(anchor=tk.W)
            
            btn = ttk.Button(card_content, text="Select", 
                           command=lambda r=rounds: self.start_tournament(r))
            btn.pack(anchor=tk.E, pady=(10, 0))
        
        # Custom tournament button
        custom_btn = ttk.Button(options_frame, text="Custom Tournament", 
                              command=self.custom_tournament)
        custom_btn.pack(pady=10)
        
        # Back button
        back_btn = ttk.Button(tournament_frame, text="Back to Main Menu", 
                            command=self.show_main_menu)
        back_btn.pack(pady=10)
    
    def start_tournament(self, rounds):
        global tournament_mode, round_limit, current_round, user_score, computer_score, ties
        
        tournament_mode = True
        round_limit = rounds
        current_round = 0
        
        # Reset scores for tournament
        user_score = 0
        computer_score = 0
        ties = 0
        
        self.show_game_screen()
    
    def custom_tournament(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Tournament")
        dialog.geometry("350x200")
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        ttk.Label(dialog, text="Enter number of rounds (1-100):", 
                 style='Stats.TLabel').pack(pady=10)
        
        rounds_entry = ttk.Entry(dialog, font=('Arial', 12))
        rounds_entry.pack(pady=5, padx=20, fill=tk.X)
        rounds_entry.focus()
        
        def set_custom():
            try:
                rounds = int(rounds_entry.get())
                if 1 <= rounds <= 100:
                    dialog.destroy()
                    self.start_tournament(rounds)
                else:
                    messagebox.showerror("Invalid Input", "Please enter a number between 1 and 100")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Start", command=set_custom).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_game_screen(self):
        self.hide_all_frames()
        
        game_frame = ttk.Frame(self.main_container)
        game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tournament mode display
        if tournament_mode:
            remaining = round_limit - current_round
            header_text = f"🏆 TOURNAMENT MODE - Round {current_round + 1}/{round_limit} | Remaining: {remaining}"
        else:
            header_text = f"🎮 QUICK PLAY MODE - Difficulty: {difficulty.title()}"
        
        header_label = ttk.Label(game_frame, text=header_text, style='Header.TLabel')
        header_label.pack(pady=(0, 10))
        
        # Score display with progress bar
        score_frame = ttk.Frame(game_frame)
        score_frame.pack(fill=tk.X, pady=(0, 20))
        
        score_text = f"You: {user_score} | Computer: {computer_score} | Streak: {streak}"
        score_label = ttk.Label(score_frame, text=score_text, style='Stats.TLabel')
        score_label.pack()
        
        # Progress bar for tournament
        if tournament_mode:
            progress_frame = ttk.Frame(score_frame)
            progress_frame.pack(fill=tk.X, pady=5)
            
            progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
            progress.pack(fill=tk.X)
            progress['value'] = (current_round / round_limit) * 100
            
            progress_label = ttk.Label(progress_frame, text=f"{current_round}/{round_limit} rounds completed", 
                                     style='Stats.TLabel')
            progress_label.pack()
        
        # Choice buttons with animations
        choices_frame = ttk.Frame(game_frame)
        choices_frame.pack(pady=20)
        
        # Create animated buttons
        self.choice_buttons = {}
        choices = ['rock', 'paper', 'scissors']
        emojis = ['🪨', '📄', '✂️']
        
        for i, (choice, emoji) in enumerate(zip(choices, emojis)):
            btn_frame = ttk.Frame(choices_frame)
            btn_frame.pack(side=tk.LEFT, padx=20)
            
            # Create canvas for animation
            canvas = tk.Canvas(btn_frame, width=120, height=120, highlightthickness=0, 
                             bg=self.colors['secondary_bg'])
            canvas.pack()
            
            # Draw choice on canvas
            self.draw_choice_on_canvas(canvas, choice)
            
            # Create button
            btn = ttk.Button(btn_frame, text=f"{emoji} {choice.title()}", 
                           command=lambda c=choice: self.make_choice(c))
            btn.pack(pady=10)
            
            self.choice_buttons[choice] = {'canvas': canvas, 'button': btn}
        
        # Back button
        back_btn = ttk.Button(game_frame, text="🚪 Back to Menu", 
                            command=self.show_main_menu)
        back_btn.pack(pady=20)
        
        # Result display area
        self.result_frame = ttk.Frame(game_frame)
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Placeholder for result
        self.result_label = ttk.Label(self.result_frame, text="Make your choice!", style='Game.TLabel')
        self.result_label.pack()
    
    def draw_choice_on_canvas(self, canvas, choice):
        """Draw choice on canvas with animation"""
        canvas.delete("all")
        
        # Draw background circle
        canvas.create_oval(10, 10, 110, 110, fill=self.colors['accent'], outline="")
        
        # Draw choice
        if choice == 'rock':
            # Draw rock
            canvas.create_polygon(60, 30, 90, 60, 60, 90, 30, 60, fill=self.colors['bg'], outline="")
        elif choice == 'paper':
            # Draw paper
            canvas.create_rectangle(30, 30, 90, 90, fill=self.colors['bg'], outline="")
        elif choice == 'scissors':
            # Draw scissors
            canvas.create_line(40, 40, 80, 80, fill=self.colors['bg'], width=5)
            canvas.create_line(40, 80, 80, 40, fill=self.colors['bg'], width=5)
    
    def animate_choice(self, choice):
        """Animate the choice button"""
        if not settings['animations']:
            return
            
        canvas = self.choice_buttons[choice]['canvas']
        
        # Scale animation
        for scale in [1.1, 1.2, 1.1, 1.0]:
            canvas.delete("all")
            
            # Draw background circle
            size = 50 * scale
            canvas.create_oval(60-size, 60-size, 60+size, 60+size, 
                             fill=self.colors['accent'], outline="")
            
            # Draw choice
            if choice == 'rock':
                # Draw rock
                canvas.create_polygon(60, 60-size*0.7, 60+size*0.7, 60, 60, 60+size*0.7, 
                                    60-size*0.7, 60, fill=self.colors['bg'], outline="")
            elif choice == 'paper':
                # Draw paper
                canvas.create_rectangle(60-size*0.7, 60-size*0.7, 60+size*0.7, 60+size*0.7, 
                                      fill=self.colors['bg'], outline="")
            elif choice == 'scissors':
                # Draw scissors
                canvas.create_line(60-size*0.7, 60-size*0.7, 60+size*0.7, 60+size*0.7, 
                                 fill=self.colors['bg'], width=5)
                canvas.create_line(60-size*0.7, 60+size*0.7, 60+size*0.7, 60-size*0.7, 
                                 fill=self.colors['bg'], width=5)
            
            self.root.update()
            time.sleep(0.05)  # Reduced time for faster animation
    
    def make_choice(self, user_choice):
        global user_score, computer_score, ties, total_games, streak, max_streak, current_round
        
        # Record start time for speed demon achievement
        start_time = time.time()
        
        # Animate choice
        self.animate_choice(user_choice)
        
        # Update choice statistics
        choice_stats[user_choice] += 1
        
        # Computer makes a choice based on difficulty
        computer_choice = self.get_computer_choice()
        
        # Determine the winner
        result = self.determine_winner(user_choice, computer_choice)
        
        # Update scores
        if result == 'Win':
            user_score += 1
            streak += 1
            if streak > max_streak:
                max_streak = streak
            win_by_choice[user_choice] += 1
        elif result == 'Loss':
            computer_score += 1
            streak = 0
        else:  # Tie
            ties += 1
        
        total_games += 1
        
        # Add to game history
        game_history.append({
            'user_choice': user_choice,
            'computer_choice': computer_choice,
            'result': result,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Update tournament scores
        if tournament_mode:
            current_round += 1
        
        # Record response time
        response_time = time.time() - start_time
        response_times.append(response_time)
        
        # Check for achievements
        self.check_achievements()
        
        # Save game data
        self.save_game_data()
        
        # Display the result
        self.display_result(user_choice, computer_choice, result)
        
        # Check if tournament is over
        if tournament_mode and current_round >= round_limit:
            self.root.after(2000, self.show_tournament_results)
        elif settings['auto_continue']:
            self.root.after(2000, self.show_game_screen)
    
    def get_computer_choice(self):
        global difficulty
        
        if difficulty == 'easy':
            # Easy mode: Computer makes more predictable choices
            choices = ['rock', 'paper', 'scissors']
            weights = [0.4, 0.3, 0.3]  # Slightly favor rock
            return random.choices(choices, weights=weights)[0]
        
        elif difficulty == 'hard':
            # Hard mode: Computer tries to counter player's most used choice
            if total_games > 3:
                most_used = max(choice_stats, key=choice_stats.get)
                counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
                # 60% chance to counter, 40% random
                if random.random() < 0.6:
                    return counters[most_used]
            return random.choice(['rock', 'paper', 'scissors'])
        
        elif difficulty == 'expert':
            # Expert mode: Advanced AI that analyzes patterns
            if total_games > 5:
                # Analyze last 3 moves for patterns
                recent_moves = [game['user_choice'] for game in game_history[-3:]]
                if len(recent_moves) >= 2:
                    # Look for patterns
                    if recent_moves[-1] == recent_moves[-2]:
                        # Player might repeat, counter it
                        counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
                        return counters[recent_moves[-1]]
                    elif len(set(recent_moves)) == len(recent_moves):
                        # Player is cycling, predict next in cycle
                        cycle = ['rock', 'paper', 'scissors']
                        try:
                            last_idx = cycle.index(recent_moves[-1])
                            next_choice = cycle[(last_idx + 1) % 3]
                            counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
                            return counters[next_choice]
                        except ValueError:
                            pass
            
            # Fallback to smart random
            least_used = min(choice_stats, key=choice_stats.get)
            counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
            return counters[least_used]
        
        else:  # Normal mode
            return random.choice(['rock', 'paper', 'scissors'])
    
    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return 'Tie'
        
        if (user_choice == 'rock' and computer_choice == 'scissors') or \
           (user_choice == 'paper' and computer_choice == 'rock') or \
           (user_choice == 'scissors' and computer_choice == 'paper'):
            return 'Win'
        
        return 'Loss'
    
    def display_result(self, user_choice, computer_choice, result):
        # Clear previous result
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Set result color
        if result == 'Win':
            result_color = self.colors['success']
            if settings['confetti']:
                self.create_confetti()
        elif result == 'Loss':
            result_color = self.colors['danger']
        else:  # Tie
            result_color = self.colors['warning']
        
        # Display choices with ASCII art
        choices_frame = ttk.Frame(self.result_frame)
        choices_frame.pack(fill=tk.BOTH, expand=True)
        
        # User choice
        user_frame = ttk.Frame(choices_frame)
        user_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        ttk.Label(user_frame, text="Your Choice:", style='Header.TLabel').pack()
        ttk.Label(user_frame, text=user_choice.upper(), style='Stats.TLabel').pack()
        
        user_art = self.get_choice_art(user_choice)
        user_art_label = ttk.Label(user_frame, text=user_art, style='Game.TLabel')
        user_art_label.pack()
        
        # Computer choice
        computer_frame = ttk.Frame(choices_frame)
        computer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        ttk.Label(computer_frame, text="Computer's Choice:", style='Header.TLabel').pack()
        ttk.Label(computer_frame, text=computer_choice.upper(), style='Stats.TLabel').pack()
        
        computer_art = self.get_choice_art(computer_choice)
        computer_art_label = ttk.Label(computer_frame, text=computer_art, style='Game.TLabel')
        computer_art_label.pack()
        
        # Result
        result_label = ttk.Label(self.result_frame, text=f"Result: {result.upper()}", 
                                style='Header.TLabel', foreground=result_color)
        result_label.pack(pady=20)
        
        # Continue button if not auto continue
        if not settings['auto_continue']:
            continue_btn = ttk.Button(self.result_frame, text="Continue", 
                                   command=self.show_game_screen)
            continue_btn.pack(pady=10)
    
    def get_choice_art(self, choice):
        if choice == 'rock':
            return ROCK_ART
        elif choice == 'paper':
            return PAPER_ART
        elif choice == 'scissors':
            return SCISSORS_ART
        return ''
    
    def create_confetti(self):
        """Create confetti animation"""
        if not settings['particles']:
            return
            
        confetti_count = 50  # Reduced count for better performance
        colors = [self.colors['success'], self.colors['warning'], self.colors['accent_text'], 
                 self.colors['accent'], self.colors['button_bg']]
        
        for _ in range(confetti_count):
            x = random.randint(0, self.root.winfo_width())
            y = random.randint(-50, 0)
            size = random.randint(5, 15)
            color = random.choice(colors)
            speed = random.uniform(2, 5)
            
            confetti = self.particles_canvas.create_rectangle(
                x, y, x+size, y+size, fill=color, outline=""
            )
            
            self.animate_confetti(confetti, speed)
    
    def animate_confetti(self, confetti, speed):
        """Animate a single confetti piece"""
        y = self.particles_canvas.coords(confetti)[1]
        
        if y < self.root.winfo_height():
            self.particles_canvas.move(confetti, random.uniform(-1, 1), speed)
            self.root.after(30, lambda: self.animate_confetti(confetti, speed))  # Increased delay for performance
        else:
            self.particles_canvas.delete(confetti)
    
    def animate_particles(self):
        """Animate background particles"""
        if not settings['particles']:
            self.root.after(100, self.animate_particles)
            return
            
        # Create new particles occasionally
        if random.random() < 0.05:  # Reduced frequency for better performance
            x = random.randint(0, self.root.winfo_width())
            y = self.root.winfo_height()
            size = random.randint(2, 5)
            color = random.choice([self.colors['accent'], self.colors['button_bg'], 
                                  self.colors['secondary_bg']])
            speed = random.uniform(0.5, 2)
            
            particle = self.particles_canvas.create_oval(
                x, y, x+size, y+size, fill=color, outline=""
            )
            
            self.animate_particle(particle, speed)
        
        self.root.after(100, self.animate_particles)
    
    def animate_particle(self, particle, speed):
        """Animate a single particle"""
        y = self.particles_canvas.coords(particle)[1]
        
        if y > -10:
            self.particles_canvas.move(particle, random.uniform(-0.5, 0.5), -speed)
            self.root.after(50, lambda: self.animate_particle(particle, speed))
        else:
            self.particles_canvas.delete(particle)
    
    def show_tournament_results(self):
        self.hide_all_frames()
        
        results_frame = ttk.Frame(self.main_container)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(results_frame, text="🏆 TOURNAMENT RESULTS", style='Header.TLabel')
        title_label.pack(pady=(0, 20))
        
        if user_score > computer_score:
            result_text = "🏆 YOU WON THE TOURNAMENT! 🏆"
            result_color = self.colors['success']
            if settings['confetti']:
                self.create_confetti()
        elif user_score < computer_score:
            result_text = "💻 COMPUTER WON THE TOURNAMENT! 💻"
            result_color = self.colors['danger']
        else:
            result_text = "🤝 TOURNAMENT ENDED IN A TIE! 🤝"
            result_color = self.colors['warning']
        
        result_label = ttk.Label(results_frame, text=result_text, 
                                style='Header.TLabel', foreground=result_color)
        result_label.pack(pady=20)
        
        score_text = f"Final Score: You {user_score} - {computer_score} Computer | Ties: {ties}"
        score_label = ttk.Label(results_frame, text=score_text, style='Stats.TLabel')
        score_label.pack(pady=10)
        
        # Performance metrics
        metrics_frame = ttk.Frame(results_frame, style='Card.TFrame')
        metrics_frame.pack(fill=tk.X, pady=20, padx=20, ipady=10)
        
        metrics_label = ttk.Label(metrics_frame, text="Performance Metrics", style='Header.TLabel')
        metrics_label.pack(pady=(10, 5))
        
        win_rate = (user_score / (user_score + computer_score) * 100) if (user_score + computer_score) > 0 else 0
        avg_response = sum(response_times[-10:]) / min(len(response_times), 10) if response_times else 0
        
        metrics_text = f"Win Rate: {win_rate:.1f}% | Avg. Response Time: {avg_response:.2f}s | Best Streak: {max_streak}"
        metrics_detail = ttk.Label(metrics_frame, text=metrics_text, style='Stats.TLabel')
        metrics_detail.pack(pady=5)
        
        # Check for tournament winner achievement
        if user_score > computer_score and 'tournament_winner' not in achievements:
            achievements.add('tournament_winner')
            self.show_achievement_unlocked('tournament_winner')
        
        # Save game data
        self.save_game_data()
        
        # Reset tournament mode
        global tournament_mode, current_round
        tournament_mode = False
        current_round = 0
        
        # Buttons
        buttons_frame = ttk.Frame(results_frame)
        buttons_frame.pack(pady=20)
        
        ttk.Button(buttons_frame, text="Play Again", 
                  command=lambda: self.start_tournament(round_limit)).pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="Back to Main Menu", 
                  command=self.show_main_menu).pack(side=tk.LEFT, padx=10)
    
    def show_profile(self):
        self.hide_all_frames()
        
        profile_frame = ttk.Frame(self.main_container)
        profile_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(profile_frame, text="👤 PLAYER PROFILE", style='Header.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Profile card
        profile_card = ttk.Frame(profile_frame, style='Card.TFrame')
        profile_card.pack(fill=tk.X, pady=10, padx=20, ipady=10)
        
        # Avatar and info
        info_frame = ttk.Frame(profile_card)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Avatar
        avatar_frame = ttk.Frame(info_frame)
        avatar_frame.pack(side=tk.LEFT, padx=20)
        
        self.profile_avatar_canvas = tk.Canvas(avatar_frame, width=100, height=100, highlightthickness=0)
        self.profile_avatar_canvas.pack()
        self.draw_avatar(self.profile_avatar_canvas, player_avatar)
        
        # Player info
        player_info_frame = ttk.Frame(info_frame)
        player_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        # Player name
        name_frame = ttk.Frame(player_info_frame)
        name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(name_frame, text="Player Name:", style='Stats.TLabel').pack(side=tk.LEFT, padx=5)
        
        name_entry = ttk.Entry(name_frame, font=('Arial', 12))
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        name_entry.insert(0, player_name)
        
        def update_name():
            global player_name
            new_name = name_entry.get().strip()
            if new_name:
                player_name = new_name
                self.save_game_data()
                messagebox.showinfo("Profile Updated", f"Player name updated to: {player_name}")
                self.show_profile()
        
        ttk.Button(name_frame, text="Update", command=update_name).pack(side=tk.LEFT, padx=5)
        
        # Player level
        level = self.calculate_level()
        xp = self.calculate_xp()
        xp_to_next = self.calculate_xp_to_next_level()
        
        level_text = f"Level: {level} | XP: {xp}/{xp_to_next}"
        level_label = ttk.Label(player_info_frame, text=level_text, style='Stats.TLabel')
        level_label.pack(anchor=tk.W, pady=5)
        
        # XP progress bar
        xp_progress = ttk.Progressbar(player_info_frame, length=300, mode='determinate')
        xp_progress.pack(fill=tk.X, pady=5)
        xp_progress['value'] = (xp / xp_to_next) * 100
        
        # Avatar selection
        avatar_frame = ttk.Frame(profile_card)
        avatar_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(avatar_frame, text="Select Avatar:", style='Stats.TLabel').pack(anchor=tk.W, pady=5)
        
        avatar_options = ttk.Frame(avatar_frame)
        avatar_options.pack(fill=tk.X)
        
        for avatar_id, avatar_info in AVATARS.items():
            avatar_btn_frame = ttk.Frame(avatar_options)
            avatar_btn_frame.pack(side=tk.LEFT, padx=10)
            
            avatar_btn_canvas = tk.Canvas(avatar_btn_frame, width=60, height=60, highlightthickness=0)
            avatar_btn_canvas.pack()
            self.draw_avatar(avatar_btn_canvas, avatar_id)
            
            avatar_btn = ttk.Button(avatar_btn_frame, text=avatar_info['name'], 
                                  command=lambda a=avatar_id: self.change_avatar(a))
            avatar_btn.pack()
        
        # Stats
        stats_frame = ttk.Frame(profile_card)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(stats_frame, text="Player Statistics", style='Header.TLabel').pack(anchor=tk.W, pady=5)
        
        win_rate = (user_score / total_games * 100) if total_games > 0 else 0
        avg_response = sum(response_times) / len(response_times) if response_times else 0
        
        stats_text = f"Games Played: {total_games} | Win Rate: {win_rate:.1f}% | Best Streak: {max_streak} | Avg. Response: {avg_response:.2f}s"
        stats_label = ttk.Label(stats_frame, text=stats_text, style='Stats.TLabel')
        stats_label.pack(anchor=tk.W, pady=5)
        
        # Back button
        back_btn = ttk.Button(profile_frame, text="Back to Main Menu", 
                            command=self.show_main_menu)
        back_btn.pack(pady=20)
    
    def change_avatar(self, avatar_id):
        global player_avatar
        player_avatar = avatar_id
        self.save_game_data()
        self.draw_avatar(self.profile_avatar_canvas, player_avatar)
        messagebox.showinfo("Avatar Updated", f"Avatar changed to {AVATARS[avatar_id]['name']}")
    
    def show_settings(self):
        self.hide_all_frames()
        
        settings_frame = ttk.Frame(self.main_container)
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(settings_frame, text="⚙️ GAME SETTINGS", style='Header.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(settings_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Game settings tab
        game_tab = ttk.Frame(notebook)
        notebook.add(game_tab, text="Game")
        
        # Player name
        name_frame = ttk.Frame(game_tab)
        name_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(name_frame, text="Player Name:", style='Stats.TLabel').pack(side=tk.LEFT, padx=10)
        
        name_entry = ttk.Entry(name_frame, font=('Arial', 12))
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        name_entry.insert(0, player_name)
        
        def update_name():
            global player_name
            new_name = name_entry.get().strip()
            if new_name:
                player_name = new_name
                self.save_game_data()
                messagebox.showinfo("Settings Updated", f"Player name updated to: {player_name}")
        
        ttk.Button(name_frame, text="Update", command=update_name).pack(side=tk.LEFT, padx=10)
        
        # Difficulty
        diff_frame = ttk.Frame(game_tab)
        diff_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(diff_frame, text="Difficulty:", style='Stats.TLabel').pack(side=tk.LEFT, padx=10)
        
        diff_var = tk.StringVar(value=difficulty)
        diff_combo = ttk.Combobox(diff_frame, textvariable=diff_var, 
                                 values=['easy', 'normal', 'hard', 'expert'], 
                                 state='readonly', font=('Arial', 12))
        diff_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        def update_difficulty():
            global difficulty
            difficulty = diff_var.get()
            self.save_game_data()
            messagebox.showinfo("Settings Updated", f"Difficulty set to: {difficulty.title()}")
        
        ttk.Button(diff_frame, text="Update", command=update_difficulty).pack(side=tk.LEFT, padx=10)
        
        # Appearance settings tab
        appearance_tab = ttk.Frame(notebook)
        notebook.add(appearance_tab, text="Appearance")
        
        # Theme selection
        theme_frame = ttk.Frame(appearance_tab)
        theme_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(theme_frame, text="Theme:", style='Stats.TLabel').pack(side=tk.LEFT, padx=10)
        
        theme_var = tk.StringVar(value=settings['theme'])
        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, 
                                  values=['dark', 'light', 'custom'], 
                                  state='readonly', font=('Arial', 12))
        theme_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        def update_theme():
            settings['theme'] = theme_var.get()
            self.configure_theme()
            self.save_game_data()
            messagebox.showinfo("Settings Updated", f"Theme set to: {settings['theme'].title()}")
            self.show_settings()  # Refresh settings to apply new theme
        
        ttk.Button(theme_frame, text="Update", command=update_theme).pack(side=tk.LEFT, padx=10)
        
        # Toggles
        toggles_frame = ttk.Frame(appearance_tab)
        toggles_frame.pack(fill=tk.X, pady=20, padx=10)
        
        ttk.Label(toggles_frame, text="Options:", style='Header.TLabel').pack(anchor=tk.W, padx=10)
        
        # Animations
        anim_var = tk.BooleanVar(value=settings['animations'])
        anim_check = ttk.Checkbutton(toggles_frame, text="Animations", variable=anim_var,
                                    command=lambda: self.update_setting('animations', anim_var.get()))
        anim_check.pack(anchor=tk.W, padx=20, pady=5)
        
        # Sound effects
        sound_var = tk.BooleanVar(value=settings['sound_effects'])
        sound_check = ttk.Checkbutton(toggles_frame, text="Sound Effects", variable=sound_var,
                                     command=lambda: self.update_setting('sound_effects', sound_var.get()))
        sound_check.pack(anchor=tk.W, padx=20, pady=5)
        
        # Auto continue
        auto_var = tk.BooleanVar(value=settings['auto_continue'])
        auto_check = ttk.Checkbutton(toggles_frame, text="Auto Continue", variable=auto_var,
                                    command=lambda: self.update_setting('auto_continue', auto_var.get()))
        auto_check.pack(anchor=tk.W, padx=20, pady=5)
        
        # Particles
        particles_var = tk.BooleanVar(value=settings['particles'])
        particles_check = ttk.Checkbutton(toggles_frame, text="Background Particles", variable=particles_var,
                                        command=lambda: self.update_setting('particles', particles_var.get()))
        particles_check.pack(anchor=tk.W, padx=20, pady=5)
        
        # Confetti
        confetti_var = tk.BooleanVar(value=settings['confetti'])
        confetti_check = ttk.Checkbutton(toggles_frame, text="Win Confetti", variable=confetti_var,
                                        command=lambda: self.update_setting('confetti', confetti_var.get()))
        confetti_check.pack(anchor=tk.W, padx=20, pady=5)
        
        # Back button
        back_btn = ttk.Button(settings_frame, text="Back to Main Menu", 
                            command=self.show_main_menu)
        back_btn.pack(pady=20)
    
    def update_setting(self, setting, value):
        global settings
        settings[setting] = value
        self.save_game_data()
        messagebox.showinfo("Settings Updated", f"{setting.replace('_', ' ').title()}: {'On' if value else 'Off'}")
    
    def show_statistics(self):
        self.hide_all_frames()
        
        stats_frame = ttk.Frame(self.main_container)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(stats_frame, text="📊 STATISTICS & ACHIEVEMENTS", style='Header.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(stats_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Game statistics tab
        game_stats_tab = ttk.Frame(notebook)
        notebook.add(game_stats_tab, text="Game Stats")
        
        win_percentage = (user_score / total_games * 100) if total_games > 0 else 0
        loss_percentage = (computer_score / total_games * 100) if total_games > 0 else 0
        tie_percentage = (ties / total_games * 100) if total_games > 0 else 0
        
        stats_text = f"""
Total Games: {total_games}
Wins: {user_score} ({win_percentage:.1f}%) | Losses: {computer_score} ({loss_percentage:.1f}%) | Ties: {ties} ({tie_percentage:.1f}%)
Current Streak: {streak}
Best Streak: {max_streak}
Difficulty: {difficulty.title()}
        """
        
        stats_label = ttk.Label(game_stats_tab, text=stats_text, style='Stats.TLabel')
        stats_label.pack(pady=10, padx=10, anchor=tk.W)
        
        # Response time stats
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            min_response = min(response_times)
            max_response = max(response_times)
            
            response_text = f"""
Response Time Statistics:
Average: {avg_response:.2f}s
Fastest: {min_response:.2f}s
Slowest: {max_response:.2f}s
            """
            
            response_label = ttk.Label(game_stats_tab, text=response_text, style='Stats.TLabel')
            response_label.pack(pady=10, padx=10, anchor=tk.W)
        
        # Choice statistics tab
        choice_stats_tab = ttk.Frame(notebook)
        notebook.add(choice_stats_tab, text="Choice Stats")
        
        total_choices = sum(choice_stats.values())
        choice_stats_text = "Choice Statistics:\n\n"
        
        for choice in ['rock', 'paper', 'scissors']:
            emoji = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}[choice]
            used = choice_stats[choice]
            won = win_by_choice[choice]
            percentage = (used / total_choices * 100) if total_choices > 0 else 0
            win_rate = (won / used * 100) if used > 0 else 0
            choice_stats_text += f"{emoji} {choice.title()}: Used {used} times ({percentage:.1f}%) | Won {won} ({win_rate:.1f}%)\n\n"
        
        choice_stats_label = ttk.Label(choice_stats_tab, text=choice_stats_text, style='Stats.TLabel')
        choice_stats_label.pack(pady=10, padx=10, anchor=tk.W)
        
        # Achievements tab
        achievements_tab = ttk.Frame(notebook)
        notebook.add(achievements_tab, text="Achievements")
        
        achievements_text = f"Achievements ({len(achievements)}/{len(ACHIEVEMENTS)}):\n\n"
        
        if achievements:
            for achievement in sorted(achievements):
                achievements_text += f"✓ {ACHIEVEMENTS[achievement]['icon']} {ACHIEVEMENTS[achievement]['name']}\n"
                achievements_text += f"  {ACHIEVEMENTS[achievement]['desc']}\n\n"
        else:
            achievements_text += "No achievements unlocked yet. Keep playing!\n\n"
        
        # Show locked achievements
        locked = set(ACHIEVEMENTS.keys()) - achievements
        if locked and len(achievements) < len(ACHIEVEMENTS):
            achievements_text += "\nLocked Achievements:\n\n"
            for achievement in sorted(list(locked)[:5]):  # Show first 5 locked
                achievements_text += f"○ {ACHIEVEMENTS[achievement]['icon']} {ACHIEVEMENTS[achievement]['name']}\n"
                achievements_text += f"  {ACHIEVEMENTS[achievement]['desc']}\n\n"
        
        achievements_label = ttk.Label(achievements_tab, text=achievements_text, style='Stats.TLabel')
        achievements_label.pack(pady=10, padx=10, anchor=tk.W)
        
        # Back button
        back_btn = ttk.Button(stats_frame, text="Back to Main Menu", 
                            command=self.show_main_menu)
        back_btn.pack(pady=10)
    
    def show_history(self):
        self.hide_all_frames()
        
        history_frame = ttk.Frame(self.main_container)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(history_frame, text="📜 GAME HISTORY", style='Header.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create treeview for history
        tree_frame = ttk.Frame(history_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_tree = ttk.Treeview(tree_frame, columns=('user', 'computer', 'result', 'time'), 
                                   show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=history_tree.yview)
        
        history_tree.heading('user', text='Your Choice')
        history_tree.heading('computer', text='Computer Choice')
        history_tree.heading('result', text='Result')
        history_tree.heading('time', text='Time')
        
        history_tree.column('user', width=150)
        history_tree.column('computer', width=150)
        history_tree.column('result', width=100)
        history_tree.column('time', width=200)
        
        # Add game history
        if not game_history:
            history_tree.insert('', tk.END, values=('No games played yet!', '', '', ''))
        else:
            for i, game in enumerate(game_history[-20:]):  # Show last 20 games
                result_color = 'green' if game['result'] == 'Win' else 'red' if game['result'] == 'Loss' else 'yellow'
                history_tree.insert('', tk.END, values=(
                    game['user_choice'], 
                    game['computer_choice'], 
                    game['result'],
                    game.get('timestamp', 'Unknown')
                ), tags=(result_color,))
            
            # Configure tags for colors
            history_tree.tag_configure('green', foreground=self.colors['success'])
            history_tree.tag_configure('red', foreground=self.colors['danger'])
            history_tree.tag_configure('yellow', foreground=self.colors['warning'])
        
        history_tree.pack(fill=tk.BOTH, expand=True)
        
        # Back button
        back_btn = ttk.Button(history_frame, text="Back to Main Menu", 
                            command=self.show_main_menu)
        back_btn.pack(pady=10)
    
    def show_rules(self):
        self.hide_all_frames()
        
        rules_frame = ttk.Frame(self.main_container)
        rules_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(rules_frame, text="📖 RULES & HELP", style='Header.TLabel')
        title_label.pack(pady=(0, 20))
        
        rules_text = """
🪨 ROCK beats ✂️ SCISSORS
✂️ SCISSORS beats 📄 PAPER
📄 PAPER beats 🪨 ROCK
🎮 GAME MODES:
• Quick Play: Single rounds, play as much as you want
• Tournament: Fixed number of rounds with special scoring
🏆 ACHIEVEMENTS:
Unlock achievements by winning streaks, playing games,
mastering specific choices, and completing tournaments!
⚙️ DIFFICULTY LEVELS:
• Easy: Computer makes predictable choices
• Normal: Random computer choices
• Hard: Computer analyzes your most-used choice
• Expert: Advanced AI with pattern recognition
📊 PLAYER LEVELS:
Gain XP by playing games and unlocking achievements.
Level up to show your mastery of the game!
👤 PLAYER PROFILE:
Customize your player name and avatar to personalize
your gaming experience.
        """
        
        rules_label = ttk.Label(rules_frame, text=rules_text, style='Stats.TLabel')
        rules_label.pack(pady=10, padx=10, anchor=tk.W)
        
        # Back button
        back_btn = ttk.Button(rules_frame, text="Back to Main Menu", 
                            command=self.show_main_menu)
        back_btn.pack(pady=10)
    
    def reset_progress(self):
        if messagebox.askyesno("Reset Progress", 
                              "Are you sure you want to reset all progress? This cannot be undone."):
            global user_score, computer_score, ties, total_games, game_history
            global streak, max_streak, achievements, choice_stats, win_by_choice, stats
            global response_times
            
            user_score = 0
            computer_score = 0
            ties = 0
            total_games = 0
            game_history = []
            streak = 0
            max_streak = 0
            achievements = set()
            choice_stats = {'rock': 0, 'paper': 0, 'scissors': 0}
            win_by_choice = {'rock': 0, 'paper': 0, 'scissors': 0}
            stats = defaultdict(int)
            response_times = []
            
            self.save_game_data()
            messagebox.showinfo("Reset Complete", "All progress has been reset!")
            self.show_main_menu()
    
    def check_achievements(self):
        global achievements, streak, max_streak, total_games, user_score
        new_achievements = []
        
        # First win
        if user_score >= 1 and 'first_win' not in achievements:
            achievements.add('first_win')
            new_achievements.append('first_win')
        
        # Streak achievements
        if streak >= 5 and 'streak_5' not in achievements:
            achievements.add('streak_5')
            new_achievements.append('streak_5')
        
        if streak >= 10 and 'streak_10' not in achievements:
            achievements.add('streak_10')
            new_achievements.append('streak_10')
        
        # Century club
        if total_games >= 100 and 'century' not in achievements:
            achievements.add('century')
            new_achievements.append('century')
        
        # Perfectionist achievement
        if streak >= 10 and 'perfectionist' not in achievements:
            # Check if there are any losses in the last 10 games
            recent_games = game_history[-10:] if len(game_history) >= 10 else game_history
            if all(game['result'] != 'Loss' for game in recent_games):
                achievements.add('perfectionist')
                new_achievements.append('perfectionist')
        
        # Choice-based achievements
        for choice in ['rock', 'paper', 'scissors']:
            if win_by_choice[choice] >= 20 and f'{choice}_master' not in achievements:
                achievements.add(f'{choice}_master')
                new_achievements.append(f'{choice}_master')
        
        # Speed demon achievement
        if response_times and response_times[-1] < 2 and 'speed_demon' not in achievements:
            achievements.add('speed_demon')
            new_achievements.append('speed_demon')
        
        # Lucky seven achievement
        if total_games >= 7 and 'lucky_seven' not in achievements:
            # Check if player has won exactly 7 games
            if user_score == 7:
                achievements.add('lucky_seven')
                new_achievements.append('lucky_seven')
        
        # Comeback achievement
        if 'comeback' not in achievements and len(game_history) >= 4:
            # Check if player lost 3 in a row and then won
            last_four = game_history[-4:]
            if (last_four[0]['result'] == 'Loss' and 
                last_four[1]['result'] == 'Loss' and 
                last_four[2]['result'] == 'Loss' and 
                last_four[3]['result'] == 'Win'):
                achievements.add('comeback')
                new_achievements.append('comeback')
        
        # Display new achievements
        for achievement in new_achievements:
            self.show_achievement_unlocked(achievement)
    
    def show_achievement_unlocked(self, achievement):
        dialog = tk.Toplevel(self.root)
        dialog.title("Achievement Unlocked!")
        dialog.geometry("450x250")
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        ttk.Label(dialog, text="🎊 ACHIEVEMENT UNLOCKED! 🎊", 
                 style='Header.TLabel').pack(pady=10)
        
        ttk.Label(dialog, text=ACHIEVEMENTS[achievement]['icon'], 
                 font=('Arial', 40)).pack(pady=5)
        
        ttk.Label(dialog, text=ACHIEVEMENTS[achievement]['name'], 
                 style='Header.TLabel').pack(pady=5)
        
        ttk.Label(dialog, text=ACHIEVEMENTS[achievement]['desc'], 
                 style='Stats.TLabel').pack(pady=5)
        
        ttk.Button(dialog, text="OK", command=dialog.destroy).pack(pady=10)
    
    def save_game_data(self):
        data = {
            'user_score': user_score,
            'computer_score': computer_score,
            'ties': ties,
            'total_games': total_games,
            'max_streak': max_streak,
            'achievements': list(achievements),
            'player_name': player_name,
            'player_avatar': player_avatar,
            'settings': settings,
            'stats': dict(stats),
            'choice_stats': choice_stats,
            'win_by_choice': win_by_choice,
            'response_times': response_times[-100:]  # Save only last 100 response times
        }
        
        try:
            with open('rps_save.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save game data: {e}")
    
    def load_game_data(self):
        global user_score, computer_score, ties, total_games, max_streak
        global achievements, player_name, player_avatar, settings, stats
        global choice_stats, win_by_choice, response_times
        
        try:
            with open('rps_save.json', 'r') as f:
                data = json.load(f)
                
            user_score = data.get('user_score', 0)
            computer_score = data.get('computer_score', 0)
            ties = data.get('ties', 0)
            total_games = data.get('total_games', 0)
            max_streak = data.get('max_streak', 0)
            achievements = set(data.get('achievements', []))
            player_name = data.get('player_name', 'Player')
            player_avatar = data.get('player_avatar', 'default')
            settings.update(data.get('settings', {}))
            stats.update(data.get('stats', {}))
            choice_stats.update(data.get('choice_stats', {'rock': 0, 'paper': 0, 'scissors': 0}))
            win_by_choice.update(data.get('win_by_choice', {'rock': 0, 'paper': 0, 'scissors': 0}))
            response_times = data.get('response_times', [])
            
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load game data: {e}")
            return False
    
    def on_closing(self):
        self.save_game_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsApp(root)
    root.mainloop()