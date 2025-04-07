# app/utils/data/data_helpers.py
"""
Data manipulation utility functions.
"""
import json
import yaml
from pathlib import Path

def deep_merge(dict1, dict2):
    """
    Recursively merge two dictionaries, with dict2 values taking precedence.
    
    Parameters:
    - dict1 (dict): Base dictionary
    - dict2 (dict): Dictionary to merge into dict1, overwriting where keys match
    
    Returns:
    - dict: Merged dictionary
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def load_json_file(file_content):
    """
    Load and parse a JSON file content.
    
    Args:
        file_content: Content of the JSON file
        
    Returns:
        tuple: (data, error) where data is the parsed JSON or None if error occurred
               and error is an error message or None if successful
    """
    try:
        data = json.loads(file_content)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Error decoding JSON: {e}"
    except Exception as e:
        return None, f"Error processing data: {e}"

def load_yaml_content(file_content):
    """
    Load and parse YAML content.
    
    Args:
        file_content: Content of the YAML file
        
    Returns:
        tuple: (data, error) where data is the parsed YAML or None if error occurred
               and error is an error message or None if successful
    """
    try:
        data = yaml.safe_load(file_content)
        return data, None
    except yaml.YAMLError as e:
        return None, f"Error decoding YAML: {e}"
    except Exception as e:
        return None, f"Error processing data: {e}"

def filter_json(data, query):
    """
    Filter a JSON object for keys/values that match a search query.
    
    Args:
        data: JSON object (dict or list)
        query: Search query string
        
    Returns:
        filtered object of the same type as input
    """
    if not query:
        return data
        
    filtered_data = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if query.lower() in str(key).lower() or query.lower() in str(value).lower():
                filtered_data[key] = value
            elif isinstance(value, (dict, list)):
                result = filter_json(value, query)
                if result:
                    filtered_data[key] = result
    elif isinstance(data, list):
        filtered_list = []
        for item in data:
            result = filter_json(item, query)
            if result:
                filtered_list.append(result)
        return filtered_list

    return filtered_data