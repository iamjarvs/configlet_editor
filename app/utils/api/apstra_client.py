# app/utils/api/apstra_client.py
"""
Apstra API client module.
This module provides a class for interacting with the Apstra API.
"""
import datetime
import jwt
import json
from .http_client import get_request, post_request, put_request, delete_request, patch_request
def get_login(base_url, username, password):
    """
    Performs a POST request to the login endpoint with a body containing username and password.

    Parameters:
    - base_url (str): The base URL of the API.
    - username (str): The username for login.
    - password (str): The password for login.

    Returns:
    - Response object: The response from the server after the POST request with token.
    """
    # Construct the full URL for the login endpoint
    url = f"https://{base_url}/api/aaa/login"
    
    # Body to be sent in the POST request
    body = {
        "username": username,
        "password": password
    }
    
    # Perform the POST request
    try:
        response = post_request(url, body, headers=None)
        return response
    except Exception as e:
        return {"error": f"Login error: {str(e)}"}

def get_design_configlets(base_url, token):
    """
    Performs a GET request to retrieve design configlets.

    Parameters:
    - base_url (str): The base URL of the API.
    - token (str): Apstra API Token.

    Returns:
    - Response object: The response from the server containing design configlets.
    """
    # Construct the full URL for the design configlets endpoint
    url = f"https://{base_url}/api/design/configlets"
    
    # Headers for the GET request
    headers = {
        "AuthToken": token,
    }
    
    # Perform the GET request
    try:
        response = get_request(url, headers=headers)
        return response
    except Exception as e:
        return {"error": f"Error fetching design configlets: {str(e)}"}

def get_all_blueprints(base_url, token):
    """
    Performs a GET request to blueprints API.

    Parameters:
    - base_url (str): The base URL of the API.
    - token (str): Apstra API Token.

    Returns:
    - Response object: The response from the server with blueprints data.
    """
    # Construct the full URL for the blueprints endpoint
    url = f"https://{base_url}/api/blueprints"
    
    # Headers for the GET request
    headers = {
        "AuthToken": token,
    }
    
    # Perform the GET request
    try:
        response = get_request(url, headers=headers)
        return response
    except Exception as e:
        return {"error": f"Error fetching blueprints: {str(e)}"}

def get_blueprint_nodes(base_url, token, blueprint_id):
    """
    Performs a POST request to query all blueprint system nodes using the QE API.

    Parameters:
    - base_url (str): The base URL of the API.
    - token (str): Apstra API Token.
    - blueprint_id (str): ID of the blueprint to query.

    Returns:
    - Response object: The response from the server with nodes data.
    """
    # Construct the full URL for the query engine endpoint
    url = f"https://{base_url}/api/blueprints/{blueprint_id}/qe"
    
    # Headers for the POST request
    headers = {
        "AuthToken": token,
    }
    
    # Query body for switches
    body = {
        "query": "node(type='system', name='switch_nodes', system_type='switch')"
    }
    
    # Perform the POST request
    try:
        response = post_request(url, body, headers=headers)
        return response
    except Exception as e:
        return {"error": f"Error fetching blueprint nodes: {str(e)}"}

def get_device_context(base_url, token, blueprint_id, node_id):
    """
    Performs a GET request to retrieve device configuration rendering context.

    Parameters:
    - base_url (str): The base URL of the API.
    - token (str): Apstra API Token.
    - blueprint_id (str): ID of the blueprint.
    - node_id (str): ID of the node to get context for.

    Returns:
    - Response object: The response from the server with device context.
    """
    url = f"https://{base_url}/api/blueprints/{blueprint_id}/nodes/{node_id}/config-context"

    
    # Headers for the GET request
    headers = {
        "AuthToken": token,
    }
    
    # Perform the GET request
    try:
        response = get_request(url, headers=headers)
        return json.loads(response['context'])
    except Exception as e:
        return {"error": f"Error fetching device context: {str(e)}"}

def get_property_sets(base_url, token):
    """
    Performs a GET request to retrieve property sets from Apstra.

    Parameters:
    - base_url (str): The base URL of the API.
    - token (str): Apstra API Token.

    Returns:
    - dict: The response from the server with property sets.
    """
    url = f"https://{base_url}/api/property-sets"
    
    # Headers for the GET request
    headers = {
        "AuthToken": token,
    }
    
    # Perform the GET request
    try:
        response = get_request(url, headers=headers)
        return response
    except Exception as e:
        return {"error": f"Error fetching property sets: {str(e)}"}

def get_configlets(base_url, token):
    """
    Performs a GET request to retrieve configlets from Apstra.

    Parameters:
    - base_url (str): The base URL of the API.
    - token (str): Apstra API Token.

    Returns:
    - dict: The response from the server with configlets.
    """
    url = f"https://{base_url}/api/design/configlets"
    
    # Headers for the GET request
    headers = {
        "AuthToken": token,
    }
    
    # Perform the GET request
    try:
        response = get_request(url, headers=headers)
        return response
    except Exception as e:
        return {"error": f"Error fetching configlets: {str(e)}"}

def get_connection_test(base_url, token):
    """
    Performs a GET request to api docs to test connection.

    Parameters:
    - base_url (str): The base URL of the API.
    - token (str): Apstra API Token.

    Returns:
    - Response object: The response from the server with the api docs.
    """
    # Construct the full URL for the config rendering endpoint
    url = f"https://{base_url}/api/docs"
    
    # Headers for the GET request
    headers = {
        "AuthToken": token,
    }
    
    # Perform the GET request
    try:
        response = get_request(url, headers=headers)
        return response
    except Exception as e:
        return {"error": f"Error fetching device context: {str(e)}"}

def get_any_endpoint(base_url, token, endpoint):
    """
    Performs a GET request to any valid endpoint.

    Parameters:
    - base_url (str): The base URL of the API.
    - token (str): Apstra API Token.

    Returns:
    - Response object: The response from the server containing design configlets.
    """
    # Construct the full URL for the design configlets endpoint
    url = f"https://{base_url}/{endpoint}"
    
    # Headers for the GET request
    headers = {
        "AuthToken": token,
    }
    
    # Perform the GET request
    try:
        response = get_request(url, headers=headers)
        return response
    except Exception as e:
        return {"error": f"Error fetching design configlets: {str(e)}"}