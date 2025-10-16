#!/bin/bash

# Setup script for the Google ADK A2A Multi-Agent System

echo "Setting up Google ADK A2A Multi-Agent System..."
echo "=============================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 10 ]); then
    echo "Error: Python 3.10 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi

echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠ Please edit .env file with your configuration"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p logs

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x scripts/*.sh

echo ""
echo "=============================================="
echo "Setup complete! 🎉"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Google Cloud credentials"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Start the agents: ./scripts/start_all_agents.sh"
echo "4. Try the example client: python client_example.py"
echo ""
echo "For more information, see README.md"

