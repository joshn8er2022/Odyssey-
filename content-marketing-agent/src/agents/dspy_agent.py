"""
DSPy-powered Self-Automated React Content Marketing Agent
Advanced architecture with signature management and autonomous decision making
"""

import dspy
from typing import Dict, List, Optional, Any, Union, Type
import asyncio
import json
from datetime import datetime
import streamlit as st
from enum import Enum
from dataclasses import dataclass
import inspect
import time

# Core DSPy Signatures - AI-Heavy Operations Only
class TrendAnalyzer(dspy.Signature):
    """Analyze social media trends and identify content opportunities"""
    
    user_profile: str = dspy.InputField(desc="User expertise, interests, and cultural context")
    raw_trend_data: str = dspy.InputField(desc="Raw trend data from social media platforms")
    platform_focus: str = dspy.InputField(desc="Primary social media platforms to analyze")
    
    trending_topics: str = dspy.OutputField(desc="Top 5 trending topics with relevance scores")
    content_opportunities: str = dspy.OutputField(desc="Specific content ideas with engagement predictions")
    cultural_insights: str = dspy.OutputField(desc="Cultural adaptation recommendations")


class ContentStrategist(dspy.Signature):
    """Generate comprehensive content strategy based on trends and user goals"""
    
    user_goals: str = dspy.InputField(desc="Business goals, target audience, and brand positioning")
    trending_insights: str = dspy.InputField(desc="Current trending topics and opportunities")
    content_type: str = dspy.InputField(desc="Desired content type and platform specifications")
    
    content_strategy: str = dspy.OutputField(desc="Detailed content strategy with hooks and messaging")
    engagement_tactics: str = dspy.OutputField(desc="Specific tactics to maximize engagement")
    success_metrics: str = dspy.OutputField(desc="Expected outcomes and KPIs")


class BilingualContentCreator(dspy.Signature):
    """Create engaging bilingual content optimized for cultural context"""
    
    strategy_brief: str = dspy.InputField(desc="Content strategy and key messaging points")
    language_requirements: str = dspy.InputField(desc="Language preferences and cultural context")
    platform_specs: str = dspy.InputField(desc="Platform requirements and best practices")
    trending_elements: str = dspy.InputField(desc="Trending hashtags, topics, or formats to incorporate")
    
    primary_content: str = dspy.OutputField(desc="Main content text optimized for engagement")
    secondary_content: str = dspy.OutputField(desc="Alternative language version if bilingual")
    hashtags_and_cta: str = dspy.OutputField(desc="Optimized hashtags and call-to-action")


class ConversationManager(dspy.Signature):
    """Manage intelligent conversations about content marketing strategy"""
    
    user_query: str = dspy.InputField(desc="User's question or request for assistance")
    conversation_context: str = dspy.InputField(desc="Previous conversation history and user profile")
    current_trends: str = dspy.InputField(desc="Latest trend data and content opportunities")
    
    response: str = dspy.OutputField(desc="Helpful, actionable response with specific recommendations")
    follow_up_questions: str = dspy.OutputField(desc="Suggested follow-up questions to deepen engagement")
    action_items: str = dspy.OutputField(desc="Specific next steps the user can take")


class ContentOptimizer(dspy.Signature):
    """Optimize existing content for better performance"""
    
    original_content: str = dspy.InputField(desc="Content to be optimized")
    performance_goals: str = dspy.InputField(desc="Desired improvements and target metrics")
    platform_context: str = dspy.InputField(desc="Platform-specific optimization requirements")
    
    optimized_content: str = dspy.OutputField(desc="Improved content with better engagement potential")
    optimization_rationale: str = dspy.OutputField(desc="Explanation of changes made and expected impact")
    ab_test_suggestions: str = dspy.OutputField(desc="Alternative versions for A/B testing")


class ContentStrategist(dspy.Signature):
    """Generate personalized content strategy based on trends and user profile"""
    
    user_profile: str = dspy.InputField(desc="User's brand, expertise, and target audience")
    trending_topics: str = dspy.InputField(desc="Current trending topics relevant to user")
    content_type: str = dspy.InputField(desc="Type of content to create (educational, motivational, etc.)")
    platform: str = dspy.InputField(desc="Target platform specifications")
    
    content_strategy: str = dspy.OutputField(desc="Detailed content strategy with hooks and messaging")
    target_outcome: str = dspy.OutputField(desc="Expected engagement and business outcomes")
    key_messages: str = dspy.OutputField(desc="Core messages to communicate")


class BilingualContentCreator(dspy.Signature):
    """Create engaging bilingual content optimized for specific platforms"""
    
    content_strategy: str = dspy.InputField(desc="Content strategy and key messages")
    language: str = dspy.InputField(desc="Target language (en, fr, or bilingual)")
    platform: str = dspy.InputField(desc="Platform specifications and requirements")
    cultural_context: str = dspy.InputField(desc="Cultural adaptation requirements")
    trending_elements: str = dspy.InputField(desc="Trending hashtags, topics, or formats to incorporate")
    
    content_text: str = dspy.OutputField(desc="Complete content with captions and descriptions")
    hashtags: str = dspy.OutputField(desc="Relevant hashtags optimized for platform and culture")
    call_to_action: str = dspy.OutputField(desc="Compelling call-to-action based on business goals")


class ChatAssistant(dspy.Signature):
    """Provide helpful responses about content marketing and social media strategy"""
    
    user_message: str = dspy.InputField(desc="User's question or request")
    user_context: str = dspy.InputField(desc="User's profile and previous conversation context")
    current_trends: str = dspy.InputField(desc="Current trending topics and opportunities")
    
    response: str = dspy.OutputField(desc="Helpful, actionable response with specific recommendations")
    suggested_actions: str = dspy.OutputField(desc="Specific next steps the user can take")


# React Agent States
class ReactState(Enum):
    THINK = "think"
    ACT = "act"
    RETHINK = "rethink"
    PLAN = "plan"
    EXECUTE = "execute"
    CREATE = "create"
    SLEEP = "sleep"

# Agent Types for Dynamic Creation
class AgentType(Enum):
    REACT = "react"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    PREDICT = "predict"

@dataclass
class AgentState:
    """Centralized agent state tracking"""
    current_state: ReactState = ReactState.SLEEP
    previous_state: Optional[ReactState] = None
    execution_result: Optional[Dict[str, Any]] = None
    error_occurred: bool = False
    success_metrics: Dict[str, float] = None
    task_complexity: float = 0.5
    timestamp: float = None
    iteration_count: int = 0
    current_task: Optional[str] = None
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.success_metrics is None:
            self.success_metrics = {}
        if self.context is None:
            self.context = {}
    
    def transition_to(self, new_state: ReactState):
        """Transition to a new state with proper tracking"""
        self.previous_state = self.current_state
        self.current_state = new_state
        self.timestamp = time.time()
    
    def update_result(self, result: Dict[str, Any], error: bool = False):
        """Update execution result and error status"""
        self.execution_result = result
        self.error_occurred = error
        self.timestamp = time.time()
    
    def increment_iteration(self):
        """Increment iteration counter"""
        self.iteration_count += 1

@dataclass
class BotState:
    """Main bot state container"""
    agentState: AgentState = None
    user_profile: Dict[str, Any] = None
    conversation_history: List[Dict[str, Any]] = None
    trends_cache: Dict[str, Any] = None
    cache_timestamp: Optional[float] = None
    created_agents: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.agentState is None:
            self.agentState = AgentState()
        if self.user_profile is None:
            self.user_profile = {}
        if self.conversation_history is None:
            self.conversation_history = []
        if self.trends_cache is None:
            self.trends_cache = {}
        if self.created_agents is None:
            self.created_agents = {}

@dataclass
class ExecutionContext:
    """Context for tracking execution state and results - DEPRECATED"""
    current_state: ReactState
    execution_result: Optional[Dict[str, Any]] = None
    error_occurred: bool = False
    success_metrics: Dict[str, float] = None
    task_complexity: float = 0.5
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.success_metrics is None:
            self.success_metrics = {}

class ReactDecisionEngine:
    """Neural-style decision engine for autonomous state transitions"""
    
    def __init__(self):
        self.state_history: List[ExecutionContext] = []
        self.context_memory: Dict[str, Any] = {}
        self.decision_weights = self._initialize_decision_matrix()
        self.learning_rate = 0.1
    
    def _initialize_decision_matrix(self) -> Dict[str, Dict[ReactState, float]]:
        """Initialize decision weights for state transitions"""
        return {
            "error_occurred": {
                ReactState.RETHINK: 0.9,
                ReactState.PLAN: 0.7,
                ReactState.THINK: 0.5,
                ReactState.SLEEP: 0.2
            },
            "high_success": {
                ReactState.EXECUTE: 0.8,
                ReactState.CREATE: 0.7,
                ReactState.ACT: 0.6,
                ReactState.PLAN: 0.4
            },
            "new_task": {
                ReactState.THINK: 0.9,
                ReactState.PLAN: 0.8,
                ReactState.ACT: 0.3
            },
            "complex_task": {
                ReactState.PLAN: 0.9,
                ReactState.THINK: 0.8,
                ReactState.RETHINK: 0.6
            },
            "simple_task": {
                ReactState.ACT: 0.8,
                ReactState.EXECUTE: 0.7,
                ReactState.CREATE: 0.5
            },
            "fatigue": {
                ReactState.SLEEP: 0.9,
                ReactState.RETHINK: 0.3,
                ReactState.PLAN: 0.2
            }
        }
    
    def decide_next_state(self, agent_state: AgentState) -> ReactState:
        """Decide the next state based on agent state and history"""
        
        # Analyze current context
        context_factors = self._analyze_agent_state(agent_state)
        
        # Calculate weighted scores for each possible next state
        state_scores = {}
        for state in ReactState:
            score = 0.0
            for factor, weight in context_factors.items():
                if factor in self.decision_weights:
                    score += self.decision_weights[factor].get(state, 0.0) * weight
            state_scores[state] = score
        
        # Add randomness for exploration
        import random
        exploration_factor = 0.1
        for state in state_scores:
            state_scores[state] += random.uniform(0, exploration_factor)
        
        # Select state with highest score
        next_state = max(state_scores, key=state_scores.get)
        
        # Update history (convert agent_state to execution_context for compatibility)
        execution_context = ExecutionContext(
            current_state=agent_state.current_state,
            execution_result=agent_state.execution_result,
            error_occurred=agent_state.error_occurred,
            success_metrics=agent_state.success_metrics,
            task_complexity=agent_state.task_complexity,
            timestamp=agent_state.timestamp
        )
        
        self.state_history.append(execution_context)
        if len(self.state_history) > 50:  # Keep last 50 contexts
            self.state_history.pop(0)
        
        return next_state
    
    def _analyze_agent_state(self, agent_state: AgentState) -> Dict[str, float]:
        """Analyze agent state to determine relevant factors"""
        factors = {}
        
        # Error analysis
        if agent_state.error_occurred:
            factors["error_occurred"] = 1.0
        
        # Success analysis
        avg_success = sum(agent_state.success_metrics.values()) / max(len(agent_state.success_metrics), 1)
        if avg_success > 0.8:
            factors["high_success"] = avg_success
        
        # Task complexity analysis
        if agent_state.task_complexity > 0.7:
            factors["complex_task"] = agent_state.task_complexity
        elif agent_state.task_complexity < 0.3:
            factors["simple_task"] = 1.0 - agent_state.task_complexity
        
        # Fatigue analysis (based on recent activity)
        recent_contexts = [c for c in self.state_history if time.time() - c.timestamp < 300]  # Last 5 minutes
        if len(recent_contexts) > 10:
            factors["fatigue"] = min(len(recent_contexts) / 20.0, 1.0)
        
        # New task detection
        if not self.state_history or agent_state.current_state == ReactState.THINK:
            factors["new_task"] = 1.0
        
        return factors

class DSPyContentAgent:
    """Self-Automated React DSPy-powered content marketing agent"""
    
    def __init__(self):
        # Initialize DSPy with OpenAI (updated API)
        openai_key = self._get_api_key("OPENAI_API_KEY")
        if openai_key:
            import os
            os.environ["OPENAI_API_KEY"] = openai_key
            lm = dspy.LM(model="gpt-3.5-turbo", api_key=openai_key)
            dspy.settings.configure(lm=lm)
        
        # Signature Management System
        self.signatures: List[Type[dspy.Signature]] = [
            TrendAnalyzer,
            ContentStrategist, 
            BilingualContentCreator,
            ConversationManager,
            ContentOptimizer,
            ChatAssistant
        ]
        
        # Initialize DSPy modules for AI-heavy operations only
        self.trend_analyzer = dspy.ChainOfThought(TrendAnalyzer)
        self.content_strategist = dspy.ChainOfThought(ContentStrategist)
        self.content_creator = dspy.ChainOfThought(BilingualContentCreator)
        self.conversation_manager = dspy.ChainOfThought(ConversationManager)
        self.content_optimizer = dspy.ChainOfThought(ContentOptimizer)
        
        # React Agent System with Centralized State
        self.decision_engine = ReactDecisionEngine()
        self.botState = BotState()
        
        # Tools available to the React agent
        self.tools = {
            "createAgent": self.createAgent,
            "analyze_trends": self.analyze_trends_with_apify,
            "generate_content": self.generate_content_with_trends,
            "chat_response": self.chat_response,
            "optimize_content": self.optimize_content
        }
    
    def _get_api_key(self, key_name: str) -> str:
        """Get API key from Streamlit secrets or environment"""
        try:
            return st.secrets[key_name]
        except:
            import os
            return os.getenv(key_name, "")
    
    def createAgent(
        self, 
        agent_type: Union[str, AgentType], 
        signature: Union[str, Type[dspy.Signature], dspy.Signature],
        agent_name: Optional[str] = None
    ) -> Any:
        """
        Dynamic agent creation tool for the React agent
        
        Args:
            agent_type: Type of agent ('react', 'chain_of_thought', 'predict' or AgentType enum)
            signature: DSPy signature (class, instance, or string name from self.signatures)
            agent_name: Optional name for the created agent
        
        Returns:
            Created DSPy agent instance
        """
        try:
            # Normalize agent type
            if isinstance(agent_type, str):
                agent_type = AgentType(agent_type.lower())
            
            # Resolve signature
            resolved_signature = self._resolve_signature(signature)
            if resolved_signature is None:
                raise ValueError(f"Could not resolve signature: {signature}")
            
            # Create agent based on type
            if agent_type == AgentType.REACT:
                agent = dspy.ReAct(resolved_signature)
            elif agent_type == AgentType.CHAIN_OF_THOUGHT:
                agent = dspy.ChainOfThought(resolved_signature)
            elif agent_type == AgentType.PREDICT:
                agent = dspy.Predict(resolved_signature)
            else:
                raise ValueError(f"Unsupported agent type: {agent_type}")
            
            # Store created agent
            if agent_name:
                self.botState.created_agents[agent_name] = agent
            
            return agent
            
        except Exception as e:
            raise RuntimeError(f"Failed to create agent: {str(e)}")
    
    def _resolve_signature(self, signature: Union[str, Type[dspy.Signature], dspy.Signature]) -> Optional[Type[dspy.Signature]]:
        """
        Resolve signature from various input types
        
        Args:
            signature: String name, signature class, or signature instance
            
        Returns:
            Resolved signature class or None if not found
        """
        # If it's already a signature class
        if inspect.isclass(signature) and issubclass(signature, dspy.Signature):
            return signature
        
        # If it's a signature instance, get its class
        if isinstance(signature, dspy.Signature):
            return type(signature)
        
        # If it's a string, search in self.signatures
        if isinstance(signature, str):
            for sig_class in self.signatures:
                if sig_class.__name__.lower() == signature.lower():
                    return sig_class
                # Also check for partial matches
                if signature.lower() in sig_class.__name__.lower():
                    return sig_class
        
        return None
    
    async def react_engine(
        self, 
        task: str, 
        context: Optional[Dict[str, Any]] = None,
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Self-automated React engine with try-except-finally preprocessing
        
        Args:
            task: The task to execute
            context: Optional context for the task
            max_iterations: Maximum number of state transitions
            
        Returns:
            Final execution result
        """
        
        if context is None:
            context = {}
        
        iteration_count = 0
        final_result = {}
        
        # Initialize agent state
        self.botState.agentState.current_task = task
        self.botState.agentState.task_complexity = self._estimate_task_complexity(task)
        self.botState.agentState.transition_to(ReactState.THINK)
        self.botState.agentState.context = context
        
        while iteration_count < max_iterations:
            iteration_count += 1
            
            try:
                # Execute current state
                state_result = await self._execute_state(task, context)
                
                # Update agent state with results
                self.botState.agentState.update_result(state_result, error=False)
                
                # Calculate success metrics
                success_metrics = self._calculate_success_metrics(state_result)
                self.botState.agentState.success_metrics = success_metrics
                
                # Update final result
                final_result.update(state_result)
                
                # Check if task is complete
                if self._is_task_complete(state_result, task):
                    final_result["status"] = "completed"
                    final_result["iterations"] = iteration_count
                    break
                    
            except Exception as e:
                # Handle errors
                error_result = {"error": str(e)}
                self.botState.agentState.update_result(error_result, error=True)
                
                final_result["error"] = str(e)
                final_result["error_state"] = self.botState.agentState.current_state.value
                
            finally:
                # PREPROCESSING FOR NEXT ROUND
                next_state = self.decision_engine.decide_next_state(self.botState.agentState)
                
                # Log state transition
                final_result.setdefault("state_transitions", []).append({
                    "from": self.botState.agentState.current_state.value,
                    "to": next_state.value,
                    "iteration": iteration_count,
                    "timestamp": time.time(),
                    "context": {
                        "error_occurred": self.botState.agentState.error_occurred,
                        "success_metrics": self.botState.agentState.success_metrics,
                        "task_complexity": self.botState.agentState.task_complexity
                    }
                })
                
                # Update agent state for next iteration
                self.botState.agentState.transition_to(next_state)
                self.botState.agentState.increment_iteration()
                
                # Sleep state handling
                if next_state == ReactState.SLEEP:
                    sleep_duration = self._calculate_sleep_duration()
                    final_result["sleep_duration"] = sleep_duration
                    await asyncio.sleep(sleep_duration)
                    # After sleep, transition to THINK
                    self.botState.agentState.transition_to(ReactState.THINK)
        
        final_result["final_state"] = self.botState.agentState.current_state.value
        final_result["total_iterations"] = iteration_count
        
        return final_result
    
    async def _execute_state(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the current state action"""
        
        state = self.botState.agentState.current_state
        
        if state == ReactState.THINK:
            return await self._think(task, context)
        elif state == ReactState.ACT:
            return await self._act(task, context)
        elif state == ReactState.RETHINK:
            return await self._rethink(task, context)
        elif state == ReactState.PLAN:
            return await self._plan(task, context)
        elif state == ReactState.EXECUTE:
            return await self._execute(task, context)
        elif state == ReactState.CREATE:
            return await self._create(task, context)
        elif state == ReactState.SLEEP:
            return {"action": "sleep", "duration": self._calculate_sleep_duration()}
        else:
            return {"error": f"Unknown state: {state}"}
    
    async def _think(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Think state: Analyze the task and gather information"""
        
        # Use conversation manager to think about the task
        thinking_prompt = f"""
        Task: {task}
        Context: {json.dumps(context, indent=2)}
        
        I need to think about this task and understand:
        1. What exactly needs to be done?
        2. What information do I need?
        3. What approach should I take?
        4. What are the potential challenges?
        """
        
        try:
            # Create a thinking agent if needed
            thinking_agent = self.createAgent("chain_of_thought", "ConversationManager", "thinking_agent")
            
            result = thinking_agent(
                user_query=thinking_prompt,
                conversation_context="Task analysis and planning phase",
                current_trends="Analyzing current task requirements"
            )
            
            return {
                "action": "think",
                "analysis": result.response,
                "follow_up": result.follow_up_questions,
                "action_items": result.action_items,
                "complexity_assessment": self._estimate_task_complexity(task)
            }
            
        except Exception as e:
            return {
                "action": "think",
                "analysis": f"Basic task analysis: {task}",
                "error": str(e),
                "complexity_assessment": 0.5
            }
    
    async def _act(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Act state: Take direct action on the task"""
        
        # Determine what type of action to take based on task
        if "content" in task.lower() or "generate" in task.lower():
            return await self._act_content_generation(task, context)
        elif "trend" in task.lower() or "analyze" in task.lower():
            return await self._act_trend_analysis(task, context)
        elif "chat" in task.lower() or "respond" in task.lower():
            return await self._act_chat_response(task, context)
        else:
            return await self._act_general(task, context)
    
    async def _act_content_generation(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Act on content generation tasks"""
        
        user_profile = context.get("user_profile", {})
        platform = context.get("platform", "instagram")
        content_type = context.get("content_type", "educational")
        language = context.get("language", "en")
        
        result = await self.generate_content_with_trends(
            user_profile=user_profile,
            platform=platform,
            content_type=content_type,
            language=language
        )
        
        return {
            "action": "act_content_generation",
            "result": result,
            "success": bool(result.get("content_text"))
        }
    
    async def _act_trend_analysis(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Act on trend analysis tasks"""
        
        user_profile = context.get("user_profile", {})
        trend_data = await self.analyze_trends_with_apify(user_profile)
        
        return {
            "action": "act_trend_analysis",
            "result": trend_data,
            "success": bool(trend_data.get("trending_topics"))
        }
    
    async def _act_chat_response(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Act on chat response tasks"""
        
        user_message = context.get("user_message", task)
        user_profile = context.get("user_profile", {})
        conversation_history = context.get("conversation_history", [])
        
        response = await self.chat_response(user_message, user_profile, conversation_history)
        
        return {
            "action": "act_chat_response",
            "result": {"response": response},
            "success": bool(response)
        }
    
    async def _act_general(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """General action for unspecified tasks"""
        
        return {
            "action": "act_general",
            "result": {"message": f"Executed general action for: {task}"},
            "success": True
        }
    
    async def _rethink(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Rethink state: Reconsider approach after errors or suboptimal results"""
        
        previous_result = self.botState.agentState.execution_result
        error_info = previous_result.get("error", "No specific error") if previous_result else "No previous result"
        
        rethinking_prompt = f"""
        Original Task: {task}
        Previous Result: {json.dumps(previous_result, indent=2) if previous_result else 'None'}
        Error/Issue: {error_info}
        
        I need to rethink this approach because something went wrong or the result wasn't optimal.
        What should I do differently?
        """
        
        try:
            rethinking_agent = self.createAgent("chain_of_thought", "ConversationManager", "rethinking_agent")
            
            result = rethinking_agent(
                user_query=rethinking_prompt,
                conversation_context="Error analysis and approach reconsideration",
                current_trends="Analyzing what went wrong and how to improve"
            )
            
            return {
                "action": "rethink",
                "analysis": result.response,
                "new_approach": result.action_items,
                "lessons_learned": result.follow_up_questions
            }
            
        except Exception as e:
            return {
                "action": "rethink",
                "analysis": f"Need to reconsider approach for: {task}",
                "error": str(e),
                "new_approach": "Try a simpler approach"
            }
    
    async def _plan(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Plan state: Create detailed execution plan"""
        
        planning_prompt = f"""
        Task: {task}
        Context: {json.dumps(context, indent=2)}
        
        Create a detailed step-by-step plan to accomplish this task:
        1. Break down the task into smaller steps
        2. Identify required resources and tools
        3. Estimate time and complexity for each step
        4. Identify potential risks and mitigation strategies
        """
        
        try:
            planning_agent = self.createAgent("chain_of_thought", "ContentStrategist", "planning_agent")
            
            result = planning_agent(
                user_goals=planning_prompt,
                trending_insights="Current task planning phase",
                content_type="Strategic planning and execution roadmap"
            )
            
            return {
                "action": "plan",
                "strategy": result.content_strategy,
                "tactics": result.engagement_tactics,
                "success_metrics": result.success_metrics,
                "plan_complexity": self._estimate_task_complexity(task)
            }
            
        except Exception as e:
            return {
                "action": "plan",
                "strategy": f"Basic plan for: {task}",
                "error": str(e),
                "plan_complexity": 0.5
            }
    
    async def _execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute state: Execute the planned actions"""
        
        # Get the plan from previous context if available
        plan = context.get("plan", {})
        
        # Execute based on the plan or task type
        if plan:
            return await self._execute_planned_action(plan, task, context)
        else:
            # Fallback to direct execution
            return await self._act(task, context)
    
    async def _execute_planned_action(self, plan: Dict[str, Any], task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific planned action"""
        
        strategy = plan.get("strategy", "")
        tactics = plan.get("tactics", "")
        
        # Use the strategy and tactics to guide execution
        execution_context = {
            **context,
            "execution_strategy": strategy,
            "execution_tactics": tactics
        }
        
        # Execute the main action
        result = await self._act(task, execution_context)
        
        return {
            "action": "execute_planned",
            "plan_used": plan,
            "execution_result": result,
            "success": result.get("success", False)
        }
    
    async def _create(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create state: Create new agents, tools, or resources"""
        
        # Determine what to create based on task and context
        if "agent" in task.lower():
            return await self._create_agent(task, context)
        elif "content" in task.lower():
            return await self._create_content(task, context)
        else:
            return await self._create_resource(task, context)
    
    async def _create_agent(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new specialized agent"""
        
        # Extract agent requirements from task
        agent_type = "chain_of_thought"  # Default
        signature = "ConversationManager"  # Default
        
        if "react" in task.lower():
            agent_type = "react"
        elif "predict" in task.lower():
            agent_type = "predict"
        
        # Create the agent
        try:
            agent_name = f"created_agent_{len(self.botState.created_agents)}"
            new_agent = self.createAgent(agent_type, signature, agent_name)
            
            return {
                "action": "create_agent",
                "agent_name": agent_name,
                "agent_type": agent_type,
                "signature": signature,
                "success": True
            }
            
        except Exception as e:
            return {
                "action": "create_agent",
                "error": str(e),
                "success": False
            }
    
    async def _create_content(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create new content"""
        
        return await self._act_content_generation(task, context)
    
    async def _create_resource(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create other resources"""
        
        return {
            "action": "create_resource",
            "resource": f"Created resource for: {task}",
            "success": True
        }
    
    def _estimate_task_complexity(self, task: str) -> float:
        """Estimate task complexity from 0.0 to 1.0"""
        
        complexity_indicators = {
            "generate": 0.6,
            "create": 0.7,
            "analyze": 0.8,
            "optimize": 0.9,
            "bilingual": 0.7,
            "multi-platform": 0.8,
            "trend": 0.6,
            "chat": 0.3,
            "simple": 0.2,
            "complex": 0.9,
            "advanced": 0.8
        }
        
        task_lower = task.lower()
        complexity = 0.5  # Default
        
        for indicator, weight in complexity_indicators.items():
            if indicator in task_lower:
                complexity = max(complexity, weight)
        
        # Adjust based on task length
        if len(task) > 100:
            complexity += 0.1
        
        return min(complexity, 1.0)
    
    def _calculate_success_metrics(self, result: Dict[str, Any]) -> Dict[str, float]:
        """Calculate success metrics from execution result"""
        
        metrics = {}
        
        # Basic success metric
        if result.get("success", False):
            metrics["execution_success"] = 1.0
        else:
            metrics["execution_success"] = 0.0
        
        # Error metric
        if "error" in result:
            metrics["error_rate"] = 1.0
        else:
            metrics["error_rate"] = 0.0
        
        # Content quality metric (if applicable)
        if "content_text" in result.get("result", {}):
            content_length = len(result["result"]["content_text"])
            metrics["content_quality"] = min(content_length / 500.0, 1.0)  # Normalize to 500 chars
        
        # Response quality metric (if applicable)
        if "response" in result.get("result", {}):
            response_length = len(result["result"]["response"])
            metrics["response_quality"] = min(response_length / 200.0, 1.0)  # Normalize to 200 chars
        
        return metrics
    
    def _is_task_complete(self, result: Dict[str, Any], task: str) -> bool:
        """Determine if the task is complete based on result"""
        
        # Check for explicit success indicators
        if result.get("success", False):
            return True
        
        # Check for content generation completion
        if "content_text" in result.get("result", {}):
            return True
        
        # Check for response completion
        if "response" in result.get("result", {}):
            return True
        
        # Check for analysis completion
        if "trending_topics" in result.get("result", {}):
            return True
        
        return False
    
    def _calculate_sleep_duration(self) -> float:
        """Calculate how long to sleep based on context"""
        
        # Base sleep duration
        base_duration = 1.0
        
        # Adjust based on recent activity
        recent_contexts = [c for c in self.decision_engine.state_history if time.time() - c.timestamp < 300]
        if len(recent_contexts) > 10:
            # High activity, longer sleep
            base_duration *= 2.0
        
        # Adjust based on errors
        recent_errors = sum(1 for c in recent_contexts if c.error_occurred)
        if recent_errors > 3:
            # Many errors, longer sleep to cool down
            base_duration *= 1.5
        
        return min(base_duration, 10.0)  # Max 10 seconds
    
    # Test method for the React agent system
    async def test_react_system(self) -> Dict[str, Any]:
        """Test the complete React agent system"""
        
        test_task = "Generate educational content about personal development"
        test_context = {
            "user_profile": {
                "name": "Test User",
                "expertise_areas": ["Personal Development"],
                "cultural_background": "cameroon",
                "primary_language": "en",
                "active_platforms": ["instagram", "tiktok"]
            },
            "platform": "instagram",
            "content_type": "educational",
            "language": "en"
        }
        
        print("🚀 Testing Self-Automated React Agent System...")
        print(f"📋 Task: {test_task}")
        print(f"🎯 Initial State: {self.botState.agentState.current_state.value}")
        
        # Run the React engine
        result = await self.react_engine(test_task, test_context, max_iterations=5)
        
        print(f"✅ Final State: {result.get('final_state', 'unknown')}")
        print(f"🔄 Total Iterations: {result.get('total_iterations', 0)}")
        print(f"📊 Status: {result.get('status', 'incomplete')}")
        
        # Print state transitions
        transitions = result.get('state_transitions', [])
        if transitions:
            print("\n🔄 State Transitions:")
            for i, transition in enumerate(transitions, 1):
                print(f"  {i}. {transition['from']} → {transition['to']} (iteration {transition['iteration']})")
        
        return result
    
    def get_bot_state_summary(self) -> Dict[str, Any]:
        """Get a summary of the current bot state"""
        
        return {
            "agent_state": {
                "current_state": self.botState.agentState.current_state.value,
                "previous_state": self.botState.agentState.previous_state.value if self.botState.agentState.previous_state else None,
                "current_task": self.botState.agentState.current_task,
                "iteration_count": self.botState.agentState.iteration_count,
                "error_occurred": self.botState.agentState.error_occurred,
                "task_complexity": self.botState.agentState.task_complexity
            },
            "created_agents": list(self.botState.created_agents.keys()),
            "cache_status": {
                "has_trends_cache": bool(self.botState.trends_cache),
                "cache_timestamp": self.botState.cache_timestamp
            },
            "conversation_history_length": len(self.botState.conversation_history),
            "available_signatures": [sig.__name__ for sig in self.signatures],
            "available_tools": list(self.tools.keys())
        }
    
    async def analyze_trends_with_apify(self, user_profile: Dict) -> Dict[str, Any]:
        """Analyze trends using Apify data"""
        
        # Check cache first (cache for 30 minutes)
        current_time = datetime.now()
        if (self.botState.cache_timestamp and 
            (current_time.timestamp() - self.botState.cache_timestamp) < 1800 and
            self.botState.trends_cache):
            return self.botState.trends_cache
        
        try:
            from ..api.apify_integration import ApifyTrendAnalyzer
            
            # Initialize Apify analyzer
            apify_analyzer = ApifyTrendAnalyzer()
            
            # Get trend data
            trend_data = await apify_analyzer.comprehensive_trend_analysis(
                user_interests=user_profile.get('expertise_areas', []),
                expertise_areas=user_profile.get('expertise_areas', []),
                cultural_context=user_profile.get('cultural_background', 'cameroon')
            )
            
            # Cache the results
            self.botState.trends_cache = trend_data
            self.botState.cache_timestamp = current_time.timestamp()
            
            return trend_data
            
        except Exception as e:
            st.warning(f"Apify trend analysis unavailable: {str(e)}")
            # Fallback to simulated trend data
            return self._get_fallback_trends(user_profile)
    
    def _get_fallback_trends(self, user_profile: Dict) -> Dict[str, Any]:
        """Fallback trend data when Apify is unavailable"""
        
        expertise = user_profile.get('expertise_areas', ['Personal Development'])[0]
        
        return {
            "trending_topics": [
                {
                    "topic": f"{expertise} Tips",
                    "platform": "instagram",
                    "engagement_score": 85.0,
                    "relevance_score": 9.2
                },
                {
                    "topic": "Monday Motivation",
                    "platform": "tiktok", 
                    "engagement_score": 92.0,
                    "relevance_score": 8.8
                },
                {
                    "topic": "Success Mindset",
                    "platform": "linkedin",
                    "engagement_score": 78.0,
                    "relevance_score": 9.0
                }
            ],
            "content_opportunities": [
                {
                    "topic": f"5 {expertise} Mistakes to Avoid",
                    "engagement_potential": 88.5,
                    "suggested_approach": "Educational carousel post with personal examples"
                },
                {
                    "topic": "Behind the Scenes: My Daily Routine",
                    "engagement_potential": 82.3,
                    "suggested_approach": "Authentic video showing your process"
                }
            ],
            "optimal_timing": {
                "instagram": ["Tuesday-Thursday: 11 AM - 1 PM", "Evening: 7 PM - 9 PM"],
                "tiktok": ["Tuesday-Thursday: 6 AM - 10 AM", "Weekend: 9 AM - 12 PM"]
            }
        }
    
    async def generate_content_with_trends(
        self, 
        user_profile: Dict, 
        platform: str, 
        content_type: str, 
        language: str,
        topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate content using DSPy pipeline with trend analysis"""
        
        try:
            # Step 1: Get trend data (simple Python utility)
            trend_data = await self.analyze_trends_with_apify(user_profile)
            
            # Step 2: DSPy Trend Analysis
            user_profile_str = self._format_user_profile(user_profile)
            trend_data_str = self._format_trend_data(trend_data)
            platform_focus = ", ".join(user_profile.get('active_platforms', [platform]))
            
            trend_analysis = self.trend_analyzer(
                user_profile=user_profile_str,
                raw_trend_data=trend_data_str,
                platform_focus=platform_focus
            )
            
            # Step 3: DSPy Content Strategy
            user_goals = self._format_user_goals(user_profile, content_type)
            
            strategy = self.content_strategist(
                user_goals=user_goals,
                trending_insights=trend_analysis.trending_topics,
                content_type=f"{content_type} for {platform}"
            )
            
            # Step 4: DSPy Content Creation
            language_requirements = self._format_language_requirements(language, user_profile)
            platform_specs = self._get_platform_specs(platform)
            trending_elements = self._format_trending_elements(trend_analysis)
            
            content = self.content_creator(
                strategy_brief=strategy.content_strategy,
                language_requirements=language_requirements,
                platform_specs=platform_specs,
                trending_elements=trending_elements
            )
            
            # Step 5: Parse and format results (simple Python)
            return self._format_content_result(content, strategy, trend_analysis, trend_data)
            
        except Exception as e:
            st.error(f"DSPy content generation failed: {str(e)}")
            return self._generate_fallback_content(user_profile, platform, content_type, language, topic)
    
    def _format_user_profile(self, user_profile: Dict) -> str:
        """Simple utility to format user profile for DSPy"""
        return f"""
        Name: {user_profile.get('name', 'Content Creator')}
        Brand: {user_profile.get('brand_name', 'Personal Brand')}
        Expertise: {', '.join(user_profile.get('expertise_areas', []))}
        Cultural Background: {user_profile.get('cultural_background', 'cameroon')}
        Primary Language: {user_profile.get('primary_language', 'en')}
        Active Platforms: {', '.join(user_profile.get('active_platforms', []))}
        """
    
    def _format_trend_data(self, trend_data: Dict) -> str:
        """Simple utility to format trend data for DSPy"""
        trending_topics = trend_data.get('trending_topics', [])[:5]
        return json.dumps({
            'trending_topics': trending_topics,
            'content_opportunities': trend_data.get('content_opportunities', [])[:3],
            'data_sources': trend_data.get('data_sources', {})
        }, indent=2)
    
    def _format_user_goals(self, user_profile: Dict, content_type: str) -> str:
        """Simple utility to format user goals for DSPy"""
        return f"""
        Content Type: {content_type}
        Business Goals: Lead generation and brand awareness
        Target Audience: {user_profile.get('cultural_background', 'cameroon')} professionals interested in {', '.join(user_profile.get('expertise_areas', []))}
        Brand Voice: Professional yet authentic, culturally aware
        Success Metrics: Engagement, shares, comments, lead generation
        """
    
    def _format_language_requirements(self, language: str, user_profile: Dict) -> str:
        """Simple utility to format language requirements for DSPy"""
        cultural_bg = user_profile.get('cultural_background', 'cameroon')
        return f"""
        Primary Language: {language}
        Cultural Context: {cultural_bg}
        Tone: Professional yet warm and authentic
        Cultural Adaptation: Include relevant cultural references and values
        Bilingual: {'Yes' if language == 'bilingual' else 'No'}
        """
    
    def _get_platform_specs(self, platform: str) -> str:
        """Simple utility to get platform specifications"""
        specs = {
            "instagram": "Visual-first, 1-3 sentences, engaging hooks, 5-10 hashtags, stories-friendly",
            "tiktok": "Short-form video script, trending sounds, quick hooks, viral potential",
            "linkedin": "Professional tone, thought leadership, longer form, industry insights",
            "facebook": "Community-focused, shareable, conversation starters, family-friendly",
            "youtube": "Educational or entertaining, longer form, clear value proposition"
        }
        return specs.get(platform, "General social media best practices")
    
    def _format_trending_elements(self, trend_analysis) -> str:
        """Simple utility to format trending elements for DSPy"""
        return f"""
        Trending Topics: {trend_analysis.trending_topics}
        Content Opportunities: {trend_analysis.content_opportunities}
        Cultural Insights: {trend_analysis.cultural_insights}
        """
    
    def _format_content_result(self, content, strategy, trend_analysis, trend_data) -> Dict[str, Any]:
        """Simple utility to format final content result"""
        
        # Parse hashtags from content
        hashtags = self._extract_hashtags(content.hashtags_and_cta)
        cta = self._extract_cta(content.hashtags_and_cta)
        
        return {
            "content_text": content.primary_content,
            "secondary_content": content.secondary_content if content.secondary_content else None,
            "hashtags": hashtags,
            "call_to_action": cta,
            "strategy": strategy.content_strategy,
            "engagement_tactics": strategy.engagement_tactics,
            "trending_topics": trend_analysis.trending_topics,
            "cultural_insights": trend_analysis.cultural_insights,
            "trend_data": trend_data
        }
    
    def _extract_hashtags(self, hashtags_and_cta: str) -> List[str]:
        """Simple utility to extract hashtags"""
        import re
        hashtags = re.findall(r'#\w+', hashtags_and_cta)
        return hashtags[:10]  # Limit to 10 hashtags
    
    def _extract_cta(self, hashtags_and_cta: str) -> str:
        """Simple utility to extract call-to-action"""
        lines = hashtags_and_cta.split('\n')
        for line in lines:
            if not line.startswith('#') and len(line.strip()) > 10:
                return line.strip()
        return "Share your thoughts in the comments!"
    
    def _generate_fallback_content(
        self, 
        user_profile: Dict, 
        platform: str, 
        content_type: str, 
        language: str,
        topic: Optional[str]
    ) -> Dict[str, Any]:
        """Fallback content generation when DSPy fails"""
        
        expertise = user_profile.get('expertise_areas', ['Personal Development'])[0]
        name = user_profile.get('name', 'Content Creator')
        
        templates = {
            "educational": {
                "en": f"🎯 {topic or 'Success'} Tips from {name}\n\nAs a {expertise.lower()} expert, here's what I've learned:\n\n✨ Focus on progress, not perfection\n✨ Consistency beats intensity\n✨ Your mindset shapes your reality\n\nWhat's your biggest challenge right now? 👇",
                "fr": f"🎯 Conseils {topic or 'Succès'} de {name}\n\nEn tant qu'expert en {expertise.lower()}, voici ce que j'ai appris:\n\n✨ Concentrez-vous sur le progrès, pas la perfection\n✨ La cohérence bat l'intensité\n✨ Votre état d'esprit façonne votre réalité\n\nQuel est votre plus grand défi en ce moment? 👇"
            }
        }
        
        content_template = templates.get(content_type, templates["educational"])
        content_text = content_template.get(language, content_template["en"])
        
        hashtags = [f"#{expertise.replace(' ', '')}", "#Success", "#Motivation"]
        if user_profile.get('cultural_background') == 'cameroon':
            hashtags.extend(["#CameroonPride", "#AfricanWisdom"])
        
        return {
            "content_text": content_text,
            "hashtags": hashtags,
            "call_to_action": "Share your thoughts in the comments!",
            "strategy": f"Educational content about {expertise} with personal touch",
            "trending_topics": f"Current focus on {expertise} and personal development",
            "optimal_timing": "Post during peak engagement hours for your audience"
        }
    
    async def chat_response(
        self, 
        user_message: str, 
        user_profile: Dict, 
        conversation_history: List[Dict]
    ) -> str:
        """Generate intelligent chat response using DSPy conversation management"""
        
        try:
            # Get current trends (simple utility)
            trend_data = await self.analyze_trends_with_apify(user_profile)
            
            # Format context for DSPy (simple utilities)
            conversation_context = self._format_conversation_context(user_profile, conversation_history)
            current_trends = self._format_trends_for_chat(trend_data)
            
            # DSPy Conversation Management
            response = self.conversation_manager(
                user_query=user_message,
                conversation_context=conversation_context,
                current_trends=current_trends
            )
            
            # Format response (simple utility)
            return self._format_chat_response(response)
            
        except Exception as e:
            # Simple fallback
            return self._generate_fallback_chat_response(user_message, user_profile)
    
    def _format_conversation_context(self, user_profile: Dict, conversation_history: List[Dict]) -> str:
        """Simple utility to format conversation context"""
        context = f"""
        User Profile:
        - Name: {user_profile.get('name', 'User')}
        - Expertise: {', '.join(user_profile.get('expertise_areas', []))}
        - Platforms: {', '.join(user_profile.get('active_platforms', []))}
        - Cultural Background: {user_profile.get('cultural_background', 'cameroon')}
        - Primary Language: {user_profile.get('primary_language', 'en')}
        
        Recent Conversation:
        """
        
        # Add last 3 messages for context
        recent_messages = conversation_history[-3:] if conversation_history else []
        for msg in recent_messages:
            context += f"- {msg.get('role', 'unknown')}: {msg.get('content', '')[:100]}...\n"
        
        return context
    
    def _format_trends_for_chat(self, trend_data: Dict) -> str:
        """Simple utility to format trends for chat context"""
        trending_topics = trend_data.get('trending_topics', [])[:3]
        opportunities = trend_data.get('content_opportunities', [])[:2]
        
        trends_summary = "Current Trending Topics:\n"
        for topic in trending_topics:
            trends_summary += f"- {topic.get('topic', 'Unknown')}: {topic.get('engagement_score', 0):.1f}% engagement\n"
        
        trends_summary += "\nContent Opportunities:\n"
        for opp in opportunities:
            trends_summary += f"- {opp.get('topic', 'Unknown')}: {opp.get('engagement_potential', 0):.1f}% potential\n"
        
        return trends_summary
    
    def _format_chat_response(self, response) -> str:
        """Simple utility to format chat response"""
        formatted_response = response.response
        
        if response.follow_up_questions and response.follow_up_questions.strip():
            formatted_response += f"\n\n**💡 Follow-up Questions:**\n{response.follow_up_questions}"
        
        if response.action_items and response.action_items.strip():
            formatted_response += f"\n\n**🎯 Action Items:**\n{response.action_items}"
        
        return formatted_response
    
    def _generate_fallback_chat_response(self, user_message: str, user_profile: Dict) -> str:
        """Simple fallback chat response"""
        expertise = ', '.join(user_profile.get('expertise_areas', ['personal development']))
        
        return f"""I understand you're asking about: "{user_message}"

Based on your expertise in {expertise}, here are some thoughts:

💡 **Quick Suggestion:** Focus on creating authentic content that showcases your knowledge while connecting with your audience's needs.

🎯 **Next Steps:**
- Consider creating educational content around this topic
- Share your personal experience or client success stories
- Engage with your audience by asking questions

Would you like me to help you create some content around this topic?"""
    
    async def optimize_content(
        self, 
        original_content: str, 
        performance_goals: str,
        platform: str,
        user_profile: Dict
    ) -> Dict[str, Any]:
        """Optimize existing content using DSPy"""
        
        try:
            # Format inputs for DSPy
            platform_context = f"""
            Platform: {platform}
            Platform Specs: {self._get_platform_specs(platform)}
            User Profile: {self._format_user_profile(user_profile)}
            """
            
            # DSPy Content Optimization
            optimization = self.content_optimizer(
                original_content=original_content,
                performance_goals=performance_goals,
                platform_context=platform_context
            )
            
            return {
                "optimized_content": optimization.optimized_content,
                "optimization_rationale": optimization.optimization_rationale,
                "ab_test_suggestions": optimization.ab_test_suggestions,
                "original_content": original_content
            }
            
        except Exception as e:
            # Simple fallback optimization
            return {
                "optimized_content": original_content,
                "optimization_rationale": f"Unable to optimize due to: {str(e)}",
                "ab_test_suggestions": "Try different hooks, hashtags, or call-to-actions",
                "original_content": original_content
            }
    
    def get_trend_summary(self, trend_data: Dict) -> str:
        """Get a formatted summary of current trends"""
        
        if not trend_data:
            return "No trend data available"
        
        summary = "📈 **Current Trends:**\n\n"
        
        trending_topics = trend_data.get('trending_topics', [])
        for i, topic in enumerate(trending_topics[:3], 1):
            summary += f"{i}. **{topic.get('topic', 'Unknown')}** ({topic.get('platform', 'general')})\n"
            summary += f"   Engagement: {topic.get('engagement_score', 0):.1f}% | Relevance: {topic.get('relevance_score', 0):.1f}/10\n\n"
        
        opportunities = trend_data.get('content_opportunities', [])
        if opportunities:
            summary += "💡 **Content Opportunities:**\n\n"
            for i, opp in enumerate(opportunities[:2], 1):
                summary += f"{i}. {opp.get('topic', 'Content Idea')}\n"
                summary += f"   Potential: {opp.get('engagement_potential', 0):.1f}%\n\n"
        
        return summary