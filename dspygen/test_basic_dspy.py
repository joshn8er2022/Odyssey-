#!/usr/bin/env python3
"""
Basic DSPy example that works with the current version
"""

import dspy
import os
from typing import Optional

def setup_dspy(api_key: Optional[str] = None):
    """Setup DSPy with OpenAI"""
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    # Use the new LM interface
    lm = dspy.LM(model="gpt-3.5-turbo", max_tokens=150)
    dspy.configure(lm=lm)
    return lm

# Define a simple signature
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
    print("DSPyGen Basic Example")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  No OPENAI_API_KEY found in environment")
        print("To use OpenAI models, set your API key:")
        print("export OPENAI_API_KEY='your-key-here'")
        print("\nAlternatively, you can use local models with Ollama.")
        return
    
    try:
        # Setup DSPy
        lm = setup_dspy(api_key)
        print(f"✅ DSPy configured with {lm.model}")
        
        # Create module
        summarizer = SummaryModule()
        
        # Test text
        test_text = """
        The quick brown fox jumps over the lazy dog. This is a common sentence used in typing practice
        because it contains every letter of the alphabet at least once. It's also known as a pangram.
        The sentence has been used for decades to test typewriters, keyboards, and fonts.
        """
        
        print(f"\n📝 Original text:\n{test_text.strip()}")
        
        # Get summary
        result = summarizer(text=test_text.strip())
        print(f"\n📄 Summary:\n{result.summary}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()