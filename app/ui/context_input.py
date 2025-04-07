import streamlit as st
import json
from typing import Dict, Any, Optional
import base64

from app.utils.config.session_state import get_state
from app.utils.config.example_data import EXAMPLE_DEVICE_CONTEXT
from app.utils.api.apstra_client import *
from app.utils.data.data_helpers import *
from app.utils.ui.json_display_controls import render_json_controls
from app.utils.ui.apstra_context_loader import render_apstra_context_loader



def render_context_input() -> None:
    """
    Render the context input UI component.
    
    This function handles:
    - Loading device context from file upload
    - Loading device context from pasted text
    - Loading example device context
    - Loading device context from Apstra API (to be implemented)
    - Displaying loaded context data with search functionality
    
    Returns:
        None
    """
    st.subheader("Device Context (JSON)")
    state = get_state()
    
    # Initialize state variables if they don't exist
    if 'context_loaded' not in state or not state.context_loaded:
        state.context_loaded = False
    
    if 'device_context_data' not in state:
        state.device_context_data = None
        
    if 'context_error' not in state:
        state.context_error = None
    
    # Display loaded context if available - placing this at the top ensures it's always shown when data is loaded
    if state.context_loaded and state.device_context_data:
        with st.expander("View Loaded Device Context", expanded=True):
            # Add search bar
            search_query = st.text_input("Search Device Context", key="context_search")
            
            # Filter JSON based on search query
            if search_query:
                filtered_context = filter_json(state.device_context_data, search_query)
            else:
                filtered_context = state.device_context_data
            
            # Create a separate container for JSON display and controls
            with st.container():
                # Add the JSON controls
                expansion_depth = render_json_controls(
                    filtered_context, 
                    prefix="context"
                )
                # Apply height constraint to the container
                st.markdown(f"""
                <style>
                    [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] > [data-testid="stVerticalBlock"] {{
                        max-height: 11px;
                        overflow-y: auto;
                    }}
                </style>
                """, unsafe_allow_html=True)
                # Add some space between controls and JSON
                st.markdown("<div style='margin-top: 1em;'></div>", unsafe_allow_html=True)
                
                # Display JSON with the selected expansion depth
                st.json(filtered_context, expanded=expansion_depth)
            
            # Create some space before the Clear button
            st.markdown("<div style='margin-top: 1em;'></div>", unsafe_allow_html=True)
            
            # Button to clear context - moved to its own container to avoid layout conflicts
            with st.container():
                if st.button("Clear/Change Context", key="clear_context", use_container_width=False):
                    state.device_context_data = None
                    state.context_error = None
                    state.context_loaded = False
                    # Clear any JSON control session state
                    for key in list(st.session_state.keys()):
                        if key.startswith("context_"):
                            st.session_state.pop(key, None)
                    st.rerun()
        
        # If context is loaded, we can return early and not show the input methods
        return
    
    # Context input method selection - only show if no context is loaded
    context_input_method = st.radio(
        "Select how you add your device context - _*Mandatory*_",
        ("Load From Apstra", "File Upload", "Paste Text", "Example Device Config"),
        key="context_method",
        horizontal=True,
    )
    
    # Function to process context data - centralizing the logic to avoid repetition
    def process_context_data(data, error_prefix="Error"):
        try:
            if isinstance(data, str):
                context_data = json.loads(data)
            else:
                context_data = data
                
            state.device_context_data = context_data
            state.context_error = None
            state.context_loaded = True
            st.rerun()  # Rerun to show the expander view
            return True
        except json.JSONDecodeError as e:
            state.context_error = f"{error_prefix} decoding JSON: {e}"
            state.context_loaded = False
        except Exception as e:
            state.context_error = f"{error_prefix}: {e}"
            state.context_loaded = False
        
        return False
    
    # Branch based on selected input method
    if context_input_method == "Load From Apstra":
        render_apstra_context_loader(state)
        
    elif context_input_method == "File Upload":
        uploaded_context_file = st.file_uploader(
            "Upload Device Context JSON File", type=["json"], key="context_upload"
        )
        
        if uploaded_context_file:
            try:
                # Read file content
                file_content = uploaded_context_file.getvalue().decode('utf-8')
                
                # Use the load_json_file helper function
                data, error = load_json_file(file_content)
                
                if error:
                    state.context_error = error
                    state.context_loaded = False
                else:
                    state.device_context_data = data
                    state.context_error = None
                    state.context_loaded = True
                    st.rerun()
            except UnicodeDecodeError:
                state.context_error = "File encoding issue: Could not decode the file as UTF-8"
                state.context_loaded = False
            except Exception as e:
                state.context_error = f"Error reading file: {str(e)}"
                state.context_loaded = False
                
    elif context_input_method == "Paste Text":
        context_text = st.text_area(
            "Paste Device Context JSON", 
            height=150, 
            key="context_paste",
            help="Paste your JSON device context data here"
        )
        
        col1, col2 = st.columns([1, 5])
        
        with col1:
            if st.button("Load JSON", key="load_paste"):
                if context_text:
                    success = process_context_data(context_text, "Error processing pasted Device Context")
                else:
                    state.context_error = "No JSON data provided"
                    
    elif context_input_method == "Example Device Config":
        if st.button("Load Example Data"):
            success = process_context_data(EXAMPLE_DEVICE_CONTEXT, "Error processing example JSON")
    
    # Display error if one occurred
    if state.context_error:
        st.error(state.context_error)