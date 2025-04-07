import streamlit as st
from app.utils.api.apstra_client import get_property_sets
from app.utils.ui.json_display_controls import render_json_controls

def render_apstra_property_loader(state):
    """
    Render the Apstra property set loader UI component.
    
    This function handles:
    - Property set selection from Apstra
    - Loading the selected property set
    - Displaying the property set in JSON format
    
    Args:
        state: Application state object
        
    Returns:
        None
    """
    # Check if API connection is established
    if not state.api_ip_url or not state.api_token:
        st.warning("Please connect to Apstra API first")
        return
    
    try:
        # Fetch property sets from Apstra
        with st.spinner("Fetching property sets from Apstra..."):
            property_sets_response = get_property_sets(state.api_ip_url, state.api_token)
        
        if not property_sets_response or "items" not in property_sets_response or not property_sets_response["items"]:
            st.warning("No property sets found in Apstra.")
            return
        
        # Prepare property set options
        property_data = []
        property_data.append({"label": "-- Select a Property Set --", "id": None})
        
        for prop_set in property_sets_response["items"]:
            if "id" in prop_set and "label" in prop_set:
                property_data.append({
                    "label": prop_set["label"],
                    "id": prop_set["id"],
                    "values": prop_set.get("values", {}),
                    "created_at": prop_set.get("created_at", "Unknown"),
                    "updated_at": prop_set.get("updated_at", "Unknown")
                })
        
        property_labels = [prop["label"] for prop in property_data]
        
        # Initialize selection in session state if needed
        if "property_preview_active" not in st.session_state:
            st.session_state["property_preview_active"] = False
            
        # Create property set dropdown
        prop_index = st.selectbox(
            "Select Property Set",
            options=range(len(property_labels)),
            format_func=lambda i: property_labels[i],
            key="property_set_selector",
            on_change=lambda: setattr(st.session_state, "property_preview_active", prop_index > 0)
        )
        
        # Only proceed if a property set is selected
        if prop_index > 0:
            selected_prop = property_data[prop_index]
            
            # Show property set info
            st.info(f"Selected property set: {selected_prop['label']}")
            st.caption(f"Created: {selected_prop['created_at']} | Last Updated: {selected_prop['updated_at']}")
            
            # Load button for property set - Only this button should update the application state
            if st.button("Load Property Set", key="load_property_set"):
                with st.spinner("Loading property set..."):
                    # Get the property set values
                    property_values = selected_prop["values"]
                    
                    if property_values:
                        # Store property set in state
                        state.property_set_data = property_values
                        state.prop_error = None
                        state.prop_set_loaded = True
                        
                        # Store information about the property set source
                        state.prop_source = {
                            "type": "apstra",
                            "property_id": selected_prop["id"],
                            "property_name": selected_prop["label"]
                        }
                        
                        # Rerun to display the property set
                        st.rerun()
                    else:
                        st.error("Selected property set has no values.")
    except Exception as e:
        st.error(f"Error: {str(e)}")