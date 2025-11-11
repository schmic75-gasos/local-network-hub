#!/bin/bash

# Local Network Hub Startup Script

echo "🏠 Starting Local Network Hub..."
echo ""

# Check if Python 3 is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""

# Get local IP address
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")

echo "🚀 Starting server..."
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  🏠 Local Network Hub"
echo "═══════════════════════════════════════════════════════════"
echo "  📱 Access from this device:"
echo "     http://localhost:5000"
echo ""
echo "  🌐 Access from other devices on your network:"
echo "     http://$LOCAL_IP:5000"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Start the server
python server.py
