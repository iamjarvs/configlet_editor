"""
Render Output UI component for the Apstra Configlet Builder.

This module provides functionality for rendering Jinja2 templates
with context data and displaying the output.
"""

import streamlit as st
import jinja2
import pyperclip
from typing import Dict, Any, Optional, Tuple

from app.utils.config.session_state import get_state
from app.utils.data.template_engine import render_template, deep_merge

def render_output() -> None:
    """
    Render the output UI component.
    
    This function handles:
    - Template rendering using device context and property set
    - Displaying rendered output
    - Error handling for rendering issues
    - Download and copy functionality for output
    
    Returns:
        None
    """
    st.subheader("Rendered Output")
    state = get_state()
    
    # Get data from session state
    device_context_data = getattr(state, 'device_context_data', None)
    property_set_data = getattr(state, 'property_set_data', None)
    context_loaded = getattr(state, 'context_loaded', False)
    template_string = getattr(state, 'template_input', "")
    
    # Initialize render variables
    rendered_output = ""
    render_error = None
    
    # Check prerequisites
    if not context_loaded:
        render_error = "Device Context not loaded."
    elif getattr(state, 'context_error', None):
        render_error = f"Cannot render: {state.context_error}"
    elif not isinstance(device_context_data, dict):
        render_error = "Cannot render: Loaded Device Context is not a valid JSON object (dictionary)."
    elif not template_string:
        render_error = "Please provide a Jinja2 template."
    # Property set check - only error if user *tried* to load one and failed
    elif getattr(state, 'prop_set_loaded', False) and getattr(state, 'prop_error', None):
        render_error = f"Cannot merge: {state.prop_error}"
    elif getattr(state, 'prop_set_loaded', False) and property_set_data is not None and not isinstance(property_set_data, dict):
        render_error = "Cannot merge: Loaded Property Set is not a valid JSON/YAML object (dictionary)."
    
    # If prerequisites are met, proceed with render
    if not render_error:
        try:
            # Call template engine to handle rendering
            rendered_output, error = render_template(
                template_string=template_string,
                device_context=device_context_data,
                property_set=property_set_data
            )
            
            if error:
                render_error = error
        except Exception as e:
            render_error = f"An unexpected error occurred: {e}"
    
    # Display error if any
    if render_error:
        st.error(f"Processing Error: {render_error}")
    
    # Display rendered output if available
    if rendered_output:
        with st.expander("Rendered Output", expanded=True):
            st.code(rendered_output, language="text", line_numbers=True)
            
            # Copy to clipboard button
            if st.button("Copy to Clipboard"):
                try:
                    pyperclip.copy(rendered_output)
                    st.success("Copied to clipboard!")
                except ImportError:
                    st.warning("`pyperclip` not installed. Please install it to use the copy button.")
                except Exception as e:
                    st.error(f"Copy failed: {e}")
    elif not render_error and context_loaded and template_string:
        st.info("Template rendered successfully, but the output is empty.")
    elif not render_error:
        st.info("Output will appear here once valid context and template are provided.")
    
    # Download buttons
    st.divider()
    st.subheader("Download")
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            label="Download Template",
            data=template_string,
            file_name="template.j2",
            mime="text/plain",
            disabled=not template_string
        )
    
    with col_dl2:
        st.download_button(
            label="Download Rendered Output",
            data=rendered_output,
            file_name="rendered_config.txt",
            mime="text/plain",
            disabled=not rendered_output or render_error is not None
        )