#!/usr/bin/env python3
"""
Excel Agent Web Dashboard
Simple web interface for easy reconciliation analysis
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from pathlib import Path
import subprocess
import threading
import time

app = Flask(__name__)

class ExcelAgentDashboard:
    """Web dashboard for Excel Agent"""
    
    def __init__(self):
        self.analysis_running = False
        self.last_analysis = None
        self.results = {}
    
    def run_analysis(self):
        """Run the auto-reconciliation analysis"""
        if self.analysis_running:
            return {"status": "already_running"}
        
        self.analysis_running = True
        
        try:
            # Run the auto-reconciliation script
            result = subprocess.run([
                "python", "auto_reconciliation.py"
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            # Load results
            report_file = Path("reconciliation_analysis_report.json")
            if report_file.exists():
                with open(report_file, 'r') as f:
                    self.results = json.load(f)
                self.last_analysis = time.time()
            
            return {
                "status": "success",
                "output": result.stdout,
                "results": self.results
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            self.analysis_running = False

# Initialize dashboard
dashboard = ExcelAgentDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/run-analysis', methods=['POST'])
def run_analysis():
    """API endpoint to run analysis"""
    result = dashboard.run_analysis()
    return jsonify(result)

@app.route('/api/status')
def get_status():
    """Get current analysis status"""
    return jsonify({
        "running": dashboard.analysis_running,
        "last_analysis": dashboard.last_analysis,
        "has_results": bool(dashboard.results)
    })

@app.route('/api/results')
def get_results():
    """Get analysis results"""
    return jsonify(dashboard.results)

@app.route('/api/files')
def get_files():
    """Get list of Excel files in data folder"""
    data_folder = Path("data")
    if not data_folder.exists():
        return jsonify({"files": []})
    
    files = []
    for file_path in data_folder.glob("*.xlsx"):
        files.append({
            "name": file_path.name,
            "size": file_path.stat().st_size,
            "modified": file_path.stat().st_mtime
        })
    
    return jsonify({"files": files})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Create basic HTML template
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Excel Agent Dashboard</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .status {
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .results {
            margin-top: 20px;
        }
        .file-list {
            list-style: none;
            padding: 0;
        }
        .file-list li {
            padding: 10px;
            background: #f8f9fa;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 3px solid #667eea;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Excel Agent Dashboard</h1>
            <p>Automated Reconciliation Analysis System</p>
        </div>
        
        <div class="content">
            <div class="card">
                <h2>📊 Quick Analysis</h2>
                <p>Run a complete reconciliation analysis on all Excel files in your data folder.</p>
                <button class="btn" id="runAnalysisBtn" onclick="runAnalysis()">
                    🚀 Run Analysis
                </button>
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing your data...</p>
                </div>
                <div id="status"></div>
            </div>
            
            <div class="card">
                <h2>📁 Data Files</h2>
                <p>Excel files found in your data folder:</p>
                <ul class="file-list" id="fileList">
                    <li>Loading files...</li>
                </ul>
            </div>
            
            <div class="card results" id="results" style="display: none;">
                <h2>📈 Analysis Results</h2>
                <div id="resultsContent"></div>
            </div>
        </div>
    </div>

    <script>
        // Load files on page load
        window.onload = function() {
            loadFiles();
            checkStatus();
        };

        function loadFiles() {
            fetch('/api/files')
                .then(response => response.json())
                .then(data => {
                    const fileList = document.getElementById('fileList');
                    if (data.files.length === 0) {
                        fileList.innerHTML = '<li>No Excel files found in data folder</li>';
                    } else {
                        fileList.innerHTML = data.files.map(file => 
                            `<li>📄 ${file.name} (${(file.size / 1024).toFixed(1)} KB)</li>`
                        ).join('');
                    }
                });
        }

        function runAnalysis() {
            const btn = document.getElementById('runAnalysisBtn');
            const loading = document.getElementById('loading');
            const status = document.getElementById('status');
            
            btn.disabled = true;
            loading.style.display = 'block';
            status.innerHTML = '<div class="status info">Starting analysis...</div>';
            
            fetch('/api/run-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                btn.disabled = false;
                
                if (data.status === 'success') {
                    status.innerHTML = '<div class="status success">✅ Analysis completed successfully!</div>';
                    showResults(data.results);
                } else if (data.status === 'already_running') {
                    status.innerHTML = '<div class="status info">⏳ Analysis already running...</div>';
                } else {
                    status.innerHTML = `<div class="status error">❌ Error: ${data.message || 'Unknown error'}</div>`;
                }
            })
            .catch(error => {
                loading.style.display = 'none';
                btn.disabled = false;
                status.innerHTML = `<div class="status error">❌ Error: ${error.message}</div>`;
            });
        }

        function showResults(results) {
            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');
            
            if (results && results.discrepancies_found > 0) {
                resultsContent.innerHTML = `
                    <div class="status error">
                        <h3>🚨 ${results.discrepancies_found} Discrepancies Found</h3>
                        <ul>
                            ${results.discrepancies.map(d => `<li>${d.description}</li>`).join('')}
                        </ul>
                    </div>
                `;
            } else {
                resultsContent.innerHTML = `
                    <div class="status success">
                        <h3>✅ No Discrepancies Found</h3>
                        <p>All GL accounts are balanced correctly.</p>
                    </div>
                `;
            }
            
            resultsDiv.style.display = 'block';
        }

        function checkStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    if (data.running) {
                        document.getElementById('runAnalysisBtn').disabled = true;
                        document.getElementById('loading').style.display = 'block';
                    }
                });
        }

        // Check status every 5 seconds
        setInterval(checkStatus, 5000);
    </script>
</body>
</html>
    """
    
    with open(templates_dir / "dashboard.html", "w") as f:
        f.write(html_template)
    
    print("🚀 Starting Excel Agent Dashboard...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
