"""
Session state management for the Apstra Configlet Builder.

This module handles session state initialization and access,
providing a consistent way for UI components to share data.
"""

import streamlit as st
from typing import Any

def initialize_session_state() -> None:
    """
    Initialize session state variables if they don't exist.
    
    This function sets up all session state variables needed by the application.
    It's safe to call multiple times as it only initializes variables
    that haven't been set already.
    
    Returns:
        None
    """
    # Input widget values/selections
    if 'context_paste' not in st.session_state:
        st.session_state.context_paste = ""
    if 'context_method' not in st.session_state:
        st.session_state.context_method = "File Upload"
    if 'prop_method' not in st.session_state:
        st.session_state.prop_method = "None"
    if 'prop_paste' not in st.session_state:
        st.session_state.prop_paste = ""
    if 'prop_paste_format' not in st.session_state:
        st.session_state.prop_paste_format = "JSON"


    # Loaded data and status flags/errors
    if 'device_context_data' not in st.session_state:
        st.session_state.device_context_data = None
    if 'context_error' not in st.session_state:
        st.session_state.context_error = None
    if 'context_loaded' not in st.session_state:  # Flag to control UI display
        st.session_state.context_loaded = False

    if 'property_set_data' not in st.session_state:
        st.session_state.property_set_data = None
    if 'prop_error' not in st.session_state:
        st.session_state.prop_error = None
    if 'prop_set_loaded' not in st.session_state:  # Flag to control UI display
        st.session_state.prop_set_loaded = False
    if 'raw_prop_content_for_display' not in st.session_state:
        st.session_state.raw_prop_content_for_display = None

    # API connection settings
    if 'api_ip_url' not in st.session_state:
        st.session_state.api_ip_url = ""
    if 'api_username' not in st.session_state:
        st.session_state.api_username = ""
    if 'api_token' not in st.session_state:
        st.session_state.api_token = ""
    if 'api_connected' not in st.session_state:
        st.session_state.api_connected = False

def get_state() -> Any:
    """
    Get the current Streamlit session state.
    
    This function provides a consistent way to access the session state
    across different UI components.
    
    Returns:
        The Streamlit session state object
    """
    return st.session_state