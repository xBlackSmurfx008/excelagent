#!/bin/bash

# AI Thinking Agent Launcher
# Spins up the real AI thinking agent with OpenAI API

echo "🧠 AI THINKING AGENT LAUNCHER"
echo "=============================="
echo "🎯 Spinning up real AI thinking agent"
echo "🔄 Using OpenAI API for deep analysis"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "ai_thinking_agent.py" ]; then
    echo "❌ Error: ai_thinking_agent.py not found"
    echo "   Please run this from the Excel Agent directory"
    exit 1
fi

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "   Please run setup first"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo "   Please set your OpenAI API key:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "   Or create a .env file with:"
    echo "   OPENAI_API_KEY=your-api-key-here"
    echo ""
    read -p "Enter your OpenAI API key now: " api_key
    if [ -n "$api_key" ]; then
        export OPENAI_API_KEY="$api_key"
        echo "✅ API key set for this session"
    else
        echo "❌ No API key provided. Cannot proceed."
        exit 1
    fi
fi

# Check for OP document
if [ ! -f "Knowledge Base/op-ncb-reconciliation-8-28-25.md" ]; then
    echo "❌ Error: OP document not found"
    echo "   Expected: Knowledge Base/op-ncb-reconciliation-8-28-25.md"
    exit 1
fi

echo "✅ All requirements met!"
echo ""

# Run the AI thinking task
echo "🚀 LAUNCHING AI THINKING AGENT"
echo "=============================="
echo "🎯 This will perform 10 thinking sequences"
echo "⏱️  This may take several minutes..."
echo ""

python3 run_ai_thinking_task.py

echo ""
echo "🎉 AI THINKING TASK COMPLETE!"
echo "=============================="
echo "✅ Check the generated files for results"
echo "✅ AI agent has been retrained"
echo "✅ Ready for enhanced reconciliation"
