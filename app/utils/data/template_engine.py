# app/utils/data/template_engine.py
"""
Template rendering functionality using Jinja2.
"""
import jinja2
from .data_helpers import deep_merge

def render_template(template_string, device_context, property_set=None):
    """
    Render a Jinja2 template with the given context and optional property set.
    
    Args:
        template_string (str): Jinja2 template
        context (dict): Base template rendering context (device context)
        property_set (dict, optional): Additional properties to merge into context
        
    Returns:
        tuple: (rendered_output, error) where rendered_output is the rendered template
               or None if error occurred, and error is an error message or None if successful
    """
    try:
        # Create a merged context if property_set is provided
        final_context = device_context
        if property_set is not None:
            try:
                final_context = deep_merge(device_context.copy(), property_set)
            except Exception as e:
                return None, f"Error merging property set: {e}"
        
        # Create Jinja2 environment with strict undefined handling
        env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            undefined=jinja2.StrictUndefined  # Raise error for undefined variables
        )
        
        # Create template from string
        template = env.from_string(template_string)
        
        # Render template with context
        rendered_output = template.render(**final_context)
        
        return rendered_output, None
        
    except jinja2.exceptions.TemplateSyntaxError as e:
        return None, f"Template Syntax Error: {e.message} (Line: {e.lineno})"
    except jinja2.exceptions.UndefinedError as e:
        return None, f"Template Rendering Error: Undefined variable - {e.message} - Check this variable exists in the devcie context or property set"
    except Exception as e:
        return None, f"An unexpected error occurred during rendering: {e}"