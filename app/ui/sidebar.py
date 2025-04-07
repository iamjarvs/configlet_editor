"""
Sidebar UI component for the Apstra Configlet Builder.

This module provides the sidebar functionality for the application,
including login controls, token information, and token management.
"""

import streamlit as st
import jwt
import datetime
import pyperclip
from typing import Dict, Any, Optional
# get_login, get_design_configlets, get_all_blueprints, get_blueprint_nodes, 
#     get_device_context, 
#     get_connection_test, 
#     get_any_endpoint
from app.utils.api.apstra_client import *
from app.utils.config.session_state import initialize_session_state, get_state
from ..utils.ui.blueprint_dropdown import *



def render_sidebar() -> None:
    """
    Render the sidebar UI component.
    
    This function handles:
    - Apstra server connection settings
    - Login credentials
    - Connection testing
    - API token information display
    - Token management options
    
    Returns:
        None
    """

    # Initialize session state if not already done
    initialize_session_state()
    state = get_state()

    st.sidebar.title("Apstra Configlet Builder")
    st.sidebar.subheader("Login")
    ip_url = st.sidebar.text_input("IP/URL", value=state.api_ip_url, key="ip_url_input")
    username = st.sidebar.text_input("Username", value=state.api_username , key="username_input")
    password = st.sidebar.text_input("Password", type="password", key="password_input")

    # Update session state when input changes
    state.api_ip_url = ip_url
    state.api_username = username

    login_cols = st.columns(2)
    with login_cols[0]:
        if st.sidebar.button("Login"):
            if not ip_url:
                st.sidebar.error("Please enter an IP/URL")
            elif not username or not password:
                st.sidebar.error("Please enter username and password")
            else:
                with st.spinner(f"Logging in with: {state.api_username}@{state.api_ip_url}"):
                    # Use the specialized login function
                    login_response = get_login(ip_url, username, password)
                    
                    if "error" in login_response:
                        st.sidebar.error(f"Login failed: {login_response['error']}")
                    elif "token" in login_response:
                        # Save the token to session state
                        state.api_token = login_response["token"]
                        state.api_connected = True
                        st.sidebar.success("Login successful!")

    with login_cols[1]:
        if st.sidebar.button("Test Connection"):
            if state.api_ip_url and state.api_token:
                with st.spinner("Testing connection..."):
                    # Use the new make_api_call function to test connection
                    response = get_connection_test(
                        state.api_ip_url, 
                        state.api_token
                    )
                    
                    if "error" in response:
                        st.sidebar.error(f"Connection failed: {response['error']}")
                        state.api_connected = False
                    else:
                        st.sidebar.success("Connection successful!")
                        state.api_connected = True
            else:
                st.sidebar.error("Please enter IP/URL and login first")

    st.sidebar.divider()

    # Display token information if one is set
    if state.api_token:
        try:
            decoded_token = jwt.decode(state.api_token, options={"verify_signature": False})
            created_at = datetime.datetime.fromisoformat(decoded_token['created_at'])
            expiry = datetime.datetime.fromtimestamp(decoded_token['exp'], tz=datetime.timezone.utc)
            expiry_delta = expiry - datetime.datetime.now(datetime.timezone.utc)

            st.sidebar.write(f"Username: {decoded_token['username']}")
            st.sidebar.write(f"Created At: {created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            st.sidebar.write(f"Expiry: {expiry_delta.days} days, {expiry_delta.seconds // 3600} hours, {(expiry_delta.seconds % 3600) // 60} minutes, {expiry_delta.seconds % 60} seconds")

        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidTokenError):
            st.sidebar.error("Invalid API token")
        except KeyError:
            st.sidebar.error("Missing required fields in API token")
        except Exception as e:
            st.sidebar.error(f"An error occurred: {e}")

    st.sidebar.divider()

    if st.sidebar.button("Copy API Token"):
        try:
            pyperclip.copy(state.api_token)
            st.sidebar.success("API token copied to clipboard!")
        except:
            st.sidebar.error("Could not copy to clipboard, please copy manually")

    if st.sidebar.button("Reveal API Token"):
        # st.toast("API Token", value=state.api_token)
        st.sidebar.info(state.api_token)


    if state.api_ip_url and state.api_token:
        st.sidebar.divider()

        st.subheader("Blueprint Selection")
        
        # Display the blueprint dropdown
        selected_blueprint, selected_blueprint_id = render_blueprint_dropdown(state)

        if selected_blueprint and selected_blueprint_id:
            # Store both values in state for use elsewhere
            state.selected_blueprint = selected_blueprint
            state.selected_blueprint_id = selected_blueprint_id
        else:
            # Clear the selection if none is made
            state.selected_blueprint = None
            state.selected_blueprint_id = None


    # st.sidebar.title("Apstra Configlet Builder")
    
    # # Initialize session state if not already done
    # initialize_session_state()
    # state = get_state()
    
    # # Apstra server connection section
    # st.sidebar.subheader("Login")
    
    # # Server URL input with default value
    # server_url = st.sidebar.text_input(
    #     "IP/URL", 
    #     value=state.api_ip_url if hasattr(state, 'api_ip_url') else "10.28.143.3",
    #     key="ip_url_input"
    # )
    
    # # Login credentials
    # username = st.sidebar.text_input(
    #     "Username",
    #     value=state.api_username if hasattr(state, 'api_username') else "admin",
    #     key="username_input"
    # )
    
    # password = st.sidebar.text_input(
    #     "Password",
    #     type="password",
    #     key="password_input"
    # )
    
    # # Update session state when input changes
    # state.api_ip_url = server_url
    # state.api_username = username
    
    # # Login and Test Connection buttons in two columns
    # login_cols = st.sidebar.columns(2)
    
    # with login_cols[0]:
    #     if st.button("Login"):
    #         if not state.api_ip_url:
    #             st.sidebar.error("Please enter an IP/URL")
    #         elif not username or not password:
    #             st.sidebar.error("Please enter username and password")
    #         else:
    #             with st.sidebar.spinner(f"Logging in with: {state.api_username}@{state.api_ip_url}"):
    #                 try:
    #                     client = ApstraClient(server_url)
    #                     response = client.login(username, password)
                        
    #                     if "token" in response:
    #                         # Update session state with login information
    #                         state.api_token = response["token"]
    #                         state.api_connected = True
    #                         st.sidebar.success("Login successful!")
    #                     else:
    #                         error_msg = response.get("error", "Unknown error occurred")
    #                         st.sidebar.error(f"Login failed: {error_msg}")
    #                 except Exception as e:
    #                     st.sidebar.error(f"Error connecting to server: {str(e)}")
    
    # with login_cols[1]:
    #     if st.button("Test Connection"):
    #         if state.api_ip_url and state.api_token:
    #             with st.sidebar.spinner("Testing connection..."):
    #                 try:
    #                     client = ApstraClient(server_url)
    #                     client.token = state.api_token
    #                     response = client.test_connection()
                        
    #                     if "error" in response:
    #                         st.sidebar.error(f"Connection failed: {response['error']}")
    #                         state.api_connected = False
    #                     else:
    #                         st.sidebar.success("Connection successful!")
    #                         state.api_connected = True
    #                 except Exception as e:
    #                     st.sidebar.error(f"Error testing connection: {str(e)}")
    #                     state.api_connected = False
    #         else:
    #             st.sidebar.error("Please enter IP/URL and login first")
    
    # st.sidebar.divider()
    
    # # Display token information if one is set
    # if hasattr(state, 'api_token') and state.api_token:
    #     try:
    #         decoded_token = jwt.decode(state.api_token, options={"verify_signature": False})
    #         created_at = datetime.datetime.fromisoformat(decoded_token['created_at'])
    #         expiry = datetime.datetime.fromtimestamp(decoded_token['exp'], tz=datetime.timezone.utc)
    #         expiry_delta = expiry - datetime.datetime.now(datetime.timezone.utc)
            
    #         st.sidebar.write(f"Username: {decoded_token['username']}")
    #         st.sidebar.write(f"Created At: {created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    #         st.sidebar.write(f"Expiry: {expiry_delta.days} days, {expiry_delta.seconds // 3600} hours, {(expiry_delta.seconds % 3600) // 60} minutes, {expiry_delta.seconds % 60} seconds")
            
    #     except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidTokenError):
    #         st.sidebar.error("Invalid API token")
    #     except KeyError:
    #         st.sidebar.error("Missing required fields in API token")
    #     except Exception as e:
    #         st.sidebar.error(f"An error occurred: {e}")
    
    # st.sidebar.divider()
    
    # # Token management options
    # if hasattr(state, 'api_token') and state.api_token:
    #     if st.sidebar.button("Copy API Token"):
    #         try:
    #             pyperclip.copy(state.api_token)
    #             st.sidebar.success("API token copied to clipboard!")
    #         except Exception as e:
    #             st.sidebar.error(f"Could not copy to clipboard: {e}")
                
    #     if st.sidebar.button("Reveal API Token"):
    #         st.sidebar.info(state.api_token)
    
    # # Add version information
    # st.sidebar.markdown("---")
    # st.sidebar.caption("Apstra Configlet Builder v1.0.0")