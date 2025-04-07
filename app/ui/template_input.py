"""
Template Input UI component for the Apstra Configlet Builder.

This module provides functionality for editing Jinja2 templates,
browsing existing configlets, and displaying a reference guide.
"""

import streamlit as st
from streamlit_ace import st_ace
from typing import Dict, Any, Optional
import re

from app.utils.config.session_state import get_state
from app.utils.api.apstra_client import get_configlets

def render_template_input() -> None:
    """
    Render the template input UI component.
    
    This function handles:
    - Jinja2 template editor with syntax highlighting
    - Configlet browser and editor integrated
    - Jinja2 reference guide
    
    Returns:
        None
    """
    st.subheader("Jinja2 Template")
    state = get_state()
    
    # Create tabs for different template features
    tab_names = ["Template Editor", "Jinja2 Reference"]
    tabs = st.tabs(tab_names)
    
    # Template Editor tab
    with tabs[0]:
        render_collapsible_editor(state)
    
    # Jinja2 Reference tab
    with tabs[1]:
        render_jinja2_reference()

def render_collapsible_editor(state):
    """
    Render a template editor with a collapsible configlet browser.
    
    Args:
        state: Application state object
    """
    # Initialize show_browser state if not exists
    if 'show_browser' not in st.session_state:
        st.session_state.show_browser = True
    
    # Toggle for the configlet browser
    if st.button("➡️ Show configlet browser" if not st.session_state.show_browser else "⬅️ Hide Configlet Browser", 
                help="Toggle configlet browser" if st.session_state.show_browser else "Show configlet browser"):
        st.session_state.show_browser = not st.session_state.show_browser
        st.rerun()
    
    # Conditional layout based on browser visibility
    if st.session_state.show_browser:
        # Two-column layout with browser and editor
        col1, col2 = st.columns([1, 1])
        
        with col1:
            render_configlet_browser(state)
        
        with col2:
            render_template_editor(state)
    else:
        # Full-width editor
        render_template_editor(state)

def render_configlet_browser(state):
    """
    Render the configlet browser component.
    
    Args:
        state: Application state object
    """
    # Configlet browser section
    st.write("##### Browse Configlets")
    
    # Check if API connection is established
    api_connected = hasattr(state, 'api_ip_url') and hasattr(state, 'api_token') and state.api_ip_url and state.api_token
    
    if not api_connected:
        st.warning("Connect to Apstra API to browse configlets")
    else:
        try:
            # Fetch configlets from Apstra
            with st.spinner("Fetching configlets from Apstra..."):
                configlets_response = get_configlets(state.api_ip_url, state.api_token)
            
            if not configlets_response or "items" not in configlets_response or not configlets_response["items"]:
                st.warning("No configlets found in Apstra.")
            else:
                # Create options for the dropdown
                configlet_options = ["-- Select a Configlet --"]
                configlet_data = [None]  # First item is None
                
                for configlet in configlets_response["items"]:
                    if "display_name" in configlet:
                        configlet_options.append(configlet["display_name"])
                        configlet_data.append(configlet)
                
                # Show the dropdown
                selected_index = st.selectbox(
                    "Select a configlet to preview",
                    options=range(len(configlet_options)),
                    format_func=lambda i: configlet_options[i]
                )
                
                # When a configlet is selected
                if selected_index > 0:
                    selected_configlet = configlet_data[selected_index]
                    
                    # Show configlet info
                    st.info(f"Selected configlet: {selected_configlet['display_name']}")
                    
                    # Display metadata
                    st.caption(f"Created: {selected_configlet.get('created_at', 'Unknown')}")
                    st.caption(f"Last Modified: {selected_configlet.get('last_modified_at', 'Unknown')}")
                    
                    # Check if the configlet has any generators
                    generators = selected_configlet.get("generators", [])
                    if not generators:
                        st.warning("This configlet does not contain any templates.")
                    else:
                        # Get the first generator/template
                        generator = generators[0]
                        
                        # Show template text for copying
                        if "template_text" in generator:
                            st.write("##### Template Code (copy to use):")
                            st.code(generator["template_text"], language="jinja2", height=500)
                        else:
                            st.warning("No template text available.")
                        
                        # Show negation template if available
                        if "negation_template_text" in generator and generator["negation_template_text"]:
                            st.write("##### Negation Template (copy to use):")
                            st.code(generator["negation_template_text"], language="jinja2")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def render_template_editor(state):
    """
    Render the template editor component.
    
    Args:
        state: Application state object
    """
    # Template editor section
    st.write("##### Configlet Template")
    
    # Get template content from state
    template_value = getattr(state, "template_input", "")
    
    # Render the ACE editor
    template_content = st_ace(
        value=template_value,
        language="django",
        theme="xcode",
        key="ace_editor",
        show_gutter=True,
        wrap=True,
        auto_update=True,
        height=700,
    )
    
    # Store the template content in the state
    state.template_input = template_content
    
    # # Add a button to analyze the template for missing values
    # if st.button("Analyze Template"):
    #     # Analyze the template and show suggested property set structure
    #     analyze_template(template_content, None)

def analyze_template(template_text, negation_text=None, state=None):
    """
    Analyze template to find variables and suggest missing ones for property set.
    
    Args:
        template_text: The main template text
        negation_text: Optional negation template text
        state: Application state containing device context and property set
    """
    if not template_text:
        st.warning("Template is empty. Nothing to analyze.")
        return
    
    # Find all variables in the template using regex
    # This regex looks for {{ variable }} pattern in Jinja2 templates
    var_pattern = r'{{\s*([^{}|]+?)(?:\s*\|\s*[^}]+)?\s*}}'
    main_vars = re.findall(var_pattern, template_text)
    
    # Also find variables in negation template if it exists
    negation_vars = []
    if negation_text:
        negation_vars = re.findall(var_pattern, negation_text)
    
    # Combine all unique variables
    all_vars = set(main_vars + negation_vars)
    
    # Clean up variable names (remove whitespace, quotes, etc.)
    clean_vars = set()
    for var in all_vars:
        # Remove whitespace and quotes
        clean_var = var.strip().strip('"\'')
        
        # Handle attribute access (dot notation) and array access (square brackets)
        parts = re.split(r'\.|\[|\]', clean_var)
        base_var = parts[0].strip()
        
        if base_var and not base_var.isdigit() and base_var != 'None' and base_var != 'True' and base_var != 'False':
            clean_vars.add(base_var)
    
    # Get existing variables from device context and property set
    existing_vars = set()
    
    # Check device context
    if state and hasattr(state, 'device_context_data') and state.device_context_data:
        if isinstance(state.device_context_data, dict):
            existing_vars.update(state.device_context_data.keys())
    
    # Check property set
    if state and hasattr(state, 'property_set_data') and state.property_set_data:
        if isinstance(state.property_set_data, dict):
            existing_vars.update(state.property_set_data.keys())
    
    # Find missing variables (in template but not in context or property set)
    missing_vars = clean_vars - existing_vars
    
    # Display analysis results
    if clean_vars:
        st.write("### Template Analysis")
        
        # Show all variables found in template
        st.write(f"**Variables found in template:** {len(clean_vars)}")
        st.code(", ".join(sorted(clean_vars)))
        
        # Show existing variables
        if existing_vars:
            st.write(f"**Variables available in context/property set:** {len(existing_vars)}")
            st.code(", ".join(sorted(existing_vars)))
        else:
            st.warning("No variables found in device context or property set.")
        
        # Show and suggest missing variables
        if missing_vars:
            st.write("### Suggested Property Set Additions")
            st.write(f"The following {len(missing_vars)} variables are referenced in your template but not found in device context or property set:")
            
            # Create a JSON-like structure for the missing variables
            property_additions = {}
            for var in sorted(missing_vars):
                property_additions[var] = "REPLACE_WITH_YOUR_VALUE"
            
            # Display the suggested property additions
            st.code(repr(property_additions), language="python")
            
            # Additional helper text
            st.info("You can add these variables to your property set. Replace the placeholder values with your actual data.")
        else:
            st.success("All template variables are already available in the device context or property set!")
    else:
        st.success("No variables found in the template.")

def render_jinja2_reference() -> None:
    """
    Render the Jinja2 quick reference guide with examples.
    
    Returns:
        None
    """
    # Create tabs for different Jinja2 concepts
    tab_vars, tab_loops, tab_ifs, tab_set, tab_filters, tab_comments, tab_whitespace = st.tabs([
        "Variables", "For Loops", "If/Elif/Else", "Set Variables", "Filters", "Comments", "Whitespace"
    ])
    
    with tab_vars:
        st.markdown("Access variables from the Device Context / Property Set:")
        st.code("{{ hostname }}")
        st.code("{{ interface['IF-et-0/0/1']['description'] }}")
        st.code("{{ ip['IP-et-0/0/1'].ipv4_address }}")  # Dot notation also works
    
    with tab_loops:
        st.markdown("Iterate over items (e.g., interfaces):")
        st.code("""
{% for if_name, if_data in interface.items() %}
Interface: {{ if_name }}
  Description: {{ if_data.description }}
  IP Address: {{ ip[if_data.ip_address_obj_name].ipv4_address | default('N/A') }}
{% endfor %}
        """, language="jinja2")
        st.markdown("*(Note: Assumes `ip_address_obj_name` exists in `if_data` linking to the IP object)*")
        
        st.markdown("Iterate over a list:")
        st.code("""
{% for slot in slots %}
Slot number: {{ slot }}
{% endfor %}
        """, language="jinja2")
    
    with tab_ifs:
        st.markdown("Conditional logic:")
        st.code("""
{% if role == 'leaf' %}
This is a leaf switch.
{% elif role == 'spine' %}
This is a spine switch.
{% else %}
Role is {{ role }}.
{% endif %}
        """, language="jinja2")
        
        st.markdown("Check if a variable exists:")
        st.code("""
{% if my_variable is defined %}
Value: {{ my_variable }}
{% else %}
my_variable is not defined.
{% endif %}
        """, language="jinja2")
    
    with tab_set:
        st.markdown("Define temporary variables within the template:")
        st.code("""
{% set my_var = "Some Value" %}
{% set loopback_ip = ip['lo0.0'].ipv4_address %}

Variable my_var: {{ my_var }}
Loopback: {{ loopback_ip }}
        """, language="jinja2")
    
    with tab_filters:
        st.markdown("Modify variables using filters:")
        st.code("{{ hostname | upper }}")
        st.code("{{ description | default('No description set') }}")
        st.code("{{ slots | length }}")
        st.code("{{ some_list | join(', ') }}")
        st.markdown("[Full list of built-in filters](https://jinja.palletsprojects.com/en/latest/templates/#list-of-builtin-filters)")
    
    with tab_comments:
        st.markdown("Add comments (not included in output):")
        st.code("{# This is a comment #}")
        st.code("""
{#
  This is a
  multi-line comment.
#}
        """, language="jinja2")
    
    with tab_whitespace:
        st.markdown("Control whitespace around blocks:")
        st.markdown("`-` removes whitespace before/after a block.")
        st.code("""
{%- for item in items -%}
  {{ item }}
{%- endfor -%}
        """, language="jinja2")
        st.markdown("Removes newlines before and after the loop.")