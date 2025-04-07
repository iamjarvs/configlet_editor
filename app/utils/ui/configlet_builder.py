import streamlit as st
from app.utils.api.apstra_client import get_configlets

def render_configlet_builder(state):
    """
    Render the configlet builder UI component.
    
    This function handles:
    - Building configlets from scratch
    - Viewing existing configlets from Apstra
    
    Args:
        state: Application state object
        
    Returns:
        None
    """
    st.subheader("Jinja2 Template Configlets")
    
    # Tabs for different modes
    builder_tab, browser_tab = st.tabs(["Build New Configlet", "Browse Existing Configlets"])
    
    # Build New Configlet tab
    with builder_tab:
        render_configlet_editor(state)
    
    # Browse Existing Configlets tab
    with browser_tab:
        render_apstra_configlet_loader(state)

def render_configlet_editor(state):
    """
    Render the configlet builder/editor interface.
    
    Args:
        state: Application state object
        
    Returns:
        None
    """
    # Initialize editor state if needed
    if 'configlet_editor_state' not in st.session_state:
        st.session_state.configlet_editor_state = {
            'display_name': '',
            'config_style': 'junos',
            'section': 'system',
            'template_text': '',
            'negation_template_text': '',
            'filename': ''
        }
    
    # Display name input
    st.text_input("Configlet Name", 
                 key="configlet_name",
                 value=st.session_state.configlet_editor_state['display_name'],
                 on_change=lambda: setattr(st.session_state.configlet_editor_state, 'display_name', st.session_state.configlet_name))
    
    # Metadata columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.selectbox("Config Style", 
                    options=["junos", "nxos", "sonic", "eos", "custom"],
                    key="configlet_style",
                    index=["junos", "nxos", "sonic", "eos", "custom"].index(st.session_state.configlet_editor_state['config_style']),
                    on_change=lambda: setattr(st.session_state.configlet_editor_state, 'config_style', st.session_state.configlet_style))
    
    with col2:
        st.selectbox("Section", 
                    options=["system", "system_top", "set_based_system", "file", "custom"],
                    key="configlet_section",
                    index=["system", "system_top", "set_based_system", "file", "custom"].index(st.session_state.configlet_editor_state['section']),
                    on_change=lambda: setattr(st.session_state.configlet_editor_state, 'section', st.session_state.configlet_section))
    
    with col3:
        st.text_input("Filename (optional)", 
                     key="configlet_filename",
                     value=st.session_state.configlet_editor_state['filename'],
                     on_change=lambda: setattr(st.session_state.configlet_editor_state, 'filename', st.session_state.configlet_filename))
    
    # Template text editor
    st.write("##### Template Code")
    template_text = st.text_area("Template Code", 
                                value=st.session_state.configlet_editor_state['template_text'],
                                height=300,
                                key="template_code",
                                on_change=lambda: setattr(st.session_state.configlet_editor_state, 'template_text', st.session_state.template_code))
    
    # Toggle for negation template
    include_negation = st.checkbox("Include Negation Template", 
                                  value=bool(st.session_state.configlet_editor_state['negation_template_text']),
                                  key="include_negation")
    
    # Negation template text editor (if enabled)
    if include_negation:
        st.write("##### Negation Template Code")
        negation_text = st.text_area("Negation Template Code", 
                                    value=st.session_state.configlet_editor_state['negation_template_text'],
                                    height=200,
                                    key="negation_code",
                                    on_change=lambda: setattr(st.session_state.configlet_editor_state, 'negation_template_text', st.session_state.negation_code))
    elif not include_negation and st.session_state.configlet_editor_state['negation_template_text']:
        # Clear negation text if checkbox is unchecked
        st.session_state.configlet_editor_state['negation_template_text'] = ''
    
    # Preview button
    if st.button("Preview Template"):
        st.write("##### Template Preview")
        with st.expander("Template Code", expanded=True):
            st.code(template_text, language="jinja2")
        
        if include_negation and st.session_state.configlet_editor_state['negation_template_text']:
            st.write("##### Negation Template Preview")
            with st.expander("Negation Template Code", expanded=True):
                st.code(st.session_state.configlet_editor_state['negation_template_text'], language="jinja2")
    
    # Save/Clear buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Configlet", type="primary"):
            # Placeholder for save functionality
            st.success("Configlet saved successfully (placeholder - actual save functionality would be implemented here)")
    
    with col2:
        if st.button("Clear"):
            # Reset the editor state
            st.session_state.configlet_editor_state = {
                'display_name': '',
                'config_style': 'junos',
                'section': 'system',
                'template_text': '',
                'negation_template_text': '',
                'filename': ''
            }
            st.rerun()

def render_apstra_configlet_loader(state):
    """
    Render the Apstra configlet loader UI component.
    
    This function handles:
    - Configlet selection from Apstra
    - Displaying the selected configlet's template text
    - Supporting multiple templates per configlet
    
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
        # Fetch configlets from Apstra
        with st.spinner("Fetching configlets from Apstra..."):
            configlets_response = get_configlets(state.api_ip_url, state.api_token)
        
        if not configlets_response or "items" not in configlets_response or not configlets_response["items"]:
            st.warning("No configlets found in Apstra.")
            return
        
        # Prepare configlet options
        configlet_data = []
        configlet_data.append({"label": "-- Select a Configlet --", "id": None})
        
        for configlet in configlets_response["items"]:
            if "id" in configlet and "display_name" in configlet:
                configlet_data.append({
                    "label": configlet["display_name"],
                    "id": configlet["id"],
                    "generators": configlet.get("generators", []),
                    "created_at": configlet.get("created_at", "Unknown"),
                    "last_modified_at": configlet.get("last_modified_at", "Unknown"),
                    "ref_archs": configlet.get("ref_archs", [])
                })
        
        configlet_labels = [item["label"] for item in configlet_data]
        
        # Create configlet dropdown with search
        st.write("### Select Configlet")
        
        # Add search filter
        search_query = st.text_input("Search Configlets", key="configlet_search")
        
        # Filter configlets based on search query
        filtered_configlet_data = configlet_data
        filtered_configlet_labels = configlet_labels
        
        if search_query:
            filtered_configlet_data = [configlet for configlet in configlet_data if 
                                      search_query.lower() in configlet["label"].lower() or 
                                      (configlet["id"] and search_query.lower() in configlet["id"].lower())]
            filtered_configlet_labels = [item["label"] for item in filtered_configlet_data]
            
            # Show count of filtered results
            st.caption(f"Found {len(filtered_configlet_data)-1} configlets matching '{search_query}'")
        
        # Show dropdown with filtered results
        if len(filtered_configlet_data) > 0:
            configlet_index = st.selectbox(
                "Available Configlets",
                options=range(len(filtered_configlet_labels)),
                format_func=lambda i: filtered_configlet_labels[i],
                key="configlet_selector"
            )
            
            # Only proceed if a configlet is selected
            if configlet_index > 0:
                selected_configlet = filtered_configlet_data[configlet_index]
                
                # Show configlet info
                st.info(f"Selected configlet: {selected_configlet['label']}")
                
                # Display metadata
                meta_col1, meta_col2 = st.columns(2)
                with meta_col1:
                    st.caption(f"Created: {selected_configlet['created_at']}")
                    st.caption(f"ID: {selected_configlet['id']}")
                with meta_col2:
                    st.caption(f"Last Modified: {selected_configlet['last_modified_at']}")
                    if selected_configlet['ref_archs']:
                        st.caption(f"Reference Architectures: {', '.join(selected_configlet['ref_archs'])}")
                
                # Check if there are any templates in the configlet
                if not selected_configlet["generators"]:
                    st.warning("This configlet does not contain any templates.")
                    return
                
                # Create tabs for multiple templates
                if len(selected_configlet["generators"]) > 1:
                    # Create a tab for each template
                    tab_labels = []
                    for i, generator in enumerate(selected_configlet["generators"]):
                        tab_name = f"Template {i+1}"
                        # Add config style if available for better context
                        if "config_style" in generator:
                            tab_name += f" ({generator['config_style']})"
                        tab_labels.append(tab_name)
                    
                    tabs = st.tabs(tab_labels)
                    
                    for i, (generator, tab) in enumerate(zip(selected_configlet["generators"], tabs)):
                        with tab:
                            render_template(generator, i)
                else:
                    # Just one template, show it directly
                    render_template(selected_configlet["generators"][0], 0)
                
                # Copy to editor button
                if st.button("Copy to Editor"):
                    # Get the first template for simplicity
                    generator = selected_configlet["generators"][0]
                    # Update the editor state with this template
                    st.session_state.configlet_editor_state = {
                        'display_name': selected_configlet['label'] + " (Copy)",
                        'config_style': generator.get('config_style', 'junos'),
                        'section': generator.get('section', 'system'),
                        'template_text': generator.get('template_text', ''),
                        'negation_template_text': generator.get('negation_template_text', ''),
                        'filename': generator.get('filename', '')
                    }
                    # Switch to the editor tab
                    st.rerun()
        else:
            st.warning("No configlets found matching your search criteria.")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

def render_template(generator, index):
    """
    Render a single template within a configlet.
    
    Args:
        generator: The generator containing template text
        index: The index of this template
    """
    if "template_text" not in generator:
        st.warning("This template does not contain any template text.")
        return
    
    # Container for template metadata
    with st.container():
        # Display template metadata in columns
        metadata_col1, metadata_col2, metadata_col3 = st.columns(3)
        
        with metadata_col1:
            if "config_style" in generator:
                st.caption(f"**Config Style:** {generator['config_style']}")
        
        with metadata_col2:
            if "section" in generator:
                st.caption(f"**Section:** {generator['section']}")
        
        with metadata_col3:
            if "filename" in generator and generator["filename"]:
                st.caption(f"**Filename:** {generator['filename']}")
    
    # Create a container for the template code
    with st.container():
        st.write("##### Template Code")
        
        # Create expandable code viewer
        with st.expander("View Template Code", expanded=True):
            # Display the template code with syntax highlighting
            st.code(generator["template_text"], language="jinja2")
    
    # If there's a negation template, show it too
    if "negation_template_text" in generator and generator["negation_template_text"]:
        with st.container():
            st.write("##### Negation Template Code")
            
            # Create expandable code viewer for negation template
            with st.expander("View Negation Template Code", expanded=False):
                # Display the negation template code with syntax highlighting
                st.code(generator["negation_template_text"], language="jinja2")