# app/utils/api/http_client.py
"""
Base HTTP client functions for making API requests.
"""
import requests
import json

def get_request(url, headers=None, verify=False):
    """Makes a GET request with error handling and returns JSON response."""
    try:
        response = requests.get(url, headers=headers, verify=verify)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        return {"error": f"HTTP Error: {errh}", "status_code": response.status_code}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Connection Error: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request Error: {err}"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON response", "response_text": response.text}

def post_request(url, body, headers=None, verify=False):
    """Makes a POST request with error handling and returns JSON response."""
    try:
        response = requests.post(url, json=body, headers=headers, verify=verify)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        try:
            error_resp = response.json()
            return {"error": f"HTTP Error: {errh}", "status_code": response.status_code, "details": error_resp}
        except:
            return {"error": f"HTTP Error: {errh}", "status_code": response.status_code, "response_text": response.text}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Connection Error: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request Error: {err}"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON response", "response_text": response.text}

def put_request(url, body, headers=None, verify=False):
    """Makes a PUT request with error handling and returns JSON response."""
    try:
        response = requests.put(url, json=body, headers=headers, verify=verify)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        try:
            error_resp = response.json()
            return {"error": f"HTTP Error: {errh}", "status_code": response.status_code, "details": error_resp}
        except:
            return {"error": f"HTTP Error: {errh}", "status_code": response.status_code, "response_text": response.text}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Connection Error: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request Error: {err}"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON response", "response_text": response.text}

def delete_request(url, headers=None, verify=False):
    """Makes a DELETE request with error handling and returns status code or JSON if available."""
    try:
        response = requests.delete(url, headers=headers, verify=verify)
        response.raise_for_status()
        try:
            return response.json()  # Some APIs return JSON even for DELETE
        except json.JSONDecodeError:
            return {"status_code": response.status_code, "message": "Delete successful"}
    except requests.exceptions.HTTPError as errh:
        return {"error": f"HTTP Error: {errh}", "status_code": response.status_code}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Connection Error: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request Error: {err}"}

def patch_request(url, body, headers=None, verify=False):
    """Makes a PATCH request with error handling and returns JSON response."""
    try:
        response = requests.patch(url, json=body, headers=headers, verify=verify)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        try:
            error_resp = response.json()
            return {"error": f"HTTP Error: {errh}", "status_code": response.status_code, "details": error_resp}
        except:
            return {"error": f"HTTP Error: {errh}", "status_code": response.status_code, "response_text": response.text}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Connection Error: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request Error: {err}"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON response", "response_text": response.text}