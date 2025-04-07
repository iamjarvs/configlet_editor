from ..api.apstra_client import get_all_blueprints
import streamlit as st
import json

def render_blueprint_dropdown(state):
    """
    Renders a dropdown list of blueprints fetched from the API.
    
    Args:
        state: The application state containing API connection details
        
    Returns:
        tuple: (selected_blueprint_label, selected_blueprint_id) or (None, None) if no selection
    """
    # Initialize return values
    selected_blueprint_label = None
    selected_blueprint_id = None
    
    # Only attempt to fetch blueprints if we have API connection details
    if state.api_ip_url and state.api_token:
        try:
            # Get all blueprints from the API
            blueprints_response = get_all_blueprints(state.api_ip_url, state.api_token)
            
            if blueprints_response and "items" in blueprints_response:
                # Store blueprint data (both label and id)
                blueprint_data = []
                
                # Add a "None" option at the beginning
                blueprint_data.append({"label": "-- Select a Blueprint --", "id": None})
                
                # Extract data from each blueprint
                for blueprint in blueprints_response["items"]:
                    if "label" in blueprint and "id" in blueprint:
                        blueprint_data.append({
                            "label": blueprint["label"],
                            "id": blueprint["id"]
                        })
                
                # Extract just the labels for display in the dropdown
                blueprint_labels = [bp["label"] for bp in blueprint_data]
                
                # Create the dropdown
                selected_index = st.selectbox(
                    "Select Blueprint",
                    options=range(len(blueprint_labels)),
                    format_func=lambda i: blueprint_labels[i],
                    key="blueprint_selector"
                )
                
                # Get the selected blueprint data
                if selected_index > 0:  # Skip the "None" option
                    selected_blueprint_label = blueprint_data[selected_index]["label"]
                    selected_blueprint_id = blueprint_data[selected_index]["id"]
                    
                    # Optional: Display information about the selected blueprint
                    st.info(f"Selected blueprint: {selected_blueprint_label} (ID: {selected_blueprint_id})")
                    
            else:
                st.warning("No blueprints found or invalid response format")
                
        except Exception as e:
            st.error(f"Error fetching blueprints: {str(e)}")
    else:
        st.warning("Please connect to the API first")
        
    # Return both the label and ID
    return selected_blueprint_label, selected_blueprint_id