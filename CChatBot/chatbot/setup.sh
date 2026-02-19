#!/bin/bash

# ============================================================================
# Career Advisor Chatbot - Setup Script for macOS/Linux
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Career Advisor Chatbot - Setup Script                         ║"
echo "║  Python Environment Configuration                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "✓ Python is installed"
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d venv ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install requirements
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠ .env file created. Please edit it and add your GEMINI_API_KEY"
else
    echo "✓ .env file already exists"
fi
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Setup Complete!                                               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Edit the .env file and add your GEMINI_API_KEY"
echo "   Get API key from: https://aistudio.google.com/app/apikeys"
echo ""
echo "2. Run the application:"
echo "   streamlit run app.py"
echo ""
