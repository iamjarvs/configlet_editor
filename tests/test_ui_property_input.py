"""
Unit tests for the property input UI component.
"""

import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import json
import yaml
from io import BytesIO
from pathlib import Path

class TestPropertyInput(unittest.TestCase):
    """Test cases for the property input UI component."""
    
    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('app.utils.config.session_state.get_state')
    def test_none_selection(self, mock_get_state, mock_radio, mock_subheader):
        """Test 'None' selection for property input."""
        from app.ui.property_input import render_property_input
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "None"
        
        # Call the function
        render_property_input()
        
        # Assert session state was updated correctly
        self.assertIsNone(mock_state.property_set_data)
        self.assertIsNone(mock_state.prop_error)
        self.assertFalse(mock_state.prop_set_loaded)
        self.assertIsNone(mock_state.raw_prop_content_for_display)
        self.assertEqual(mock_state.prop_paste, "")

    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('streamlit.file_uploader')
    @patch('app.utils.config.session_state.get_state')
    def test_json_file_upload(self, mock_get_state, mock_file_uploader, 
                              mock_radio, mock_subheader):
        """Test JSON file upload for property input."""
        from app.ui.property_input import render_property_input, process_property_file
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "File Upload"
        
        # Create a mock file with JSON content
        json_data = {"custom_property": "test_value"}
        mock_file = MagicMock()
        mock_file.name = "test.json"
        mock_file.read.return_value = json.dumps(json_data).encode()
        mock_file_uploader.return_value = mock_file
        
        # Call the function
        render_property_input()
        
        # Assert session state was updated correctly
        self.assertEqual(mock_state.property_set_data, json_data)
        self.assertIsNone(mock_state.prop_error)
        self.assertTrue(mock_state.prop_set_loaded)
        
        # Test the process_property_file function directly
        prop_data, raw_content, error = process_property_file(mock_file)
        self.assertEqual(prop_data, json_data)
        self.assertIsNone(raw_content)  # Raw content is None for JSON
        self.assertIsNone(error)

    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('streamlit.file_uploader')
    @patch('app.utils.config.session_state.get_state')
    def test_yaml_file_upload(self, mock_get_state, mock_file_uploader, 
                              mock_radio, mock_subheader):
        """Test YAML file upload for property input."""
        from app.ui.property_input import render_property_input, process_property_file
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "File Upload"
        
        # Create a mock file with YAML content
        yaml_content = "custom_property: test_value\nlist_property:\n  - item1\n  - item2"
        yaml_data = yaml.safe_load(yaml_content)
        
        mock_file = MagicMock()
        mock_file.name = "test.yaml"
        mock_file.read.return_value = yaml_content.encode()
        mock_file_uploader.return_value = mock_file
        
        # Call the function
        render_property_input()
        
        # Assert session state was updated correctly
        self.assertEqual(mock_state.property_set_data, yaml_data)
        self.assertIsNone(mock_state.prop_error)
        self.assertTrue(mock_state.prop_set_loaded)
        self.assertEqual(mock_state.raw_prop_content_for_display, yaml_content)
        
        # Test the process_property_file function directly
        prop_data, raw_content, error = process_property_file(mock_file)
        self.assertEqual(prop_data, yaml_data)
        self.assertEqual(raw_content, yaml_content)
        self.assertIsNone(error)

    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('streamlit.text_area')
    @patch('app.utils.config.session_state.get_state')
    def test_paste_json(self, mock_get_state, mock_text_area, mock_radio, mock_subheader):
        """Test pasting JSON for property input."""
        from app.ui.property_input import render_property_input
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "Paste Text"
        
        # Mock additional radio for format selection and text area
        mock_radio.side_effect = ["Paste Text", "JSON"]
        
        # Mock text area with valid JSON
        json_content = '{"custom_property": "test_value"}'
        mock_text_area.return_value = json_content
        
        # Call the function
        render_property_input()
        
        # Assert session state was updated correctly
        self.assertEqual(mock_state.property_set_data, json.loads(json_content))
        self.assertIsNone(mock_state.prop_error)
        self.assertTrue(mock_state.prop_set_loaded)
        self.assertIsNone(mock_state.raw_prop_content_for_display)

    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('app.utils.config.session_state.get_state')
    @patch('streamlit.json')
    def test_example_property_set(self, mock_json, mock_get_state, 
                                  mock_radio, mock_subheader):
        """Test loading example property set."""
        from app.ui.property_input import render_property_input
        from app.utils.config.example_data import EXAMPLE_PROPERTY_SET
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "Example Property Set"
        
        # Call the function
        render_property_input()
        
        # Assert session state was updated correctly
        self.assertEqual(mock_state.property_set_data, json.loads(EXAMPLE_PROPERTY_SET))
        self.assertIsNone(mock_state.prop_error)
        self.assertTrue(mock_state.prop_set_loaded)
        self.assertEqual(mock_state.raw_prop_content_for_display, EXAMPLE_PROPERTY_SET)
        mock_json.assert_called_once()

    @patch('streamlit.subheader')
    @patch('streamlit.radio')
    @patch('streamlit.file_uploader')
    @patch('app.utils.config.session_state.get_state')
    @patch('streamlit.error')
    def test_invalid_json_file(self, mock_error, mock_get_state, mock_file_uploader,
                               mock_radio, mock_subheader):
        """Test upload of invalid JSON file."""
        from app.ui.property_input import render_property_input, process_property_file
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_radio.return_value = "File Upload"
        
        # Create a mock file with invalid JSON content
        invalid_json = "{property: 'value'}"  # Missing quotes
        
        mock_file = MagicMock()
        mock_file.name = "invalid.json"
        mock_file.read.return_value = invalid_json.encode()
        mock_file_uploader.return_value = mock_file
        
        # Call the function
        render_property_input()
        
        # Assert error was handled
        self.assertFalse(mock_state.prop_set_loaded)
        self.assertIsNotNone(mock_state.prop_error)
        mock_error.assert_called_once()
        
        # Test the process_property_file function directly
        prop_data, raw_content, error = process_property_file(mock_file)
        self.assertIsNone(prop_data)
        self.assertIsNone(raw_content)
        self.assertIsNotNone(error)
        self.assertIn("Error decoding Property Set JSON", error)


if __name__ == '__main__':
    unittest.main()