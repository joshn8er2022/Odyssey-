#!/usr/bin/env python3
"""
GPT-5 Examples with OpenRouter and DSPy
"""

import dspy
import os
from typing import Optional, List, Dict
from openai import OpenAI

# Updated model configurations with GPT-5
GPT5_MODELS = {
    # GPT-5 Models (Available now!)
    "gpt-5": "openai/gpt-5",
    "gpt-5-chat": "openai/gpt-5-chat", 
    "gpt-5-mini": "openai/gpt-5-mini",
    "gpt-5-nano": "openai/gpt-5-nano",
    
    # GPT-4 Models
    "gpt-4o": "openai/gpt-4o-2024-11-20",
    "gpt-4": "openai/gpt-4-turbo-2024-04-09",
    
    # Claude 4.1 (Latest)
    "claude-4.1": "anthropic/claude-opus-4.1",
    
    # Other cutting-edge models
    "qwen3-235b": "qwen/qwen3-235b-a22b-thinking-2507",
    "glm-4.5v": "z-ai/glm-4.5v",
}

def setup_openrouter_client(model: str, api_key: Optional[str] = None):
    """Setup OpenAI client for OpenRouter"""
    api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY required")
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://github.com/seanchatmangpt/dspygen",
            "X-Title": "DSPyGen GPT-5 Integration"
        }
    )
    return client, model

def setup_gpt5(model_name: str = "gpt-5", **kwargs):
    """Setup DSPy with GPT-5 via OpenRouter"""
    
    if model_name not in GPT5_MODELS:
        print(f"❌ Model '{model_name}' not found. Available models:")
        for name in GPT5_MODELS.keys():
            print(f"  - {name}")
        return None
    
    model_id = GPT5_MODELS[model_name]
    
    try:
        # Setup using OpenRouter with manual client
        client, model = setup_openrouter_client(model_id)
        
        # For now, we'll create a simple wrapper that works with DSPy
        class SimpleOpenRouterLM:
            def __init__(self, client, model):
                self.client = client
                self.model = model
                
            def __call__(self, prompt, **kwargs):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=kwargs.get("max_tokens", 2000),
                        temperature=kwargs.get("temperature", 0.0)
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    return f"Error: {str(e)}"
        
        # For demo purposes, we'll work with the client directly
        print(f"✅ OpenRouter client configured: {model_name} ({model_id})")
        return client, model_id
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return None

# Advanced DSPy Signatures for GPT-5

class AdvancedAnalysis(dspy.Signature):
    """Perform advanced analysis using GPT-5's enhanced reasoning"""
    content = dspy.InputField(desc="Content to analyze")
    analysis_type = dspy.InputField(desc="Type of analysis (sentiment, technical, strategic, etc.)")
    depth = dspy.InputField(desc="Analysis depth (surface, detailed, comprehensive)")
    analysis = dspy.OutputField(desc="Detailed analysis with insights and recommendations")

class CodeArchitect(dspy.Signature):
    """Design software architecture with GPT-5's advanced coding capabilities"""
    requirements = dspy.InputField(desc="Project requirements and constraints")
    language = dspy.InputField(desc="Programming language or technology stack")
    scale = dspy.InputField(desc="Expected scale (small, medium, enterprise)")
    architecture = dspy.OutputField(desc="Detailed architecture design with implementation notes")

class CreativeWriter(dspy.Signature):
    """Generate creative content with GPT-5's enhanced writing capabilities"""
    topic = dspy.InputField(desc="Topic or theme")
    style = dspy.InputField(desc="Writing style (academic, creative, technical, etc.)")
    length = dspy.InputField(desc="Desired length (short, medium, long)")
    content = dspy.OutputField(desc="High-quality creative content")

class StrategicPlanner(dspy.Signature):
    """Create strategic plans with GPT-5's advanced reasoning"""
    objective = dspy.InputField(desc="Strategic objective or goal")
    context = dspy.InputField(desc="Current context and constraints")
    timeline = dspy.InputField(desc="Timeline for implementation")
    plan = dspy.OutputField(desc="Comprehensive strategic plan with actionable steps")

# GPT-5 Modules

class GPT5Analyst(dspy.Module):
    def __init__(self):
        super().__init__()
        self.analyze = dspy.Predict(AdvancedAnalysis)
    
    def forward(self, content, analysis_type="comprehensive", depth="detailed"):
        return self.analyze(content=content, analysis_type=analysis_type, depth=depth)

class GPT5Architect(dspy.Module):
    def __init__(self):
        super().__init__()
        self.design = dspy.Predict(CodeArchitect)
    
    def forward(self, requirements, language="Python", scale="medium"):
        return self.design(requirements=requirements, language=language, scale=scale)

class GPT5Writer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.write = dspy.Predict(CreativeWriter)
    
    def forward(self, topic, style="professional", length="medium"):
        return self.write(topic=topic, style=style, length=length)

class GPT5Strategist(dspy.Module):
    def __init__(self):
        super().__init__()
        self.plan = dspy.Predict(StrategicPlanner)
    
    def forward(self, objective, context="general business", timeline="6 months"):
        return self.plan(objective=objective, context=context, timeline=timeline)

def demo_gpt5_capabilities():
    """Demonstrate GPT-5's advanced capabilities"""
    
    print("🚀 GPT-5 Advanced Capabilities Demo")
    print("=" * 60)
    
    # Setup GPT-5
    lm = setup_gpt5("gpt-5", max_tokens=2000)
    if not lm:
        print("⚠️  Demo requires OpenRouter API key")
        print("Get your key: https://openrouter.ai/")
        print("Set: export OPENROUTER_API_KEY='your-key'")
        return
    
    # Initialize modules
    analyst = GPT5Analyst()
    architect = GPT5Architect()
    writer = GPT5Writer()
    strategist = GPT5Strategist()
    
    demos = [
        {
            "title": "📊 Advanced Analysis",
            "module": analyst,
            "args": {
                "content": "The AI industry is experiencing rapid growth with new models released monthly, increasing competition among tech companies, and growing concerns about AI safety and regulation.",
                "analysis_type": "strategic market analysis",
                "depth": "comprehensive"
            },
            "result_key": "analysis"
        },
        {
            "title": "🏗️ Software Architecture",
            "module": architect,
            "args": {
                "requirements": "Build a scalable e-commerce platform that can handle 10M users, with real-time inventory, payment processing, and AI-powered recommendations",
                "language": "Python/JavaScript",
                "scale": "enterprise"
            },
            "result_key": "architecture"
        },
        {
            "title": "✍️ Creative Writing",
            "module": writer,
            "args": {
                "topic": "The future of human-AI collaboration",
                "style": "thought-provoking essay",
                "length": "medium"
            },
            "result_key": "content"
        },
        {
            "title": "📋 Strategic Planning",
            "module": strategist,
            "args": {
                "objective": "Launch an AI-powered startup in the education technology sector",
                "context": "Competitive EdTech market with $350B global opportunity",
                "timeline": "18 months"
            },
            "result_key": "plan"
        }
    ]
    
    for demo in demos:
        print(f"\n{demo['title']}")
        print("-" * 50)
        
        try:
            result = demo['module'](**demo['args'])
            output = getattr(result, demo['result_key'])
            print(f"🤖 GPT-5 Response:\n{output}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)

def compare_models():
    """Compare different GPT-5 variants"""
    
    print("🔬 GPT-5 Model Comparison")
    print("=" * 50)
    
    models_to_test = ["gpt-5-nano", "gpt-5-mini", "gpt-5"]
    test_prompt = "Explain quantum computing in simple terms"
    
    for model in models_to_test:
        print(f"\n🤖 Testing {model}...")
        lm = setup_gpt5(model, max_tokens=200)
        
        if lm:
            try:
                # Simple test
                class SimpleExplainer(dspy.Signature):
                    topic = dspy.InputField()
                    explanation = dspy.OutputField()
                
                explainer = dspy.Predict(SimpleExplainer)
                result = explainer(topic=test_prompt)
                print(f"Response: {result.explanation[:200]}...")
            except Exception as e:
                print(f"Error: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            demo_gpt5_capabilities()
        elif sys.argv[1] == "compare":
            compare_models()
        elif sys.argv[1] == "models":
            print("🤖 Available GPT-5 Models:")
            for name, model_id in GPT5_MODELS.items():
                print(f"  {name:15} -> {model_id}")
    else:
        print("GPT-5 with OpenRouter and DSPy")
        print("\nUsage:")
        print("  python gpt5_examples.py demo     # Run capabilities demo")
        print("  python gpt5_examples.py compare  # Compare model variants")
        print("  python gpt5_examples.py models   # List available models")