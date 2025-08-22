#!/usr/bin/env python3
"""
Simplified DSPyGen CLI that works with current Python/DSPy versions
"""

import typer
import os
import sys
from pathlib import Path
from typing import Optional

app = typer.Typer(help="Simplified DSPyGen CLI for AI development")

@app.command()
def init(project_name: str = typer.Argument(..., help="Name of the project to initialize")):
    """Initialize a new DSPyGen project"""
    
    project_path = Path(project_name)
    
    if project_path.exists():
        typer.echo(f"❌ Directory '{project_name}' already exists")
        return
    
    # Create project structure
    project_path.mkdir()
    (project_path / "modules").mkdir()
    (project_path / "data").mkdir()
    
    # Create basic files
    env_file = project_path / ".env"
    env_file.write_text("""# Add your API keys here
OPENAI_API_KEY=your-openai-key-here
GROQ_API_KEY=your-groq-key-here
""")
    
    readme_file = project_path / "README.md"
    readme_file.write_text(f"""# {project_name}

A DSPyGen project for AI development.

## Setup

1. Add your API keys to `.env`
2. Install dependencies: `pip install dspy-ai typer`
3. Run modules: `python simple_dspygen.py module run <module_name>`

## Usage

```bash
# Create a new module
python simple_dspygen.py module create TextSummarizer

# Run a module
python simple_dspygen.py module run TextSummarizer "Your text here"
```
""")
    
    # Create a sample module
    sample_module = project_path / "modules" / "text_summarizer.py"
    sample_module.write_text('''import dspy
import os

class TextSummarizer(dspy.Signature):
    """Summarize the given text concisely."""
    text = dspy.InputField(desc="Text to summarize")
    summary = dspy.OutputField(desc="Concise summary")

class TextSummarizerModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarize = dspy.Predict(TextSummarizer)
    
    def forward(self, text):
        return self.summarize(text=text)

def setup():
    """Setup DSPy configuration"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ No OPENAI_API_KEY found. Set it in .env file")
        return None
    
    lm = dspy.LM(model="gpt-3.5-turbo", max_tokens=150)
    dspy.configure(lm=lm)
    return lm

def run(text):
    """Run the text summarizer"""
    lm = setup()
    if not lm:
        return "Error: No API key configured"
    
    try:
        module = TextSummarizerModule()
        result = module(text=text)
        return result.summary
    except Exception as e:
        return f"Error: {str(e)}"
''')
    
    typer.echo(f"✅ Project '{project_name}' initialized successfully!")
    typer.echo(f"📁 Project structure created in: {project_path.absolute()}")
    typer.echo(f"📝 Next steps:")
    typer.echo(f"   cd {project_name}")
    typer.echo(f"   # Edit .env with your API keys")
    typer.echo(f"   python ../simple_dspygen.py module run text_summarizer 'Your text here'")

module_app = typer.Typer(help="Module management commands")
app.add_typer(module_app, name="module")

@module_app.command("create")
def create_module(
    class_name: str = typer.Argument(..., help="Module class name (e.g., TextSummarizer)"),
    inputs: str = typer.Option("text", "--inputs", "-i", help="Input fields (comma-separated)"),
    output: str = typer.Option("result", "--output", "-o", help="Output field name")
):
    """Create a new DSPy module"""
    
    # Convert class name to file name
    file_name = ''.join(['_' + c.lower() if c.isupper() else c for c in class_name]).lstrip('_')
    
    input_fields = [inp.strip() for inp in inputs.split(',')]
    
    module_content = f'''import dspy
import os

class {class_name}(dspy.Signature):
    """Generated {class_name} module."""
'''
    
    # Add input fields
    for inp in input_fields:
        module_content += f'    {inp} = dspy.InputField(desc="{inp.replace("_", " ").title()} input")\n'
    
    # Add output field
    module_content += f'    {output} = dspy.OutputField(desc="{output.replace("_", " ").title()} output")\n\n'
    
    # Add module class
    module_content += f'''class {class_name}Module(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict({class_name})
    
    def forward(self, {", ".join(input_fields)}):
        return self.predict({", ".join([f"{inp}={inp}" for inp in input_fields])})

def setup():
    """Setup DSPy configuration"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ No OPENAI_API_KEY found. Set it in .env file")
        return None
    
    lm = dspy.LM(model="gpt-3.5-turbo", max_tokens=150)
    dspy.configure(lm=lm)
    return lm

def run({", ".join(input_fields)}):
    """Run the {class_name} module"""
    lm = setup()
    if not lm:
        return "Error: No API key configured"
    
    try:
        module = {class_name}Module()
        result = module({", ".join([f"{inp}={inp}" for inp in input_fields])})
        return getattr(result, "{output}")
    except Exception as e:
        return f"Error: {{str(e)}}"
'''
    
    # Create modules directory if it doesn't exist
    modules_dir = Path("modules")
    modules_dir.mkdir(exist_ok=True)
    
    # Write module file
    module_file = modules_dir / f"{file_name}.py"
    module_file.write_text(module_content)
    
    typer.echo(f"✅ Module '{class_name}' created: {module_file}")
    typer.echo(f"📝 Inputs: {', '.join(input_fields)}")
    typer.echo(f"📤 Output: {output}")

@module_app.command("run")
def run_module(
    module_name: str = typer.Argument(..., help="Module name to run"),
    *args: str
):
    """Run a DSPy module"""
    
    # Look for module file
    modules_dir = Path("modules")
    module_file = modules_dir / f"{module_name}.py"
    
    if not module_file.exists():
        typer.echo(f"❌ Module '{module_name}' not found at {module_file}")
        return
    
    # Load environment variables
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    # Import and run the module
    try:
        sys.path.insert(0, str(modules_dir))
        module = __import__(module_name)
        
        if hasattr(module, 'run'):
            result = module.run(*args)
            typer.echo(f"📄 Result: {result}")
        else:
            typer.echo(f"❌ Module '{module_name}' has no run() function")
            
    except ImportError as e:
        typer.echo(f"❌ Failed to import module: {e}")
    except Exception as e:
        typer.echo(f"❌ Error running module: {e}")

@app.command()
def version():
    """Show version information"""
    typer.echo("Simple DSPyGen CLI v1.0")
    typer.echo("Built for DSPy 2.6+ with Python 3.13 support")

if __name__ == "__main__":
    app()