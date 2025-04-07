import streamlit as st
from app.utils.api.apstra_client import get_all_blueprints, get_blueprint_nodes, get_device_context

def render_apstra_context_loader(state):
    """
    Render the Apstra device context loader UI component.
    
    This function handles:
    - Blueprint selection
    - Device selection from the blueprint
    - Loading device context from Apstra API
    
    Args:
        state: Application state object
        
    Returns:
        None
    """

    # Check if API connection is established
    if not state.api_ip_url or not state.api_token:
        st.warning("Please connect to Apstra API first")
        return
    if state.selected_blueprint_id:
        nodes_response = get_blueprint_nodes(state.api_ip_url, state.api_token, state.selected_blueprint_id)
    
        if not nodes_response or "items" not in nodes_response or not nodes_response["items"]:
            st.warning("No devices found in the selected blueprint.")
            return
        
        # Prepare node options
        node_data = []
        node_data.append({"label": "-- Select a Device --", "id": None})
        
        for node_item in nodes_response["items"]:
            if "switch_nodes" in node_item:
                node = node_item["switch_nodes"]
                if "id" in node and "label" in node:
                    node_data.append({
                        "label": f"{node['label']} ({node.get('hostname', 'Unknown')})",
                        "id": node["id"],
                        "role": node.get("role", "unknown"),
                        "system_id": node.get("system_id", "unknown")
                    })
        
        node_labels = [node["label"] for node in node_data]
        
        # Create node dropdown
        node_index = st.selectbox(
            "Select Device",
            options=range(len(node_labels)),
            format_func=lambda i: node_labels[i],
            key="context_node_selector"
        )
        
        # Only proceed if a node is selected
        if node_index > 0:
            selected_node = node_data[node_index]
            node_id = selected_node["id"]
            
            # Show device info
            st.info(f"Selected device: {selected_node['label']} (Role: {selected_node['role']}, System ID: {selected_node['system_id']})")
            
            # Step 3: Load button for device context
            if st.button("Load Device Context", key="load_device_context"):
                with st.spinner("Loading device context from Apstra..."):
                    # Fetch device context
                    device_context = get_device_context(state.api_ip_url, state.api_token, state.selected_blueprint_id
                    , node_id)
                    
                    if device_context:
                        # Store device context in state
                        state.device_context_data = device_context
                        state.context_error = None
                        state.context_loaded = True
                        
                        # Store information about the context source
                        state.context_source = {
                            "type": "apstra",
                            "blueprint_id": state.selected_blueprint_id,
                            "blueprint_name": state.selected_blueprint,
                            "node_id": node_id,
                            "node_name": selected_node["label"]
                        }
                        
                        # Rerun to display the context
                        st.rerun()
                    else:
                        st.error("Failed to load device context. Please try again.")
    