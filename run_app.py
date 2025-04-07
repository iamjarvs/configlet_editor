#!/usr/bin/env python3
"""
Wrapper script to run the Apstra Configlet Builder.

This script ensures proper importing of modules by setting up Python path.
"""

import streamlit.web.cli as stcli
import sys
import os

# Add current directory to path for proper imports
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_path)

# Run the Streamlit app
if __name__ == "__main__":
    sys.argv = ["streamlit", "run", os.path.join(root_path, "app", "main.py")]
    sys.exit(stcli.main())