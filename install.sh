#!/bin/bash

# ChatBot-Therapist Installation Script
# This script installs the therapy chatbot and its dependencies

set -e

echo "🧠 ChatBot-Therapist Installation Script"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️ Ollama is not installed. Installing Ollama..."
    
    # Detect OS and install Ollama
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            echo "❌ Homebrew not found. Please install Homebrew first or install Ollama manually from https://ollama.ai/download"
            exit 1
        fi
    else
        echo "❌ Unsupported OS. Please install Ollama manually from https://ollama.ai/download"
        exit 1
    fi
else
    echo "✅ Ollama is already installed"
fi

# Start Ollama service
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Pull Mistral model
echo "📥 Downloading Mistral model (this may take a while)..."
ollama pull mistral

# Stop Ollama service
kill $OLLAMA_PID

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To start the therapy chatbot:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Start Ollama: ollama serve"
echo "3. Run the app: python main.py"
echo ""
echo "The app will open automatically in your browser at http://127.0.0.1:5000"
echo ""
echo "For more information, see the README.md file." 