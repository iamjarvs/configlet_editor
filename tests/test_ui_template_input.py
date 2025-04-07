"""
Unit tests for the template input UI component.
"""

import unittest
from unittest.mock import patch, MagicMock
import streamlit as st

class TestTemplateInput(unittest.TestCase):
    """Test cases for the template input UI component."""
    
    @patch('streamlit.subheader')
    @patch('streamlit_ace.st_ace')
    @patch('app.utils.config.session_state.get_state')
    @patch('streamlit.expander')
    def test_template_editor_initialization(self, mock_expander, mock_get_state, 
                                          mock_st_ace, mock_subheader):
        """Test template editor initialization with default template."""
        from app.ui.template_input import render_template_input
        
        # Set up mocks
        mock_state = MagicMock()
        mock_state.template_input = None  # No template set yet
        mock_get_state.return_value = mock_state
        
        # Mock Ace editor return value (user edited template)
        mock_st_ace.return_value = "{% for item in items %}{{ item }}{% endfor %}"
        
        # Create mock expander
        mock_expander_instance = MagicMock()
        mock_expander.return_value.__enter__.return_value = mock_expander_instance
        
        # Call the function
        render_template_input()
        
        # Assert default template was set and Ace editor was initialized with it
        self.assertIsNotNone(mock_state.template_input)
        mock_st_ace.assert_called_once()
        self.assertEqual(mock_st_ace.call_args[1]['language'], "jinja2")
        self.assertEqual(mock_st_ace.call_args[1]['theme'], "chrome")
        self.assertTrue(mock_st_ace.call_args[1]['show_gutter'])
        
        # Assert template was updated with editor value
        self.assertEqual(mock_state.template_input, "{% for item in items %}{{ item }}{% endfor %}")

    @patch('streamlit.subheader')
    @patch('streamlit_ace.st_ace')
    @patch('app.utils.config.session_state.get_state')
    @patch('streamlit.expander')
    def test_template_editor_with_existing_template(self, mock_expander, mock_get_state, 
                                                 mock_st_ace, mock_subheader):
        """Test template editor initialization with existing template."""
        from app.ui.template_input import render_template_input
        
        # Set up mocks
        mock_state = MagicMock()
        existing_template = "{% if condition %}true{% else %}false{% endif %}"
        mock_state.template_input = existing_template
        mock_get_state.return_value = mock_state
        
        # Mock Ace editor return value (user edited template)
        edited_template = "{% if condition %}TRUE{% else %}FALSE{% endif %}"
        mock_st_ace.return_value = edited_template
        
        # Create mock expander
        mock_expander_instance = MagicMock()
        mock_expander.return_value.__enter__.return_value = mock_expander_instance
        
        # Call the function
        render_template_input()
        
        # Assert Ace editor was initialized with existing template
        mock_st_ace.assert_called_once()
        self.assertEqual(mock_st_ace.call_args[1]['value'], existing_template)
        
        # Assert template was updated with editor value
        self.assertEqual(mock_state.template_input, edited_template)

    @patch('streamlit.subheader')
    @patch('streamlit_ace.st_ace')
    @patch('app.utils.config.session_state.get_state')
    @patch('streamlit.expander')
    @patch('streamlit.tabs')
    def test_jinja2_reference_tabs(self, mock_tabs, mock_expander, mock_get_state,
                                  mock_st_ace, mock_subheader):
        """Test that Jinja2 reference tabs are created correctly."""
        from app.ui.template_input import render_template_input
        
        # Set up mocks
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        
        # Mock tabs return
        mock_tab_instances = [MagicMock() for _ in range(7)]  # 7 tabs in reference
        mock_tabs.return_value = mock_tab_instances
        
        # Create mock expander that calls render_jinja2_reference
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__.return_value = mock_expander_context
        
        def mock_enter_expander(*args, **kwargs):
            # When entering the expander context, call the render function
            from app.ui.template_input import render_jinja2_reference
            render_jinja2_reference()
            return mock_expander_context
            
        mock_expander.return_value.__enter__ = mock_enter_expander
        
        # Call the function
        render_template_input()
        
        # Assert tabs were created with correct names
        mock_tabs.assert_called_once()
        tab_names = mock_tabs.call_args[0][0]
        self.assertEqual(len(tab_names), 7)
        self.assertIn("Variables", tab_names)
        self.assertIn("For Loops", tab_names)
        self.assertIn("If/Elif/Else", tab_names)
        self.assertIn("Set Variables", tab_names)
        self.assertIn("Filters", tab_names)
        self.assertIn("Comments", tab_names)
        self.assertIn("Whitespace", tab_names)


if __name__ == '__main__':
    unittest.main()