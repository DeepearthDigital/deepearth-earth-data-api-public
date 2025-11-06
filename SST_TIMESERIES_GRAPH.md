# SST Time Series Graph Generator

A Python script to generate visual time series graphs of Sea Surface Temperature (SST) data from the DeepEarth Digital Earth Data API.

## Overview

This script queries the DeepEarth Digital API to collect SST temperature (mean) and anomaly data for a specific location over a date range (default: 1981-2025), then generates a dual-axis time series graph showing both datasets.

## Features

- **Monthly Sampling**: Automatically samples the first day of each month to balance data coverage with API call efficiency
- **Dual Data Types**: Fetches both temperature (mean) and anomaly data simultaneously
- **Dual-Axis Visualisation**: Creates a graph with temperature on the left axis and anomaly on the right axis
- **Error Handling**: Gracefully handles API errors and missing data points
- **Progress Tracking**: Shows progress during data collection
- **Customisable**: Command-line options for location, date range, and output settings

## Prerequisites

### Required Python Packages

- `requests` - Already included in project requirements
- `matplotlib` - Must be installed separately

### Installation

```bash
# Install matplotlib if not already installed
pip install matplotlib
```

## Usage

### Basic Usage

Generate a graph for the default location (38.13°N, 4.13°E - Mediterranean):

```bash
python -m scripts.sst_timeseries_graph
```

### Custom Location

Specify a different latitude and longitude:

```bash
python -m scripts.sst_timeseries_graph --lat 40.0 --lon 5.0
```

### Custom Output File

Save the graph with a custom filename:

```bash
python -m scripts.sst_timeseries_graph --output my_sst_graph.png
```

### Custom Date Range

Specify a different year range:

```bash
python -m scripts.sst_timeseries_graph --start-year 2000 --end-year 2020
```

### Adjust API Call Rate

If you encounter rate limiting, increase the delay between API calls:

```bash
python -m scripts.sst_timeseries_graph --delay 0.5
```

### Custom API Key

Use a different API key (if you have one):

```bash
python -m scripts.sst_timeseries_graph --api-key your_api_key_here
```

## Command-Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--lat` | float | 38.13 | Latitude in degrees (-90 to 90) |
| `--lon` | float | 4.13 | Longitude in degrees (-180 to 180) |
| `--start-year` | int | 1981 | Starting year for data collection |
| `--end-year` | int | 2025 | Ending year for data collection |
| `--output` | string | `sst_timeseries.png` | Output filename for the graph |
| `--api-key` | string | (hardcoded) | API key for authentication |
| `--delay` | float | 0.1 | Delay in seconds between API calls |

## Output

The script generates a PNG image file with:

- **X-axis**: Time (dates from start year to end year)
- **Left Y-axis**: SST Temperature in °C (blue line)
- **Right Y-axis**: SST Anomaly in °C (red line)
- **Title**: Includes location coordinates and date range
- **Legend**: Identifies both data series
- **Grid**: Light grid lines for easier reading

The graph is saved at 300 DPI for high-quality output suitable for presentations or publications.

## Example Output

The generated graph will show:
- Long-term temperature trends (blue line)
- Temperature anomalies relative to the baseline (red line)
- Seasonal patterns and interannual variability
- Any notable warming or cooling trends over the period

## Data Collection Details

- **Sampling Frequency**: First day of each month
- **Total API Calls**: 2 × number of months (one for temperature, one for anomaly)
- **Example**: For 1981-2025 (45 years), approximately 540 API calls per run
- **Estimated Runtime**: ~1-2 minutes with default 0.1s delay (depends on API response time)

## Troubleshooting

### API Rate Limiting

If you receive HTTP 429 (Too Many Requests) errors:

1. Increase the delay between calls:
   ```bash
   python -m scripts.sst_timeseries_graph --delay 0.5
   ```

2. Reduce the date range to fewer years

### Missing Data Points

The script handles missing data gracefully:
- Missing points are skipped (not plotted)
- Warnings are logged for failed API calls
- The graph will still be generated with available data

### Authentication Errors

If you receive authentication errors:
- Verify your API key is correct
- Check that the API key has access to the SST endpoints
- Ensure the API key format is correct (starts with `sst_`)

### Matplotlib Display Issues

If the graph doesn't display:
- The file is still saved to disk even if display fails
- Check that `matplotlib` is properly installed
- On headless systems, the script will save the file without displaying

### Network Timeouts

If requests timeout:
- Check your internet connection
- The script uses a 30-second timeout per request
- Failed requests are logged and skipped

## Performance Tips

1. **Reduce Date Range**: For faster execution, use a smaller date range
2. **Adjust Delay**: Lower delays (0.05s) are faster but may trigger rate limits
3. **Run During Off-Peak**: API response times may vary based on server load

## API Information

- **Base URL**: `https://api.deepearth.digital`
- **Endpoint**: `/api/sst/point`
- **Authentication**: X-API-Key header
- **Data Source**: NOAA Optimum Interpolation Sea Surface Temperature (OISST)

## Notes

- The script uses monthly sampling to balance data coverage with API efficiency
- Daily sampling would require ~32,000 API calls for 1981-2025, which is impractical
- Monthly sampling provides good temporal resolution for trend analysis
- The anomaly data shows deviation from the long-term mean baseline

## Example Workflow

```bash
# 1. Generate graph for Mediterranean location
python -m scripts.sst_timeseries_graph --lat 38.13 --lon 4.13 --output med_sst.png

# 2. Generate graph for a different location (e.g., North Atlantic)
python -m scripts.sst_timeseries_graph --lat 50.0 --lon -10.0 --output north_atlantic_sst.png

# 3. Generate graph for recent years only
python -m scripts.sst_timeseries_graph --start-year 2010 --end-year 2025 --output recent_sst.png
```

## Support

For issues or questions:
- Check the API documentation
- Verify your API key is valid
- Review the error messages in the console output
- Ensure all dependencies are installed correctly

