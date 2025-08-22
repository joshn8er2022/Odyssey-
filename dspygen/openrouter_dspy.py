#!/usr/bin/env python3
"""
OpenRouter integration for DSPy - Access GPT-5 and other latest models
"""

import dspy
import os
from typing import Optional, Dict, Any
from openai import OpenAI

class OpenRouterLM(dspy.LM):
    """DSPy Language Model using OpenRouter API"""
    
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = "https://openrouter.ai/api/v1",
        max_tokens: int = 1000,
        temperature: float = 0.0,
        **kwargs
    ):
        super().__init__(model, **kwargs)
        
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=api_base,
        )
        
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.kwargs = kwargs
    
    def basic_request(self, prompt: str, **kwargs) -> str:
        """Make a basic request to OpenRouter"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                temperature=kwargs.get("temperature", self.temperature),
                **{k: v for k, v in kwargs.items() if k not in ["max_tokens", "temperature"]}
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

def setup_openrouter(
    model: str = "openai/gpt-4o-2024-11-20", 
    api_key: Optional[str] = None,
    max_tokens: int = 1000
):
    """Setup DSPy with OpenRouter"""
    
    # Check for API key
    api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OpenRouter API key required!")
        print("Get your key from: https://openrouter.ai/")
        print("Set it as: export OPENROUTER_API_KEY='your-key-here'")
        return None
    
    try:
        # Create OpenRouter LM instance
        lm = OpenRouterLM(
            model=model,
            api_key=api_key,
            max_tokens=max_tokens
        )
        
        # Configure DSPy
        dspy.configure(lm=lm)
        
        print(f"✅ DSPy configured with OpenRouter model: {model}")
        return lm
        
    except Exception as e:
        print(f"❌ Error setting up OpenRouter: {e}")
        return None

# Popular models available on OpenRouter
OPENROUTER_MODELS = {
    # GPT Models (if available)
    "gpt-5": "openai/gpt-5",  # When available
    "gpt-4o": "openai/gpt-4o-2024-11-20",
    "gpt-4": "openai/gpt-4-turbo-2024-04-09",
    "gpt-3.5": "openai/gpt-3.5-turbo",
    
    # Claude Models
    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "claude-3-opus": "anthropic/claude-3-opus",
    "claude-3-haiku": "anthropic/claude-3-haiku",
    
    # Gemini Models
    "gemini-pro": "google/gemini-pro-1.5",
    "gemini-flash": "google/gemini-flash-1.5",
    
    # Open Source Models
    "llama-3.1-405b": "meta-llama/llama-3.1-405b-instruct",
    "llama-3.1-70b": "meta-llama/llama-3.1-70b-instruct",
    "mixtral-8x7b": "mistralai/mixtral-8x7b-instruct",
    
    # Specialized Models
    "qwen-2.5-72b": "qwen/qwen-2.5-72b-instruct",
    "deepseek-coder": "deepseek/deepseek-coder",
}

def list_models():
    """List available models"""
    print("📋 Available OpenRouter Models:")
    print("=" * 50)
    
    for name, model_id in OPENROUTER_MODELS.items():
        print(f"🤖 {name:20} -> {model_id}")

class TextProcessor(dspy.Signature):
    """Process text with advanced AI capabilities"""
    text = dspy.InputField(desc="Input text to process")
    task = dspy.InputField(desc="Task description (e.g., 'summarize', 'analyze sentiment')")
    result = dspy.OutputField(desc="Processed result")

class AdvancedTextProcessor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.processor = dspy.Predict(TextProcessor)
    
    def forward(self, text, task="analyze"):
        return self.processor(text=text, task=task)

def demo_gpt5_usage():
    """Demonstrate GPT-5 usage via OpenRouter"""
    print("🚀 GPT-5 Demo with OpenRouter")
    print("=" * 50)
    
    # Setup with GPT-4o (use GPT-5 when available)
    model = "openai/gpt-4o-2024-11-20"  # Change to openai/gpt-5 when available
    lm = setup_openrouter(model=model)
    
    if not lm:
        return
    
    # Create processor
    processor = AdvancedTextProcessor()
    
    # Test cases
    test_cases = [
        {
            "text": "Artificial intelligence is rapidly evolving, with new breakthroughs in machine learning, natural language processing, and computer vision happening every month.",
            "task": "summarize in one sentence"
        },
        {
            "text": "I absolutely love this new AI technology! It's incredible how fast it's progressing.",
            "task": "analyze sentiment and emotion"
        },
        {
            "text": "The weather forecast shows rain for the next three days with temperatures around 60°F.",
            "task": "extract key information"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['task']}")
        print(f"Input: {test['text']}")
        
        try:
            result = processor(text=test['text'], task=test['task'])
            print(f"🤖 Result: {result.result}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "models":
        list_models()
    elif len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_gpt5_usage()
    else:
        print("Usage:")
        print("python openrouter_dspy.py models  # List available models")
        print("python openrouter_dspy.py demo    # Run GPT-5 demo")