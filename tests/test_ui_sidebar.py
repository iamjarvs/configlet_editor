"""
Unit tests for the sidebar UI component.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import datetime

# Import from test fixtures to ensure proper mocking
from conftest import patch_session_state

# Patch the modules with mocks
import streamlit as st
import jwt

class TestSidebar(unittest.TestCase):
    """Test cases for the sidebar UI component."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Patch session_state module
        self.session_state = patch_session_state()
        
        # Create a mock state object
        self.mock_state = MagicMock()
        
        # Ensure the get_state function returns our mock
        self.original_get_state = self.session_state.get_state
        self.session_state.get_state = lambda: self.mock_state
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Restore original get_state function
        self.session_state.get_state = self.original_get_state
    
    @patch('streamlit.sidebar.title')
    @patch('streamlit.sidebar.subheader')
    @patch('streamlit.sidebar.text_input')
    @patch('streamlit.sidebar.button')
    @patch('app.utils.api.apstra_client.ApstraClient')
    def test_sidebar_login_success(self, mock_client, mock_button, 
                                mock_text_input, mock_subheader, mock_title):
        """Test successful login flow in sidebar."""
        from app.ui.sidebar import render_sidebar
        
        # Set up mocks
        mock_text_input.side_effect = ["10.28.143.3", "admin", "password"]
        
        # Mock the button click for login
        mock_button.return_value = True
        
        # Mock client login response
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.login.return_value = {"token": "test_token"}
        
        # Call the function
        render_sidebar()
        
        # Assert that the login attempt was made with correct credentials
        mock_client.assert_called_once_with("10.28.143.3")
        mock_client_instance.login.assert_called_once_with("admin", "password")
        
        # Assert session state was updated correctly
        self.assertEqual(self.mock_state.api_token, "test_token")
        self.assertEqual(self.mock_state.api_connected, True)

    @patch('streamlit.sidebar.title')
    @patch('streamlit.sidebar.subheader')
    @patch('streamlit.sidebar.text_input')
    @patch('streamlit.sidebar.button')
    @patch('app.utils.api.apstra_client.ApstraClient')
    def test_sidebar_login_failure(self, mock_client, mock_button, 
                                mock_text_input, mock_subheader, mock_title):
        """Test failed login flow in sidebar."""
        from app.ui.sidebar import render_sidebar
        
        # Set up mocks
        mock_text_input.side_effect = ["10.28.143.3", "admin", "wrong_password"]
        
        # Mock the button click for login
        mock_button.return_value = True
        
        # Mock client login response - failure
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_client_instance.login.return_value = {"error": "Invalid credentials"}
        
        # Call the function
        render_sidebar()
        
        # Assert login attempt was made
        mock_client.assert_called_once()
        mock_client_instance.login.assert_called_once()
        
        # Assert session state was not updated with token
        self.assertFalse(hasattr(self.mock_state, 'api_token') or self.mock_state.api_token == "test_token")

    @patch('streamlit.sidebar.title')
    @patch('streamlit.sidebar.subheader')
    @patch('streamlit.sidebar.text_input')
    @patch('streamlit.sidebar.button')
    @patch('jwt.decode')
    def test_sidebar_token_display(self, mock_jwt_decode, mock_button, 
                                  mock_text_input, mock_subheader, mock_title):
        """Test token information display in sidebar."""
        from app.ui.sidebar import render_sidebar
        
        # Set up mocks
        self.mock_state.api_token = "test_token"
        
        # Mock JWT decode response
        created_at = datetime.datetime.now().isoformat()
        expiry = int((datetime.datetime.now() + 
                     datetime.timedelta(days=1)).timestamp())
        
        mock_jwt_decode.return_value = {
            "username": "admin",
            "created_at": created_at,
            "exp": expiry
        }
        
        # Call the function
        render_sidebar()
        
        # Assert JWT decode was called with correct token
        mock_jwt_decode.assert_called_once_with("test_token", options={"verify_signature": False})


if __name__ == '__main__':
    unittest.main()