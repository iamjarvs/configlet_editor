# Updated app/utils/ui/json_display_controls.py without download button

import streamlit as st
import json

def render_json_controls(data, prefix=""):
    """
    Render controls for JSON display with expand/collapse options.
    
    Args:
        data: The JSON data to be controlled
        prefix: A prefix for the key to avoid conflicts between multiple JSON viewers
        
    Returns:
        int: The expansion depth selected by the user
    """
    # Calculate max reasonable depth based on data structure
    max_depth = calculate_max_depth(data)
    
    # Use a container for the controls to keep them together
    with st.container():
        # Create a more compact button layout - 3 columns without download
        cols = st.columns([1, 1, 2])
        
        # Define the default depth value safely
        if f"{prefix}_expansion_depth" not in st.session_state:
            st.session_state[f"{prefix}_expansion_depth"] = 1
        
        # Get expansion depth (ensure it's within bounds)
        current_depth = min(st.session_state[f"{prefix}_expansion_depth"], max_depth)
        
        # Collapse button
        with cols[0]:
            if st.button("Collapse", key=f"{prefix}_collapse", use_container_width=True):
                st.session_state[f"{prefix}_expansion_depth"] = 0
                st.rerun()  # Ensure state change is immediately reflected
        
        # Expand button
        with cols[1]:
            if st.button("Expand", key=f"{prefix}_expand", use_container_width=True):
                st.session_state[f"{prefix}_expansion_depth"] = max_depth
                st.rerun()  # Ensure state change is immediately reflected
                
        # Depth selector
        with cols[2]:
            depth_value = st.slider(
                "Depth",
                min_value=0,
                max_value=max_depth,
                value=current_depth,
                key=f"{prefix}_depth_slider"
            )
            # Update session state when slider changes
            if depth_value != st.session_state.get(f"{prefix}_expansion_depth"):
                st.session_state[f"{prefix}_expansion_depth"] = depth_value
    
    # Return the current expansion depth
    return st.session_state[f"{prefix}_expansion_depth"]

def calculate_max_depth(data, expand_all=False):
    """
    Calculate the maximum depth for JSON expansion.
    
    Args:
        data: The JSON data to analyze
        expand_all: If True, returns a very large value to ensure full expansion
        
    Returns:
        int: The appropriate depth value
    """
    # For "Expand All" functionality, return a very large number
    if expand_all:
        return 99  # This will expand everything, including empty arrays
        
    # Normal depth calculation for other cases
    def _depth(obj, level=0):
        """Inner recursive function to calculate depth"""
        if not isinstance(obj, (dict, list)) or not obj:
            return level
            
        if isinstance(obj, dict):
            child_depths = [_depth(value, level + 1) for value in obj.values() 
                           if isinstance(value, (dict, list))]
            return max(child_depths) if child_depths else level + 1
            
        elif isinstance(obj, list):
            child_depths = [_depth(item, level + 1) for item in obj 
                           if isinstance(item, (dict, list))]
            return max(child_depths) if child_depths else level + 1
    
    # Calculate a reasonable depth for normal display
    reasonable_depth = _depth(data)
    
    # Add 1 to ensure we get full expansion of the deepest level
    # Cap at 10 to prevent performance issues with extremely deep structures
    return min(reasonable_depth + 1, 10)