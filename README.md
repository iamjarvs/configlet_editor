# Apstra Configlet Builder

A powerful web-based tool for network administrators to create, test, and manage Jinja2 templates for Apstra configlets.

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/iamjarvs/apstraconfigletbuilder/ci.yml?branch=main)
![Docker Pulls](https://img.shields.io/docker/pulls/iamjarvs/apstraconfigletbuilder)

## Overview

The Apstra Configlet Builder provides a user-friendly interface for developing and testing Jinja2 templates used in Apstra configlets. It allows network engineers to preview rendered configurations using real device context data and custom property sets before deploying to production environments.

This was build with a mixture of my own brain and Google's Gemini 2.5 Pro via Cline (VScode extension)

## Features

- **Interactive Template Editor**: Create and edit Jinja2 templates with syntax highlighting
- **Device Context Loader**: Import device context from Apstra, file upload, or example data
- **Property Set Integration**: Add custom variables via property sets loaded from Apstra or file
- **Real-time Rendering**: Instantly see rendered output as you edit templates
- **Template Reference**: Built-in Jinja2 syntax guide and examples
- **Apstra API Integration**: Connect directly to your Apstra instance
- **Configlet Browser**: View and copy existing configlets from your Apstra instance
- **Export Options**: Download templates and rendered output

## Demo

Live demo @ https://apstra-configlet.streamlit.app/ 

Usage Example

https://github.com/user-attachments/assets/15cb1b29-de08-4359-b7d3-fb70e2577370


## Installation

### Using Docker (Recommended)

The application is available as a Docker image:

```bash
docker run -p 8501:8501 iamjarvs/apstraconfigletbuilder:latest
```

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/iamjarvs/apstraconfigletbuilder.git
   cd apstraconfigletbuilder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app/main.py
   ```
   
### Access

Access the UI at:
- Local URL: http://localhost:8501
- Network URL: http://<your_ip>:8501

## Usage

### 1. Connect to Apstra

Enter your Apstra server details in the sidebar:
- IP/URL: Your Apstra server address
- Username and Password: Your Apstra credentials
- Click "Login" to connect

### 2. Provide Context Data

You can provide device context data in several ways:
- Load directly from a connected Apstra instance
- Upload a JSON file exported from Apstra
- Paste JSON text
- Use the provided example data

### 3. Add Property Set (Optional)

Property sets allow you to extend the template context with custom variables:
- Load from Apstra
- Upload from JSON or YAML files
- Paste JSON or YAML text
- Use the example property set

### 4. Create Template

Use the Jinja2 template editor to write your configuration template:
- Syntax highlighting helps identify errors
- Use the Jinja2 reference tab for syntax examples
- Browse existing configlets from Apstra for inspiration

### 5. View Rendered Output

The rendered output is displayed in real-time as you edit:
- See exactly how your template will be rendered
- Copy the result to the clipboard
- Download the template or rendered output

## Technical Details

- Built with Python and Streamlit
- Communicates with Apstra API for device context, property sets, and configlets
- Uses Jinja2 template engine for rendering
- Supports JSON and YAML property sets
- Runs in Docker for easy deployment

## Project Structure

```
apstra-configlet-builder/
├── app/                   # Main application code
│   ├── __init__.py
│   ├── main.py            # Application entry point
│   ├── ui/                # Streamlit UI components
│   │   ├── __init__.py
│   │   ├── sidebar.py     # Authentication and navigation
│   │   ├── context_input.py  # Device context input
│   │   ├── property_input.py # Property set input
│   │   ├── template_input.py # Template editor
│   │   ├── render_output.py  # Rendered output display
│   │   └── api_actions.py    # Additional API operations
│   └── utils/             # Utility functions
│       ├── __init__.py
│       ├── api/           # API communication
│       ├── config/        # Configuration utilities
│       ├── data/          # Data processing
│       └── ui/            # UI helper components
├── tests/                 # Test suite
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Running Tests

To run the test suite:

```bash
python -m unittest tests.test_foundation
python -m unittest tests.test_apstra_client
python -m unittest tests.test_template_engine
```

Or run all tests:

```bash
python run_all_tests.py
```

## Contact

- **GitHub Repository**: [https://github.com/iamjarvs/apstraconfigletbuilder](https://github.com/iamjarvs/apstraconfigletbuilder)
- **Author**: Adam Jarvis
