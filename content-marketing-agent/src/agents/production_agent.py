"""
Production-Ready Content Marketing Agent
Fixed DSPy initialization, direct scraper integration, and production optimizations
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
import os
import sys
from pathlib import Path

# Add scrapers to path
scrapers_path = Path(__file__).parent.parent / "scrapers"
sys.path.insert(0, str(scrapers_path))

from direct_scraper import DirectScraper

# Core DSPy Signatures
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

class ScraperQuery(dspy.Signature):
    """Query social media scrapers for specific content"""
    
    user_request: str = dspy.InputField(desc="User's request for specific social media content")
    target_platforms: str = dspy.InputField(desc="Platforms to scrape (twitter, tiktok, instagram)")
    search_terms: str = dspy.InputField(desc="Search terms or hashtags to use")
    
    scraper_strategy: str = dspy.OutputField(desc="Strategy for scraping the requested content")
    search_queries: str = dspy.OutputField(desc="Optimized search queries for each platform")
    analysis_focus: str = dspy.OutputField(desc="What to analyze in the scraped content")

# React Agent States
class ReactState(Enum):
    THINK = "think"
    ACT = "act"
    RETHINK = "rethink"
    PLAN = "plan"
    EXECUTE = "execute"
    CREATE = "create"
    SCRAPE = "scrape"
    SLEEP = "sleep"

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

class ProductionContentAgent:
    """Production-ready DSPy-powered content marketing agent"""
    
    def __init__(self):
        # Initialize DSPy with proper error handling
        self.dspy_initialized = False
        self._initialize_dspy()
        
        # Signature Management System
        self.signatures: List[Type[dspy.Signature]] = [
            TrendAnalyzer,
            ContentStrategist, 
            BilingualContentCreator,
            ConversationManager,
            ScraperQuery
        ]
        
        # Initialize DSPy modules only if DSPy is properly loaded
        if self.dspy_initialized:
            self.trend_analyzer = dspy.ChainOfThought(TrendAnalyzer)
            self.content_strategist = dspy.ChainOfThought(ContentStrategist)
            self.content_creator = dspy.ChainOfThought(BilingualContentCreator)
            self.conversation_manager = dspy.ChainOfThought(ConversationManager)
            self.scraper_query = dspy.ChainOfThought(ScraperQuery)
        
        # Direct scraper integration
        self.scraper = DirectScraper()
        
        # React Agent System
        self.botState = BotState()
        
        # Tools available to the React agent
        self.tools = {
            "createAgent": self.createAgent,
            "scrape_content": self.scrape_content,
            "analyze_trends": self.analyze_trends_direct,
            "generate_content": self.generate_content_with_trends,
            "chat_response": self.chat_response,
            "optimize_content": self.optimize_content
        }
    
    def _initialize_dspy(self):
        """Initialize DSPy with proper error handling"""
        try:
            openai_key = self._get_api_key("OPENAI_API_KEY")
            if openai_key:
                # Set environment variable for DSPy
                os.environ["OPENAI_API_KEY"] = openai_key
                
                # Initialize DSPy LM
                lm = dspy.LM(model="gpt-3.5-turbo", api_key=openai_key)
                dspy.settings.configure(lm=lm)
                
                self.dspy_initialized = True
                print("✅ DSPy initialized successfully")
            else:
                print("⚠️ No OpenAI API key found - DSPy features disabled")
                self.dspy_initialized = False
                
        except Exception as e:
            print(f"❌ DSPy initialization failed: {e}")
            self.dspy_initialized = False
    
    def _get_api_key(self, key_name: str) -> str:
        """Get API key from Streamlit secrets or environment"""
        try:
            return st.secrets[key_name]
        except:
            return os.getenv(key_name, "")
    
    async def scrape_content(self, query: str, platforms: List[str] = None, max_results: int = 10) -> Dict[str, Any]:
        """Direct scraper integration for real-time content"""
        
        try:
            if platforms is None:
                platforms = ["twitter", "tiktok", "instagram"]
            
            # Use direct scraper
            results = await self.scraper.scrape_multi_platform(query, platforms, max_results)
            
            # Format results
            formatted_results = {
                "query": query,
                "platforms": platforms,
                "timestamp": datetime.now().isoformat(),
                "data": results,
                "summary": self.scraper.format_scraper_results(results),
                "total_items": sum(len(data) for data in results.values())
            }
            
            return formatted_results
            
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "data": {},
                "summary": f"Scraping failed: {str(e)}",
                "total_items": 0
            }
    
    async def analyze_trends_direct(self, user_profile: Dict) -> Dict[str, Any]:
        """Direct trend analysis using scrapers"""
        
        try:
            # Get user interests for scraping
            expertise_areas = user_profile.get('expertise_areas', ['business'])
            
            # Scrape content for each expertise area
            all_results = {}
            
            for area in expertise_areas[:2]:  # Limit to 2 areas to avoid rate limits
                results = await self.scrape_content(area, max_results=5)
                all_results[area] = results
            
            # Process results into trend format
            trending_topics = []
            content_opportunities = []
            
            for area, results in all_results.items():
                if results.get('data'):
                    for platform, data in results['data'].items():
                        for item in data[:3]:  # Top 3 per platform
                            trending_topics.append({
                                "topic": f"{area} - {item['text'][:50]}...",
                                "platform": platform,
                                "engagement_score": item['engagement_score'],
                                "relevance_score": 8.5,  # High relevance since it's user's expertise
                                "source_data": item
                            })
                            
                            content_opportunities.append({
                                "topic": f"Create content about {area} inspired by @{item['author']}",
                                "engagement_potential": item['engagement_score'],
                                "suggested_approach": f"Respond to or build upon this {platform} post"
                            })
            
            # Cache the results
            trend_data = {
                "trending_topics": trending_topics,
                "content_opportunities": content_opportunities,
                "data_sources": {
                    "twitter_posts_count": sum(len(r.get('data', {}).get('twitter', [])) for r in all_results.values()),
                    "tiktok_videos_count": sum(len(r.get('data', {}).get('tiktok', [])) for r in all_results.values()),
                    "instagram_posts_count": sum(len(r.get('data', {}).get('instagram', [])) for r in all_results.values())
                },
                "analysis_timestamp": datetime.now().isoformat(),
                "raw_scraper_data": all_results
            }
            
            self.botState.trends_cache = trend_data
            self.botState.cache_timestamp = time.time()
            
            return trend_data
            
        except Exception as e:
            # Fallback to sample data
            return self._get_fallback_trends(user_profile)
    
    def _get_fallback_trends(self, user_profile: Dict) -> Dict[str, Any]:
        """Fallback trend data when scraping fails"""
        
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
            "data_sources": {
                "twitter_posts_count": 0,
                "tiktok_videos_count": 0,
                "instagram_posts_count": 0
            },
            "analysis_timestamp": datetime.now().isoformat()
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
            # Step 1: Get trend data using direct scraper
            trend_data = await self.analyze_trends_direct(user_profile)
            
            if self.dspy_initialized:
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
                
                # Step 5: Parse and format results
                return self._format_content_result(content, strategy, trend_analysis, trend_data)
            else:
                # Fallback without DSPy
                return self._generate_fallback_content(user_profile, platform, content_type, language, topic)
                
        except Exception as e:
            st.error(f"Content generation failed: {str(e)}")
            return self._generate_fallback_content(user_profile, platform, content_type, language, topic)
    
    async def chat_response(
        self, 
        user_message: str, 
        user_profile: Dict, 
        conversation_history: List[Dict]
    ) -> str:
        """Enhanced chat response with scraper integration"""
        
        try:
            # Check if user is asking for specific content scraping
            scraping_keywords = ["scrape", "find", "show me", "get content", "trending", "what's popular"]
            
            if any(keyword in user_message.lower() for keyword in scraping_keywords):
                # Extract search terms from user message
                search_terms = self._extract_search_terms(user_message, user_profile)
                
                if search_terms:
                    # Perform direct scraping
                    scrape_results = await self.scrape_content(search_terms, max_results=5)
                    
                    response = f"🔍 **Found real-time content for '{search_terms}':**\n\n"
                    response += scrape_results['summary']
                    
                    if self.dspy_initialized:
                        # Use DSPy to analyze the scraped content
                        try:
                            analysis = self.conversation_manager(
                                user_query=f"Analyze this scraped content and provide insights: {scrape_results['summary'][:500]}",
                                conversation_context=self._format_conversation_context(user_profile, conversation_history),
                                current_trends=scrape_results['summary']
                            )
                            
                            response += f"\n\n**🤖 AI Analysis:**\n{analysis.response}"
                            
                            if analysis.action_items:
                                response += f"\n\n**🎯 Suggested Actions:**\n{analysis.action_items}"
                                
                        except Exception as e:
                            response += f"\n\n💡 **Quick Insight:** This content shows current engagement patterns in your niche. Consider creating similar content with your unique perspective!"
                    
                    return response
            
            # Regular chat response
            if self.dspy_initialized:
                # Get current trends
                trend_data = await self.analyze_trends_direct(user_profile)
                
                # Format context for DSPy
                conversation_context = self._format_conversation_context(user_profile, conversation_history)
                current_trends = self._format_trends_for_chat(trend_data)
                
                # DSPy Conversation Management
                response = self.conversation_manager(
                    user_query=user_message,
                    conversation_context=conversation_context,
                    current_trends=current_trends
                )
                
                # Format response
                return self._format_chat_response(response)
            else:
                # Simple fallback
                return self._generate_fallback_chat_response(user_message, user_profile)
                
        except Exception as e:
            # Simple fallback
            return self._generate_fallback_chat_response(user_message, user_profile)
    
    def _extract_search_terms(self, user_message: str, user_profile: Dict) -> str:
        """Extract search terms from user message"""
        
        # Simple extraction - look for quoted terms or use expertise areas
        message_lower = user_message.lower()
        
        # Look for quoted terms
        import re
        quoted_terms = re.findall(r'"([^"]*)"', user_message)
        if quoted_terms:
            return quoted_terms[0]
        
        # Look for hashtags
        hashtags = re.findall(r'#(\w+)', user_message)
        if hashtags:
            return hashtags[0]
        
        # Use expertise areas as fallback
        expertise_areas = user_profile.get('expertise_areas', ['business'])
        
        for area in expertise_areas:
            if area.lower() in message_lower:
                return area
        
        # Default to first expertise area
        return expertise_areas[0] if expertise_areas else "business"
    
    def createAgent(
        self, 
        agent_type: Union[str, AgentType], 
        signature: Union[str, Type[dspy.Signature], dspy.Signature],
        agent_name: Optional[str] = None
    ) -> Any:
        """Dynamic agent creation tool for the React agent"""
        
        if not self.dspy_initialized:
            raise RuntimeError("DSPy not initialized - cannot create agents")
        
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
        """Resolve signature from various input types"""
        
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
    
    # Helper methods (keeping the existing ones from the original agent)
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
        
        if not self.dspy_initialized:
            return {
                "optimized_content": original_content,
                "optimization_rationale": "DSPy not available - no optimization performed",
                "ab_test_suggestions": "Try different hooks, hashtags, or call-to-actions",
                "original_content": original_content
            }
        
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
            "available_tools": list(self.tools.keys()),
            "dspy_initialized": self.dspy_initialized,
            "scraper_available": bool(self.scraper.api_token)
        }