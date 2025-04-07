#!/usr/bin/env python3
"""
Test runner script for the Apstra Configlet Builder application.

This script discovers and runs all tests in the project and generates
a comprehensive test report.

Usage:
    python run_tests.py
"""

import unittest
import sys
import os
import time
from datetime import datetime

def print_header(text):
    """Print a formatted header."""
    line = "=" * 70
    print("\n" + line)
    print(f"{text:^70}")
    print(line + "\n")

def print_section(text):
    """Print a formatted section header."""
    line = "-" * 70
    print("\n" + line)
    print(f"{text}")
    print(line)

def discover_and_run_tests():
    """Discover and run all tests in the project."""
    # Record start time
    start_time = time.time()
    
    # Create a test suite and discover tests
    print_header("APSTRA CONFIGLET BUILDER TEST SUITE")
    
    # Print current timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Test run started at: {now}\n")
    
    # Find the tests directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(base_dir, 'tests')
    
    # Ensure tests directory exists
    if not os.path.exists(test_dir):
        print(f"Error: Tests directory '{test_dir}' not found!")
        return 1
    
    # Add the project root to the Python path to ensure imports work correctly
    sys.path.insert(0, base_dir)
    
    # Discover tests
    print_section("Discovering tests...")
    discover = unittest.defaultTestLoader.discover(
        start_dir=test_dir,
        pattern='test_*.py',
        top_level_dir=base_dir
    )
    
    # Count the number of tests
    test_count = 0
    for suite in discover:
        for test_case in suite:
            test_count += test_case.countTestCases()
    
    print(f"Found {test_count} tests in the test suite.\n")
    
    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    print_section("Running tests...")
    result = runner.run(discover)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Print test summary
    print_section("TEST SUMMARY")
    print(f"Total tests: {test_count}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Test run completed in {duration:.2f} seconds")
    
    # Print failures and errors if any
    if result.failures:
        print_section("FAILURES")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"Failure {i}: {test}")
            print(traceback)
            print()
    
    if result.errors:
        print_section("ERRORS")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"Error {i}: {test}")
            print(traceback)
            print()
    
    # Calculate pass percentage
    if result.testsRun > 0:
        success_count = result.testsRun - len(result.failures) - len(result.errors)
        success_percentage = (success_count / result.testsRun) * 100
        print(f"\nPass percentage: {success_percentage:.2f}%")
    
    # Return appropriate exit code
    return 0 if len(result.failures) == 0 and len(result.errors) == 0 else 1

if __name__ == "__main__":
    # Ensure we use proper mocks for streamlit and other modules
    # We need to set these imports before importing any app modules
    try:
        from tests.conftest import patch_session_state
        
        # Initialize patched session state
        patch_session_state()
        
        # Run the tests and get the exit code
        exit_code = discover_and_run_tests()
        
        # Exit with the appropriate code
        sys.exit(exit_code)
    except ImportError as e:
        print(f"Error: Failed to import required test modules: {e}")
        print("Make sure you have all required dependencies installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)