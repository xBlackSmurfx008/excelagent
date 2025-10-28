#!/bin/bash
# Unified Excel Agent Dashboard Launcher
# Single command to launch the complete system

echo "🤖 Excel Agent - Unified Dashboard Launcher"
echo "============================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if we're in the right directory
if [ ! -f "unified_dashboard.py" ]; then
    echo "❌ Error: unified_dashboard.py not found in $SCRIPT_DIR"
    echo "💡 Make sure the file exists in the Excel Agent folder"
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "💡 Please install Python 3 first"
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install --upgrade pip >/dev/null 2>&1 || true
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt >/dev/null 2>&1
    else
        pip install flask flask-socketio pandas openpyxl >/dev/null 2>&1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment found"
    source venv/bin/activate
    echo "📦 Verifying dependencies..."
    python - <<'PY'
try:
    import flask, flask_socketio, pandas, openpyxl
    print('deps-ok')
except Exception:
    print('deps-missing')
PY
    if [ "$(python - <<'PY'
try:
    import flask, flask_socketio, pandas, openpyxl
    print('ok')
except Exception:
    print('missing')
PY
)" = "missing" ]; then
        echo "📦 Installing missing dependencies..."
        pip install --upgrade pip >/dev/null 2>&1 || true
        if [ -f requirements.txt ]; then
            pip install -r requirements.txt >/dev/null 2>&1
        else
            pip install flask flask-socketio pandas openpyxl >/dev/null 2>&1
        fi
    fi
fi

# Check if required directories exist
if [ ! -d "uploads" ]; then
    echo "📁 Creating uploads folder..."
    mkdir uploads
    echo "✅ Uploads folder created"
fi

if [ ! -d "data" ]; then
    echo "📁 Creating data folder..."
    mkdir data
    echo "✅ Data folder created"
fi

if [ ! -d "templates" ]; then
    echo "📁 Creating templates folder..."
    mkdir templates
    echo "✅ Templates folder created"
fi

# Kill any existing processes on common ports
echo "🔧 Checking for existing processes..."
for port in 5000 5001 5002 5003 5004 5005; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Killing process on port $port"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
done

# Wait a moment for ports to be released
sleep 2

# Check for available port
PORT=5001
MAX_ATTEMPTS=10
ATTEMPT=0
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 && [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    echo "⚠️  Port $PORT is in use, trying port $((PORT+1))"
    PORT=$((PORT+1))
    ATTEMPT=$((ATTEMPT+1))
    sleep 1
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo "❌ Error: Could not find available port after $MAX_ATTEMPTS attempts"
    echo "💡 Please manually kill processes using ports 5001-5010"
    read -p "Press Enter to continue..."
    exit 1
fi

echo ""
echo "🚀 Starting Unified Excel Agent Dashboard..."
echo "📱 Features:"
echo "   • 📁 Drag & drop file upload"
echo "   • 💬 Chat with AI agent"
echo "   • 📈 Real-time activity timeline"
echo "   • 🔍 Automatic discrepancy detection"
echo "   • 📊 Live analysis monitoring"
echo ""
echo "🌐 Opening web browser..."
echo "📱 Dashboard URL: http://localhost:$PORT"
open "http://localhost:$PORT" >/dev/null 2>&1 || true
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Set the port as an environment variable
export EXCEL_AGENT_PORT=$PORT

# Start the unified dashboard
python3 unified_dashboard.py
