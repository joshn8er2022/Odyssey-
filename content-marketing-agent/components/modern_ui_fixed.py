"""
Fixed Modern UI Components - Reliable HTML Rendering
Enhanced Streamlit components with better HTML handling
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import json

def render_modern_hero_fixed(title: str, subtitle: str, gradient_colors: List[str] = None):
    """Fixed modern hero section"""
    
    if gradient_colors is None:
        gradient_colors = ["#667eea", "#764ba2"]
    
    # Use a more reliable approach with containers and native Streamlit styling
    hero_container = st.container()
    
    with hero_container:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {gradient_colors[0]}, {gradient_colors[1]});
            padding: 4rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        ">
            <h1 style="
                color: white;
                font-size: 3.5rem;
                font-weight: 800;
                margin-bottom: 1rem;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                line-height: 1.2;
            ">{title}</h1>
            <p style="
                color: rgba(255,255,255,0.9);
                font-size: 1.3rem;
                margin-bottom: 2rem;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
                line-height: 1.6;
            ">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

def render_modern_card_fixed(title: str, content: str, icon: str = "🎯", accent_color: str = "#667eea"):
    """Fixed modern card component using native Streamlit elements"""
    
    # Create card using Streamlit's native container with custom CSS
    with st.container():
        # Add custom CSS for this specific card
        st.markdown(f"""
        <style>
        .card-container {{
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid rgba(0,0,0,0.05);
            border-top: 4px solid {accent_color};
            margin-bottom: 1rem;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .card-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }}
        .card-icon {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        .card-title {{
            color: #1a1a1a;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            line-height: 1.3;
        }}
        .card-content {{
            color: #666;
            line-height: 1.6;
            margin-bottom: 1rem;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Render card content
        st.markdown(f"""
        <div class="card-container">
            <div class="card-icon">{icon}</div>
            <h3 class="card-title">{title}</h3>
            <p class="card-content">{content}</p>
        </div>
        """, unsafe_allow_html=True)

def render_modern_stats_fixed(stats: List[Dict[str, Any]], title: str = "Key Metrics"):
    """Fixed modern stats display"""
    
    st.markdown(f"""
    <h2 style="
        text-align: center;
        color: #1a1a1a;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2rem;
    ">{title}</h2>
    """, unsafe_allow_html=True)
    
    # Use Streamlit's native columns with custom styling
    cols = st.columns(len(stats))
    
    for i, stat in enumerate(stats):
        with cols[i]:
            color = stat.get('color', '#667eea')
            
            # Use native Streamlit metric with custom styling
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 2rem 1rem;
                background: white;
                border-radius: 16px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border: 1px solid rgba(0,0,0,0.05);
                margin-bottom: 1rem;
            ">
                <div style="
                    font-size: 3rem;
                    font-weight: 800;
                    color: {color};
                    margin-bottom: 0.5rem;
                ">{stat['value']}</div>
                <div style="
                    color: #666;
                    font-size: 1rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                ">{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)

def render_modern_feature_grid_fixed(features: List[Dict[str, Any]], title: str = "Features"):
    """Fixed modern feature grid using native Streamlit layout"""
    
    st.markdown(f"""
    <h2 style="
        text-align: center;
        color: #1a1a1a;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 3rem;
    ">{title}</h2>
    """, unsafe_allow_html=True)
    
    # Create responsive grid using Streamlit columns
    cols_per_row = 3 if len(features) >= 3 else len(features)
    rows = [features[i:i + cols_per_row] for i in range(0, len(features), cols_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        
        for i, feature in enumerate(row):
            with cols[i]:
                render_modern_card_fixed(
                    title=feature['title'],
                    content=feature['description'],
                    icon=feature.get('icon', '🎯'),
                    accent_color=feature.get('color', '#667eea')
                )

def render_modern_alert_fixed(message: str, alert_type: str = "info"):
    """Fixed modern alert component"""
    
    colors = {
        "info": {"bg": "#e3f2fd", "border": "#2196f3", "text": "#0d47a1", "icon": "ℹ️"},
        "success": {"bg": "#e8f5e8", "border": "#4caf50", "text": "#1b5e20", "icon": "✅"},
        "warning": {"bg": "#fff3e0", "border": "#ff9800", "text": "#e65100", "icon": "⚠️"},
        "error": {"bg": "#ffebee", "border": "#f44336", "text": "#b71c1c", "icon": "❌"}
    }
    
    color_config = colors.get(alert_type, colors["info"])
    
    st.markdown(f"""
    <div style="
        background: {color_config['bg']};
        border-left: 4px solid {color_config['border']};
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: {color_config['text']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <span style="font-size: 1.2rem;">{color_config['icon']}</span>
        <span style="flex: 1; font-weight: 500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)

def render_modern_chat_interface_fixed(messages: List[Dict], user_input_key: str = "modern_chat_input"):
    """Fixed modern AI chat interface"""
    
    # Chat header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    ">
        <h2 style="
            color: #1a1a1a;
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
        ">💬 AI Assistant</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat messages using native Streamlit chat elements
    chat_container = st.container()
    
    with chat_container:
        for message in messages:
            if message['role'] == 'user':
                # User message (right-aligned)
                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: flex-end;
                    margin-bottom: 1rem;
                ">
                    <div style="
                        background: #667eea;
                        color: white;
                        padding: 1rem 1.5rem;
                        border-radius: 20px 20px 5px 20px;
                        max-width: 70%;
                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                    ">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Assistant message (left-aligned)
                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: flex-start;
                    margin-bottom: 1rem;
                ">
                    <div style="
                        background: white;
                        color: #1a1a1a;
                        padding: 1rem 1.5rem;
                        border-radius: 20px 20px 20px 5px;
                        max-width: 70%;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                        border: 1px solid rgba(0,0,0,0.05);
                    ">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Input area using native Streamlit components
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="Ask me anything about content marketing...",
            key=user_input_key,
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    return user_input, send_button

def add_modern_css_fixed():
    """Add reliable modern CSS styling"""
    
    st.markdown("""
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Modern button styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Modern input styles */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .stButton > button {
            padding: 0.5rem 1.5rem;
            font-size: 0.9rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)