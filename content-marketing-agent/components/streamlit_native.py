"""
Native Streamlit Components - No HTML Rendering Issues
Using only Streamlit's built-in components with minimal custom CSS
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import json

def render_native_hero(title: str, subtitle: str):
    """Hero section using native Streamlit components"""
    
    # Create a colored container using Streamlit's built-in styling
    st.markdown("---")
    
    # Center the content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"# {title}")
        st.markdown(f"### {subtitle}")
        st.markdown("")
    
    st.markdown("---")

def render_native_card(title: str, content: str, icon: str = "🎯"):
    """Card using native Streamlit components"""
    
    # Use Streamlit's built-in container and styling
    with st.container():
        # Create a simple card using expander or container
        st.markdown(f"### {icon} {title}")
        st.write(content)
        st.markdown("---")

def render_native_stats(stats: List[Dict[str, Any]], title: str = "Key Metrics"):
    """Stats using native Streamlit metrics"""
    
    st.markdown(f"## {title}")
    
    # Use Streamlit's native metric component
    cols = st.columns(len(stats))
    
    for i, stat in enumerate(stats):
        with cols[i]:
            st.metric(
                label=stat['label'],
                value=stat['value'],
                help=stat.get('description', '')
            )

def render_native_feature_grid(features: List[Dict[str, Any]], title: str = "Features"):
    """Feature grid using native Streamlit layout"""
    
    st.markdown(f"## {title}")
    
    # Create responsive grid using Streamlit columns
    cols_per_row = 3 if len(features) >= 3 else len(features)
    rows = [features[i:i + cols_per_row] for i in range(0, len(features), cols_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        
        for i, feature in enumerate(row):
            with cols[i]:
                # Use native Streamlit components
                st.markdown(f"### {feature.get('icon', '🎯')} {feature['title']}")
                st.write(feature['description'])
                
                # Add some spacing
                st.markdown("")

def render_native_alert(message: str, alert_type: str = "info"):
    """Alert using native Streamlit components"""
    
    if alert_type == "success":
        st.success(message)
    elif alert_type == "warning":
        st.warning(message)
    elif alert_type == "error":
        st.error(message)
    else:
        st.info(message)

def render_native_chat_interface(messages: List[Dict], user_input_key: str = "native_chat_input"):
    """Chat interface using native Streamlit components"""
    
    st.markdown("## 💬 AI Assistant")
    
    # Display messages using native Streamlit chat
    for message in messages:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")
        st.markdown("")
    
    # Input area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="Ask me anything about content marketing...",
            key=user_input_key
        )
    
    with col2:
        send_button = st.button("Send", type="primary")
    
    return user_input, send_button

def render_native_form(form_config: Dict[str, Any], form_key: str = "native_form"):
    """Form using native Streamlit components"""
    
    st.markdown(f"## {form_config.get('title', 'Form')}")
    
    if form_config.get('description'):
        st.write(form_config['description'])
    
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
            type="primary"
        )
        
        return form_data, submit_button

def render_native_sidebar(profile: Dict[str, Any], navigation_items: List[Dict[str, str]]):
    """Sidebar using native Streamlit components"""
    
    with st.sidebar:
        # Profile section
        st.markdown("### 👤 Profile")
        st.write(f"**{profile.get('name', 'User')}**")
        st.write(f"Brand: {profile.get('brand_name', 'Content Creator')}")
        st.write(f"Language: {profile.get('primary_language', 'en').upper()}")
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### Navigation")
        
        selected_page = None
        for item in navigation_items:
            if st.button(item['label'], key=f"nav_{item['key']}", use_container_width=True):
                selected_page = item['key']
        
        # Quick stats
        st.markdown("---")
        st.markdown("### Quick Stats")
        
        st.metric("Platforms", len(profile.get('active_platforms', [])))
        st.metric("Expertise", len(profile.get('expertise_areas', [])))
        
        return selected_page

def add_minimal_css():
    """Add minimal CSS for better appearance"""
    
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Improve button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Improve input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)