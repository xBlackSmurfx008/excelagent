# Excel Agent - AI-Powered Reconciliation System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/excelagent/excel-agent)
[![Code Quality](https://img.shields.io/badge/code%20quality-A-brightgreen.svg)](https://github.com/excelagent/excel-agent)

An enterprise-grade AI-powered Excel reconciliation system with advanced thinking capabilities, designed for financial institutions and credit unions.

## 🚀 Features

### 🧠 **AI-Powered Intelligence**
- **Advanced Thinking Agents** - GPT-4 powered reasoning for complex scenarios
- **Document Analysis** - Deep analysis of training documents and procedures
- **Pattern Recognition** - Intelligent matching and anomaly detection
- **Continuous Learning** - Agents learn from failures and improve over time

### 📊 **Comprehensive Reconciliation**
- **Multi-File Processing** - Handle GL Activity and Bank Statement files
- **Real-Time Analysis** - Live reconciliation with instant results
- **Timing Differences** - Automated handling of month-end timing differences
- **Variance Analysis** - Intelligent variance detection and reporting

### 🏗️ **Enterprise Architecture**
- **Modular Design** - Clean separation of concerns
- **Scalable Infrastructure** - Docker containerization and microservice-ready
- **Comprehensive Testing** - Unit, integration, and E2E test coverage
- **Production Monitoring** - Health checks and performance monitoring

### 🔒 **Security & Compliance**
- **Audit Trails** - Complete logging and audit documentation
- **Data Validation** - Comprehensive input validation and error handling
- **OP Compliance** - Full compliance with operational procedures
- **Secure Configuration** - Environment-based configuration management

## 📋 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/excelagent/excel-agent.git
   cd excel-agent
   ```

2. **Install dependencies**
   ```bash
   make install-dev
   # or manually:
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Set up environment**
   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key and other settings
   ```

4. **Validate configuration**
   ```bash
   make validate
   # or manually:
   python -m excel_agent.cli validate
   ```

5. **Start the dashboard**
   ```bash
   make dev
   # or manually:
   python -m excel_agent.cli dashboard
   ```

6. **Access the application**
   Open your browser to `http://localhost:5000`

## 🏗️ Project Structure

```
Excel Agent/
├── 📁 src/excel_agent/           # Main source code
│   ├── 📁 agents/                # AI Agents
│   ├── 📁 core/                  # Business logic
│   ├── 📁 api/                   # Web interface
│   ├── 📁 config/                # Configuration
│   └── 📁 utils/                 # Utilities
├── 📁 tests/                     # Test suite
├── 📁 docs/                      # Documentation
├── 📁 scripts/                   # Automation scripts
├── 📁 config/                    # Configuration files
└── 📁 data/                      # Data storage
```

## 🎯 Usage

### Web Dashboard
The primary interface is the web dashboard:
- Upload GL Activity and Bank Statement files
- Run AI-powered reconciliation analysis
- View real-time results and reports
- Monitor agent activities and performance

### Command Line Interface
```bash
# Start dashboard
excel-agent dashboard

# Run reconciliation
excel-agent reconcile gl_file.xlsx bank_file.xlsx

# Analyze training document
excel-agent analyze training_doc.md --rounds 10

# Show configuration
excel-agent config

# Run tests
excel-agent test --coverage
```

### Python API
```python
from excel_agent import ReconciliationEngine, OrchestrationAgent

# Initialize reconciliation engine
engine = ReconciliationEngine()

# Run reconciliation
result = engine.reconcile(gl_file="gl_data.xlsx", bank_file="bank_data.xlsx")

# Get results
print(f"Status: {result.status}")
print(f"Discrepancies: {result.discrepancies}")
```

## 🧠 AI Agents

### Enhanced Thinking Agent
- Analyzes complex reconciliation scenarios
- Provides strategic recommendations
- Learns from matching failures
- Generates detailed reasoning reports

### Training Document Deep Thinker
- Performs 10 rounds of deep analysis
- Extracts key insights from procedures
- Generates strategic recommendations
- Provides comprehensive understanding

### Reconciliation Matcher
- Matches GL transactions with bank transactions
- Handles all 21 transaction types from OP procedures
- Implements timing difference logic
- Provides variance analysis

### Data Quality Validator
- Validates data completeness and accuracy
- Checks consistency between data sources
- Provides quality scoring
- Generates validation reports

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_api_key_here

# Optional
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key
LOG_LEVEL=INFO
MAX_WORKERS=4
```

### Configuration Files
- `config/dev/settings.yaml` - Development settings
- `config/prod/settings.yaml` - Production settings
- `config/test/settings.yaml` - Test settings

## 🧪 Testing

### Run Tests
```bash
# All tests
make test

# With coverage
make test-cov

# Specific test type
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

### Test Coverage
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **E2E Tests**: Complete workflow testing
- **Coverage Target**: 90%+

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
make docker-build

# Run with Docker Compose
docker-compose up -d

# Scale services
docker-compose up -d --scale excel-agent=3
```

### Production Deployment
```bash
# Set production environment
export FLASK_ENV=production

# Run with production settings
make run

# Or use systemd service
sudo systemctl start excel-agent
```

## 📊 Monitoring

### Health Checks
```bash
# Check application health
make health-check

# Monitor performance
python scripts/monitoring/performance_monitor.py
```

### Logging
- **Application Logs**: `logs/app.log`
- **Error Logs**: `logs/error.log`
- **Audit Logs**: `logs/audit.log`
- **Agent Logs**: `logs/{agent_name}.log`

## 📚 Documentation

- **[User Guide](docs/user/getting_started.md)** - Getting started guide
- **[API Documentation](docs/api/endpoints.md)** - API reference
- **[Developer Guide](docs/developer/architecture.md)** - Architecture overview
- **[Deployment Guide](docs/developer/deployment.md)** - Deployment instructions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
make install-dev

# Set up pre-commit hooks
pre-commit install

# Run code formatting
make format

# Run linting
make lint
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/excelagent/excel-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/excelagent/excel-agent/discussions)

## 🏆 Acknowledgments

- OpenAI for GPT-4 API
- Flask community for web framework
- Pandas team for data processing
- All contributors and users

---

**Built with ❤️ by the Excel Agent Team**