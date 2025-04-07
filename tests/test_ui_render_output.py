"""
Unit tests for the render output UI component.
"""

import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import jinja2

class TestRenderOutput(unittest.TestCase):
    """Test cases for the render output UI component."""
    
    @patch('streamlit.subheader')
    @patch('app.utils.config.session_state.get_state')
    @patch('app.utils.data.template_engine.render_template')
    @patch('streamlit.code')
    @patch('streamlit.expander')
    @patch('streamlit.download_button')
    def test_successful_render(self, mock_download, mock_expander, mock_code, 
                              mock_render_template, mock_get_state, mock_subheader):
        """Test successful template rendering and output display."""
        from app.ui.render_output import render_output
        
        # Set up mocks
        mock_state = MagicMock()
        mock_state.device_context_data = {"hostname": "switch1", "interfaces": {}}
        mock_state.context_loaded = True
        mock_state.context_error = None
        mock_state.template_input = "Hostname: {{ hostname }}"
        mock_get_state.return_value = mock_state
        
        # Mock template rendering result
        mock_render_template.return_value = ("Hostname: switch1", None)
        
        # Mock expander context
        mock_expander_instance = MagicMock()
        mock_expander.return_value.__enter__.return_value = mock_expander_instance
        
        # Call the function
        render_output()
        
        # Assert template engine was called with correct parameters
        mock_