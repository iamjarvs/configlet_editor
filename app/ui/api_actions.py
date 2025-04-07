"""
API Actions UI component for the Apstra Configlet Builder.

This module provides functionality for making various API calls to the Apstra API
and displaying the results.
"""

import streamlit as st
from typing import Dict, Any, Optional

from app.utils.config.session_state import get_state
from app.utils.api.apstra_client import *

def render_api_actions() -> None:
    """
    Render the API actions UI component.
    
    This function handles:
    - API calls to get blueprints
    - API calls to get design configlets
    - Custom API calls to any endpoint
    - Displaying API call results
    
    Returns:
        None
    """
    st.subheader("Other API Calls")
    state = get_state()
    
    # Create an expandable section for API actions
    with st.expander("API Actions", expanded=False):
        # Create tabs for different API actions
        Get_Blueprints, Get_Design_Configlets, Any_Get_Request = st.tabs([
            "Get Blueprints", "Get Design Configlets", "Any GET Request"
        ])
        
        with Get_Blueprints:
            if not state.api_token:
                st.warning("Please log in to use API actions")
            elif st.button("Get Blueprints"):
                if not state.api_token:
                    st.error("Please log in first")
                else:
                    with st.spinner("Fetching blueprints..."):
                        try:
                            
                            # Get blueprints
                            response = get_all_blueprints(state.api_ip_url, state.api_token)
                            
                            if "error" in response:
                                st.error(f"Error fetching blueprints: {response['error']}")
                            else:
                                st.success("Blueprints fetched successfully!")
                                st.json(response)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        with Get_Design_Configlets:
            if not state.api_token:
                st.warning("Please log in to use API actions")
            elif st.button("Get Design Configlets"):
                    if not state.api_token:
                        st.error("Please log in first")
                    else:
                        with st.spinner("Fetching configlets..."):
                            try:                            
                                # Get design configlets
                                response = get_design_configlets(state.api_ip_url, state.api_token)
                                
                                if "error" in response:
                                    st.error(f"Error fetching configlets: {response['error']}")
                                else:
                                    st.success("Configlets fetched successfully!")
                                    st.json(response)
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
        
        with Any_Get_Request:
            if not state.api_token:
                st.warning("Please log in to use API actions")
            else:
                # Custom API call section
                st.subheader("Custom API Call")
                api_endpoint = st.text_input("API Endpoint", placeholder="e.g., api/blueprints")
                
                if st.button("Execute API Call"):
                    if not api_endpoint:
                        st.error("Please enter an API endpoint")
                    else:
                        with st.spinner(f"Executing GET request to {api_endpoint}..."):
                            try:
                                # Create client instance and set token

                                # Execute custom API call
                                response = get_any_endpoint(state.api_ip_url, state.api_token, api_endpoint)
                                
                                if "error" in response:
                                    st.error(f"API call failed: {response['error']}")
                                else:
                                    st.success("API call successful!")
                                    st.json(response)
                            except Exception as e:
                                st.error(f"Error: {str(e)}")