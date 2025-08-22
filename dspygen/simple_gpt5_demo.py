#!/usr/bin/env python3
"""
Simple GPT-5 Demo with OpenRouter
"""

import os
from openai import OpenAI
from typing import Optional, Dict, Any

# Available GPT-5 models on OpenRouter
GPT5_MODELS = {
    "gpt-5": "openai/gpt-5",
    "gpt-5-chat": "openai/gpt-5-chat", 
    "gpt-5-mini": "openai/gpt-5-mini",
    "gpt-5-nano": "openai/gpt-5-nano",
    "gpt-4o": "openai/gpt-4o-2024-11-20",  # Fallback option
}

class GPT5Client:
    """Simple GPT-5 client using OpenRouter"""
    
    def __init__(self, model: str = "openai/gpt-5", api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY required. Get it from https://openrouter.ai/")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://github.com/seanchatmangpt/dspygen",
                "X-Title": "DSPyGen GPT-5 Integration"
            }
        )
        self.model = model
    
    def chat(self, message: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """Send a chat message to GPT-5"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze(self, content: str, analysis_type: str = "comprehensive") -> str:
        """Perform advanced analysis with GPT-5"""
        prompt = f"""
        Perform a {analysis_type} analysis of the following content:
        
        Content: {content}
        
        Please provide:
        1. Key insights
        2. Important patterns or trends
        3. Actionable recommendations
        4. Potential implications
        
        Be thorough and analytical in your response.
        """
        return self.chat(prompt, max_tokens=3000)
    
    def code_architect(self, requirements: str, language: str = "Python") -> str:
        """Design software architecture with GPT-5"""
        prompt = f"""
        As a senior software architect, design a comprehensive architecture for:
        
        Requirements: {requirements}
        Primary Language: {language}
        
        Please provide:
        1. High-level architecture overview
        2. Key components and their responsibilities
        3. Data flow and API design
        4. Technology recommendations
        5. Scalability considerations
        6. Security considerations
        
        Format your response clearly with sections and bullet points.
        """
        return self.chat(prompt, max_tokens=4000)
    
    def strategic_plan(self, objective: str, context: str = "", timeline: str = "6 months") -> str:
        """Create strategic plans with GPT-5"""
        prompt = f"""
        Create a comprehensive strategic plan for:
        
        Objective: {objective}
        Context: {context}
        Timeline: {timeline}
        
        Please include:
        1. Executive Summary
        2. Key Milestones
        3. Resource Requirements
        4. Risk Assessment
        5. Success Metrics
        6. Implementation Roadmap
        
        Make it actionable and specific.
        """
        return self.chat(prompt, max_tokens=3500)

def demo_gpt5_capabilities():
    """Demonstrate GPT-5's advanced capabilities"""
    
    print("🚀 GPT-5 Advanced Capabilities Demo")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY required!")
        print("1. Get your key from: https://openrouter.ai/")
        print("2. Set it: export OPENROUTER_API_KEY='your-key-here'")
        print("3. Note: GPT-5 may require BYOK (Bring Your Own Key) setup")
        return
    
    # Try different models in order of preference
    for model_name, model_id in GPT5_MODELS.items():
        print(f"\n🤖 Trying {model_name}...")
        
        try:
            gpt5 = GPT5Client(model=model_id)
            
            # Quick test
            test_response = gpt5.chat("Say 'Hello from GPT-5!' if you're working correctly.", max_tokens=50)
            
            if "error" not in test_response.lower():
                print(f"✅ {model_name} is working!")
                break
            else:
                print(f"❌ {model_name}: {test_response}")
                continue
                
        except Exception as e:
            print(f"❌ {model_name}: {str(e)}")
            continue
    else:
        print("❌ No working models found. Check your API key and BYOK setup.")
        return
    
    # Run capability demos
    demos = [
        {
            "title": "📊 Advanced Market Analysis",
            "method": "analyze",
            "args": {
                "content": "The AI industry is experiencing unprecedented growth with new foundation models released monthly, increasing competition among tech giants, growing concerns about AI safety and regulation, and emerging applications in healthcare, finance, and education.",
                "analysis_type": "strategic market analysis"
            }
        },
        {
            "title": "🏗️ Software Architecture Design",
            "method": "code_architect",
            "args": {
                "requirements": "Build a real-time collaborative document editing platform like Google Docs that supports 100K concurrent users, with offline sync, version control, and AI-powered writing assistance",
                "language": "TypeScript/Node.js"
            }
        },
        {
            "title": "📋 Strategic Business Plan",
            "method": "strategic_plan",
            "args": {
                "objective": "Launch an AI-powered personal finance app that uses machine learning to optimize spending and investments",
                "context": "Competitive fintech market with established players like Mint and YNAB",
                "timeline": "12 months"
            }
        }
    ]
    
    for demo in demos:
        print(f"\n{demo['title']}")
        print("-" * 50)
        
        try:
            method = getattr(gpt5, demo['method'])
            result = method(**demo['args'])
            print(f"🤖 GPT-5 Response:\n{result}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)

def interactive_gpt5():
    """Interactive GPT-5 chat session"""
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY required!")
        return
    
    print("🤖 GPT-5 Interactive Chat")
    print("Type 'quit' to exit, 'models' to switch models")
    print("-" * 40)
    
    # Try to find a working model
    gpt5 = None
    current_model = None
    
    for model_name, model_id in GPT5_MODELS.items():
        try:
            gpt5 = GPT5Client(model=model_id)
            test = gpt5.chat("Hi", max_tokens=10)
            if "error" not in test.lower():
                current_model = model_name
                print(f"✅ Using {model_name}")
                break
        except:
            continue
    
    if not gpt5:
        print("❌ No working models found")
        return
    
    while True:
        try:
            user_input = input(f"\n[{current_model}] You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            elif user_input.lower() == 'models':
                print("Available models:")
                for i, (name, _) in enumerate(GPT5_MODELS.items(), 1):
                    print(f"{i}. {name}")
                continue
            elif not user_input:
                continue
            
            print(f"🤖 GPT-5: ", end="", flush=True)
            response = gpt5.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            demo_gpt5_capabilities()
        elif sys.argv[1] == "chat":
            interactive_gpt5()
        elif sys.argv[1] == "models":
            print("🤖 Available GPT-5 Models:")
            for name, model_id in GPT5_MODELS.items():
                print(f"  {name:15} -> {model_id}")
    else:
        print("🚀 GPT-5 with OpenRouter")
        print("\nCommands:")
        print("  python simple_gpt5_demo.py demo     # Run capabilities demo")
        print("  python simple_gpt5_demo.py chat     # Interactive chat")
        print("  python simple_gpt5_demo.py models   # List models")
        print("\nSetup:")
        print("  export OPENROUTER_API_KEY='your-key'")
        print("  Get key from: https://openrouter.ai/")