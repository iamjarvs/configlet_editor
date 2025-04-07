"""
Property Input UI component for the Apstra Configlet Builder.

This module provides functionality for loading property set data
from various sources (file upload, paste, example data).
"""

import streamlit as st
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union
import base64

from app.utils.config.session_state import get_state
from app.utils.config.example_data import EXAMPLE_PROPERTY_SET
from app.utils.api.apstra_client import *
from app.utils.data.data_helpers import *
from app.utils.ui.json_display_controls import render_json_controls
from app.utils.data.data_helpers import load_json_file, load_yaml_content


# Update your property_input.py file to integrate the Apstra property loader

def render_property_input() -> None:
    """
    Render the property input UI component.
    
    This function handles:
    - Loading property set from Apstra API
    - Loading property set from file upload (JSON or YAML)
    - Loading property set from pasted text (JSON or YAML)
    - Loading example property set
    - Displaying loaded property set data
    
    Returns:
        None
    """
    st.subheader("Property Set (Optional)")
    state = get_state()
    
    # Initialize state variables if they don't exist
    if 'prop_set_loaded' not in state:
        state.prop_set_loaded = False
        
    if 'property_set_data' not in state:
        state.property_set_data = None
        
    if 'prop_error' not in state:
        state.prop_error = None
        
    if 'raw_prop_content_for_display' not in state:
        state.raw_prop_content_for_display = None
    
    # Display loaded property set if available
    if state.prop_set_loaded and state.property_set_data is not None:
        with st.expander("View Loaded Property Set", expanded=True):
            # Display property set source if available
            if hasattr(state, 'prop_source') and state.prop_source:
                if state.prop_source.get('type') == 'apstra':
                    st.caption(f"Source: Apstra Property Set '{state.prop_source.get('property_name')}'")
                elif state.prop_source.get('type') == 'file':
                    st.caption(f"Source: File '{state.prop_source.get('filename')}'")
                elif state.prop_source.get('type') == 'paste':
                    st.caption("Source: Pasted Text")
                elif state.prop_source.get('type') == 'example':
                    st.caption("Source: Example Property Set")
            
            # Determine display format
            display_format = "JSON"  # Default to JSON
            
            # If we're in fullscreen mode, don't show any other UI
            if st.session_state.get("property_fullscreen_active", False):
                # The fullscreen UI is handled entirely within render_json_controls
                expansion_depth = render_json_controls(
                    state.property_set_data, 
                    prefix="property"
                )
            else:
                # Regular non-fullscreen view
                if display_format == "JSON":
                    # Add search functionality
                    search_col1, search_col2 = st.columns([4, 1])
                    
                    with search_col1:
                        search_query = st.text_input("Search Property Set", key="property_search")
                    
                    with search_col2:
                        exact_match = st.checkbox("Exact Match", key="property_exact_match", 
                                                 help="Toggle between exact matching and partial matching")
                    
                    # Filter JSON based on search query
                    if search_query:
                        filtered_property = filter_json(state.property_set_data, search_query, exact_match)
                    else:
                        filtered_property = state.property_set_data
                    
                    # Create a separate container for JSON display
                    with st.container():
                        # Add the JSON controls
                        expansion_depth = render_json_controls(
                            filtered_property, 
                            prefix="property"
                        )
                        
                        # Add some space between controls and JSON
                        st.markdown("<div style='margin-top: 1em;'></div>", unsafe_allow_html=True)
                        
                        # Display JSON with the selected expansion depth
                        st.json(filtered_property, expanded=expansion_depth)
                else:  # YAML
                    # Display YAML
                    st.code(state.raw_prop_content_for_display, language='yaml')
            
            # Create some space before the Clear button
            st.markdown("<div style='margin-top: 1em;'></div>", unsafe_allow_html=True)
            
            # Button to clear property set - moved to its own container to avoid layout conflicts
            with st.container():
                if st.button("Clear/Change Property Set", key="clear_prop", use_container_width=False):
                    state.property_set_data = None
                    state.prop_error = None
                    state.prop_set_loaded = False
                    # Clear property source information
                    if hasattr(state, 'prop_source'):
                        state.prop_source = None
                    st.session_state.pop('prop_paste', None)  # Clear pasted text in session state
                    # Clear any JSON control session state
                    for key in list(st.session_state.keys()):
                        if key.startswith("property_"):
                            st.session_state.pop(key, None)
                    state.raw_prop_content_for_display = None
                    st.rerun()
                
        # If property set is loaded, return early (don't show input methods)
        return
    
    # Property input method selection
    prop_input_method = st.radio(
        "Select how you add your property set - _*Optional*_",
        ("None", "Load From Apstra", "File Upload", "Paste Text", "Example Property Set"),
        key="prop_method",
        horizontal=True,
    )
    
    # Handle "None" selection immediately
    if prop_input_method == "None":
        state.property_set_data = None
        state.prop_error = None
        state.prop_set_loaded = False
        state.raw_prop_content_for_display = None
        st.info("No Property Set provided.")
        
        if st.button("Add/Change Property Set", key="add_prop"):
            # Simply rerun - the radio selection will still be "None" but user can change it
            st.rerun()
    
    # Branch based on selected input method (other than "None")
    elif prop_input_method == "Load From Apstra":
        # Import and use the Apstra property loader
        from app.utils.ui.apstra_property_loader import render_apstra_property_loader
        render_apstra_property_loader(state)
    
    elif prop_input_method == "File Upload":
        uploaded_prop_file = st.file_uploader(
            "Upload Property Set File", type=["json", "yaml", "yml"], key="prop_upload"
        )
        
        if uploaded_prop_file:
            try:
                # Read file content
                file_content = uploaded_prop_file.getvalue().decode('utf-8')
                file_type = uploaded_prop_file.name.split('.')[-1].lower()
                
                # Process based on file type
                if file_type in ['json']:
                    # Use the load_json_file helper function
                    data, error = load_json_file(file_content)
                    raw_content = None  # JSON doesn't need raw content preservation
                elif file_type in ['yaml', 'yml']:
                    # Use the load_yaml_content helper function
                    data, error = load_yaml_content(file_content)
                    raw_content = file_content if not error else None  # Preserve raw YAML for display
                else:
                    data = None
                    error = f"Unsupported file type: {file_type}"
                    raw_content = None
                
                # Update state based on results
                if error:
                    state.prop_error = error
                    state.prop_set_loaded = False
                else:
                    state.property_set_data = data
                    state.prop_error = None
                    state.prop_set_loaded = True
                    state.raw_prop_content_for_display = raw_content
                    # Set property source
                    state.prop_source = {
                        "type": "file",
                        "filename": uploaded_prop_file.name
                    }
                    st.rerun()
                    
            except UnicodeDecodeError:
                state.prop_error = "File encoding issue: Could not decode the file as UTF-8"
                state.prop_set_loaded = False
            except Exception as e:
                state.prop_error = f"Error reading file: {str(e)}"
                state.prop_set_loaded = False
    
    elif prop_input_method == "Paste Text":
        pasted_prop_format = st.radio(
            "Pasted Format",
            ("JSON", "YAML"),
            key="prop_paste_format",
            horizontal=True
        )
        
        prop_text = st.text_area(
            "Paste Property Set JSON or YAML", 
            height=150, 
            key="prop_paste",
            help="Paste your property set data here"
        )
        
        col1, col2 = st.columns([1, 5])
        
        with col1:
            if st.button("Load Data", key="load_prop_paste"):
                if prop_text:
                    try:
                        if pasted_prop_format == "JSON":
                            # Use the load_json_file helper function
                            data, error = load_json_file(prop_text)
                            raw_content = None
                        else:  # YAML
                            # Use the load_yaml_content helper function
                            data, error = load_yaml_content(prop_text)
                            raw_content = prop_text if not error else None
                        
                        # Update state based on results
                        if error:
                            state.prop_error = error
                            state.prop_set_loaded = False
                        else:
                            state.property_set_data = data
                            state.prop_error = None
                            state.prop_set_loaded = True
                            state.raw_prop_content_for_display = raw_content
                            # Set property source
                            state.prop_source = {
                                "type": "paste"
                            }
                            st.rerun()
                            
                    except Exception as e:
                        state.prop_error = f"Error processing pasted data: {str(e)}"
                        state.prop_set_loaded = False
                else:
                    state.prop_error = "No data provided"
                    state.prop_set_loaded = False
    
    elif prop_input_method == "Example Property Set":
        if st.button("Load Example Data"):
            try:
                # Use the load_json_file helper function
                data, error = load_json_file(EXAMPLE_PROPERTY_SET)
                
                if error:
                    state.prop_error = error
                    state.prop_set_loaded = False
                else:
                    state.property_set_data = data
                    state.raw_prop_content_for_display = None
                    state.prop_error = None
                    state.prop_set_loaded = True
                    # Set property source
                    state.prop_source = {
                        "type": "example"
                    }
                    st.rerun()
            except Exception as e:
                state.prop_error = f"Error loading example data: {str(e)}"
                state.prop_set_loaded = False
    
    # Display error if one occurred
    if state.prop_error:
        st.error(state.prop_error)