"""
Main application file for the Apstra Configlet Builder.

This file orchestrates the UI components and manages the overall
application flow.
"""
import os
import sys
sys.path.append(os.getcwd())  # Add the current directory to the Python path
import streamlit as st

from app.utils.config.session_state import initialize_session_state
from app.ui.sidebar import render_sidebar
from app.ui.context_input import render_context_input
from app.ui.property_input import render_property_input
from app.ui.template_input import render_template_input
from app.ui.render_output import render_output
from app.ui.api_actions import render_api_actions

def main():
    """
    Main function to run the Apstra Configlet Builder application.
    
    This function:
    1. Sets up the page configuration
    2. Initializes the session state
    3. Renders the UI components in the correct order
    
    Returns:
        None
    """
    # Set page configuration
    st.set_page_config(
        page_title="Apstra Configlet Builder",
        page_icon="🔧",
        layout="wide"
    )
    
    # Set application title
    st.title("Apstra Configlet Builder")
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar (login and connection controls)
    render_sidebar()
    
    # Create a container for the main content
    with st.container():
        # Apply custom CSS for bordered containers
        st.markdown(
            '''
            <style>
            .bordered-container {
                border: 1px solid #CCCCCC;
                padding: 10px;
                border-radius: 5px;
            }
            </style>
            ''',
            unsafe_allow_html=True,
        )
        
        # Create two columns for context and property inputs
        col1, col2 = st.columns(2)
        
        with col1:
            # Render context input component
            render_context_input()
        
        with col2:
            # Render property input component
            render_property_input()
    
    # Add a divider
    st.divider()
    
    # Render template input component
    render_template_input()
    
    # Add a divider
    st.divider()
    
    # Render output component
    render_output()
    
    # Add a divider
    st.divider()
    
    # Render API actions component
    render_api_actions()

if __name__ == "__main__":
    main()