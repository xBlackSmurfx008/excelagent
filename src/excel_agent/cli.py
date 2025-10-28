"""
Excel Agent - CLI Interface

Command-line interface for the Excel Agent system.
"""

import click
import os
import sys
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from excel_agent.api.dashboard import create_app
from excel_agent.agents.enhanced_thinking_agent import EnhancedThinkingAgent
from excel_agent.config.settings import get_config

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Excel Agent - AI-powered reconciliation system"""
    pass

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def dashboard(host: str, port: int, debug: bool):
    """Start the Excel Agent dashboard"""
    app = create_app()
    app.run(host=host, port=port, debug=debug)

@cli.command()
@click.argument('gl_file', type=click.Path(exists=True))
@click.argument('bank_file', type=click.Path(exists=True))
@click.option('--training-doc', type=click.Path(exists=True), help='Training document path')
@click.option('--output', '-o', help='Output file path')
def reconcile(gl_file: str, bank_file: str, training_doc: Optional[str], output: Optional[str]):
    """Run reconciliation analysis"""
    try:
        agent = EnhancedThinkingAgent()
        result = agent.run_enhanced_reconciliation_with_thinking(
            gl_file, bank_file, training_doc
        )
        
        if output:
            import json
            with open(output, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            click.echo(f"Results saved to {output}")
        else:
            click.echo("Reconciliation completed successfully")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('document_path', type=click.Path(exists=True))
@click.option('--rounds', default=10, help='Number of thinking rounds')
def analyze(document_path: str, rounds: int):
    """Analyze training document with deep thinking"""
    try:
        from excel_agent.agents.training_document_deep_thinker import TrainingDocumentDeepThinker
        
        thinker = TrainingDocumentDeepThinker()
        thinker.thinking_rounds = rounds
        
        result = thinker.run_analysis()
        click.echo(f"Analysis completed with {rounds} rounds of thinking")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
def config():
    """Show current configuration"""
    config = get_config()
    click.echo("Current Configuration:")
    click.echo("=" * 50)
    
    config_dict = config.to_dict()
    for section, values in config_dict.items():
        click.echo(f"\n{section.upper()}:")
        if isinstance(values, dict):
            for key, value in values.items():
                click.echo(f"  {key}: {value}")
        else:
            click.echo(f"  {values}")

@cli.command()
def validate():
    """Validate configuration and environment"""
    config = get_config()
    
    click.echo("Validating configuration...")
    
    if config.validate():
        click.echo("✅ Configuration is valid")
    else:
        click.echo("❌ Configuration validation failed", err=True)
        sys.exit(1)
    
    # Check OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        click.echo("⚠️  OpenAI API key not set")
    else:
        click.echo("✅ OpenAI API key is set")
    
    # Check required directories
    required_dirs = ['data', 'uploads', 'reports', 'logs']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            click.echo(f"✅ Created directory: {dir_name}")
        else:
            click.echo(f"✅ Directory exists: {dir_name}")

@cli.command()
@click.option('--pattern', default='test_*.py', help='Test pattern')
@click.option('--coverage', is_flag=True, help='Run with coverage')
def test(pattern: str, coverage: bool):
    """Run tests"""
    import subprocess
    
    cmd = ['pytest', f'tests/{pattern}']
    if coverage:
        cmd.extend(['--cov=src/excel_agent', '--cov-report=html'])
    
    try:
        subprocess.run(cmd, check=True)
        click.echo("✅ Tests passed")
    except subprocess.CalledProcessError:
        click.echo("❌ Tests failed", err=True)
        sys.exit(1)

@cli.command()
def install():
    """Install dependencies"""
    import subprocess
    
    click.echo("Installing production dependencies...")
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
    
    click.echo("Installing development dependencies...")
    subprocess.run(['pip', 'install', '-r', 'requirements-dev.txt'], check=True)
    
    click.echo("✅ Dependencies installed")

def main():
    """Main entry point"""
    cli()

if __name__ == '__main__':
    main()
