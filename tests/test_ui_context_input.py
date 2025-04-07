"""
Unit tests for the context input UI component.
"""

import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import json

class TestContextInput(unittest.TestCase):
    """Test cases for the context input UI component."""
    
    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('streamlit.file_uploader')
    @patch('app.utils.config.session_state.get_state')
    def test_file_upload_success(self, mock_get_state, mock_file_uploader, 
                                mock_radio, mock_subheader):
        """Test successful file upload for context input."""
        from app.ui.context_input import render_context_input
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "File Upload"
        
        # Mock file uploader with valid JSON
        mock_file = MagicMock()
        valid_json = json.dumps({"hostname": "test-device", "interfaces": {}})
        mock_file.getvalue.return_value = valid_json.encode()
        mock_file_uploader.return_value = mock_file
        
        # Call the function
        render_context_input()
        
        # Assert session state was updated correctly
        self.assertEqual(mock_state.device_context_data, json.loads(valid_json))
        self.assertIsNone(mock_state.context_error)
        self.assertTrue(mock_state.context_loaded)

    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('streamlit.file_uploader')
    @patch('app.utils.config.session_state.get_state')
    @patch('streamlit.error')
    def test_file_upload_invalid_json(self, mock_error, mock_get_state, 
                                     mock_file_uploader, mock_radio, mock_subheader):
        """Test file upload with invalid JSON for context input."""
        from app.ui.context_input import render_context_input
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "File Upload"
        
        # Mock file uploader with invalid JSON
        mock_file = MagicMock()
        invalid_json = "{hostname: 'test-device', interfaces: {}"  # Missing quotes and closing brace
        mock_file.getvalue.return_value = invalid_json.encode()
        mock_file_uploader.return_value = mock_file
        
        # Call the function
        render_context_input()
        
        # Assert error was handled
        self.assertFalse(mock_state.context_loaded)
        self.assertIsNotNone(mock_state.context_error)
        mock_error.assert_called_once()

    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('streamlit.text_area')
    @patch('app.utils.config.session_state.get_state')
    def test_paste_text_success(self, mock_get_state, mock_text_area, 
                              mock_radio, mock_subheader):
        """Test successful text paste for context input."""
        from app.ui.context_input import render_context_input
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "Paste Text"
        
        # Mock text area with valid JSON
        valid_json = '{"hostname": "test-device", "interfaces": {}}'
        mock_text_area.return_value = valid_json
        
        # Call the function
        render_context_input()
        
        # Assert session state was updated correctly
        self.assertEqual(mock_state.device_context_data, json.loads(valid_json))
        self.assertIsNone(mock_state.context_error)
        self.assertTrue(mock_state.context_loaded)

    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('app.utils.config.session_state.get_state')
    @patch('streamlit.json')
    def test_example_device_config(self, mock_json, mock_get_state, 
                                  mock_radio, mock_subheader):
        """Test loading example device config."""
        from app.ui.context_input import render_context_input
        from app.utils.config.example_data import EXAMPLE_DEVICE_CONTEXT
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "Example Device Config"
        
        # Call the function
        render_context_input()
        
        # Assert session state was updated correctly
        self.assertEqual(mock_state.device_context_data, json.loads(EXAMPLE_DEVICE_CONTEXT))
        self.assertIsNone(mock_state.context_error)
        self.assertTrue(mock_state.context_loaded)
        mock_json.assert_called_once()

    def test_filter_json(self):
        """Test the JSON filtering functionality."""
        from app.ui.context_input import filter_json
        
        # Test data
        test_data = {
            "hostname": "switch1",
            "interfaces": {
                "eth0": {"description": "management", "speed": "1G"},
                "eth1": {"description": "uplink", "speed": "10G"}
            },
            "vlans": [
                {"id": 10, "name": "data"},
                {"id": 20, "name": "voice"}
            ]
        }
        
        # Test filtering by key
        filtered = filter_json(test_data, "hostname")
        self.assertIn("hostname", filtered)
        self.assertEqual(filtered["hostname"], "switch1")
        self.assertNotIn("interfaces", filtered)
        
        # Test filtering by value
        filtered = filter_json(test_data, "management")
        self.assertIn("interfaces", filtered)
        self.assertIn("eth0", filtered["interfaces"])
        self.assertNotIn("eth1", filtered["interfaces"])
        
        # Test filtering nested structure
        filtered = filter_json(test_data, "10G")
        self.assertIn("interfaces", filtered)
        self.assertIn("eth1", filtered["interfaces"])
        self.assertNotIn("eth0", filtered["interfaces"])
        
        # Test filtering list items
        filtered = filter_json(test_data, "voice")
        self.assertIn("vlans", filtered)
        
        # Test with no matches
        filtered = filter_json(test_data, "nonexistent")
        self.assertEqual(filtered, {})


if __name__ == '__main__':
    unittest.main()