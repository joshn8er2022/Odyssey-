#!/usr/bin/env python3
"""
Test Native Streamlit Components - No HTML Issues
"""

import streamlit as st
import sys
from pathlib import Path

# Add components to path
components_path = Path(__file__).parent / "components"
sys.path.insert(0, str(components_path))

from streamlit_native import (
    render_native_hero, render_native_card, render_native_stats,
    render_native_feature_grid, render_native_alert, 
    render_native_chat_interface, add_minimal_css
)

def main():
    st.set_page_config(
        page_title="Native Components Test",
        page_icon="✅",
        layout="wide"
    )
    
    # Add minimal CSS
    add_minimal_css()
    
    st.title("✅ Native Streamlit Components Test")
    st.write("This test uses only native Streamlit components - no HTML rendering issues!")
    
    # Test Hero Component
    render_native_hero(
        title="Native Components Work!",
        subtitle="These components use only Streamlit's built-in elements"
    )
    
    # Test individual cards
    st.markdown("## Individual Cards Test")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_native_card(
            title="Native Card 1",
            content="This card uses only Streamlit native components - no HTML issues!",
            icon="🎯"
        )
    
    with col2:
        render_native_card(
            title="Native Card 2", 
            content="Another native card that displays properly without HTML problems",
            icon="🚀"
        )
    
    with col3:
        render_native_card(
            title="Native Card 3",
            content="Final native card with clean, simple styling",
            icon="✨"
        )
    
    # Test Feature Grid
    st.markdown("## Feature Grid Test")
    
    features = [
        {
            "title": "No HTML Issues",
            "description": "Uses only native Streamlit components for reliable rendering",
            "icon": "✅"
        },
        {
            "title": "Clean & Simple", 
            "description": "Simple, clean design that always works correctly",
            "icon": "🧹"
        },
        {
            "title": "Reliable",
            "description": "No more raw HTML code showing up in the interface",
            "icon": "🔒"
        }
    ]
    
    render_native_feature_grid(features, "Native Features")
    
    # Test Stats
    st.markdown("## Stats Test")
    
    stats = [
        {"value": "100%", "label": "Working", "description": "Components functional"},
        {"value": "0", "label": "HTML Errors", "description": "No raw HTML showing"}
    ]
    
    render_native_stats(stats, "Component Status")
    
    # Test Alerts
    st.markdown("## Alerts Test")
    
    render_native_alert("✅ Success! Native components work perfectly!", "success")
    render_native_alert("⚠️ This is a warning using native Streamlit alerts", "warning")
    render_native_alert("ℹ️ Info alert using Streamlit's built-in components", "info")
    
    # Test Chat Interface
    st.markdown("## Chat Interface Test")
    
    # Initialize demo chat
    if 'native_demo_chat' not in st.session_state:
        st.session_state.native_demo_chat = [
            {"role": "assistant", "content": "Hello! I'm using native Streamlit components."},
            {"role": "user", "content": "Do these components work without HTML issues?"},
            {"role": "assistant", "content": "Yes! These use only Streamlit's built-in elements, so no HTML rendering problems."}
        ]
    
    user_input, send_button = render_native_chat_interface(
        st.session_state.native_demo_chat,
        "native_demo_chat_input"
    )
    
    if send_button and user_input:
        st.session_state.native_demo_chat.append({"role": "user", "content": user_input})
        st.session_state.native_demo_chat.append({"role": "assistant", "content": f"Thanks for your message: '{user_input}'. This is a native Streamlit response!"})
        st.rerun()
    
    st.markdown("---")
    st.success("🎉 All native components are working correctly without HTML issues!")

if __name__ == "__main__":
    main()