#!/usr/bin/env python3
"""
DSPy example using Ollama for local inference
"""

import dspy
import requests
import json

def check_ollama():
    """Check if Ollama is running and what models are available"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        return []
    except:
        return []

def setup_ollama_dspy(model="llama2"):
    """Setup DSPy with Ollama"""
    try:
        # Try to use Ollama model
        lm = dspy.LM(model=f"ollama/{model}", api_base="http://localhost:11434", max_tokens=150)
        dspy.configure(lm=lm)
        return lm
    except Exception as e:
        print(f"Error setting up Ollama: {e}")
        return None

class TextSummarizer(dspy.Signature):
    """Summarize the given text in a concise manner."""
    text = dspy.InputField(desc="Text to summarize")
    summary = dspy.OutputField(desc="Concise summary of the text")

class SummaryModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarize = dspy.Predict(TextSummarizer)
    
    def forward(self, text):
        return self.summarize(text=text)

def main():
    print("DSPyGen Ollama Example")
    print("=" * 50)
    
    # Check if Ollama is available
    models = check_ollama()
    
    if not models:
        print("❌ Ollama not running or no models available")
        print("\nTo use Ollama:")
        print("1. Install Ollama: https://ollama.com/")
        print("2. Pull a model: ollama pull llama2")
        print("3. Start Ollama service")
        print("\nFalling back to mock example...")
        
        # Mock example without actually calling a model
        print("\n📝 Mock Summary Example:")
        print("Original: The quick brown fox jumps over the lazy dog...")
        print("Summary: A common pangram sentence used for typing practice.")
        return
    
    print(f"✅ Ollama is running with models: {', '.join(models[:3])}")
    
    # Use the first available model
    model = models[0]
    
    try:
        # Setup DSPy with Ollama
        lm = setup_ollama_dspy(model.split(':')[0])  # Remove tag if present
        
        if lm is None:
            print("❌ Failed to setup Ollama with DSPy")
            return
            
        print(f"✅ DSPy configured with Ollama model: {model}")
        
        # Create module
        summarizer = SummaryModule()
        
        # Test text
        test_text = """
        DSPyGen is a Ruby on Rails style framework for DSPy that helps developers create
        language model pipelines more efficiently. It provides a command-line interface
        for quick initialization, modular design, and intuitive commands for managing
        AI development workflows.
        """
        
        print(f"\n📝 Original text:\n{test_text.strip()}")
        
        # Get summary
        print("\n🤖 Generating summary with local model...")
        result = summarizer(text=test_text.strip())
        print(f"\n📄 Summary:\n{result.summary}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Try with a simpler model or check Ollama setup")

if __name__ == "__main__":
    main()