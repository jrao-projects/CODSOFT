import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import math
import random
import time
from datetime import datetime
import json
import os

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        
        # Initialize variables
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.expression_var = tk.StringVar()
        self.history = []
        self.memory = 0
        self.theme = self.load_theme()
        self.last_calculation_time = 0
        self.angle_mode = "DEG"  # DEG, RAD, GRAD
        
        # Create UI
        self.create_ui()
        
        # Apply theme
        self.apply_theme()
        
        # Add animation
        self.animate_buttons()
    
    def load_theme(self):
        # Ultra vibrant neon theme
        theme = {
            "bg": "#0a0014",          # Deep dark purple
            "display_bg": "#1a0033",   # Dark purple
            "button_bg": "#2d1b69",    # Medium purple
            "button_fg": "#ffffff",    # White text
            "operator_bg": "#ff006e",  # Hot pink
            "operator_fg": "#ffffff",  # White text
            "function_bg": "#00f5ff",  # Bright cyan
            "function_fg": "#000000",  # Black text for contrast
            "equal_bg": "#ffbe0b",     # Bright yellow
            "equal_fg": "#000000",     # Black text for contrast
            "clear_bg": "#fb5607",     # Bright orange
            "clear_fg": "#ffffff",     # White text
            "mode_bg": "#8338ec",      # Purple
            "mode_fg": "#ffffff",      # White text
            "font": "Arial",
            "font_size": 14
        }
        
        # Try to load saved theme
        try:
            if os.path.exists("calculator_theme.json"):
                with open("calculator_theme.json", "r") as f:
                    saved_theme = json.load(f)
                    theme.update(saved_theme)
        except:
            pass
        
        return theme
    
    def save_theme(self):
        try:
            with open("calculator_theme.json", "w") as f:
                json.dump(self.theme, f)
        except:
            pass
    
    def apply_theme(self):
        self.root.configure(bg=self.theme["bg"])
        
        # Apply theme to all widgets
        for widget in self.root.winfo_children():
            self.apply_theme_to_widget(widget)
    
    def apply_theme_to_widget(self, widget):
        widget_class = widget.winfo_class()
        
        if widget_class == "Frame":
            widget.configure(bg=self.theme["bg"])
            for child in widget.winfo_children():
                self.apply_theme_to_widget(child)
        elif widget_class == "Label":
            widget.configure(bg=self.theme["display_bg"], fg=self.theme["button_fg"])
        elif widget_class == "Entry":
            widget.configure(bg=self.theme["display_bg"], fg=self.theme["button_fg"], 
                             insertbackground=self.theme["button_fg"])
        elif widget_class == "Button":
            # Determine button type and apply appropriate style
            text = widget.cget("text")
            if text in ["=", "ENTER"]:
                widget.configure(bg=self.theme["equal_bg"], fg=self.theme["equal_fg"])
            elif text in ["C", "CE", "⌫", "AC", "DEL"]:
                widget.configure(bg=self.theme["clear_bg"], fg=self.theme["clear_fg"])
            elif text in ["+", "-", "×", "÷", "±", "%", "π", "e", "x²", "x³", "√", "x√y", "1/x", "n!"]:
                widget.configure(bg=self.theme["operator_bg"], fg=self.theme["operator_fg"])
            elif text in ["sin", "cos", "tan", "sin⁻¹", "cos⁻¹", "tan⁻¹", "log", "ln", "logₐ", "x^y", "mod", "rand"]:
                widget.configure(bg=self.theme["function_bg"], fg=self.theme["function_fg"])
            elif text in ["DEG", "RAD", "GRAD", "hyp", "SHIFT", "ALPHA", "MODE", "ON"]:
                widget.configure(bg=self.theme["mode_bg"], fg=self.theme["mode_fg"])
            else:
                widget.configure(bg=self.theme["button_bg"], fg=self.theme["button_fg"])
    
    def create_ui(self):
        # Create main frames
        self.top_frame = tk.Frame(self.root, bg=self.theme["bg"])
        self.top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.display_frame = tk.Frame(self.root, bg=self.theme["bg"])
        self.display_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.mode_frame = tk.Frame(self.root, bg=self.theme["bg"])
        self.mode_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.button_frame = tk.Frame(self.root, bg=self.theme["bg"])
        self.button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create mode display
        self.mode_label = tk.Label(
            self.mode_frame, 
            text=f"Angle: {self.angle_mode}", 
            font=(self.theme["font"], 10),
            bg=self.theme["display_bg"],
            fg=self.theme["button_fg"],
            anchor="w",
            padx=10
        )
        self.mode_label.pack(fill=tk.X)
        
        # Create display
        self.expression_label = tk.Label(
            self.display_frame, 
            textvariable=self.expression_var, 
            font=(self.theme["font"], 12),
            bg=self.theme["display_bg"],
            fg=self.theme["button_fg"],
            anchor="e",
            pady=5
        )
        self.expression_label.pack(fill=tk.X)
        
        self.result_entry = tk.Entry(
            self.display_frame, 
            textvariable=self.result_var, 
            font=(self.theme["font"], 24),
            bg=self.theme["display_bg"],
            fg=self.theme["button_fg"],
            justify="right",
            bd=0,
            highlightthickness=0
        )
        self.result_entry.pack(fill=tk.X, ipady=10)
        
        # Create buttons
        self.create_buttons()
        
        # Create menu
        self.create_menu()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="History", command=self.show_history)
        file_menu.add_command(label="Clear History", command=self.clear_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Change Colors", command=self.change_theme_colors)
        theme_menu.add_command(label="Reset Theme", command=self.reset_theme)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_buttons(self):
        # Button layout - Casio fx-991ES PLUS inspired
        button_layout = [
            ["SHIFT", "MODE", "ON", "AC", "DEL"],
            ["x⁻¹", "x²", "x³", "x^", "√"],
            ["log", "ln", "logₐ", "x√y", "x!"],
            ["sin", "cos", "tan", "sin⁻¹", "cos⁻¹"],
            ["tan⁻¹", "hyp", "DEG", "RAD", "GRAD"],
            ["(", ")", ",", "M+", "M-"],
            ["7", "8", "9", "÷", "×"],
            ["4", "5", "6", "+", "-"],
            ["1", "2", "3", "Ans", "0"],
            [".", "EXP", "(-)", "π", "e"],
            ["%", "mod", "rand", "MR", "="]
        ]
        
        # Create buttons
        for i, row in enumerate(button_layout):
            for j, btn_text in enumerate(row):
                # Create a frame for each button to control its size
                btn_frame = tk.Frame(self.button_frame, bg=self.theme["bg"])
                btn_frame.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                
                # Make the button expand to fill the frame
                btn = tk.Button(
                    btn_frame,
                    text=btn_text,
                    font=(self.theme["font"], self.theme["font_size"]),
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda text=btn_text: self.on_button_click(text)
                )
                btn.pack(fill=tk.BOTH, expand=True)
                
                # Configure grid weights for resizing - all columns equal
                self.button_frame.grid_columnconfigure(j, weight=1)
            self.button_frame.grid_rowconfigure(i, weight=1)
    
    def on_button_click(self, text):
        current_time = time.time()
        
        # Prevent multiple rapid clicks
        if current_time - self.last_calculation_time < 0.1:
            return
        
        self.last_calculation_time = current_time
        
        # Handle special buttons
        if text == "=":
            self.calculate()
        elif text == "AC":
            self.clear_all()
        elif text == "DEL":
            self.backspace()
        elif text == "SHIFT":
            # Shift functionality would go here
            self.expression_var.set("SHIFT mode activated")
        elif text == "MODE":
            # Mode functionality would go here
            self.expression_var.set("MODE menu")
        elif text == "ON":
            # Clear calculator
            self.clear_all()
        elif text == "DEG":
            self.angle_mode = "DEG"
            self.mode_label.config(text=f"Angle: {self.angle_mode}")
        elif text == "RAD":
            self.angle_mode = "RAD"
            self.mode_label.config(text=f"Angle: {self.angle_mode}")
        elif text == "GRAD":
            self.angle_mode = "GRAD"
            self.mode_label.config(text=f"Angle: {self.angle_mode}")
        elif text == "x⁻¹":
            self.reciprocal()
        elif text == "x²":
            self.square()
        elif text == "x³":
            self.cube()
        elif text == "x^":
            self.append_to_input("^")
        elif text == "√":
            self.square_root()
        elif text == "x√y":
            self.append_to_input("x√(")
        elif text == "log":
            self.logarithm(10)
        elif text == "ln":
            self.logarithm(math.e)
        elif text == "logₐ":
            self.append_to_input("log(")
        elif text == "x!":
            self.factorial()
        elif text == "sin":
            self.trig_function("sin")
        elif text == "cos":
            self.trig_function("cos")
        elif text == "tan":
            self.trig_function("tan")
        elif text == "sin⁻¹":
            self.inverse_trig_function("asin")
        elif text == "cos⁻¹":
            self.inverse_trig_function("acos")
        elif text == "tan⁻¹":
            self.inverse_trig_function("atan")
        elif text == "hyp":
            # Hyperbolic mode would go here
            self.expression_var.set("Hyperbolic mode")
        elif text == "Ans":
            self.append_to_input(str(self.result_var.get()))
        elif text == "EXP":
            self.append_to_input("E")
        elif text == "(-)":
            self.toggle_sign()
        elif text == "π":
            self.append_to_input(str(math.pi))
        elif text == "e":
            self.append_to_input(str(math.e))
        elif text == "%":
            self.percentage()
        elif text == "mod":
            self.append_to_input("%")
        elif text == "rand":
            self.random_number()
        elif text == "M+":
            self.memory_add()
        elif text == "M-":
            self.memory_subtract()
        elif text == "MR":
            self.memory_recall()
        elif text == "×":
            self.append_to_input("*")
        elif text == "÷":
            self.append_to_input("/")
        else:
            self.append_to_input(text)
    
    def append_to_input(self, value):
        self.current_input += str(value)
        self.result_var.set(self.current_input)
        self.expression_var.set(self.current_input)
    
    def clear_all(self):
        self.current_input = ""
        self.result_var.set("0")
        self.expression_var.set("")
    
    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.result_var.set(self.current_input if self.current_input else "0")
        self.expression_var.set(self.current_input)
    
    def toggle_sign(self):
        if self.current_input and self.current_input[0] == "-":
            self.current_input = self.current_input[1:]
        else:
            self.current_input = "-" + self.current_input
        self.result_var.set(self.current_input)
        self.expression_var.set(self.current_input)
    
    def square_root(self):
        try:
            value = float(self.current_input)
            result = math.sqrt(value)
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"√({value}) = {result}")
            self.add_to_history(f"√({value})", result)
        except:
            self.result_var.set("Error")
            self.expression_var.set("Invalid input for square root")
    
    def square(self):
        try:
            value = float(self.current_input)
            result = value ** 2
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"({value})² = {result}")
            self.add_to_history(f"({value})²", result)
        except:
            self.result_var.set("Error")
            self.expression_var.set("Invalid input for square")
    
    def cube(self):
        try:
            value = float(self.current_input)
            result = value ** 3
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"({value})³ = {result}")
            self.add_to_history(f"({value})³", result)
        except:
            self.result_var.set("Error")
            self.expression_var.set("Invalid input for cube")
    
    def reciprocal(self):
        try:
            value = float(self.current_input)
            if value == 0:
                raise ZeroDivisionError
            result = 1 / value
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"1/({value}) = {result}")
            self.add_to_history(f"1/({value})", result)
        except:
            self.result_var.set("Error")
            self.expression_var.set("Cannot divide by zero")
    
    def factorial(self):
        try:
            value = int(float(self.current_input))
            if value < 0:
                raise ValueError
            result = math.factorial(value)
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"{value}! = {result}")
            self.add_to_history(f"{value}!", result)
        except:
            self.result_var.set("Error")
            self.expression_var.set("Invalid input for factorial")
    
    def trig_function(self, func):
        try:
            value = float(self.current_input)
            
            if self.angle_mode == "DEG":
                radians = math.radians(value)
            elif self.angle_mode == "RAD":
                radians = value
            else:  # GRAD
                radians = value * (math.pi / 200)
            
            if func == "sin":
                result = math.sin(radians)
            elif func == "cos":
                result = math.cos(radians)
            elif func == "tan":
                result = math.tan(radians)
            
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"{func}({value}) = {result}")
            self.add_to_history(f"{func}({value})", result)
        except:
            self.result_var.set("Error")
            self.expression_var.set(f"Invalid input for {func}")
    
    def inverse_trig_function(self, func):
        try:
            value = float(self.current_input)
            
            if func == "asin":
                result = math.asin(value)
            elif func == "acos":
                result = math.acos(value)
            elif func == "atan":
                result = math.atan(value)
            
            # Convert result to current angle mode
            if self.angle_mode == "DEG":
                result = math.degrees(result)
            elif self.angle_mode == "GRAD":
                result = result * (200 / math.pi)
            
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"{func}⁻¹({value}) = {result}")
            self.add_to_history(f"{func}⁻¹({value})", result)
        except:
            self.result_var.set("Error")
            self.expression_var.set(f"Invalid input for {func}")
    
    def logarithm(self, base):
        try:
            value = float(self.current_input)
            if value <= 0:
                raise ValueError
            result = math.log(value, base)
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            
            if base == 10:
                self.expression_var.set(f"log({value}) = {result}")
                self.add_to_history(f"log({value})", result)
            else:
                self.expression_var.set(f"ln({value}) = {result}")
                self.add_to_history(f"ln({value})", result)
        except:
            self.result_var.set("Error")
            self.expression_var.set("Invalid input for logarithm")
    
    def percentage(self):
        try:
            value = float(self.current_input)
            result = value / 100
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"{value}% = {result}")
            self.add_to_history(f"{value}%", result)
        except:
            self.result_var.set("Error")
            self.expression_var.set("Invalid input for percentage")
    
    def random_number(self):
        result = random.random()
        self.current_input = str(result)
        self.result_var.set(self.current_input)
        self.expression_var.set(f"rand() = {result}")
        self.add_to_history("rand()", result)
    
    def memory_add(self):
        try:
            value = float(self.current_input)
            self.memory += value
            self.expression_var.set(f"M+ {value}")
        except:
            self.expression_var.set("Invalid input for M+")
    
    def memory_subtract(self):
        try:
            value = float(self.current_input)
            self.memory -= value
            self.expression_var.set(f"M- {value}")
        except:
            self.expression_var.set("Invalid input for M-")
    
    def memory_recall(self):
        self.current_input = str(self.memory)
        self.result_var.set(self.current_input)
        self.expression_var.set(f"MR = {self.memory}")
    
    def calculate(self):
        try:
            # Replace ^ with ** for exponentiation
            expression = self.current_input.replace("^", "**")
            
            # Evaluate expression
            result = eval(expression)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.current_input = str(result)
            self.result_var.set(self.current_input)
            self.expression_var.set(f"{expression} = {result}")
            self.add_to_history(expression, result)
        except ZeroDivisionError:
            self.result_var.set("Error")
            self.expression_var.set("Cannot divide by zero")
        except:
            self.result_var.set("Error")
            self.expression_var.set("Invalid expression")
    
    def add_to_history(self, expression, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            "expression": expression,
            "result": result,
            "timestamp": timestamp
        })
    
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("500x400")
        
        # Create frame for history
        frame = tk.Frame(history_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for history
        tree = ttk.Treeview(frame, columns=("expression", "result", "timestamp"), show="headings")
        tree.heading("expression", text="Expression")
        tree.heading("result", text="Result")
        tree.heading("timestamp", text="Timestamp")
        
        tree.column("expression", width=200)
        tree.column("result", width=100)
        tree.column("timestamp", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Add history data
        for item in self.history:
            tree.insert("", "end", values=(item["expression"], item["result"], item["timestamp"]))
        
        # Add buttons
        btn_frame = tk.Frame(history_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        clear_btn = tk.Button(btn_frame, text="Clear History", command=self.clear_history)
        clear_btn.pack(side="left", padx=5)
        
        close_btn = tk.Button(btn_frame, text="Close", command=history_window.destroy)
        close_btn.pack(side="right", padx=5)
    
    def clear_history(self):
        self.history = []
        messagebox.showinfo("History Cleared", "Calculation history has been cleared.")
    
    def change_theme_colors(self):
        color_options = [
            ("Background", "bg"),
            ("Display Background", "display_bg"),
            ("Button Background", "button_bg"),
            ("Button Text", "button_fg"),
            ("Operator Background", "operator_bg"),
            ("Operator Text", "operator_fg"),
            ("Function Background", "function_bg"),
            ("Function Text", "function_fg"),
            ("Equal Button", "equal_bg"),
            ("Equal Text", "equal_fg"),
            ("Clear Button", "clear_bg"),
            ("Clear Text", "clear_fg"),
            ("Mode Button", "mode_bg"),
            ("Mode Text", "mode_fg")
        ]
        
        color_window = tk.Toplevel(self.root)
        color_window.title("Customize Theme")
        color_window.geometry("400x550")
        
        frame = tk.Frame(color_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        color_buttons = {}
        
        for i, (label, key) in enumerate(color_options):
            tk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
            
            color_display = tk.Label(frame, width=10, bg=self.theme[key])
            color_display.grid(row=i, column=1, padx=5, pady=5)
            
            btn = tk.Button(
                frame, 
                text="Choose Color",
                command=lambda k=key, d=color_display: self.choose_color(k, d)
            )
            btn.grid(row=i, column=2, padx=5, pady=5)
            
            color_buttons[key] = color_display
        
        # Apply button
        apply_btn = tk.Button(
            frame,
            text="Apply Theme",
            command=lambda: self.apply_theme_changes(color_window)
        )
        apply_btn.grid(row=len(color_options), column=0, columnspan=3, pady=20)
    
    def choose_color(self, key, display):
        color = colorchooser.askcolor(initialcolor=self.theme[key])
        if color[1]:
            self.theme[key] = color[1]
            display.config(bg=color[1])
    
    def apply_theme_changes(self, window):
        self.apply_theme()
        self.save_theme()
        window.destroy()
        messagebox.showinfo("Theme Applied", "Theme has been applied and saved.")
    
    def reset_theme(self):
        self.theme = self.load_theme()
        self.apply_theme()
        self.save_theme()
        messagebox.showinfo("Theme Reset", "Theme has been reset to default.")
    
    def show_instructions(self):
        instructions = """
Advanced Scientific Calculator Instructions:
Basic Operations:
- Use +, -, ×, ÷ for basic arithmetic
- Press = to calculate
- Use AC to clear all, DEL to backspace
Advanced Functions:
- x⁻¹: Reciprocal
- x²: Square
- x³: Cube
- x^: Exponentiation
- √: Square root
- x√y: nth root
- log: Base 10 logarithm
- ln: Natural logarithm
- logₐ: Logarithm with custom base
- x!: Factorial
Trigonometric Functions:
- sin, cos, tan: Trigonometric functions
- sin⁻¹, cos⁻¹, tan⁻¹: Inverse trigonometric functions
- DEG, RAD, GRAD: Angle modes
Other Features:
- %: Percentage
- mod: Modulo operation
- rand: Random number between 0 and 1
- EXP: Scientific notation
- (-): Toggle sign
- π, e: Mathematical constants
- Ans: Previous result
Memory Functions:
- M+: Add to memory
- M-: Subtract from memory
- MR: Recall memory
Menu Options:
- File: View history, clear history, exit
- Theme: Customize colors, reset theme
- Help: Instructions, about
        """
        messagebox.showinfo("Instructions", instructions)
    
    def show_about(self):
        about_text = """
Advanced Scientific Calculator v2.0
A feature-rich scientific calculator inspired by Casio fx-991ES PLUS.
Features:
- Basic arithmetic operations
- Advanced mathematical functions
- Trigonometric and inverse trigonometric functions
- Logarithms with different bases
- Factorials and permutations
- Memory operations
- Calculation history
- Customizable themes
- Ultra-vibrant neon interface
Created with Python and Tkinter.
        """
        messagebox.showinfo("About", about_text)
    
    def animate_buttons(self):
        # Ultra vibrant color animation for buttons
        colors = ["#ff006e", "#fb5607", "#ffbe0b", "#8338ec", "#3a86ff", "#06ffa5", "#ff4365", "#00f5ff"]
        color_index = 0
        
        def change_color():
            nonlocal color_index
            color_index = (color_index + 1) % len(colors)
            
            # Apply to function buttons
            for widget in self.button_frame.winfo_children():
                if widget.winfo_class() == "Frame":
                    for child in widget.winfo_children():
                        if child.winfo_class() == "Button":
                            text = child.cget("text")
                            if text in ["sin", "cos", "tan", "sin⁻¹", "cos⁻¹", "tan⁻¹", "log", "ln", "logₐ", "x^y", "mod", "rand"]:
                                child.config(bg=colors[color_index])
            
            self.root.after(400, change_color)  # Faster animation
        
        change_color()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop(),m