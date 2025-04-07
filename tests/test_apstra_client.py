# tests/test_apstra_client.py
import unittest
from unittest.mock import patch, MagicMock
from app.utils.api.apstra_client import ApstraClient

class TestApstraClient(unittest.TestCase):
    """Test cases for the ApstraClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = ApstraClient("test.example.com")
    
    def test_initialization(self):
        """Test that the client initializes correctly."""
        self.assertEqual(self.client.base_url, "test.example.com")
        self.assertIsNone(self.client.token)
        self.assertIsNone(self.client.username)
    
    @patch('app.utils.api.apstra_client.post_request')
    def test_login_success(self, mock_post):
        """Test successful login."""
        # Mock the post_request function
        mock_post.return_value = {
            "token": "test_token",
            "id": "test_id"
        }
        
        # Call the login method
        response = self.client.login("admin", "password")
        
        # Verify post_request was called with correct arguments
        mock_post.assert_called_once_with(
            "https://test.example.com/api/aaa/login",
            {"username": "admin", "password": "password"}
        )
        
        # Verify response and client state
        self.assertEqual(response["token"], "test_token")
        self.assertEqual(self.client.token, "test_token")
        self.assertEqual(self.client.username, "admin")
    
    @patch('app.utils.api.apstra_client.post_request')
    def test_login_failure(self, mock_post):
        """Test login failure."""
        # Mock the post_request function to return an error
        mock_post.return_value = {
            "error": "Invalid credentials"
        }
        
        # Call the login method
        response = self.client.login("admin", "wrong_password")
        
        # Verify response and client state
        self.assertEqual(response["error"], "Invalid credentials")
        self.assertIsNone(self.client.token)

    @patch('app.utils.api.apstra_client.get_request')
    def test_get_design_configlets(self, mock_get):
        """Test getting design configlets."""
        # Set up mock
        mock_get.return_value = {"configlets": ["configlet1", "configlet2"]}
        
        # Set token
        self.client.token = "test_token"
        
        # Call method
        response = self.client.get_design_configlets()
        
        # Verify get_request was called with correct arguments
        mock_get.assert_called_once_with(
            "https://test.example.com/api/design/configlets",
            headers={"AuthToken": "test_token"}
        )
        
        # Verify response
        self.assertEqual(response["configlets"], ["configlet1", "configlet2"])
    
    def test_no_token_error(self):
        """Test methods requiring a token return an error when no token is set."""
        # Call a method without setting token
        response = self.client.get_design_configlets()
        
        # Verify error response
        self.assertIn("error", response)
        self.assertIn("No token available", response["error"])

if __name__ == '__main__':
    unittest.main()