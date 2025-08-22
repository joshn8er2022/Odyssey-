"""
Modern UI Components inspired by 21st.dev
Enhanced Streamlit components with better styling and interactions
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import json

def render_modern_hero(title: str, subtitle: str, cta_text: str = "Get Started", gradient_colors: List[str] = None):
    """Modern hero section inspired by 21st.dev"""
    
    if gradient_colors is None:
        gradient_colors = ["#667eea", "#764ba2"]
    
    gradient = f"linear-gradient(135deg, {gradient_colors[0]}, {gradient_colors[1]})"
    
    st.markdown(f"""
    <div style="
        background: {gradient};
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: relative;
            z-index: 2;
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
        <div style="
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        "></div>
    </div>
    
    <style>
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-20px) rotate(180deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_modern_card(title: str, content: str, icon: str = "🎯", accent_color: str = "#667eea", 
                      action_text: str = None, key: str = None):
    """Modern card component inspired by 21st.dev"""
    
    # Create a container for the card
    card_container = st.container()
    
    with card_container:
        # Use Streamlit's native components with custom CSS
        st.markdown(f"""
        <div class="modern-card" style="
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            height: 100%;
            position: relative;
            overflow: hidden;
            margin-bottom: 1rem;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: {accent_color};
            "></div>
            
            <div style="
                font-size: 2.5rem;
                margin-bottom: 1rem;
                text-align: center;
            ">{icon}</div>
            
            <h3 style="
                color: #1a1a1a;
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
                line-height: 1.3;
                text-align: center;
            ">{title}</h3>
            
            <p style="
                color: #666;
                line-height: 1.6;
                margin-bottom: 1rem;
                text-align: center;
            ">{content}</p>
        </div>
        
        <style>
        .modern-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Add action button if specified
        if action_text:
            st.markdown(f"""
            <div style="text-align: center; margin-top: -1rem; margin-bottom: 1rem;">
                <button style="
                    background: {accent_color};
                    color: white;
                    border: none;
                    padding: 0.75rem 1.5rem;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">{action_text}</button>
            </div>
            """, unsafe_allow_html=True)

def render_modern_stats(stats: List[Dict[str, Any]], title: str = "Key Metrics"):
    """Modern stats display inspired by 21st.dev"""
    
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h2 style="
            text-align: center;
            color: #1a1a1a;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 2rem;
        ">{title}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(stats))
    
    for i, stat in enumerate(stats):
        with cols[i]:
            color = stat.get('color', '#667eea')
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 2rem 1rem;
                background: white;
                border-radius: 16px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border: 1px solid rgba(0,0,0,0.05);
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 20px 40px rgba(0,0,0,0.15)'"
               onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)'"
            >
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
                
                {f'<div style="color: #999; font-size: 0.9rem; margin-top: 0.5rem;">{stat["description"]}</div>' if stat.get('description') else ''}
            </div>
            """, unsafe_allow_html=True)

def render_modern_chat_interface(messages: List[Dict], user_input_key: str = "modern_chat_input"):
    """Modern AI chat interface inspired by 21st.dev"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    ">
        <h2 style="
            text-align: center;
            color: #1a1a1a;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 2rem;
        ">💬 AI Assistant</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(messages):
            is_user = message['role'] == 'user'
            
            if is_user:
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
                        font-size: 1rem;
                        line-height: 1.5;
                    ">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
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
                        font-size: 1rem;
                        line-height: 1.5;
                    ">
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Modern input area
    st.markdown("""
    <div style="
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
        margin-top: 2rem;
    ">
    """, unsafe_allow_html=True)
    
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
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return user_input, send_button

def render_modern_feature_grid(features: List[Dict[str, Any]], title: str = "Features"):
    """Modern feature grid inspired by 21st.dev"""
    
    st.markdown(f"""
    <div style="margin-bottom: 3rem;">
        <h2 style="
            text-align: center;
            color: #1a1a1a;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 3rem;
        ">{title}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create responsive grid
    cols_per_row = 3 if len(features) >= 3 else len(features)
    rows = [features[i:i + cols_per_row] for i in range(0, len(features), cols_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        
        for i, feature in enumerate(row):
            with cols[i]:
                # Use direct HTML rendering instead of calling render_modern_card
                accent_color = feature.get('color', '#667eea')
                icon = feature.get('icon', '🎯')
                title_text = feature['title']
                content_text = feature['description']
                
                st.markdown(f"""
                <div style="
                    background: white;
                    border-radius: 16px;
                    padding: 2rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    border: 1px solid rgba(0,0,0,0.05);
                    transition: all 0.3s ease;
                    height: 100%;
                    position: relative;
                    overflow: hidden;
                    margin-bottom: 1rem;
                " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 20px 40px rgba(0,0,0,0.15)'"
                   onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)'"
                >
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 4px;
                        background: {accent_color};
                    "></div>
                    
                    <div style="
                        font-size: 2.5rem;
                        margin-bottom: 1rem;
                        text-align: center;
                    ">{icon}</div>
                    
                    <h3 style="
                        color: #1a1a1a;
                        font-size: 1.5rem;
                        font-weight: 700;
                        margin-bottom: 1rem;
                        line-height: 1.3;
                        text-align: center;
                    ">{title_text}</h3>
                    
                    <p style="
                        color: #666;
                        line-height: 1.6;
                        margin-bottom: 1rem;
                        text-align: center;
                    ">{content_text}</p>
                </div>
                """, unsafe_allow_html=True)

def render_modern_form(form_config: Dict[str, Any], form_key: str = "modern_form"):
    """Modern form component inspired by 21st.dev"""
    
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    ">
        <h2 style="
            text-align: center;
            color: #1a1a1a;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 2rem;
        ">{form_config.get('title', 'Form')}</h2>
        
        {f'<p style="text-align: center; color: #666; margin-bottom: 2rem; font-size: 1.1rem;">{form_config.get("description", "")}</p>' if form_config.get('description') else ''}
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(form_key):
        form_data = {}
        
        for field in form_config.get('fields', []):
            field_type = field.get('type', 'text')
            field_name = field['name']
            field_label = field.get('label', field_name.title())
            
            if field_type == 'text':
                form_data[field_name] = st.text_input(
                    field_label,
                    placeholder=field.get('placeholder', ''),
                    help=field.get('help', '')
                )
            elif field_type == 'select':
                form_data[field_name] = st.selectbox(
                    field_label,
                    options=field.get('options', []),
                    help=field.get('help', '')
                )
            elif field_type == 'multiselect':
                form_data[field_name] = st.multiselect(
                    field_label,
                    options=field.get('options', []),
                    help=field.get('help', '')
                )
            elif field_type == 'number':
                form_data[field_name] = st.number_input(
                    field_label,
                    min_value=field.get('min_value', 0),
                    max_value=field.get('max_value', 100),
                    value=field.get('default_value', 0),
                    help=field.get('help', '')
                )
            elif field_type == 'textarea':
                form_data[field_name] = st.text_area(
                    field_label,
                    placeholder=field.get('placeholder', ''),
                    help=field.get('help', '')
                )
        
        submit_button = st.form_submit_button(
            form_config.get('submit_text', 'Submit'),
            type="primary",
            use_container_width=True
        )
        
        return form_data, submit_button

def render_modern_sidebar(profile: Dict[str, Any], navigation_items: List[Dict[str, str]]):
    """Modern sidebar inspired by 21st.dev"""
    
    with st.sidebar:
        # Profile section
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 2rem 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
            color: white;
        ">
            <div style="
                width: 60px;
                height: 60px;
                background: rgba(255,255,255,0.2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1rem auto;
                font-size: 1.5rem;
            ">👤</div>
            
            <h3 style="
                margin: 0 0 0.5rem 0;
                font-size: 1.2rem;
                font-weight: 700;
            ">{profile.get('name', 'User')}</h3>
            
            <p style="
                margin: 0;
                opacity: 0.9;
                font-size: 0.9rem;
            ">{profile.get('brand_name', 'Content Creator')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### Navigation")
        
        selected_page = None
        for item in navigation_items:
            if st.button(
                item['label'],
                key=f"nav_{item['key']}",
                use_container_width=True
            ):
                selected_page = item['key']
        
        # Quick stats
        st.markdown("---")
        st.markdown("### Quick Stats")
        
        stats = [
            {"label": "Platforms", "value": len(profile.get('active_platforms', []))},
            {"label": "Expertise", "value": len(profile.get('expertise_areas', []))},
            {"label": "Language", "value": profile.get('primary_language', 'EN').upper()}
        ]
        
        for stat in stats:
            st.metric(stat['label'], stat['value'])
        
        return selected_page

def render_modern_alert(message: str, alert_type: str = "info", dismissible: bool = True):
    """Modern alert component inspired by 21st.dev"""
    
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

def add_modern_css():
    """Add modern CSS styling inspired by 21st.dev"""
    
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
    
    /* Modern selectbox styles */
    .stSelectbox > div > div > div {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
    }
    
    /* Modern metric styles */
    .metric-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    /* Modern sidebar styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Modern expander styles */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-up {
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
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