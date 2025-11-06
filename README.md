# DeepEarth Digital Earth Data API - Public Repository

This repository contains public tools and examples for working with the DeepEarth Digital Earth Data API.

## Overview

The DeepEarth Digital Earth Data API provides access to various Earth observation datasets, including Sea Surface Temperature (SST) data from NOAA's Optimum Interpolation Sea Surface Temperature (OISST) dataset.

## Contents

### SST Time Series Graph Generator

A Python script to generate visual time series graphs of Sea Surface Temperature (SST) data from the DeepEarth Digital Earth Data API.

**Files:**
- `sst_timeseries_graph.py` - Main Python script
- `SST_TIMESERIES_GRAPH.md` - Detailed documentation

**Quick Start:**
```bash
# Install dependencies
pip install requests matplotlib

# Run the script
python sst_timeseries_graph.py
```

For detailed usage instructions, see [SST_TIMESERIES_GRAPH.md](SST_TIMESERIES_GRAPH.md).

## API Information

- **Base URL**: `https://api.deepearth.digital`
- **Authentication**: X-API-Key header required
- **Documentation**: See individual script documentation files

## Requirements

- Python 3.7+
- `requests` - HTTP library for API calls
- `matplotlib` - For graph generation

## Installation

```bash
pip install requests matplotlib
```

## Contributing

This is a public repository for DeepEarth Digital's Earth Data API tools and examples. Contributions and suggestions are welcome.

## License

[Add your license information here]

## Support

For API access and support, visit [DeepEarth Digital](https://deepearth.digital)

