import sys
import json
import os
import datetime
import random
from functools import lru_cache
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem, 
                             QCheckBox, QComboBox, QTabWidget, QScrollArea, QCalendarWidget, 
                             QTimeEdit, QDateEdit, QColorDialog, QMessageBox, QInputDialog, 
                             QFileDialog, QFontDialog, QSlider, QProgressBar, QMenu, QAction,
                             QSystemTrayIcon, QSplashScreen, QDialog, QTextEdit, QGroupBox,
                             QRadioButton, QSpinBox, QToolBar, QStatusBar, QDockWidget, QFrame,
                             QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QDate, QTime, QSize, QPropertyAnimation, QRect, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPixmap, QCursor, QBrush, QLinearGradient

# Constants
APP_NAME = "TaskMaster Pro"
APP_VERSION = "1.0.0"
DEFAULT_THEME = "purple"
SAVE_FILE = "tasks.json"

# Stickers for task completion
COMPLETION_STICKERS = [
    "", "", "", "", "", "", "", "", "", ""
]

# Button icons
BUTTON_ICONS = {
    "edit": "",
    "delete": "",
    "add": "",
    "calendar": "",
    "settings": "",
    "stats": "",
    "categories": ""
}

# Theme colors
THEMES = {
    "purple": {
        "primary": "#9C27B0",
        "secondary": "#BA68C8",
        "accent": "#CE93D8",
        "background": "#F3E5F5",
        "text": "#333333",
        "completed": "#4CAF50",
        "gradient_start": "#E1BEE7",
        "gradient_end": "#F3E5F5"
    },
    "blue": {
        "primary": "#2979FF",
        "secondary": "#5393FF",
        "accent": "#75A7FF",
        "background": "#F5F9FF",
        "text": "#333333",
        "completed": "#4CAF50",
        "gradient_start": "#BBDEFB",
        "gradient_end": "#F5F9FF"
    },
    "dark": {
        "primary": "#333333",
        "secondary": "#555555",
        "accent": "#777777",
        "background": "#222222",
        "text": "#FFFFFF",
        "completed": "#4CAF50",
        "gradient_start": "#424242",
        "gradient_end": "#222222"
    },
    "red": {
        "primary": "#F44336",
        "secondary": "#EF5350",
        "accent": "#E57373",
        "background": "#FFEBEE",
        "text": "#333333",
        "completed": "#4CAF50",
        "gradient_start": "#FFCDD2",
        "gradient_end": "#FFEBEE"
    },
    "green": {
        "primary": "#4CAF50",
        "secondary": "#66BB6A",
        "accent": "#81C784",
        "background": "#E8F5E9",
        "text": "#333333",
        "completed": "#2196F3",
        "gradient_start": "#C8E6C9",
        "gradient_end": "#E8F5E9"
    }
}

# Task priority levels
PRIORITY_LEVELS = {
    "High": {"color": "#F44336", "value": 3},
    "Medium": {"color": "#FF9800", "value": 2},
    "Low": {"color": "#4CAF50", "value": 1},
    "None": {"color": "#9E9E9E", "value": 0}
}

# Task categories
DEFAULT_CATEGORIES = [
    "Work", "Personal", "Shopping", "Health", "Education", 
    "Finance", "Home", "Family", "Entertainment", "Other"
]

# Celebration stickers and messages
CELEBRATION_STICKERS = [
    "🎉", "🎊", "🥳", "🌟", "⭐", "✨", "🏆", "🎯", "💫", "🔥", "👏", "🙌", "💪", "🚀", "🎈"
]

CELEBRATION_MESSAGES = {
    "early": [
        "🚀 Wow! You finished early! You're a productivity superstar!",
        "⚡ Lightning fast! You're crushing your goals!",
        "🏆 Early bird gets the worm! Fantastic job!",
        "🌟 You're ahead of schedule! Keep up the amazing work!",
        "💫 Speed demon! You're on fire today!"
    ],
    "on_time": [
        "🎯 Perfect timing! Task completed right on schedule!",
        "✨ Well done! You hit your deadline perfectly!",
        "🎊 Great job! Right on time as always!",
        "👏 Excellent! You're a master of time management!",
        "🙌 Boom! Another task conquered!"
    ],
    "late": [
        "🎉 Better late than never! Task completed!",
        "💪 You did it! Every completion is a victory!",
        "🌟 Great job finishing this task!",
        "✨ Completed! You're making progress!",
        "🎊 Done! Keep up the momentum!"
    ],
    "general": [
        "🎉 Hooray! Another task bites the dust!",
        "🥳 Celebration time! Task completed!",
        "🏆 Victory! You're unstoppable!",
        "⭐ Awesome! One step closer to your goals!",
        "🎊 Fantastic! You're doing great!"
    ]
}

# Task stickers/emojis for visual appeal
TASK_STICKERS = {
    "Work": ["💼", "📊", "💻", "📝", "⚡", "🎯", "📈", "🔥", "💡", "🚀"],
    "Personal": ["🌟", "💫", "✨", "🎨", "📚", "🎵", "🌸", "🦋", "🌈", "💖"],
    "Shopping": ["🛒", "🛍️", "💳", "🏪", "🎁", "👕", "👠", "📱", "🍎", "🧺"],
    "Health": ["💪", "🏃", "🧘", "🥗", "💊", "🏥", "❤️", "🌿", "🍃", "⚕️"],
    "Education": ["📚", "🎓", "✏️", "📖", "🧠", "💡", "🔬", "📐", "🎯", "⭐"],
    "Finance": ["💰", "💳", "📊", "💸", "🏦", "📈", "💎", "🪙", "💵", "📋"],
    "Home": ["🏠", "🔧", "🧹", "🌱", "🛋️", "🍳", "🧽", "🔨", "🪴", "🏡"],
    "Family": ["👨‍👩‍👧‍👦", "❤️", "🎂", "🎈", "📸", "🎁", "🌟", "💕", "🤗", "👶"],
    "Entertainment": ["🎬", "🎮", "🎵", "🎪", "🎭", "🎨", "📺", "🎲", "🎯", "🎊"],
    "Other": ["⭐", "🌟", "✨", "💫", "🔥", "⚡", "🎯", "💎", "🚀", "🌈"]
}

class Task:
    def __init__(self, title, description="", due_date=None, priority="None", 
                 category="Other", completed=False, created_at=None, reminder=None,
                 subtasks=None, notes="", tags=None, color=None, recurring=None):
        self.id = random.randint(10000, 99999)
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.completed = completed
        self.created_at = created_at if created_at else datetime.datetime.now().isoformat()
        self.reminder = reminder
        self.subtasks = subtasks if subtasks else []
        self.notes = notes
        self.tags = tags if tags else []
        self.color = color
        self.recurring = recurring
        self.completion_date = None
        self.progress = 0
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "category": self.category,
            "completed": self.completed,
            "created_at": self.created_at,
            "reminder": self.reminder,
            "subtasks": self.subtasks,
            "notes": self.notes,
            "tags": self.tags,
            "color": self.color,
            "recurring": self.recurring,
            "completion_date": self.completion_date,
            "progress": self.progress
        }
    
    @classmethod
    def from_dict(cls, data):
        task = cls(data["title"])
        for key, value in data.items():
            setattr(task, key, value)
        return task

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.categories = DEFAULT_CATEGORIES.copy()
        self.tags = []
        self._task_cache = {}
        self._stats_cache = {}
        self._cache_timestamp = 0
        self.load_tasks()
    
    def add_task(self, task):
        self.tasks.append(task)
        self._clear_cache()
        self.save_tasks()
        return task
    
    def update_task(self, task_id, updated_task):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks[i] = updated_task
                self._clear_cache()
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self._clear_cache()
                self.save_tasks()
                return True
        return False
    
    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    @lru_cache(maxsize=128)
    def get_tasks_by_category(self, category):
        return tuple(task for task in self.tasks if task.category == category)
    
    @lru_cache(maxsize=128)
    def get_tasks_by_priority(self, priority):
        return tuple(task for task in self.tasks if task.priority == priority)
    
    def get_tasks_by_date(self, date):
        return [task for task in self.tasks if task.due_date == date]
    
    def get_tasks_by_tag(self, tag):
        return [task for task in self.tasks if tag in task.tags]
    
    @lru_cache(maxsize=32)
    def get_completed_tasks(self):
        return tuple(task for task in self.tasks if task.completed)
    
    @lru_cache(maxsize=32)
    def get_incomplete_tasks(self):
        return tuple(task for task in self.tasks if not task.completed)
    
    def get_overdue_tasks(self):
        today = datetime.datetime.now().date().isoformat()
        return [task for task in self.tasks if not task.completed and 
                task.due_date and task.due_date < today]
    
    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)
            self.save_tasks()
            return True
        return False
    
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
            self.save_tasks()
            return True
        return False
    
    def _clear_cache(self):
        """Clear all caches when tasks are modified"""
        self._task_cache.clear()
        self._stats_cache.clear()
        self._cache_timestamp = datetime.datetime.now().timestamp()
        # Clear lru_cache decorated methods
        if hasattr(self.get_tasks_by_category, 'cache_clear'):
            self.get_tasks_by_category.cache_clear()
        if hasattr(self.get_tasks_by_priority, 'cache_clear'):
            self.get_tasks_by_priority.cache_clear()
        if hasattr(self.get_completed_tasks, 'cache_clear'):
            self.get_completed_tasks.cache_clear()
        if hasattr(self.get_incomplete_tasks, 'cache_clear'):
            self.get_incomplete_tasks.cache_clear()

    def save_tasks(self):
        try:
            data = {
                "tasks": [task.to_dict() for task in self.tasks],
                "categories": self.categories,
                "tags": self.tags
            }
            with open(SAVE_FILE, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        if not os.path.exists(SAVE_FILE):
            return
        
        try:
            with open(SAVE_FILE, "r", encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
                self.categories = data.get("categories", DEFAULT_CATEGORIES.copy())
                self.tags = data.get("tags", [])
        except Exception as e:
            print(f"Error loading tasks: {e}")
            # Create backup of corrupted file
            if os.path.exists(SAVE_FILE):
                backup_name = f"{SAVE_FILE}.backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                try:
                    os.rename(SAVE_FILE, backup_name)
                    print(f"Corrupted file backed up as: {backup_name}")
                except Exception:
                    pass

class TaskItemWidget(QWidget):
    # Define signals for communication with parent
    task_completed = pyqtSignal(object)  # Signal when task completion changes
    task_edit_requested = pyqtSignal(object)  # Signal when edit is requested
    task_delete_requested = pyqtSignal(int)  # Signal when delete is requested
    
    def __init__(self, task, parent=None, theme=DEFAULT_THEME):
        super().__init__(parent)
        self.task = task
        self.theme = theme
        self.main_window = None  # Will be set by parent
        self.setup_ui()
        
        # Apply gradient background
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(THEMES[self.theme]['gradient_start']))
        gradient.setColorAt(1, QColor(THEMES[self.theme]['gradient_end']))
        
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)  # Reduced margins
        layout.setSpacing(10)  # Reduced spacing
        
        # Set minimum height for the widget
        self.setMinimumHeight(100)  # Increased from default
        
        # Checkbox for completion status
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.completed)
        self.checkbox.stateChanged.connect(self.on_completion_changed)
        self.checkbox.setStyleSheet(f"QCheckBox::indicator {{ width: 20px; height: 20px; }}")
        layout.addWidget(self.checkbox)
        
        # Task details container
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(6)
        
        # Title and priority
        title_layout = QHBoxLayout()
        
        # Add task sticker if available
        if hasattr(self.task, 'sticker') and self.task.sticker:
            task_sticker = QLabel(self.task.sticker)
            task_sticker.setStyleSheet("font-size: 18pt; margin-right: 8px;")
            title_layout.addWidget(task_sticker)
        
        # Add completion sticker for completed tasks
        if self.task.completed:
            import random
            completion_sticker = QLabel(random.choice(CELEBRATION_STICKERS))
            completion_sticker.setStyleSheet("font-size: 16pt; margin-right: 5px;")
            title_layout.addWidget(completion_sticker)
        
        self.title_label = QLabel(self.task.title)
        font = QFont("Segoe UI", 11)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setWordWrap(True)  # Enable word wrapping
        self.title_label.setMaximumWidth(300)  # Limit width to prevent overflow
        
        if self.task.completed:
            self.title_label.setStyleSheet(f"color: {THEMES[self.theme]['completed']}; text-decoration: line-through;")
        else:
            self.title_label.setStyleSheet(f"color: {THEMES[self.theme]['text']};")
        
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        # Priority indicator with better sizing
        if self.task.priority != "None":
            priority_color = PRIORITY_LEVELS[self.task.priority]["color"]
            priority_label = QLabel(self.task.priority)
            priority_label.setStyleSheet(f"""
                background-color: {priority_color}; 
                color: white; 
                padding: 4px 8px; 
                border-radius: 4px; 
                font-weight: bold; 
                font-size: 9pt;
                min-width: 50px;
                max-width: 80px;
            """)
            priority_label.setAlignment(Qt.AlignCenter)
            priority_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            title_layout.addWidget(priority_label)
        
        details_layout.addLayout(title_layout)
        
        # Description and metadata
        if self.task.description:
            desc_text = self.task.description[:80] + "..." if len(self.task.description) > 80 else self.task.description
            desc_label = QLabel(desc_text)
            desc_label.setStyleSheet(f"color: {THEMES[self.theme]['secondary']}; font-size: 9pt; margin-top: 2px;")
            desc_label.setWordWrap(True)
            desc_label.setMaximumWidth(350)  # Limit width
            details_layout.addWidget(desc_label)
        
        # Due date and category
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(10)
        
        if self.task.due_date:
            due_date = QDate.fromString(self.task.due_date, Qt.ISODate)
            due_label = QLabel(f"📅 {due_date.toString('MMM d, yyyy')}")
            due_label.setStyleSheet(f"color: {THEMES[self.theme]['accent']}; font-size: 9pt; font-weight: bold; background-color: rgba(200,200,200,0.2); padding: 3px 6px; border-radius: 3px;")
            meta_layout.addWidget(due_label)
        
        category_label = QLabel(f"🏷️ {self.task.category}")
        category_label.setStyleSheet(f"color: {THEMES[self.theme]['accent']}; font-size: 9pt; font-weight: bold; background-color: rgba(200,200,200,0.2); padding: 3px 6px; border-radius: 3px;")
        meta_layout.addWidget(category_label)
        meta_layout.addStretch()
        
        # Progress bar for subtasks
        if self.task.subtasks and len(self.task.subtasks) > 0:
            completed = sum(1 for subtask in self.task.subtasks if subtask["completed"])
            total = len(self.task.subtasks)
            progress = int((completed / total) * 100) if total > 0 else 0
            
            progress_bar = QProgressBar()
            progress_bar.setValue(progress)
            progress_bar.setTextVisible(False)
            progress_bar.setMaximumHeight(8)
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {THEMES[self.theme]['background']};
                    border: none;
                    border-radius: 4px;
                    margin-top: 5px;
                    margin-bottom: 5px;
                }}
                QProgressBar::chunk {{
                    background-color: {THEMES[self.theme]['primary']};
                    border-radius: 4px;
                }}
            """)
            details_layout.addWidget(progress_bar)
        
        details_layout.addLayout(meta_layout)
        layout.addWidget(details_widget)
        
        # Buttons container with vertical layout to save space
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(4)
        
        # Edit and delete buttons with compact styling
        edit_btn = QPushButton("✏️")
        edit_btn.setToolTip("Edit Task")
        edit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEMES[self.theme]['primary']};
                color: white;
                border: none;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12pt;
                min-width: 30px;
                max-width: 30px;
                min-height: 30px;
                max-height: 30px;
            }}
            QPushButton:hover {{
                background-color: {THEMES[self.theme]['secondary']};
            }}
        """)
        edit_btn.clicked.connect(self.on_edit_clicked)
        buttons_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Delete Task")
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #F44336;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12pt;
                min-width: 30px;
                max-width: 30px;
                min-height: 30px;
                max-height: 30px;
            }}
            QPushButton:hover {{
                background-color: #E53935;
            }}
        """)
        delete_btn.clicked.connect(self.on_delete_clicked)
        buttons_layout.addWidget(delete_btn)
        
        layout.addWidget(buttons_widget)
        
        # Set background color based on completion or custom color
        if self.task.color:
            self.setStyleSheet(f"background-color: {self.task.color}; border-radius: 8px; margin: 4px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1);")
        elif self.task.completed:
            self.setStyleSheet(f"background-color: {THEMES[self.theme]['background']}; border-radius: 8px; margin: 4px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1);")
        else:
            self.setStyleSheet(f"background-color: white; border-radius: 8px; margin: 4px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1);")
    
    def on_completion_changed(self, state):
        try:
            self.task.completed = (state == Qt.Checked)
            if self.task.completed:
                self.task.completion_date = datetime.datetime.now().isoformat()
                self.title_label.setStyleSheet(f"color: {THEMES[self.theme]['completed']}; text-decoration: line-through;")
            else:
                self.task.completion_date = None
                self.title_label.setStyleSheet(f"color: {THEMES[self.theme]['text']};")
            
            # Emit signal instead of using fragile parent chain
            self.task_completed.emit(self.task)
        except Exception as e:
            print(f"Error in completion change: {e}")
    
    def on_edit_clicked(self):
        try:
            self.task_edit_requested.emit(self.task)
        except Exception as e:
            print(f"Error in edit request: {e}")
    
    def on_delete_clicked(self):
        try:
            # Create a custom dialog to ensure full control over styling
            from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
            
            dialog = QDialog(self)
            dialog.setWindowTitle("🗑️ Confirm Deletion")
            dialog.setModal(True)
            dialog.resize(350, 150)
            
            # Main layout
            layout = QVBoxLayout(dialog)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Message
            message = QLabel(f"Are you sure you want to delete\n'{self.task.title}'?")
            message.setAlignment(Qt.AlignCenter)
            message.setWordWrap(True)
            message.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #333333;
                    font-weight: bold;
                    padding: 10px;
                }
            """)
            layout.addWidget(message)
            
            # Buttons
            button_layout = QHBoxLayout()
            button_layout.setSpacing(15)
            
            # No button (default)
            no_btn = QPushButton("❌ No")
            no_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
                QPushButton:pressed {
                    background-color: #1e7e34;
                }
            """)
            no_btn.clicked.connect(dialog.reject)
            
            # Yes button
            yes_btn = QPushButton("✅ Yes, Delete")
            yes_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
                QPushButton:pressed {
                    background-color: #bd2130;
                }
            """)
            yes_btn.clicked.connect(dialog.accept)
            
            button_layout.addWidget(no_btn)
            button_layout.addWidget(yes_btn)
            layout.addLayout(button_layout)
            
            # Set dialog styling
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #ffffff;
                    border: 2px solid #cccccc;
                    border-radius: 10px;
                }
            """)
            
            # Show dialog and handle result
            if dialog.exec_() == QDialog.Accepted:
                self.task_delete_requested.emit(self.task.id)
                
        except Exception as e:
            print(f"Error in delete request: {e}")

class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None, categories=None, tags=None, theme=DEFAULT_THEME):
        super().__init__(parent)
        self.task = task
        self.categories = categories if categories else DEFAULT_CATEGORIES
        self.tags = tags if tags else []
        self.theme = theme
        self.setWindowTitle("Add Task" if not task else "Edit Task")
        self.resize(600, 700)  # Increased size
        self.setMinimumSize(600, 700)  # Set minimum size
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout for the dialog
        main_layout = QVBoxLayout(self)
        
        # Create scroll area for the form content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Content widget for scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Task title
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        if self.task:
            self.title_input.setText(self.task.title)
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        content_layout.addLayout(title_layout)
        
        # Task description
        desc_layout = QVBoxLayout()
        desc_label = QLabel("Description:")
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)  # Limit height
        if self.task and self.task.description:
            self.desc_input.setText(self.task.description)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        content_layout.addLayout(desc_layout)
        
        # Due date
        date_layout = QHBoxLayout()
        date_label = QLabel("Due Date:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        if self.task and self.task.due_date:
            self.date_input.setDate(QDate.fromString(self.task.due_date, Qt.ISODate))
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        content_layout.addLayout(date_layout)
        
        # Priority
        priority_layout = QHBoxLayout()
        priority_label = QLabel("Priority:")
        self.priority_combo = QComboBox()
        for priority in PRIORITY_LEVELS.keys():
            self.priority_combo.addItem(priority)
        if self.task:
            self.priority_combo.setCurrentText(self.task.priority)
        priority_layout.addWidget(priority_label)
        priority_layout.addWidget(self.priority_combo)
        content_layout.addLayout(priority_layout)
        
        # Category
        category_layout = QHBoxLayout()
        category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.categories)
        self.category_combo.setEditable(True)
        if self.task:
            self.category_combo.setCurrentText(self.task.category)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        content_layout.addLayout(category_layout)
        
        # Tags
        tags_layout = QVBoxLayout()
        tags_label = QLabel("Tags (comma separated):")
        self.tags_input = QLineEdit()
        if self.task and self.task.tags:
            self.tags_input.setText(", ".join(self.task.tags))
        tags_layout.addWidget(tags_label)
        tags_layout.addWidget(self.tags_input)
        content_layout.addLayout(tags_layout)
        
        # Reminder
        reminder_layout = QHBoxLayout()
        reminder_label = QLabel("Set Reminder:")
        self.reminder_date = QDateEdit()
        self.reminder_date.setCalendarPopup(True)
        self.reminder_date.setDate(QDate.currentDate())
        self.reminder_time = QTimeEdit()
        self.reminder_time.setTime(QTime.currentTime())
        if self.task and self.task.reminder:
            reminder_datetime = datetime.datetime.fromisoformat(self.task.reminder)
            self.reminder_date.setDate(QDate(reminder_datetime.year, reminder_datetime.month, reminder_datetime.day))
            self.reminder_time.setTime(QTime(reminder_datetime.hour, reminder_datetime.minute))
        reminder_layout.addWidget(reminder_label)
        reminder_layout.addWidget(self.reminder_date)
        reminder_layout.addWidget(self.reminder_time)
        content_layout.addLayout(reminder_layout)
        
        # Color picker
        color_layout = QHBoxLayout()
        color_label = QLabel("Task Color:")
        self.color_btn = QPushButton("Choose Color")
        self.color_btn.clicked.connect(self.choose_color)
        self.selected_color = self.task.color if self.task and self.task.color else None
        if self.selected_color:
            self.color_btn.setStyleSheet(f"background-color: {self.selected_color};")
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_btn)
        content_layout.addLayout(color_layout)
        
        # Sticker selection
        sticker_group = QGroupBox("🎨 Choose a Sticker/Emoji")
        sticker_layout = QVBoxLayout(sticker_group)
        
        # Get stickers for current category
        current_category = self.category_combo.currentText() if hasattr(self, 'category_combo') else "Other"
        category_stickers = TASK_STICKERS.get(current_category, TASK_STICKERS["Other"])
        
        # Create sticker buttons grid
        sticker_grid = QHBoxLayout()
        self.selected_sticker = getattr(self.task, 'sticker', None) if self.task else None
        self.sticker_buttons = []
        
        for i, sticker in enumerate(category_stickers):
            sticker_btn = QPushButton(sticker)
            sticker_btn.setFixedSize(40, 40)
            sticker_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    border: 2px solid #cccccc;
                    border-radius: 20px;
                    background-color: #f9f9f9;
                }
                QPushButton:hover {
                    border-color: #007acc;
                    background-color: #e6f3ff;
                }
                QPushButton:checked {
                    border-color: #007acc;
                    background-color: #cce7ff;
                    border-width: 3px;
                }
            """)
            sticker_btn.setCheckable(True)
            sticker_btn.clicked.connect(lambda checked, s=sticker: self.select_sticker(s))
            
            if self.selected_sticker == sticker:
                sticker_btn.setChecked(True)
                
            self.sticker_buttons.append(sticker_btn)
            sticker_grid.addWidget(sticker_btn)
            
            # Add to new row every 5 stickers
            if (i + 1) % 5 == 0:
                sticker_layout.addLayout(sticker_grid)
                sticker_grid = QHBoxLayout()
        
        # Add remaining buttons
        if sticker_grid.count() > 0:
            sticker_layout.addLayout(sticker_grid)
        
        # No sticker option
        no_sticker_btn = QPushButton("❌ No Sticker")
        no_sticker_btn.clicked.connect(lambda: self.select_sticker(None))
        no_sticker_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        sticker_layout.addWidget(no_sticker_btn)
        
        content_layout.addWidget(sticker_group)
        
        # Recurring options
        recurring_layout = QHBoxLayout()
        recurring_label = QLabel("Recurring:")
        self.recurring_combo = QComboBox()
        self.recurring_combo.addItems(["None", "Daily", "Weekly", "Monthly", "Yearly"])
        if self.task and self.task.recurring:
            self.recurring_combo.setCurrentText(self.task.recurring)
        recurring_layout.addWidget(recurring_label)
        recurring_layout.addWidget(self.recurring_combo)
        content_layout.addLayout(recurring_layout)
        
        # Subtasks
        subtasks_group = QGroupBox("Subtasks")
        subtasks_layout = QVBoxLayout(subtasks_group)
        
        self.subtasks_list = QListWidget()
        self.subtasks_list.setMaximumHeight(100)  # Limit height
        if self.task and self.task.subtasks:
            for subtask in self.task.subtasks:
                item = QListWidgetItem(subtask.get("title", ""))
                item.setCheckState(Qt.Checked if subtask.get("completed", False) else Qt.Unchecked)
                self.subtasks_list.addItem(item)
        
        subtasks_btn_layout = QHBoxLayout()
        add_subtask_btn = QPushButton("Add Subtask")
        add_subtask_btn.clicked.connect(self.add_subtask)
        remove_subtask_btn = QPushButton("Remove Selected")
        remove_subtask_btn.clicked.connect(self.remove_subtask)
        
        subtasks_btn_layout.addWidget(add_subtask_btn)
        subtasks_btn_layout.addWidget(remove_subtask_btn)
        
        subtasks_layout.addWidget(self.subtasks_list)
        subtasks_layout.addLayout(subtasks_btn_layout)
        content_layout.addWidget(subtasks_group)
        
        # Notes
        notes_layout = QVBoxLayout()
        notes_label = QLabel("Notes:")
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)  # Limit height
        if self.task and self.task.notes:
            self.notes_input.setText(self.task.notes)
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(self.notes_input)
        content_layout.addLayout(notes_layout)
        
        # Set the content widget to the scroll area
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEMES[self.theme]['primary']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {THEMES[self.theme]['secondary']};
            }}
        """)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #9E9E9E;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #757575;
            }}
        """)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        main_layout.addLayout(buttons_layout)
    
    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color.name()
            self.color_btn.setStyleSheet(f"background-color: {self.selected_color};")
    
    def select_sticker(self, sticker):
        """Handle sticker selection"""
        self.selected_sticker = sticker
        
        # Uncheck all sticker buttons
        for btn in self.sticker_buttons:
            btn.setChecked(False)
        
        # Check the selected sticker button
        if sticker:
            for btn in self.sticker_buttons:
                if btn.text() == sticker:
                    btn.setChecked(True)
                    break
    
    def add_subtask(self):
        title, ok = QInputDialog.getText(self, "Add Subtask", "Subtask title:")
        if ok and title:
            item = QListWidgetItem(title)
            item.setCheckState(Qt.Unchecked)
            self.subtasks_list.addItem(item)
    
    def remove_subtask(self):
        selected_items = self.subtasks_list.selectedItems()
        for item in selected_items:
            self.subtasks_list.takeItem(self.subtasks_list.row(item))
    
    def get_task_data(self):
        title = self.title_input.text()
        description = self.desc_input.toPlainText()
        due_date = self.date_input.date().toString(Qt.ISODate)
        priority = self.priority_combo.currentText()
        category = self.category_combo.currentText()
        tags = [tag.strip() for tag in self.tags_input.text().split(",") if tag.strip()]
        
        reminder_date = self.reminder_date.date()
        reminder_time = self.reminder_time.time()
        reminder = datetime.datetime(
            reminder_date.year(), reminder_date.month(), reminder_date.day(),
            reminder_time.hour(), reminder_time.minute()
        ).isoformat()
        
        subtasks = []
        for i in range(self.subtasks_list.count()):
            item = self.subtasks_list.item(i)
            subtasks.append({
                "title": item.text(),
                "completed": item.checkState() == Qt.Checked
            })
        
        notes = self.notes_input.toPlainText()
        recurring = self.recurring_combo.currentText() if self.recurring_combo.currentText() != "None" else None
        
        if self.task:
            self.task.title = title
            self.task.description = description
            self.task.due_date = due_date
            self.task.priority = priority
            self.task.category = category
            self.task.tags = tags
            self.task.reminder = reminder
            self.task.subtasks = subtasks
            self.task.notes = notes
            self.task.color = self.selected_color
            self.task.recurring = recurring
            self.task.sticker = self.selected_sticker
            return self.task
        else:
            task = Task(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                category=category,
                tags=tags,
                reminder=reminder,
                subtasks=subtasks,
                notes=notes,
                color=self.selected_color,
                recurring=recurring
            )
            task.sticker = self.selected_sticker
            return task

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.current_theme = DEFAULT_THEME
        self.setup_ui()
        self.setup_tray_icon()
        self.setup_reminders()
    
    def setup_ui(self):
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(800, 600)
        
        # Set application style
        self.apply_theme(self.current_theme)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Create header with logo and title
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        app_title = QLabel(APP_NAME)
        app_title.setStyleSheet(f"font-family: 'Segoe UI', 'Roboto', sans-serif; font-size: 32pt; font-weight: bold; color: {THEMES[self.current_theme]['primary']}; letter-spacing: 1px; text-shadow: 2px 2px 3px rgba(0,0,0,0.2);")
        header_layout.addWidget(app_title)
        
        # Theme selector with custom styling
        theme_layout = QHBoxLayout()
        self.theme_label = QLabel("Theme:")
        self.theme_label.setStyleSheet(f"color: {THEMES[self.current_theme]['text']}; font-size: 11pt; font-weight: bold;")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEMES.keys()))
        self.theme_combo.setCurrentText(self.current_theme)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {THEMES[self.current_theme]['background']};
                color: {THEMES[self.current_theme]['text']};
                border: 1px solid {THEMES[self.current_theme]['accent']};
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 120px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
            }}
        """)
        theme_layout.addWidget(self.theme_label)
        theme_layout.addWidget(self.theme_combo)
        header_layout.addLayout(theme_layout)
        
        main_layout.addWidget(header_widget)
        
        # Create tab widget for different views
        self.tabs = QTabWidget()
        
        # All tasks tab with icon
        self.all_tasks_tab = QWidget()
        all_tasks_layout = QVBoxLayout(self.all_tasks_tab)
        
        # Search and filter bar with enhanced styling
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(15)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search tasks...")
        self.search_input.textChanged.connect(self.filter_tasks)
        self.search_input.setMinimumWidth(250)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 12px;
                border-radius: 6px;
                background-color: {THEMES[self.current_theme]['background']};
                border: 1px solid {THEMES[self.current_theme]['accent']};
            }}
        """)
        filter_layout.addWidget(self.search_input)
        
        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet(f"color: {THEMES[self.current_theme]['text']}; font-size: 11pt;")
        filter_layout.addWidget(filter_label)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Completed", "Incomplete", "High Priority", "Medium Priority", "Low Priority", "Overdue"])
        self.filter_combo.currentTextChanged.connect(self.filter_tasks)
        self.filter_combo.setMinimumWidth(150)
        self.filter_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px 12px;
                border-radius: 6px;
                background-color: {THEMES[self.current_theme]['background']};
                border: 1px solid {THEMES[self.current_theme]['accent']};
            }}
        """)
        filter_layout.addWidget(self.filter_combo)
        
        self.sort_label = QLabel("Sort:")
        self.sort_label.setStyleSheet(f"color: {THEMES[self.current_theme]['text']}; font-size: 11pt;")
        filter_layout.addWidget(self.sort_label)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Due Date", "Priority", "Title", "Creation Date", "Category"])
        self.sort_combo.currentTextChanged.connect(self.filter_tasks)
        self.sort_combo.setMinimumWidth(120)
        filter_layout.addWidget(self.sort_combo)
        
        all_tasks_layout.addWidget(filter_widget)
        
        # Tasks list
        self.tasks_list = QListWidget()
        self.tasks_list.setSpacing(5)
        all_tasks_layout.addWidget(self.tasks_list)
        
        # Add task button
        add_task_btn = QPushButton("Add New Task")
        add_task_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEMES[self.current_theme]['primary']};
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {THEMES[self.current_theme]['secondary']};
            }}
        """)
        add_task_btn.clicked.connect(self.add_task)
        all_tasks_layout.addWidget(add_task_btn)
        
        self.tabs.addTab(self.all_tasks_tab, "All Tasks")
        
        # Categories tab
        self.categories_tab = QWidget()
        categories_layout = QVBoxLayout(self.categories_tab)
        
        self.category_tabs = QTabWidget()
        categories_layout.addWidget(self.category_tabs)
        
        self.tabs.addTab(self.categories_tab, f"{BUTTON_ICONS['categories']} Categories")
        
        # Calendar tab
        self.calendar_tab = QWidget()
        calendar_layout = QVBoxLayout(self.calendar_tab)
        
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.on_calendar_clicked)
        self.calendar.setStyleSheet(f"""
            QCalendarWidget {{
                background-color: {THEMES[self.current_theme]['background']};
                color: {THEMES[self.current_theme]['text']};
            }}
            QCalendarWidget QToolButton {{
                color: {THEMES[self.current_theme]['text']};
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: {THEMES[self.current_theme]['accent']};
            }}
            QCalendarWidget QMenu {{
                background-color: {THEMES[self.current_theme]['background']};
                color: {THEMES[self.current_theme]['text']};
            }}
        """)
        calendar_layout.addWidget(self.calendar)
        
        self.calendar_tasks_list = QListWidget()
        self.calendar_tasks_list.setSpacing(5)
        calendar_layout.addWidget(QLabel("Tasks for selected date:"))
        calendar_layout.addWidget(self.calendar_tasks_list)
        
        self.tabs.addTab(self.calendar_tab, f"{BUTTON_ICONS['calendar']} Calendar")
        
        # Statistics tab
        self.stats_tab = QWidget()
        stats_layout = QVBoxLayout(self.stats_tab)
        
        stats_scroll = QScrollArea()
        stats_scroll.setWidgetResizable(True)
        stats_content = QWidget()
        stats_content_layout = QVBoxLayout(stats_content)
        
        # Task completion stats
        completion_group = QGroupBox("Task Completion")
        completion_layout = QVBoxLayout(completion_group)
        
        self.completed_progress = QProgressBar()
        self.completed_progress.setRange(0, 100)
        self.completed_progress.setTextVisible(True)
        completion_layout.addWidget(self.completed_progress)
        
        self.completed_label = QLabel()
        completion_layout.addWidget(self.completed_label)
        
        stats_content_layout.addWidget(completion_group)
        
        # Priority distribution
        priority_group = QGroupBox("Priority Distribution")
        priority_layout = QVBoxLayout(priority_group)
        
        self.high_priority_label = QLabel()
        self.medium_priority_label = QLabel()
        self.low_priority_label = QLabel()
        self.no_priority_label = QLabel()
        
        priority_layout.addWidget(self.high_priority_label)
        priority_layout.addWidget(self.medium_priority_label)
        priority_layout.addWidget(self.low_priority_label)
        priority_layout.addWidget(self.no_priority_label)
        
        stats_content_layout.addWidget(priority_group)
        
        # Category distribution
        category_group = QGroupBox("Category Distribution")
        category_layout = QVBoxLayout(category_group)
        self.category_stats_layout = QVBoxLayout()
        category_layout.addLayout(self.category_stats_layout)
        
        stats_content_layout.addWidget(category_group)
        
        # Time stats
        time_group = QGroupBox("Time Statistics")
        time_layout = QVBoxLayout(time_group)
        
        self.overdue_label = QLabel()
        self.due_today_label = QLabel()
        self.due_this_week_label = QLabel()
        self.no_due_date_label = QLabel()
        
        time_layout.addWidget(self.overdue_label)
        time_layout.addWidget(self.due_today_label)
        time_layout.addWidget(self.due_this_week_label)
        time_layout.addWidget(self.no_due_date_label)
        
        stats_content_layout.addWidget(time_group)
        
        stats_content_layout.addStretch()
        stats_scroll.setWidget(stats_content)
        stats_layout.addWidget(stats_scroll)
        
        self.tabs.addTab(self.stats_tab, "Statistics")
        
        # Settings tab
        self.settings_tab = QWidget()
        settings_layout = QVBoxLayout(self.settings_tab)
        
        # Categories management
        categories_group = QGroupBox("Manage Categories")
        categories_group_layout = QVBoxLayout(categories_group)
        
        self.categories_list = QListWidget()
        self.categories_list.addItems(self.task_manager.categories)
        categories_group_layout.addWidget(self.categories_list)
        
        categories_btn_layout = QHBoxLayout()
        add_category_btn = QPushButton(f"{BUTTON_ICONS['add']} Add Category")
        add_category_btn.clicked.connect(self.add_category)
        add_category_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEMES[self.current_theme]['primary']};
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {THEMES[self.current_theme]['secondary']};
            }}
        """)
        
        remove_category_btn = QPushButton(f"{BUTTON_ICONS['delete']} Remove Selected")
        remove_category_btn.clicked.connect(self.remove_category)
        categories_group_layout.addLayout(categories_btn_layout)
        
        settings_layout.addWidget(categories_group)
        
        # Tags management
        tags_group = QGroupBox("Manage Tags")
        tags_group_layout = QVBoxLayout(tags_group)
        
        self.tags_list = QListWidget()
        self.tags_list.addItems(self.task_manager.tags)
        tags_group_layout.addWidget(self.tags_list)
        
        tags_btn_layout = QHBoxLayout()
        add_tag_btn = QPushButton(f"{BUTTON_ICONS['add']} Add Tag")
        add_tag_btn.clicked.connect(self.add_tag)
        add_tag_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEMES[self.current_theme]['primary']};
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {THEMES[self.current_theme]['secondary']};
            }}
        """)
        
        remove_tag_btn = QPushButton(f"{BUTTON_ICONS['delete']} Remove Selected")
        remove_tag_btn.clicked.connect(self.remove_tag)
        tags_group_layout.addLayout(tags_btn_layout)
        
        settings_layout.addWidget(tags_group)
        
        # Data management
        data_group = QGroupBox("Data Management")
        data_group_layout = QVBoxLayout(data_group)
        
        export_btn = QPushButton("Export Tasks")
        export_btn.clicked.connect(self.export_tasks)
        data_group_layout.addWidget(export_btn)
        
        import_btn = QPushButton("Import Tasks")
        import_btn.clicked.connect(self.import_tasks)
        data_group_layout.addWidget(import_btn)
        
        settings_layout.addWidget(data_group)
        
        self.tabs.addTab(self.settings_tab, "Settings")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Welcome to {APP_NAME}!")
        
        # Set central widget
        self.setCentralWidget(central_widget)
        
        # Populate tasks
        self.refresh_tasks()
    
    def setup_tray_icon(self):
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip(APP_NAME)
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)
        
        add_task_action = QAction("Add Task", self)
        add_task_action.triggered.connect(self.add_task)
        tray_menu.addAction(add_task_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def setup_reminders(self):
        # Setup timer to check for reminders
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(60000)  # Check every minute
    
    def check_reminders(self):
        current_time = datetime.datetime.now()
        for task in self.task_manager.tasks:
            if task.reminder and not task.completed:
                reminder_time = datetime.datetime.fromisoformat(task.reminder)
                time_diff = (reminder_time - current_time).total_seconds()
                if 0 <= time_diff <= 60:  # Within a minute
                    self.show_reminder(task)
    
    def show_reminder(self, task):
        self.tray_icon.showMessage(
            f"Reminder: {task.title}",
            f"Due: {task.due_date if task.due_date else 'No due date'}",
            QSystemTrayIcon.Information,
            5000
        )
    
    def apply_theme(self, theme_name):
        if theme_name not in THEMES:
            theme_name = DEFAULT_THEME
        
        self.current_theme = theme_name
        theme = THEMES[theme_name]
        
        # Apply theme to application
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(theme["background"]))
        palette.setColor(QPalette.WindowText, QColor(theme["text"]))
        palette.setColor(QPalette.Base, QColor("white"))
        palette.setColor(QPalette.AlternateBase, QColor(theme["background"]))
        palette.setColor(QPalette.ToolTipBase, QColor("white"))
        palette.setColor(QPalette.ToolTipText, QColor(theme["text"]))
        palette.setColor(QPalette.Text, QColor(theme["text"]))
        palette.setColor(QPalette.Button, QColor(theme["primary"]))
        palette.setColor(QPalette.ButtonText, QColor("white"))
        palette.setColor(QPalette.BrightText, QColor("red"))
        palette.setColor(QPalette.Highlight, QColor(theme["primary"]))
        palette.setColor(QPalette.HighlightedText, QColor("white"))
        
        self.setPalette(palette)
        
        # Apply stylesheet with improved fonts and styling
        self.setStyleSheet(f"""
            * {{  /* Global font settings */
                font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
                font-size: 11pt;
            }}
            QMainWindow, QDialog {{
                background-color: {theme["background"]};
            }}
            QLabel {{
                font-size: 11pt;
            }}
            QTabWidget::pane {{
                border: 2px solid {theme["accent"]};
                background-color: white;
                border-radius: 8px;
                padding: 5px;
            }}
            QTabBar::tab {{
                background-color: {theme["background"]};
                color: {theme["text"]};
                padding: 10px 12px;
                margin-right: 3px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 11pt;
                font-weight: bold;
                min-width: 100px;
                max-width: 150px;
                text-align: center;
            }}
            QTabBar::tab:selected {{
                background-color: {theme["primary"]};
                color: white;
                font-weight: bold;
                border-bottom: 3px solid {theme["secondary"]};
            }}
            QGroupBox {{
                border: 2px solid {theme["accent"]};
                border-radius: 8px;
                margin-top: 15px;
                font-weight: bold;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.7);
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: {theme["primary"]};
                font-size: 12pt;
                font-weight: bold;
            }}
            QPushButton {{
                background-color: {theme["primary"]};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10pt;
                min-width: 80px;
                max-width: 150px;
            }}
            QPushButton:hover {{
                background-color: {theme["secondary"]};
                transform: scale(1.05);
            }}
            QLineEdit, QTextEdit, QDateEdit, QTimeEdit, QComboBox {{
                border: 2px solid {theme["accent"]};
                border-radius: 6px;
                padding: 8px;
                font-size: 11pt;
                background-color: white;
                min-height: 20px;
            }}
            QComboBox {{
                min-width: 120px;
                max-width: 200px;
            }}
            QProgressBar {{
                border: 2px solid {theme["accent"]};
                border-radius: 4px;
                text-align: center;
                height: 15px;
                font-weight: bold;
                color: white;
                background-color: #f0f0f0;
            }}
            QProgressBar::chunk {{
                background-color: {theme["primary"]};
                border-radius: 4px;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {theme["background"]};
                width: 14px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {theme["accent"]};
                min-height: 30px;
                border-radius: 7px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {theme["background"]};
                height: 14px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {theme["accent"]};
                min-width: 30px;
                border-radius: 7px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
            }}
            QListWidget, QListView, QTreeView, QTableView {{
                border: 2px solid {theme["accent"]};
                border-radius: 6px;
                padding: 5px;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }}
            QListWidget::item:selected, QListView::item:selected {{  
                background-color: {theme["primary"]};
                color: white;
                border-radius: 4px;
            }}
        """)
    
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.apply_theme(theme_name)
        
        # Update all dynamic text colors
        self.theme_label.setStyleSheet(f"color: {THEMES[self.current_theme]['text']}; font-size: 11pt; font-weight: bold;")
        
        # Update theme combo styling
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {THEMES[self.current_theme]['background']};
                color: {THEMES[self.current_theme]['text']};
                border: 1px solid {THEMES[self.current_theme]['accent']};
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 120px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
            }}
        """)
        
        # Update filter and sort labels
        if hasattr(self, 'sort_label'):
            self.sort_label.setStyleSheet(f"color: {THEMES[self.current_theme]['text']}; font-size: 11pt;")
        
        # Update search input styling
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 12px;
                border-radius: 6px;
                background-color: {THEMES[self.current_theme]['background']};
                border: 1px solid {THEMES[self.current_theme]['accent']};
                color: {THEMES[self.current_theme]['text']};
            }}
        """)
        
        # Update filter combo styling
        self.filter_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px 12px;
                border-radius: 6px;
                background-color: {THEMES[self.current_theme]['background']};
                border: 1px solid {THEMES[self.current_theme]['accent']};
                color: {THEMES[self.current_theme]['text']};
            }}
        """)
        
        # Update sort combo styling
        self.sort_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px 12px;
                border-radius: 6px;
                background-color: {THEMES[self.current_theme]['background']};
                border: 1px solid {THEMES[self.current_theme]['accent']};
                color: {THEMES[self.current_theme]['text']};
            }}
        """)
        
        self.refresh_tasks()
    
    def refresh_tasks(self):
        """Optimized task refresh with minimal widget recreation"""
        try:
            # Only clear and rebuild if necessary
            self._update_task_list()
            self._update_category_tabs()
            self._update_calendar_view()
            self._update_statistics()
        except Exception as e:
            print(f"Error refreshing tasks: {e}")
    
    def _update_task_list(self):
        """Update main task list efficiently"""
        # Store current scroll position
        scroll_pos = self.tasks_list.verticalScrollBar().value()
        
        # Clear and repopulate with filtered tasks
        self.tasks_list.clear()
        self.filter_tasks()
        
        # Restore scroll position
        self.tasks_list.verticalScrollBar().setValue(scroll_pos)
    
    def _update_category_tabs(self):
        """Update category tabs only if categories changed"""
        current_categories = [self.category_tabs.tabText(i) for i in range(self.category_tabs.count())]
        
        if set(current_categories) != set(self.task_manager.categories):
            # Categories changed, rebuild tabs
            while self.category_tabs.count() > 0:
                self.category_tabs.removeTab(0)
            
            for category in self.task_manager.categories:
                category_tab = QWidget()
                category_layout = QVBoxLayout(category_tab)
                
                category_list = QListWidget()
                category_list.setSpacing(3)
                category_layout.addWidget(category_list)
                self.category_tabs.addTab(category_tab, category)
        
        # Update tasks in category tabs
        for i, category in enumerate(self.task_manager.categories):
            if i < self.category_tabs.count():
                tab_widget = self.category_tabs.widget(i)
                category_list = tab_widget.findChild(QListWidget)
                if category_list:
                    category_list.clear()
                    
                    # Add tasks for this category
                    category_tasks = [task for task in self.task_manager.tasks if task.category == category]
                    for task in category_tasks[:50]:  # Limit to first 50 for performance
                        item = QListWidgetItem()
                        item.setSizeHint(QSize(0, 110))  # Increased height for better content display
                        task_widget = TaskItemWidget(task, theme=self.current_theme)
                        
                        # Connect signals to handlers
                        task_widget.task_completed.connect(self.on_task_completed)
                        task_widget.task_edit_requested.connect(self.edit_task)
                        task_widget.task_delete_requested.connect(self.on_task_delete_requested)
                        
                        category_list.addItem(item)
                        category_list.setItemWidget(item, task_widget)
    
    def _update_calendar_view(self):
        """Update calendar view efficiently"""
        if hasattr(self, 'calendar') and hasattr(self, 'calendar_tasks_list'):
            self.on_calendar_clicked(self.calendar.selectedDate())
    
    def _update_statistics(self):
        """Update statistics with caching"""
        try:
            cache_key = f"stats_{len(self.task_manager.tasks)}_{self.task_manager._cache_timestamp}"
            
            if hasattr(self, '_stats_cache_key') and self._stats_cache_key == cache_key:
                return  # Stats haven't changed
            
            self._stats_cache_key = cache_key
            self.update_statistics()
        except Exception as e:
            print(f"Error updating statistics: {e}")
    
    def filter_tasks(self):
        self.tasks_list.clear()
        
        search_text = self.search_input.text().lower()
        filter_option = self.filter_combo.currentText()
        sort_option = self.sort_combo.currentText()
        
        # Filter tasks
        filtered_tasks = []
        for task in self.task_manager.tasks:
            # Apply search filter
            if search_text and search_text not in task.title.lower() and search_text not in task.description.lower():
                continue
            
            # Apply status filter
            if filter_option == "Completed" and not task.completed:
                continue
            elif filter_option == "Incomplete" and task.completed:
                continue
            elif filter_option == "High Priority" and task.priority != "High":
                continue
            elif filter_option == "Medium Priority" and task.priority != "Medium":
                continue
            elif filter_option == "Low Priority" and task.priority != "Low":
                continue
            elif filter_option == "Overdue":
                if task.completed or not task.due_date:
                    continue
                due_date = datetime.datetime.fromisoformat(task.due_date).date()
                today = datetime.datetime.now().date()
                if due_date >= today:
                    continue
            
            filtered_tasks.append(task)
        
        # Sort tasks
        if sort_option == "Due Date":
            filtered_tasks.sort(key=lambda t: t.due_date if t.due_date else "9999-12-31")
        elif sort_option == "Priority":
            filtered_tasks.sort(key=lambda t: PRIORITY_LEVELS[t.priority]["value"], reverse=True)
        elif sort_option == "Title":
            filtered_tasks.sort(key=lambda t: t.title.lower())
        elif sort_option == "Creation Date":
            filtered_tasks.sort(key=lambda t: t.created_at)
        elif sort_option == "Category":
            filtered_tasks.sort(key=lambda t: t.category)
        
        # Add filtered tasks to list
        for task in filtered_tasks:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 120))  # Increased height for better content display
            task_widget = TaskItemWidget(task, theme=self.current_theme)
            
            # Connect signals to handlers
            task_widget.task_completed.connect(self.on_task_completed)
            task_widget.task_edit_requested.connect(self.edit_task)
            task_widget.task_delete_requested.connect(self.on_task_delete_requested)
            
            self.tasks_list.addItem(item)
            self.tasks_list.setItemWidget(item, task_widget)
    
    def on_calendar_clicked(self, date):
        self.calendar_tasks_list.clear()
        date_str = date.toString(Qt.ISODate)
        
        # Find tasks for the selected date
        for task in self.task_manager.tasks:
            if task.due_date == date_str:
                item = QListWidgetItem()
                item.setSizeHint(QSize(0, 120))  # Increased height for better content display
                task_widget = TaskItemWidget(task, theme=self.current_theme)
                
                # Connect signals to handlers
                task_widget.task_completed.connect(self.on_task_completed)
                task_widget.task_edit_requested.connect(self.edit_task)
                task_widget.task_delete_requested.connect(self.on_task_delete_requested)
                
                self.calendar_tasks_list.addItem(item)
                self.calendar_tasks_list.setItemWidget(item, task_widget)
    
    def update_statistics(self):
        # Task completion stats
        total_tasks = len(self.task_manager.tasks)
        completed_tasks = len(self.task_manager.get_completed_tasks())
        completion_percentage = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
        
        self.completed_progress.setValue(completion_percentage)
        self.completed_label.setText(f"Completed: {completed_tasks} out of {total_tasks} tasks ({completion_percentage}%)")
        
        # Priority distribution
        high_priority = len(self.task_manager.get_tasks_by_priority("High"))
        medium_priority = len(self.task_manager.get_tasks_by_priority("Medium"))
        low_priority = len(self.task_manager.get_tasks_by_priority("Low"))
        no_priority = len(self.task_manager.get_tasks_by_priority("None"))
        
        self.high_priority_label.setText(f"High Priority: {high_priority} tasks")
        self.medium_priority_label.setText(f"Medium Priority: {medium_priority} tasks")
        self.low_priority_label.setText(f"Low Priority: {low_priority} tasks")
        self.no_priority_label.setText(f"No Priority: {no_priority} tasks")
        
        # Clear category stats layout
        while self.category_stats_layout.count():
            item = self.category_stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Category distribution
        for category in self.task_manager.categories:
            category_tasks = len(self.task_manager.get_tasks_by_category(category))
            category_label = QLabel(f"{category}: {category_tasks} tasks")
            self.category_stats_layout.addWidget(category_label)
        
        # Time stats
        today = datetime.datetime.now().date().isoformat()
        week_end = (datetime.datetime.now() + datetime.timedelta(days=7)).date().isoformat()
        
        overdue_tasks = len(self.task_manager.get_overdue_tasks())
        due_today = len([task for task in self.task_manager.tasks if not task.completed and task.due_date == today])
        due_this_week = len([task for task in self.task_manager.tasks if not task.completed and 
                            task.due_date and today < task.due_date <= week_end])
        no_due_date = len([task for task in self.task_manager.tasks if not task.due_date])
        
        self.overdue_label.setText(f"Overdue: {overdue_tasks} tasks")
        self.due_today_label.setText(f"Due Today: {due_today} tasks")
        self.due_this_week_label.setText(f"Due This Week: {due_this_week} tasks")
        self.no_due_date_label.setText(f"No Due Date: {no_due_date} tasks")
    
    def on_task_completed(self, task):
        """Handle task completion signal with celebration"""
        try:
            self.task_manager.update_task(task.id, task)
            self.refresh_tasks()
            
            if task.completed:
                self.show_completion_celebration(task)
            else:
                status_msg = f"Task '{task.title}' marked as incomplete!"
                self.status_bar.showMessage(status_msg, 3000)
        except Exception as e:
            print(f"Error updating task completion: {e}")
    
    def show_completion_celebration(self, task):
        """Show celebration animation and message for completed task"""
        try:
            from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
            from PyQt5.QtCore import QTimer
            import datetime
            
            # Determine completion timing
            completion_type = "general"
            if task.due_date:
                try:
                    due_date = datetime.datetime.fromisoformat(task.due_date).date()
                    today = datetime.datetime.now().date()
                    
                    if today < due_date:
                        completion_type = "early"
                    elif today == due_date:
                        completion_type = "on_time"
                    else:
                        completion_type = "late"
                except:
                    completion_type = "general"
            
            # Select random celebration message and sticker
            import random
            celebration_msg = random.choice(CELEBRATION_MESSAGES[completion_type])
            celebration_sticker = random.choice(CELEBRATION_STICKERS)
            
            # Create celebration dialog
            celebration_dialog = QDialog(self)
            celebration_dialog.setWindowTitle(f"{celebration_sticker} Task Completed!")
            celebration_dialog.setModal(False)  # Non-blocking
            celebration_dialog.resize(400, 200)
            celebration_dialog.setStyleSheet("""
                QDialog {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #FFD700, stop:0.5 #FFA500, stop:1 #FF6347);
                    border-radius: 15px;
                    border: 3px solid #FFD700;
                }
            """)
            
            layout = QVBoxLayout(celebration_dialog)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Big celebration sticker
            sticker_label = QLabel(celebration_sticker)
            sticker_label.setAlignment(Qt.AlignCenter)
            sticker_label.setStyleSheet("""
                QLabel {
                    font-size: 48px;
                    background: transparent;
                    padding: 10px;
                }
            """)
            layout.addWidget(sticker_label)
            
            # Celebration message
            message_label = QLabel(celebration_msg)
            message_label.setAlignment(Qt.AlignCenter)
            message_label.setWordWrap(True)
            message_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    background: transparent;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                    padding: 10px;
                }
            """)
            layout.addWidget(message_label)
            
            # Task title
            task_label = QLabel(f"\"{ task.title}\"")
            task_label.setAlignment(Qt.AlignCenter)
            task_label.setWordWrap(True)
            task_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-style: italic;
                    color: #333333;
                    background: rgba(255,255,255,0.8);
                    border-radius: 8px;
                    padding: 8px;
                }
            """)
            layout.addWidget(task_label)
            
            # Show dialog
            celebration_dialog.show()
            
            # Auto-close after 4 seconds
            QTimer.singleShot(4000, celebration_dialog.close)
            
            # Update status bar
            status_msg = f"{celebration_sticker} Task '{task.title}' completed! {celebration_sticker}"
            self.status_bar.showMessage(status_msg, 5000)
            
        except Exception as e:
            print(f"Error showing celebration: {e}")
            # Fallback to simple message
            status_msg = f"Task '{task.title}' completed!"
            self.status_bar.showMessage(status_msg, 3000)
    
    def on_task_delete_requested(self, task_id):
        """Handle task deletion signal"""
        try:
            if self.task_manager.delete_task(task_id):
                self.refresh_tasks()
                self.status_bar.showMessage("Task deleted successfully!", 3000)
        except Exception as e:
            print(f"Error deleting task: {e}")
    
    def add_task(self):
        dialog = TaskDialog(self, categories=self.task_manager.categories, 
                          tags=self.task_manager.tags, theme=self.current_theme)
        if dialog.exec_():
            task = dialog.get_task_data()
            self.task_manager.add_task(task)
            self.refresh_tasks()
            self.status_bar.showMessage(f"Task '{task.title}' added successfully!", 3000)
    
    def edit_task(self, task):
        dialog = TaskDialog(self, task=task, categories=self.task_manager.categories, 
                          tags=self.task_manager.tags, theme=self.current_theme)
        if dialog.exec_():
            updated_task = dialog.get_task_data()
            self.task_manager.update_task(task.id, updated_task)
            self.refresh_tasks()
            self.status_bar.showMessage(f"Task '{task.title}' updated successfully!", 3000)
    
    def add_category(self):
        category, ok = QInputDialog.getText(self, "Add Category", "Category name:")
        if ok and category:
            if self.task_manager.add_category(category):
                self.categories_list.addItem(category)
                self.refresh_tasks()
                self.status_bar.showMessage(f"Category '{category}' added successfully!", 3000)
            else:
                QMessageBox.warning(self, "Warning", f"Category '{category}' already exists!")
    
    def remove_category(self):
        selected_items = self.categories_list.selectedItems()
        if not selected_items:
            return
        
        category = selected_items[0].text()
        if category in DEFAULT_CATEGORIES[:3]:  # Protect default categories
            QMessageBox.warning(self, "Warning", f"Cannot remove default category '{category}'!")
            return
        
        confirm = QMessageBox.question(self, "Confirm Deletion", 
                                      f"Are you sure you want to delete category '{category}'?",
                                      QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            # Update tasks with this category
            for task in self.task_manager.tasks:
                if task.category == category:
                    task.category = "Other"
                    self.task_manager.update_task(task.id, task)
            
            # Remove category
            self.task_manager.categories.remove(category)
            self.task_manager.save_tasks()
            self.categories_list.takeItem(self.categories_list.row(selected_items[0]))
            self.refresh_tasks()
            self.status_bar.showMessage(f"Category '{category}' removed successfully!", 3000)
    
    def add_tag(self):
        tag, ok = QInputDialog.getText(self, "Add Tag", "Tag name:")
        if ok and tag:
            if self.task_manager.add_tag(tag):
                self.tags_list.addItem(tag)
                self.status_bar.showMessage(f"Tag '{tag}' added successfully!", 3000)
            else:
                QMessageBox.warning(self, "Warning", f"Tag '{tag}' already exists!")
    
    def remove_tag(self):
        selected_items = self.tags_list.selectedItems()
        if not selected_items:
            return
        
        tag = selected_items[0].text()
        confirm = QMessageBox.question(self, "Confirm Deletion", 
                                      f"Are you sure you want to delete tag '{tag}'?",
                                      QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            # Remove tag from all tasks
            for task in self.task_manager.tasks:
                if tag in task.tags:
                    task.tags.remove(tag)
                    self.task_manager.update_task(task.id, task)
            
            # Remove tag
            self.task_manager.tags.remove(tag)
            self.task_manager.save_tasks()
            self.tags_list.takeItem(self.tags_list.row(selected_items[0]))
            self.status_bar.showMessage(f"Tag '{tag}' removed successfully!", 3000)
    
    def export_tasks(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Tasks", "", "JSON Files (*.json)")
        if file_path:
            try:
                data = {
                    "tasks": [task.to_dict() for task in self.task_manager.tasks],
                    "categories": self.task_manager.categories,
                    "tags": self.task_manager.tags
                }
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
                self.status_bar.showMessage(f"Tasks exported successfully to {file_path}!", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export tasks: {str(e)}")
    
    def import_tasks(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Tasks", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    
                    # Import tasks
                    imported_tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
                    self.task_manager.tasks = imported_tasks
                    
                    # Import categories and tags
                    if "categories" in data:
                        self.task_manager.categories = data["categories"]
                    if "tags" in data:
                        self.task_manager.tags = data["tags"]
                    
                    self.task_manager.save_tasks()
                    self.refresh_tasks()
                    self.status_bar.showMessage(f"Tasks imported successfully from {file_path}!", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import tasks: {str(e)}")

    def closeEvent(self, event):
        # Hide to system tray instead of closing
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Show splash screen
    splash_pixmap = QPixmap(400, 300)
    splash_pixmap.fill(QColor(THEMES[DEFAULT_THEME]["primary"]))
    splash = QSplashScreen(splash_pixmap)
    splash.show()
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Close splash screen
    splash.finish(window)
    
    sys.exit(app.exec_())