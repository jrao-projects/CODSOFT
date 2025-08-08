# Advanced GUI Calculator

A feature-rich, modern calculator application built with Python and Tkinter, featuring a colorful interface and advanced mathematical operations.

## Description

This Advanced Calculator is a powerful yet user-friendly application that goes beyond basic arithmetic calculations. It features a modern, eye-catching graphical interface with customizable themes, animations, and a comprehensive set of mathematical functions. The calculator is designed to be both visually appealing and highly functional, suitable for students, professionals, and anyone needing quick calculations with advanced features.

## Features

### Core Functionality
- **Basic Arithmetic**: Addition, subtraction, multiplication, division
- **Advanced Operations**: 
  - Square root (√)
  - Squaring (x²)
  - Reciprocal (1/x)
  - Factorial (n!)
  - Percentage (%)
  - Sign toggle (±)
  - Parentheses for grouping expressions

### Mathematical Functions
- **Trigonometry**: Sine, cosine, tangent (in degrees)
- **Logarithms**: Base-10 logarithm (log) and natural logarithm (ln)
- **Exponents**: Power operation (x^y)
- **Modulo**: Modulus operation (mod)
- **Constants**: π (pi) and e (Euler's number)
- **Random**: Generate random numbers between 0 and 1

### Memory Operations
- **M+**: Add current value to memory
- **M-**: Subtract current value from memory
- **MR**: Recall stored memory value

### Interface Features
- **Modern Design**: Colorful, eye-catching interface with dark theme
- **Customizable Themes**: Change colors for all UI elements
- **Animated Buttons**: Function buttons with color animations
- **Expression Display**: Shows full calculation before execution
- **Error Handling**: Clear error messages for invalid operations
- **Calculation History**: Track all calculations with timestamps

### Additional Features
- **Menu System**: Organized access to all features
- **Help Documentation**: Built-in instructions and about dialog
- **Persistent Themes**: Save and load custom color themes
- **Responsive Layout**: Adapts to different screen sizes

## How to Use

### Basic Operations
1. Enter numbers using the digit buttons (0-9)
2. Select an operation (+, -, *, /)
3. Enter the second number
4. Press "=" to calculate the result

### Advanced Functions
1. Enter a number
2. Select the desired function (√, x², 1/x, etc.)
3. The result will be calculated automatically

### Memory Operations
1. Perform a calculation
2. Use "M+" to add the result to memory or "M-" to subtract
3. Use "MR" to recall the stored memory value at any time

### Customizing Themes
1. Go to "Theme" > "Change Colors" in the menu
2. Select which UI element to customize
3. Click "Choose Color" to pick a new color
4. Click "Apply Theme" to save changes

### Viewing History
1. Go to "File" > "History" in the menu
2. View all previous calculations with timestamps
3. Use "Clear History" to reset the history log

## Technologies Used

- **Python 3**: Core programming language
- **Tkinter**: Standard GUI library for Python
- **Math Module**: For mathematical functions and constants
- **Random Module**: For random number generation
- **JSON**: For saving and loading theme configurations
- **DateTime**: For timestamping calculation history
- **OS Module**: For file operations

## Installation & Running

1. **Prerequisites**:
   - Python 3.6 or higher installed on your system
   - No additional packages required (uses only standard library)

2. **Running the Calculator**:
   ```bash
   python advanced_calculator.py