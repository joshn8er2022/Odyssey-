#!/bin/bash

echo "🎯 Starting Content Marketing Agent..."
echo "📱 The app will open at: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
streamlit run app.py --server.port 8501 --server.address localhost --browser.gatherUsageStats false