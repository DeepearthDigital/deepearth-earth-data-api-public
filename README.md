# DeepEarth Digital Earth Data API - Public Repository

This repository contains public tools and examples for working with the DeepEarth Digital Earth Data API.

## Overview

The DeepEarth Digital Earth Data API provides access to various Earth observation datasets, including Sea Surface Temperature (SST) data from NOAA's Optimum Interpolation Sea Surface Temperature (OISST) dataset.

## Contents

### SST Time Series Graph Generator

A Python script to generate visual time series graphs of Sea Surface Temperature (SST) data from the DeepEarth Digital Earth Data API.

**Files:**
- `sst_timeseries/sst_timeseries_graph.py` - Main Python script
- `sst_timeseries/SST_TIMESERIES_GRAPH.md` - Detailed documentation

**Quick Start:**
```bash
# Install dependencies
pip install requests matplotlib

# Run the script
python sst_timeseries/sst_timeseries_graph.py
```

For detailed usage instructions, see [sst_timeseries/SST_TIMESERIES_GRAPH.md](sst_timeseries/SST_TIMESERIES_GRAPH.md).

## API Information

- **Base URL**: `https://api.deepearth.digital`
- **Authentication**: X-API-Key header required
- **Documentation**: See individual script documentation files
- **Data Attribution**: All API responses include embedded data attribution information for proper citation and compliance with data source requirements

## Requirements

- Python 3.7+
- `requests` - HTTP library for API calls
- `matplotlib` - For graph generation
- `python-dotenv` - For loading environment variables from `.env` file (optional but recommended)

## Installation

```bash
# Install dependencies
pip install requests matplotlib python-dotenv
```

## Configuration

### API Key Setup

The script uses an API key for authentication. You can configure it in two ways:

1. **Using a `.env` file (recommended):**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key
   API_KEY=your_api_key_here
   ```

2. **Using environment variable:**
   ```bash
   export API_KEY=your_api_key_here
   ```

3. **Command-line argument:**
   ```bash
   python sst_timeseries/sst_timeseries_graph.py --api-key your_api_key_here
   ```

The script will automatically load the API key from the `.env` file if `python-dotenv` is installed, otherwise it will use the environment variable or the `--api-key` argument.

## Contributing

This is a public repository for DeepEarth Digital's Earth Data API tools and examples. Contributions and suggestions are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Data Attribution

All API responses from the DeepEarth Digital Earth Data API include embedded data attribution information. This ensures proper citation and compliance with data source requirements. When using data from the API, please refer to the attribution information included in each response.

## Support

For API access and support, visit [DeepEarth Digital](https://deepearth.digital)

