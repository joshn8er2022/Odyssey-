import dspy
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
