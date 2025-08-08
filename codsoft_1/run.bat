@echo off
echo Starting TaskMaster Pro...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.6 or higher.
    pause
    exit /b 1
)

:: Check if requirements are installed
echo Checking dependencies...
pip install -r requirements.txt

:: Run the application
echo Launching TaskMaster Pro...
python main.py

pause