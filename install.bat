@echo off
setlocal enabledelayedexpansion

echo 🧠 ChatBot-Therapist Installation Script
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8 or higher first.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
echo 📚 Installing Python dependencies...
pip install -r requirements.txt

REM Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Ollama is not installed. Please install Ollama manually from https://ollama.ai/download
    echo After installing Ollama, run this script again.
    pause
    exit /b 1
) else (
    echo ✅ Ollama is already installed
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo To start the therapy chatbot:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Start Ollama: ollama serve
echo 3. Run the app: python main.py
echo.
echo The app will open automatically in your browser at http://127.0.0.1:5000
echo.
echo For more information, see the README.md file.
pause 