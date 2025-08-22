# File: dspy_chat_agent.py
# Complete DSPy agent that works with your Advanced Chat Widget

import dspy
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="Hume Health DSPy Sales Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure DSPy with OpenRouter
lm = dspy.LM(
    model="anthropic/claude-3.5-haiku",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1"
)
dspy.configure(lm=lm)

# Request/Response Models (matching your chat widget)
class ChatMessage(BaseModel):
    message: str
    session_id: str
    metadata: dict = {}

class ChatResponse(BaseModel):
    response: str
    qualification: Optional[Dict[str, Any]] = None
    pricing: Optional[Dict[str, Any]] = None
    checkout_url: Optional[str] = None
    quick_actions: List[str] = []

# DSPy Signatures for Hume Health Wholesale
class QualifyWholesaleLead(dspy.Signature):
    """Analyze wholesale inquiry and extract business intelligence."""
    conversation_history: str = dspy.InputField(desc="Complete conversation context")
    current_message: str = dspy.InputField(desc="Latest user message")
    
    intent_score: int = dspy.OutputField(desc="Purchase intent score 0-100")
    business_type: str = dspy.OutputField(desc="medical, fitness, wellness, retail, or unknown")
    volume_needed: str = dspy.OutputField(desc="Estimated quantity needed (e.g., '25-50', '100+')")
    urgency_level: str = dspy.OutputField(desc="immediate, this_week, this_month, exploring")
    decision_authority: str = dspy.OutputField(desc="decision_maker, influencer, researcher")
    next_action: str = dspy.OutputField(desc="show_pricing, book_call, need_more_info, not_qualified")

class GenerateWholesaleResponse(dspy.Signature):
    """Generate personalized wholesale sales response."""
    conversation_history: str = dspy.InputField(desc="Complete conversation")
    qualification_data: str = dspy.InputField(desc="Lead qualification results")
    pricing_context: str = dspy.InputField(desc="Available pricing and products")
    
    response: str = dspy.OutputField(desc="Engaging, helpful sales response")
    suggested_actions: str = dspy.OutputField(desc="Comma-separated quick action buttons")

class CalculateWholesalePricing(dspy.Signature):
    """Calculate volume-based wholesale pricing."""
    business_type: str = dspy.InputField(desc="Type of business")
    volume_needed: str = dspy.InputField(desc="Estimated volume")
    product_interest: str = dspy.InputField(desc="Products mentioned")
    
    recommended_quantity: int = dspy.OutputField(desc="Recommended order quantity")
    unit_price: int = dspy.OutputField(desc="Price per unit in dollars")
    total_cost: int = dspy.OutputField(desc="Total cost in dollars")
    savings_percent: str = dspy.OutputField(desc="Savings percentage vs retail")
    product_name: str = dspy.OutputField(desc="Recommended product")

# DSPy Modules
class HumeWholesaleAgent(dspy.Module):
    """Complete wholesale sales agent for Hume Health."""
    
    def __init__(self):
        super().__init__()
        self.qualifier = dspy.ChainOfThought(QualifyWholesaleLead)
        self.responder = dspy.ChainOfThought(GenerateWholesaleResponse)
        self.pricer = dspy.ChainOfThought(CalculateWholesalePricing)
        
        # Company knowledge base
        self.pricing_tiers = {
            "5-10": {"price": 139, "retail": 229, "savings": "39%"},
            "11-25": {"price": 129, "retail": 229, "savings": "44%"},
            "26-50": {"price": 119, "retail": 229, "savings": "48%"},
            "51-100": {"price": 109, "retail": 229, "savings": "52%"},
            "100+": {"price": 99, "retail": 229, "savings": "57%"}
        }
        
        self.business_profiles = {
            "medical": "Healthcare practitioners value compliance, ROI, and EMR integration",
            "fitness": "Gyms focus on member engagement, retention, and competitive differentiation", 
            "wellness": "Wellness centers emphasize holistic health tracking and client outcomes",
            "retail": "Retailers need attractive margins, fast inventory turns, and customer appeal"
        }
    
    def forward(self, conversation_history: str, current_message: str) -> Dict[str, Any]:
        """Process wholesale inquiry and generate complete response."""
        
        # Step 1: Qualify the lead
        qualification = self.qualifier(
            conversation_history=conversation_history,
            current_message=current_message
        )
        
        # Step 2: Calculate pricing if appropriate
        pricing_data = None
        if qualification.next_action == "show_pricing" and qualification.volume_needed != "unknown":
            pricing = self.pricer(
                business_type=qualification.business_type,
                volume_needed=qualification.volume_needed,
                product_interest=current_message
            )
            
            pricing_data = {
                "product": pricing.product_name,
                "quantity": pricing.recommended_quantity,
                "unit_price": pricing.unit_price,
                "total_cost": pricing.total_cost,
                "retail_price": 229,  # BodyPod retail
                "savings": int(pricing.total_cost * 0.48),  # Calculate savings
                "savings_percent": pricing.savings_percent
            }
        
        # Step 3: Generate response
        pricing_context = f"""
        BodyPod Wholesale Pricing:
        - 5-10 units: $139/unit (39% off $229 retail)
        - 11-25 units: $129/unit (44% off retail)  
        - 26-50 units: $119/unit (48% off retail)
        - 51-100 units: $109/unit (52% off retail)
        - 100+ units: $99/unit (57% off retail)
        
        Free shipping on 25+ units. Payment plans available.
        """
        
        response = self.responder(
            conversation_history=conversation_history,
            qualification_data=json.dumps({
                "intent": qualification.intent_score,
                "business": qualification.business_type,
                "volume": qualification.volume_needed,
                "urgency": qualification.urgency_level,
                "authority": qualification.decision_authority
            }),
            pricing_context=pricing_context
        )
        
        # Step 4: Generate quick actions
        quick_actions = []
        if qualification.business_type == "unknown":
            quick_actions = ["Medical practice", "Fitness center", "Wellness clinic", "Retail store"]
        elif qualification.next_action == "show_pricing":
            quick_actions = ["See payment options", "Book consultation", "Request samples", "Compare competitors"]
        elif qualification.next_action == "need_more_info":
            quick_actions = ["Technical specs", "Integration options", "ROI calculator", "Customer references"]
        else:
            quick_actions = response.suggested_actions.split(",")
        
        return {
            "qualification": {
                "intent_score": qualification.intent_score,
                "business_type": qualification.business_type,
                "volume_needed": qualification.volume_needed,
                "urgency_level": qualification.urgency_level,
                "decision_authority": qualification.decision_authority
            },
            "response": response.response,
            "pricing": pricing_data,
            "quick_actions": [action.strip() for action in quick_actions[:4]],
            "next_action": qualification.next_action
        }

# Global agent instance
agent = HumeWholesaleAgent()

# Session storage (use Redis in production)
sessions: Dict[str, List[Dict[str, str]]] = {}

# Close CRM Integration
async def create_close_lead(session_id: str, qualification: Dict, conversation: List):
    """Create lead in Close CRM."""
    if not os.getenv("CLOSE_API_KEY"):
        logger.warning("Close API key not configured")
        return None
    
    try:
        async with httpx.AsyncClient() as client:
            # Create lead data
            lead_data = {
                "name": f"Wholesale Inquiry {session_id[:8]}",
                "status_id": "stat_wholesale_new",  # Update with your Close status ID
                "description": f"AI Qualified Lead - Intent: {qualification['intent_score']}/100",
                "custom": {
                    "business_type": qualification["business_type"],
                    "volume_needed": qualification["volume_needed"],
                    "urgency": qualification["urgency_level"],
                    "intent_score": qualification["intent_score"]
                }
            }
            
            # Create lead in Close
            response = await client.post(
                "https://api.close.com/api/v1/lead/",
                json=lead_data,
                auth=(os.getenv("CLOSE_API_KEY"), "")
            )
            
            if response.status_code == 201:
                lead = response.json()
                
                # Add conversation notes
                conversation_text = "\n".join([
                    f"{msg['role']}: {msg['content']}" for msg in conversation
                ])
                
                await client.post(
                    "https://api.close.com/api/v1/activity/note/",
                    json={
                        "lead_id": lead["id"],
                        "note": f"AI Conversation Log:\n\n{conversation_text}"
                    },
                    auth=(os.getenv("CLOSE_API_KEY"), "")
                )
                
                logger.info(f"Created Close lead: {lead['id']}")
                return lead["id"]
            
    except Exception as e:
        logger.error(f"Error creating Close lead: {e}")
    
    return None

# API Endpoints (matching your chat widget expectations)
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatMessage):
    """Main chat endpoint that your widget connects to."""
    
    try:
        # Get or create session
        session_id = request.session_id
        if session_id not in sessions:
            sessions[session_id] = []
            # Add welcome context
            sessions[session_id].append({
                "role": "system",
                "content": "You are a Hume Health wholesale sales specialist helping businesses get bioimpedance scales."
            })
        
        # Add user message to session
        sessions[session_id].append({
            "role": "user", 
            "content": request.message
        })
        
        # Create conversation history string
        conversation_history = "\n".join([
            f"{msg['role']}: {msg['content']}" for msg in sessions[session_id]
        ])
        
        # Process with DSPy agent
        result = agent(
            conversation_history=conversation_history,
            current_message=request.message
        )
        
        # Add agent response to session
        sessions[session_id].append({
            "role": "assistant",
            "content": result["response"]
        })
        
        # Create Close CRM lead if high intent
        if result["qualification"]["intent_score"] >= 70:
            asyncio.create_task(create_close_lead(
                session_id, 
                result["qualification"], 
                sessions[session_id]
            ))
        
        # Generate checkout URL if showing pricing
        checkout_url = None
        if result["pricing"] and result["next_action"] == "show_pricing":
            checkout_url = f"https://humehealthpartner.com/products/body-pod-wholesale?volume={result['qualification']['volume_needed']}&business={result['qualification']['business_type']}&sessionId={session_id}"
        
        return ChatResponse(
            response=result["response"],
            qualification=result["qualification"],
            pricing=result["pricing"],
            checkout_url=checkout_url,
            quick_actions=result["quick_actions"]
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return ChatResponse(
            response="I apologize, but I'm having trouble processing your request. Please try again or contact our sales team directly at sales@humehealth.com.",
            quick_actions=["Contact sales team", "Try again", "View pricing", "Request callback"]
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": "anthropic/claude-3.5-haiku",
        "active_sessions": len(sessions),
        "close_crm_configured": bool(os.getenv("CLOSE_API_KEY"))
    }

@app.get("/")
async def serve_chat_widget():
    """Serve the chat widget for testing."""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hume Health Wholesale Chat - Test</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .container { max-width: 400px; margin: 0 auto; }
            .chat-box { border: 1px solid #ddd; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
            .message { margin: 10px 0; padding: 8px; border-radius: 5px; }
            .user { background: #e3f2fd; text-align: right; }
            .assistant { background: #f5f5f5; }
            input { width: 70%; padding: 8px; }
            button { padding: 8px 16px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Hume Health Wholesale Chat</h2>
            <div class="chat-box" id="chatBox">
                <div class="message assistant">
                    <div>👋 Hi! I'm your wholesale specialist. What type of business needs bioimpedance scales?</div>
                </div>
            </div>
            <input type="text" id="messageInput" placeholder="Type your message..." />
            <button onclick="sendMessage()">Send</button>
            
            <script>
                const sessionId = 'test_' + Date.now();
                
                async function sendMessage() {
                    const input = document.getElementById('messageInput');
                    const message = input.value.trim();
                    if (!message) return;
                    
                    // Show user message
                    addMessage(message, 'user');
                    input.value = '';
                    
                    try {
                        const response = await fetch('/api/chat', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                message: message,
                                session_id: sessionId,
                                metadata: {page: 'test'}
                            })
                        });
                        
                        const data = await response.json();
                        addMessage(data.response, 'assistant');
                        
                        // Show qualification data
                        if (data.qualification) {
                            console.log('Qualification:', data.qualification);
                        }
                        
                        // Show pricing
                        if (data.pricing) {
                            console.log('Pricing:', data.pricing);
                        }
                        
                    } catch (error) {
                        addMessage('Error: ' + error.message, 'assistant');
                    }
                }
                
                function addMessage(text, sender) {
                    const chatBox = document.getElementById('chatBox');
                    const div = document.createElement('div');
                    div.className = `message ${sender}`;
                    div.innerHTML = `<div>${text}</div>`;
                    chatBox.appendChild(div);
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
                
                // Enter key support
                document.getElementById('messageInput').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') sendMessage();
                });
            </script>
        </div>
    </body>
    </html>
    """)

# WebSocket support for real-time chat
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            # Process through chat endpoint logic
            request = ChatMessage(
                message=data,
                session_id=session_id,
                metadata={"channel": "websocket"}
            )
            
            result = await chat_endpoint(request)
            
            # Send response
            await websocket.send_json({
                "response": result.response,
                "qualification": result.qualification,
                "pricing": result.pricing,
                "checkout_url": result.checkout_url,
                "quick_actions": result.quick_actions
            })
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

if __name__ == "__main__":
    # Test the agent
    print("🧪 Testing Hume Health DSPy Agent")
    print("=" * 50)
    
    # Test qualification
    test_result = agent(
        conversation_history="system: You are a wholesale specialist.",
        current_message="I need 50 BodyPods for my medical practice this week"
    )
    
    print(f"✅ Intent Score: {test_result['qualification']['intent_score']}/100")
    print(f"✅ Business Type: {test_result['qualification']['business_type']}")
    print(f"✅ Response: {test_result['response'][:100]}...")
    
    if test_result['pricing']:
        print(f"✅ Pricing: {test_result['pricing']['quantity']} units @ ${test_result['pricing']['unit_price']}")
    
    print("\n🚀 Starting server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)