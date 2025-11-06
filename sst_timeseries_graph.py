"""
SST Time Series Graph Generator

Generates a visual time series graph of SST temperature and anomaly data
from 1981-2025 for a specific location.

Usage:
    python -m scripts.sst_timeseries_graph
    python -m scripts.sst_timeseries_graph --lat 38.13 --lon 4.13
    python -m scripts.sst_timeseries_graph --output sst_graph.png
"""

import sys
import argparse
import logging
from datetime import datetime
from typing import List, Tuple, Optional
import time

import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# API Configuration
API_BASE_URL = "https://api.deepearth.digital"
API_ENDPOINT = "/api/sst/point"
API_KEY = "sst_83fd13d1b4f67420ebd3f29423cbb94bf96afcfe737b61ac47d84f7b29c6ac3f"

# Default location (Mediterranean)
DEFAULT_LAT = 38.13
DEFAULT_LON = 4.13


def fetch_sst_data(
    lat: float,
    lon: float,
    data_type: str,
    date: str,
    api_key: str,
    base_url: str = API_BASE_URL,
    endpoint: str = API_ENDPOINT
) -> Optional[float]:
    """
    Fetch SST data for a single point and date.
    
    Args:
        lat: Latitude
        lon: Longitude
        data_type: 'mean' or 'anomaly'
        date: Date in YYYY-MM-DD format
        api_key: API key for authentication
        base_url: Base URL for the API
        endpoint: API endpoint path
        
    Returns:
        Temperature or anomaly value, or None if request failed
    """
    params = {
        "lat": lat,
        "lon": lon,
        "data_type": data_type,
        "date": date,
        "data_source": "timeseries-graph",
        "zoom_level": 5,
        "max_points": 4000,
        "radius": 2.0
    }
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{base_url}{endpoint}",
            params=params,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                data_obj = data.get('data', {})
                if data_type == 'mean':
                    return data_obj.get('temperature')
                else:  # anomaly
                    return data_obj.get('anomaly')
            else:
                logger.warning(f"API returned non-success status for {date} ({data_type}): {data.get('detail', 'Unknown error')}")
        else:
            logger.warning(f"API request failed for {date} ({data_type}): HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request exception for {date} ({data_type}): {e}")
    except Exception as e:
        logger.warning(f"Unexpected error for {date} ({data_type}): {e}")
    
    return None


def generate_monthly_dates(start_year: int, end_year: int) -> List[str]:
    """
    Generate list of dates (first of each month) from start_year to end_year.
    
    Args:
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)
        
    Returns:
        List of date strings in YYYY-MM-DD format
    """
    dates = []
    current_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        # Move to first of next month
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)
    
    return dates


def collect_timeseries_data(
    lat: float,
    lon: float,
    start_year: int,
    end_year: int,
    api_key: str,
    delay: float = 0.1
) -> Tuple[List[datetime], List[Optional[float]], List[Optional[float]]]:
    """
    Collect SST temperature and anomaly data for the specified date range.
    
    Args:
        lat: Latitude
        lon: Longitude
        start_year: Starting year
        end_year: Ending year
        api_key: API key
        delay: Delay between API calls in seconds
        
    Returns:
        Tuple of (dates, temperatures, anomalies)
    """
    dates_str = generate_monthly_dates(start_year, end_year)
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates_str]
    
    temperatures = []
    anomalies = []
    
    total = len(dates_str)
    logger.info(f"Collecting data for {total} monthly samples from {start_year} to {end_year}...")
    
    for i, date_str in enumerate(dates_str):
        # Show progress
        if (i + 1) % 12 == 0 or i == 0:
            logger.info(f"Progress: {i + 1}/{total} ({100 * (i + 1) / total:.1f}%)")
        
        # Fetch mean (temperature)
        temp = fetch_sst_data(lat, lon, 'mean', date_str, api_key)
        temperatures.append(temp)
        time.sleep(delay)  # Small delay to avoid rate limiting
        
        # Fetch anomaly
        anom = fetch_sst_data(lat, lon, 'anomaly', date_str, api_key)
        anomalies.append(anom)
        time.sleep(delay)  # Small delay to avoid rate limiting
    
    logger.info(f"Data collection complete. Retrieved {sum(1 for t in temperatures if t is not None)} temperature values and {sum(1 for a in anomalies if a is not None)} anomaly values.")
    
    return dates, temperatures, anomalies


def create_graph(
    dates: List[datetime],
    temperatures: List[Optional[float]],
    anomalies: List[Optional[float]],
    lat: float,
    lon: float,
    output_file: str = "sst_timeseries.png"
) -> None:
    """
    Create and save a time series graph showing both temperature and anomaly.
    
    Args:
        dates: List of datetime objects
        temperatures: List of temperature values (can contain None)
        anomalies: List of anomaly values (can contain None)
        lat: Latitude for title
        lon: Longitude for title
        output_file: Output filename
    """
    # Filter out None values for plotting
    temp_dates = [d for d, t in zip(dates, temperatures) if t is not None]
    temp_values = [t for t in temperatures if t is not None]
    
    anom_dates = [d for d, a in zip(dates, anomalies) if a is not None]
    anom_values = [a for a in anomalies if a is not None]
    
    # Create figure with dual y-axis
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # Plot temperature on left y-axis
    color1 = 'tab:blue'
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('SST Temperature (°C)', color=color1, fontsize=12)
    line1 = ax1.plot(temp_dates, temp_values, color=color1, linewidth=1.5, label='Temperature', alpha=0.8)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)
    
    # Plot anomaly on right y-axis
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('SST Anomaly (°C)', color=color2, fontsize=12)
    line2 = ax2.plot(anom_dates, anom_values, color=color2, linewidth=1.5, label='Anomaly', alpha=0.8)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Format x-axis dates
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_minor_locator(mdates.MonthLocator((1, 7)))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Add title
    plt.title(
        f'SST Time Series: Temperature and Anomaly\n'
        f'Location: {lat}°N, {lon}°E (1981-2025)',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    
    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=10)
    
    # Adjust layout
    fig.tight_layout()
    
    # Save figure
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"Graph saved to {output_file}")
    
    # Optionally display
    plt.show()


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate SST time series graph from API data"
    )
    parser.add_argument(
        '--lat',
        type=float,
        default=DEFAULT_LAT,
        help=f'Latitude (default: {DEFAULT_LAT})'
    )
    parser.add_argument(
        '--lon',
        type=float,
        default=DEFAULT_LON,
        help=f'Longitude (default: {DEFAULT_LON})'
    )
    parser.add_argument(
        '--start-year',
        type=int,
        default=1981,
        help='Start year (default: 1981)'
    )
    parser.add_argument(
        '--end-year',
        type=int,
        default=2025,
        help='End year (default: 2025)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='sst_timeseries.png',
        help='Output filename (default: sst_timeseries.png)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        default=API_KEY,
        help='API key (default: uses hardcoded key)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=0.1,
        help='Delay between API calls in seconds (default: 0.1)'
    )
    
    args = parser.parse_args(argv)
    
    try:
        # Collect data
        dates, temperatures, anomalies = collect_timeseries_data(
            args.lat,
            args.lon,
            args.start_year,
            args.end_year,
            args.api_key,
            args.delay
        )
        
        # Create graph
        create_graph(
            dates,
            temperatures,
            anomalies,
            args.lat,
            args.lon,
            args.output
        )
        
        logger.info("Script completed successfully")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

