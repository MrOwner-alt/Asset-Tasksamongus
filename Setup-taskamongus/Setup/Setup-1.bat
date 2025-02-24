@echo off
:MENU
cls
echo ========================================
echo            Game Setup Menu
echo ========================================
echo 1. Install Python packages      (Pygame)
echo 2. install python               (Python)
echo 3. Run the game            (Launcher.py)
echo 4. Exit               (Exit The Program)
echo ========================================
set /p choice="Select an option (1-4): "

if "%choice%"=="1" (
    echo Installing Python packages...
    pip install pygame requests
    echo Packages installed successfully!
    pause
    goto MENU
) else if "%choice%"=="3" (
    echo Running the game...
    python launcher.py
    pause
    goto MENU
) else if "%choice%"=="4" (
    echo Exiting...
    exit
) else if "%choice%"=="2" (
    start https://www.python.org/downloads/
    goto MENU
) else (
    echo Invalid option! Please try again.
    pause
    goto MENU
)
