#!/bin/bash

# Content Marketing Agent - Local Startup Script

echo "🚀 Content Marketing Agent - Local Testing"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "app_production.py" ]; then
    echo "❌ Error: app_production.py not found"
    echo "Please run this script from the content-marketing-agent directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found"
    echo "Please install Python 3.7+ to continue"
    exit 1
fi

echo "✅ Using Python: $($PYTHON_CMD --version)"

# Check if streamlit is installed
if ! $PYTHON_CMD -c "import streamlit" 2>/dev/null; then
    echo "⚠️ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Run health check
echo ""
echo "🔍 Running health check..."
$PYTHON_CMD health_check.py

echo ""
echo "🎯 Choose what to do:"
echo "1. 🚀 Launch Production App (Recommended)"
echo "2. 🧪 Run Interactive Tests"
echo "3. 📱 Launch Original App"
echo "4. 🎨 Launch Modern UI App"
echo "5. ❌ Exit"

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "🚀 Launching Production App..."
        echo "📱 Opening at: http://localhost:8501"
        echo "⚠️ Press Ctrl+C to stop"
        streamlit run app_production.py
        ;;
    2)
        echo "🧪 Starting Interactive Tests..."
        $PYTHON_CMD test_local.py
        ;;
    3)
        echo "📱 Launching Original App..."
        streamlit run app.py
        ;;
    4)
        echo "🎨 Launching Modern UI App..."
        streamlit run app_modern.py
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Launching Production App by default..."
        streamlit run app_production.py
        ;;
esac