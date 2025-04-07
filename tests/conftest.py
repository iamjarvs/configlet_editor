"""
Test configuration and setup for the Apstra Configlet Builder.

This module contains test fixtures and setup code for all tests.
"""

import sys
import os
from unittest.mock import MagicMock

# Add the mocks directory to the Python path
tests_dir = os.path.dirname(os.path.abspath(__file__))
mocks_dir = os.path.join(tests_dir, 'mocks')
sys.path.insert(0, mocks_dir)

# Create mock modules for tests
sys.modules['streamlit'] = MagicMock()
sys.modules['streamlit_ace'] = MagicMock()
sys.modules['jwt'] = MagicMock()

# Mock Streamlit session state
class MockSessionState:
    def __init__(self):
        self._data = {}
    
    def __getattr__(self, name):
        if name not in self._data:
            self._data[name] = None
        return self._data[name]
    
    def __setattr__(self, name, value):
        if name != '_data':
            self._data[name] = value
        else:
            super().__setattr__(name, value)
    
    def __getitem__(self, key):
        if key not in self._data:
            self._data[key] = None
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value

# Create a patched version of the session_state module
def patch_session_state():
    """
    Create a patched version of the session_state module.
    
    This allows tests to run without actual Streamlit dependency.
    """
    from app.utils.config import session_state
    
    # Replace functions with mock implementations
    session_state.get_state = lambda: MockSessionState()
    session_state.initialize_session_state = lambda: None
    
    return session_state