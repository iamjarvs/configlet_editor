# tests/test_template_engine.py
import unittest
from app.utils.data.template_engine import render_template

class TestTemplateEngine(unittest.TestCase):
    """Test cases for the template engine."""
    
    def test_simple_template(self):
        """Test rendering a simple template."""
        template = "Hello, {{ name }}!"
        context = {"name": "World"}
        rendered, error = render_template(template, context)
        
        self.assertIsNone(error)
        self.assertEqual(rendered, "Hello, World!")
    
    def test_with_property_set(self):
        """Test rendering with merged property set."""
        template = "{{ device.name }} - {{ device.type }} - {{ custom.setting }}"
        context = {"device": {"name": "switch1", "type": "leaf"}}
        property_set = {"custom": {"setting": "value"}}
        
        rendered, error = render_template(template, context, property_set)
        
        self.assertIsNone(error)
        self.assertEqual(rendered, "switch1 - leaf - value")
    
    def test_template_error(self):
        """Test handling of template syntax errors."""
        template = "{% if x %}Missing end tag"
        context = {"x": True}
        
        rendered, error = render_template(template, context)
        
        self.assertIsNone(rendered)
        self.assertIsNotNone(error)
        self.assertIn("Template Syntax Error", error)
    
    def test_undefined_variable(self):
        """Test handling of undefined variables."""
        template = "{{ variable_that_doesnt_exist }}"
        context = {"something_else": "value"}
        
        rendered, error = render_template(template, context)
        
        self.assertIsNone(rendered)
        self.assertIsNotNone(error)
        self.assertIn("Undefined variable", error)

if __name__ == '__main__':
    unittest.main()