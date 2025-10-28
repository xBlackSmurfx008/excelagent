# Excel Agent - Installation and Setup Guide

## 🚀 **QUICK START**

### **Prerequisites**
- Python 3.8 or higher
- 4GB RAM minimum
- 1GB free disk space
- Windows, macOS, or Linux

### **Installation Steps**
```bash
# 1. Clone the repository
git clone <repository-url>
cd excel-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python src/excel_agent/api/dashboard.py
```

### **Access the Dashboard**
- Open browser to: `http://localhost:5000`
- Upload GL and Bank files
- Run reconciliation analysis

---

## 📋 **DETAILED INSTALLATION**

### **System Requirements**

#### **Hardware Requirements**
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB for application and reports
- **Network**: Local network access (optional)

#### **Software Requirements**
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Browser**: Chrome, Firefox, Safari, or Edge (for dashboard)

### **Python Dependencies**

#### **Core Dependencies**
```python
# Data processing
pandas>=1.3.0
numpy>=1.20.0
openpyxl>=3.0.0

# Web framework
flask>=2.0.0
flask-socketio>=5.0.0

# Built-in modules
difflib
pathlib
datetime
json
re
```

#### **Development Dependencies**
```python
# Testing
pytest>=6.0.0
pytest-cov>=2.10.0

# Code quality
black>=21.0.0
flake8>=3.8.0
mypy>=0.800

# Documentation
sphinx>=4.0.0
sphinx-rtd-theme>=0.5.0
```

### **Installation Methods**

#### **Method 1: Using pip**
```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install individual packages
pip install pandas numpy openpyxl flask flask-socketio
```

#### **Method 2: Using conda**
```bash
# Create conda environment
conda create -n excel-agent python=3.9
conda activate excel-agent

# Install packages
conda install pandas numpy openpyxl
pip install flask flask-socketio
```

#### **Method 3: Using Docker**
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "src/excel_agent/api/dashboard.py"]
```

```bash
# Build and run
docker build -t excel-agent .
docker run -p 5000:5000 excel-agent
```

---

## 🔧 **CONFIGURATION**

### **Environment Variables**

#### **Required Variables**
```bash
# Application settings
export FLASK_APP=src/excel_agent/api/dashboard.py
export FLASK_ENV=development  # or production
export PYTHONPATH=/path/to/excel-agent/src:$PYTHONPATH
```

#### **Optional Variables**
```bash
# File paths
export UPLOAD_DIR=uploads
export REPORTS_DIR=data/reports
export LOGS_DIR=logs

# Performance settings
export MAX_WORKERS=4
export CHUNK_SIZE=1000
export TIMEOUT=300
```

### **Configuration Files**

#### **config.py**
```python
import os

class Config:
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_DIR') or 'uploads'
    REPORTS_FOLDER = os.environ.get('REPORTS_DIR') or 'data/reports'
    
    # Performance settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 4))
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 1000))
    TIMEOUT = int(os.environ.get('TIMEOUT', 300))
    
    # Matching parameters
    EXACT_AMOUNT_TOLERANCE = 0.01
    PARTIAL_AMOUNT_TOLERANCE = 0.05
    DATE_TOLERANCE_DAYS = 3
    DESCRIPTION_SIMILARITY_THRESHOLD = 0.6
    TARGET_MATCH_RATE = 80.0
```

#### **requirements.txt**
```txt
# Core dependencies
pandas>=1.3.0
numpy>=1.20.0
openpyxl>=3.0.0
flask>=2.0.0
flask-socketio>=5.0.0

# Optional dependencies
python-dotenv>=0.19.0
gunicorn>=20.1.0
```

---

## 📁 **DIRECTORY STRUCTURE**

### **Project Layout**
```
excel-agent/
├── src/
│   └── excel_agent/
│       ├── __init__.py
│       ├── api/
│       │   └── dashboard.py
│       └── core/
│           ├── reconciliation_framework.py
│           └── A_ai_reconciliation_agent.py
├── data/
│   └── reports/
│       ├── detailed_audit_reconciliation_*.json
│       └── detailed_matches_*.csv
├── uploads/
│   ├── gl_activity_*.xlsx
│   └── bank_statement_*.xlsx
├── docs/
│   ├── README.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   └── INSTALLATION_GUIDE.md
├── scripts/
│   ├── enhanced_ncb_reconciliation_agent.py
│   ├── detailed_audit_reconciliation_agent.py
│   └── ncb_gl_reconciliation_agent.py
├── tests/
│   ├── test_reconciliation_framework.py
│   ├── test_matching_strategies.py
│   └── test_audit_trail.py
├── requirements.txt
├── requirements-dev.txt
├── config.py
├── README.md
└── .gitignore
```

### **Directory Descriptions**

#### **src/excel_agent/**
Core application code
- **api/**: Web interface and API endpoints
- **core/**: Core reconciliation logic and frameworks

#### **data/reports/**
Generated reconciliation reports
- **JSON reports**: Complete audit trail and analysis
- **CSV reports**: Spreadsheet-friendly match details

#### **uploads/**
Input files for reconciliation
- **GL files**: General Ledger activity files
- **Bank files**: Bank statement files

#### **docs/**
Documentation and guides
- **README.md**: Main project documentation
- **TECHNICAL_ARCHITECTURE.md**: Technical implementation details
- **INSTALLATION_GUIDE.md**: This installation guide

#### **scripts/**
Standalone reconciliation agents
- **enhanced_ncb_reconciliation_agent.py**: Iterative matching agent
- **detailed_audit_reconciliation_agent.py**: Audit trail agent
- **ncb_gl_reconciliation_agent.py**: Basic reconciliation agent

#### **tests/**
Unit and integration tests
- **test_reconciliation_framework.py**: Framework tests
- **test_matching_strategies.py**: Strategy tests
- **test_audit_trail.py**: Audit trail tests

---

## 🚀 **RUNNING THE APPLICATION**

### **Development Mode**

#### **Dashboard Application**
```bash
# Start the web dashboard
python src/excel_agent/api/dashboard.py

# Access at http://localhost:5000
```

#### **Standalone Agents**
```bash
# Run enhanced reconciliation agent
python scripts/enhanced_ncb_reconciliation_agent.py

# Run detailed audit agent
python scripts/detailed_audit_reconciliation_agent.py

# Run basic reconciliation agent
python scripts/ncb_gl_reconciliation_agent.py
```

### **Production Mode**

#### **Using Gunicorn**
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.excel_agent.api.dashboard:app
```

#### **Using Docker**
```bash
# Build image
docker build -t excel-agent .

# Run container
docker run -d -p 5000:5000 --name excel-agent excel-agent
```

#### **Using systemd (Linux)**
```ini
# /etc/systemd/system/excel-agent.service
[Unit]
Description=Excel Agent Reconciliation Service
After=network.target

[Service]
Type=simple
User=excel-agent
WorkingDirectory=/opt/excel-agent
ExecStart=/opt/excel-agent/venv/bin/python src/excel_agent/api/dashboard.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable excel-agent
sudo systemctl start excel-agent
```

---

## 📊 **USAGE EXAMPLES**

### **Basic Usage**

#### **1. Upload Files**
- Navigate to `http://localhost:5000`
- Upload GL activity file (Excel format)
- Upload bank statement file (Excel format)
- Click "Run Reconciliation"

#### **2. View Results**
- Review match statistics
- Download reconciliation reports
- Analyze unmatched transactions

### **Advanced Usage**

#### **1. Command Line Interface**
```bash
# Run enhanced reconciliation
python scripts/enhanced_ncb_reconciliation_agent.py

# Run with specific files
python scripts/detailed_audit_reconciliation_agent.py \
    --gl-file uploads/gl_activity.xlsx \
    --bank-file uploads/bank_statement.xlsx
```

#### **2. Programmatic Usage**
```python
from src.excel_agent.core.reconciliation_framework import ReconciliationFramework
from pathlib import Path

# Initialize framework
framework = ReconciliationFramework()

# Run reconciliation
gl_files = [Path('uploads/gl_activity.xlsx')]
bank_file = Path('uploads/bank_statement.xlsx')

result = framework.perform_reconciliation(gl_files, bank_file)

# Process results
if result['status'] == 'success':
    matches = result['data']['matches']
    summary = result['data']['summary']
    print(f"Found {len(matches)} matches")
    print(f"Match rate: {summary['match_rate']:.1f}%")
```

#### **3. Custom Configuration**
```python
from scripts.enhanced_ncb_reconciliation_agent import EnhancedNCBReconciliationAgent

# Create agent with custom settings
agent = EnhancedNCBReconciliationAgent()
agent.target_match_rate = 90.0  # Set higher target
agent.matching_strategies[0]['tolerance'] = 0.005  # Tighter tolerance

# Run reconciliation
result = agent.run_enhanced_reconciliation(gl_file, bank_file)
```

---

## 🔍 **TROUBLESHOOTING**

### **Common Issues**

#### **1. Import Errors**
```bash
# Error: ModuleNotFoundError: No module named 'excel_agent'
# Solution: Set PYTHONPATH
export PYTHONPATH=/path/to/excel-agent/src:$PYTHONPATH
```

#### **2. File Permission Errors**
```bash
# Error: Permission denied when writing reports
# Solution: Check directory permissions
chmod 755 data/reports/
chmod 755 uploads/
```

#### **3. Memory Issues**
```bash
# Error: MemoryError during processing
# Solution: Increase memory or process smaller chunks
export MAX_WORKERS=2
export CHUNK_SIZE=500
```

#### **4. Port Already in Use**
```bash
# Error: Address already in use
# Solution: Use different port
python src/excel_agent/api/dashboard.py --port 5001
```

### **Debug Mode**

#### **Enable Debug Logging**
```python
import logging

# Set up debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/debug.log'),
        logging.StreamHandler()
    ]
)
```

#### **Verbose Output**
```bash
# Run with verbose output
python scripts/enhanced_ncb_reconciliation_agent.py --verbose

# Run with debug mode
python src/excel_agent/api/dashboard.py --debug
```

---

## 📈 **PERFORMANCE TUNING**

### **Optimization Settings**

#### **Memory Optimization**
```python
# Reduce memory usage
CHUNK_SIZE = 500  # Process smaller chunks
MAX_WORKERS = 2   # Reduce parallel workers
CACHE_SIZE = 100  # Limit cache size
```

#### **Processing Optimization**
```python
# Increase processing speed
EXACT_AMOUNT_TOLERANCE = 0.01  # Keep tight tolerance
PARTIAL_AMOUNT_TOLERANCE = 0.05  # Reasonable tolerance
DATE_TOLERANCE_DAYS = 3  # Reasonable date range
```

#### **Matching Optimization**
```python
# Optimize matching strategies
matching_strategies = [
    {"name": "exact_amount", "weight": 1.0},      # High priority
    {"name": "partial_amount", "weight": 0.7},    # Medium priority
    {"name": "pattern_matching", "weight": 0.6},  # Lower priority
    # Disable ineffective strategies
    # {"name": "description_similarity", "weight": 0.0},
    # {"name": "amount_date", "weight": 0.0},
]
```

### **Performance Monitoring**

#### **Processing Metrics**
```python
import time
import psutil

# Monitor processing time
start_time = time.time()
result = agent.run_enhanced_reconciliation(gl_file, bank_file)
end_time = time.time()

print(f"Processing time: {end_time - start_time:.2f} seconds")

# Monitor memory usage
memory_usage = psutil.Process().memory_info().rss / 1024 / 1024
print(f"Memory usage: {memory_usage:.2f} MB")
```

#### **Match Rate Tracking**
```python
# Track match rate over time
match_rates = []
for iteration in range(5):
    result = agent.run_enhanced_reconciliation(gl_file, bank_file)
    match_rates.append(result['match_rate'])
    
print(f"Match rate progression: {match_rates}")
```

---

## 🔒 **SECURITY CONSIDERATIONS**

### **File Security**

#### **Input Validation**
```python
# Validate file types
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def validate_file(file_path):
    if not file_path.suffix.lower() in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type")
    
    if file_path.stat().st_size > MAX_FILE_SIZE:
        raise ValueError("File too large")
```

#### **Data Sanitization**
```python
# Sanitize input data
def sanitize_description(description):
    # Remove potentially harmful characters
    import re
    return re.sub(r'[<>"\']', '', str(description))
```

### **Access Control**

#### **File Permissions**
```bash
# Set appropriate permissions
chmod 644 uploads/*.xlsx
chmod 644 data/reports/*.json
chmod 644 data/reports/*.csv
```

#### **Directory Security**
```bash
# Secure directory access
chmod 755 uploads/
chmod 755 data/reports/
chmod 755 logs/
```

---

## 📚 **ADDITIONAL RESOURCES**

### **Documentation**
- **README.md**: Main project documentation
- **TECHNICAL_ARCHITECTURE.md**: Technical implementation details
- **API_DOCUMENTATION.md**: API reference and examples
- **TROUBLESHOOTING.md**: Common issues and solutions

### **Support**
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Complete technical documentation
- **Examples**: Usage examples and sample code
- **Tests**: Unit and integration tests

### **Contributing**
- **Code Style**: Follow PEP 8 guidelines
- **Testing**: Add tests for new features
- **Documentation**: Update documentation for changes
- **Pull Requests**: Submit PRs for review

---

**This installation guide provides complete setup instructions for IT teams to deploy and maintain the Excel Agent reconciliation system.**
