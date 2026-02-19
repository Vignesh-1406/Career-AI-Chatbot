@echo off
REM ============================================================================
REM Career Advisor Chatbot - Setup Script for Windows
REM ============================================================================

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  Career Advisor Chatbot - Setup Script                         ║
echo ║  Python Environment Configuration                              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python is installed
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo ✓ pip upgraded
echo.

REM Install requirements
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo ⚠ .env file created. Please edit it and add your GEMINI_API_KEY
) else (
    echo ✓ .env file already exists
)
echo.

REM Summary
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  Setup Complete!                                               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo 1. Edit the .env file and add your GEMINI_API_KEY
echo    Get API key from: https://aistudio.google.com/app/apikeys
echo.
echo 2. Run the application:
echo    streamlit run app.py
echo.
pause
