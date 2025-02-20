# Aviation Weather Development Environment Setup Guide

## Overview
This guide will help you set up your development environment for the Aviation Weather project, a Python utility for retrieving aviation weather information. The project uses Python and requires several dependencies for XML processing and HTTP requests.

## Prerequisites

### System Requirements
- Python 3.x
- pip (Python package installer)
- Git

### Required Software Installation

1. **Install Python**
   - For macOS:
     ```bash
     brew install python
     ```
   - Verify installation:
     ```bash
     python3 --version
     ```

2. **Install Git** (if not already installed)
   - For macOS:
     ```bash
     brew install git
     ```
   - Verify installation:
     ```bash
     git --version
     ```

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/jpegz/jpegz_aviation_weather.git
cd aviation_weather
```

### 2. Set Up Python Virtual Environment
It's recommended to use a virtual environment to isolate project dependencies:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
The project requires the following Python packages:
- lxml: XML processing
- requests: HTTP client
- xmltodict: XML to dictionary conversion

Install all dependencies using:
```bash
pip install -e .
```

This will install the package in development mode with all required dependencies.

### 4. Installing from a Different Directory
If you want to install the package from a different directory, you can use the full path to the package:

```bash
# Install directly from GitHub
pip install git+https://github.com/jpegz/jpegz_aviation_weather.git

# Or install from a local directory
pip install -e /path/to/aviation_weather
```

Note: When installing from a different directory, make sure you have Git installed if using the GitHub URL method.

### 5. Installing via requirements.txt
You can also include this package in a `requirements.txt` file to install it alongside other dependencies:

```text
# requirements.txt
git+https://github.com/jpegz/jpegz_aviation_weather.git
# Add other dependencies here
requests==2.31.0
```

Then install all requirements with:
```bash
pip install -r requirements.txt
```

This method is particularly useful when managing multiple project dependencies or in automated deployment scenarios.

## Running the Project

### Basic Usage
After installation, you can run the project using the command-line interface:

```bash
python -m aviation_weather [data_source] [stations...] [options]
```

#### Required Arguments
- `data_source`: Type of weather data to retrieve (choices: `metars`, `tafs`)
- `stations`: One or more station codes (e.g., KJFK, KLAX)

#### Optional Arguments
- `--hours-before-now`: Number of hours of history to retrieve (default: 24)
- `--most-recent`, `-r`: Only return the most recent data for each station (default: True)
- `--text`, `-t`: Display results in human-readable text format (default: True)

#### Examples

1. Get current METAR for JFK airport:
```bash
python -m aviation_weather metars KJFK
```

2. Get TAFs for multiple airports:
```bash
python -m aviation_weather tafs KJFK KLAX KBOS
```

3. Get historical METARs for the last 48 hours:
```bash
python -m aviation_weather metars KJFK --hours-before-now 48
```

### Python API Usage
For development or integration into other Python projects, you can import and use the modules directly:

```python
from aviation_weather import tools

# Get METAR data for JFK airport
metar = tools.aviation_weather(
    data_source='metars',
    station='KJFK',
    hours_before_now=24,
    most_recent=True,
    return_readable=True
)
print(metar)

# Get TAF data for multiple stations
taf = tools.aviation_weather(
    data_source='tafs',
    station='KJFK,KLAX',
    hours_before_now=24,
    most_recent=True,
    return_readable=True
)
print(taf)
```

### Output Format
When using the `--text` option or `return_readable=True`, the output includes:
- Station information (ID, latitude, longitude)
- Temperature and dewpoint (in Celsius)
- Wind conditions (direction and speed)
- Visibility (in statute miles)
- Altimeter setting
- Sea level pressure
- Sky conditions
- Flight category
- METAR type
- Station elevation

Example output:
```
Station: KJFK
Latitude: 40.63
Longitude: -73.77
Temperature: 15.0
Dewpoint: 12.0
Wind direction: 180
Wind speed: 10
Visibility: 10.0
Altimeter: 29.92
Pressure: 1013.2
Sky condition: 5000AGL: BKN
Flight category: VFR
Metar Type: METAR
Elevation: 13
```

### API Endpoints
The package uses the aviationweather.gov ADDS (Aviation Digital Data Service) API to retrieve data. The base URL is:
```
https://aviationweather.gov/adds/dataserver_current/httpparam
```

### Development Mode
For development, you can import and use the modules directly:
```python
from aviation_weather import metars, tafs
```

## Project Structure
- `aviation_weather/`: Main package directory
  - `__init__.py`: Package initialization
  - `__main__.py`: Entry point
  - `metars.py`: METAR data handling
  - `tafs.py`: TAF data handling
  - `tools.py`: Utility functions
- `setup.py`: Project configuration and dependencies

## Troubleshooting

### Common Issues and Solutions

1. **Package Installation Failures**
   - **Issue**: `lxml` installation fails
   - **Solution**: Install system-level dependencies first:
     ```bash
     # On macOS
     brew install libxml2 libxslt
     ```

2. **Import Errors**
   - **Issue**: Module not found errors
   - **Solution**: Ensure you're in the correct directory and the virtual environment is activated
   - **Check**: Run `pip list` to verify all dependencies are installed

3. **Permission Issues**
   - **Issue**: Permission denied when installing packages
   - **Solution**: Use `sudo` for system-wide installation (not recommended) or properly set up virtual environment

### Verification Steps
To verify your setup is working correctly:

1. Activate your virtual environment
2. Run Python interpreter:
   ```python
   >>> from aviation_weather import metars
   >>> # If no errors occur, setup is successful
   ```

## Best Practices

1. **Always use virtual environments** to keep project dependencies isolated
2. **Update dependencies regularly** using `pip install -e .`
3. **Keep Python and pip updated** to avoid compatibility issues
4. **Use Git branches** for development work

## Support and Resources

- Project Repository: [GitHub](http://github.com/jpegz/jpegz_aviation_weather)
- Report Issues: Create a new issue on the GitHub repository
- License: MIT

## Maintenance

To keep your development environment up to date:

1. **Update the repository**:
   ```bash
   git pull origin main
   ```

2. **Update dependencies**:
   ```bash
   pip install -e .
   ```

3. **Clean up**:
   ```bash
   # Remove compiled Python files
   find . -type f -name "*.pyc" -delete
   find . -type d -name "__pycache__" -delete
   ```