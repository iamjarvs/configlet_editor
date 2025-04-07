"""
Test package for the Apstra Configlet Builder.

This package contains the tests for the application.
"""

# Import conftest to ensure mocks are available in tests
from tests.conftest import patch_session_state

# Initialize patched session state
patch_session_state()