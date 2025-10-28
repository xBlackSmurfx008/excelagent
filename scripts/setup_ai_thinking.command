#!/bin/bash

# AI Thinking Agent Setup
# Configures the environment for AI thinking agent

echo "🧠 AI THINKING AGENT SETUP"
echo "=========================="
echo "🎯 Setting up environment for AI thinking"
echo "🔄 Configuring OpenAI API access"
echo "=========================="
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

# Check if OpenAI is installed
echo "🔍 Checking OpenAI installation..."
python3 -c "import openai; print('✅ OpenAI installed')" 2>/dev/null || {
    echo "❌ OpenAI not installed. Installing..."
    pip install openai
}

# Check for existing API key
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ OpenAI API key already set"
    echo "🎉 Ready to run AI thinking agent!"
    echo ""
    echo "🚀 To run the AI thinking agent:"
    echo "   ./Launch_AI_Thinking.command"
    echo "   or"
    echo "   python3 run_ai_thinking_task.py"
else
    echo "⚠️  OpenAI API key not set"
    echo ""
    echo "🔑 To get your OpenAI API key:"
    echo "   1. Go to https://platform.openai.com/api-keys"
    echo "   2. Create a new API key"
    echo "   3. Copy the key"
    echo ""
    echo "💾 To set your API key:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "📁 Or create a .env file with:"
    echo "   OPENAI_API_KEY=your-api-key-here"
    echo ""
    echo "🚀 After setting the API key, run:"
    echo "   ./Launch_AI_Thinking.command"
fi

echo ""
echo "📋 AI THINKING AGENT TASK:"
echo "=========================="
echo "✅ Load OP document from Knowledge Base"
echo "✅ Perform 10 thinking sequences with OpenAI"
echo "✅ Extract insights from each sequence"
echo "✅ Generate comprehensive retraining report"
echo "✅ Save all results to files"
echo ""
echo "📊 EXPECTED OUTPUTS:"
echo "• ai_thinking_sequences_TIMESTAMP.json"
echo "• ai_thinking_insights_TIMESTAMP.json"
echo "• ai_thinking_summary_TIMESTAMP.txt"
echo ""
echo "🎯 READY TO SPIN UP AI THINKING AGENT!"
