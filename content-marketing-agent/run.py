#!/usr/bin/env python3
"""
Content Marketing Agent - Main Entry Point

This script provides multiple ways to run the Content Marketing Agent:
1. Web interface (Streamlit)
2. Command-line interface
3. API server (FastAPI)
"""

import argparse
import sys
import os
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def run_web_interface():
    """Run the Streamlit web interface"""
    import subprocess
    
    print("🚀 Starting Content Marketing Agent Web Interface...")
    print("📱 Open your browser to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            "streamlit", "run", "src/main.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Content Marketing Agent stopped.")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it with: pip install streamlit")
        sys.exit(1)

def run_cli():
    """Run the command-line interface"""
    print("🎯 Content Marketing Agent - CLI Mode")
    print("This feature is coming soon!")
    print("For now, please use the web interface: python run.py --web")

async def run_api_server():
    """Run the FastAPI server"""
    try:
        import uvicorn
        from src.api.server import app
        
        print("🚀 Starting Content Marketing Agent API Server...")
        print("📡 API available at: http://localhost:8000")
        print("📚 API docs at: http://localhost:8000/docs")
        print("⏹️  Press Ctrl+C to stop")
        
        config = uvicorn.Config(
            app=app,
            host="localhost",
            port=8000,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
        
    except ImportError:
        print("❌ FastAPI/Uvicorn not found. Please install with: pip install fastapi uvicorn")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 API Server stopped.")

def setup_environment():
    """Set up the environment and check dependencies"""
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  No .env file found. Creating from template...")
        env_example = Path(".env.example")
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("✅ Created .env file. Please edit it with your API keys.")
        else:
            print("❌ No .env.example file found. Please create a .env file manually.")
    
    # Check for required API keys
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("⚠️  OPENAI_API_KEY not found in .env file.")
        print("   The agent will use default responses without AI capabilities.")
    
    print("✅ Environment setup complete!")

def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description="Content Marketing Agent - AI-powered content creation assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py --web          # Start web interface (default)
  python run.py --cli          # Start command-line interface
  python run.py --api          # Start API server
  python run.py --setup        # Set up environment only

For more information, visit: https://github.com/your-repo/content-marketing-agent
        """
    )
    
    parser.add_argument(
        "--web", 
        action="store_true", 
        help="Run the Streamlit web interface (default)"
    )
    
    parser.add_argument(
        "--cli", 
        action="store_true", 
        help="Run the command-line interface"
    )
    
    parser.add_argument(
        "--api", 
        action="store_true", 
        help="Run the FastAPI server"
    )
    
    parser.add_argument(
        "--setup", 
        action="store_true", 
        help="Set up environment and exit"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8501, 
        help="Port for web interface (default: 8501)"
    )
    
    args = parser.parse_args()
    
    # Set up environment
    setup_environment()
    
    if args.setup:
        print("🎯 Environment setup complete! You can now run the agent.")
        return
    
    # Determine which interface to run
    if args.cli:
        run_cli()
    elif args.api:
        asyncio.run(run_api_server())
    else:
        # Default to web interface
        run_web_interface()

if __name__ == "__main__":
    main()