print("Loading test_foundation.py")

import unittest

from app.utils.api.http_client import get_request, post_request
from app.utils.data.data_helpers import deep_merge, filter_json

class TestHttpClient(unittest.TestCase):
    """Test cases for the HTTP client functions."""
    
    def test_imports(self):
        """Test that HTTP client functions can be imported correctly."""
        self.assertTrue(callable(get_request))
        self.assertTrue(callable(post_request))

class TestDataHelpers(unittest.TestCase):
    """Test cases for data helper functions."""
    
    def test_deep_merge(self):
        """Test the deep_merge function."""
        dict1 = {"a": 1, "b": {"c": 2}}
        dict2 = {"b": {"d": 3}, "e": 4}
        result = deep_merge(dict1, dict2)
        expected = {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}
        self.assertEqual(result, expected)
    
    def test_filter_json(self):
        """Test the filter_json function."""
        test_data = {
            "person": {
                "name": "John Doe",
                "age": 30
            }
        }
        # Test filtering with a match
        result = filter_json(test_data, "John")
        self.assertIn("person", result)

if __name__ == '__main__':
    unittest.main()