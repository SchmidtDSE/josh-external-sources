import argparse
import climakitae as ck 
import numpy as np
import pandas as pd
import os
from climakitae.core.data_interface import (
    get_data_options, 
    get_subsetting_options, 
    get_data
)

def process_precipitation_data(county, simulation_name, warming_level, output_path, generate_test_points=False, bbox=None):
    """
    Process precipitation data for a specific county, simulation, and warming level.
    
    Args:
        county (str): County name to fetch data for
        simulation_name (str): Name of the simulation to select
        warming_level (float): Warming level to select
        output_path (str): Path where to save the output NetCDF file
        generate_test_points (bool): Whether to generate test points in CSV format
        bbox (tuple): Optional bounding box (min_lon, max_lon, min_lat, max_lat) to restrict test points
    
    Returns:
        The processed xarray dataset
    """
    print(f"Downloading total precipitation data for {county}...")
    
    # Get the raw data
    precip_data = get_data(
        variable = "Precipitation (total)", 
        downscaling_method = "Statistical", 
        resolution = "3 km", 
        timescale = "monthly", 
        cached_area = county, 
        approach = "Warming Level"
    )
    
    # Select the specific simulation
    precip_data_sim = precip_data.sel(simulation=simulation_name)
    
    # Select specific warming level
    precip_data_wl = precip_data_sim.sel(warming_level=warming_level)
    
    # Get the centered year value
    centered_year = precip_data_wl.centered_year.item()
    print(f"Centered year: {centered_year}")
    
    # Calculate calendar years from time_delta values
    # time_delta is in months, from -180 to 179 (30 years × 12 months)
    # First convert time_delta to year offset
    year_offset = precip_data_wl.time_delta / 12
    # Round down to get the year number relative to centered year
    year_offset = year_offset.astype(int)
    # Calculate actual calendar years
    calendar_years = centered_year + year_offset
    
    # Assign calendar years as a new coordinate
    precip_data_wl = precip_data_wl.assign_coords(calendar_year=("time_delta", calendar_years.values))
    
    # Now we can group by calendar_year and sum
    precip_annual = precip_data_wl.groupby("calendar_year").sum(dim="time_delta").astype(float)
    
    # Add metadata
    precip_annual.attrs['centered_year'] = centered_year
    precip_annual.attrs['warming_level'] = warming_level
    precip_annual.attrs['simulation'] = simulation_name
    
    # Export the result
    ck.export(precip_annual, filename=output_path, format="NetCDF")
    
    # Generate test points if requested
    if generate_test_points:
        generate_test_points_csv(precip_annual, output_path, bbox)
    
    return precip_annual


def generate_test_points_csv(precip_annual, output_path, bbox=None):
    """
    Generate approximately 10 test points from the precipitation dataset
    and save them as a CSV file for testing purposes.
    
    Args:
        precip_annual: xarray DataArray with precipitation data
        output_path: Base path for saving the CSV file
        bbox (tuple): Optional bounding box (min_lon, max_lon, min_lat, max_lat) to restrict test points
    """
    print("Generating test points for validation...")
    
    # Get available calendar years, latitudes, and longitudes
    calendar_years = precip_annual.calendar_year.values
    lats = precip_annual.lat.values
    lons = precip_annual.lon.values
    
    # Filter lats and lons if bounding box is provided
    if bbox:
        min_lon, max_lon, min_lat, max_lat = bbox
        print(f"Restricting test points to bounding box: lon({min_lon}, {max_lon}), lat({min_lat}, {max_lat})")
        lons = lons[(lons >= min_lon) & (lons <= max_lon)]
        lats = lats[(lats >= min_lat) & (lats <= max_lat)]
        
        # Exit if no points in bounding box
        if len(lons) == 0 or len(lats) == 0:
            print("Warning: No points found within the specified bounding box. Cannot generate test points.")
            return
    
    # Randomly select ~3 years
    if len(calendar_years) > 3:
        selected_years = np.random.choice(calendar_years, size=3, replace=False)
    else:
        selected_years = calendar_years
    
    # Select ~4 random spatial points
    num_lat_points = min(2, len(lats))
    num_lon_points = min(2, len(lons))
    
    selected_lats = np.random.choice(lats, size=num_lat_points, replace=False)
    selected_lons = np.random.choice(lons, size=num_lon_points, replace=False)
    
    # Create test points
    test_points = []
    for year in selected_years:
        for lat in selected_lats:
            for lon in selected_lons:
                # Get precipitation value for this point
                value = float(precip_annual.sel(calendar_year=year, lat=lat, lon=lon, method='nearest').values)
                test_points.append({
                    'calendar_year': int(year),
                    'lat': float(lat),
                    'lon': float(lon),
                    'precipitation': value
                })
    
    # Convert to DataFrame and save as CSV
    test_df = pd.DataFrame(test_points)
    
    # Create CSV filename based on the NetCDF output path
    csv_path = os.path.splitext(output_path)[0] + '_test_points.csv'
    test_df.to_csv(csv_path, index=False)
    print(f"Generated {len(test_points)} test points and saved to {csv_path}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process precipitation data from Cal-Adapt.')
    parser.add_argument('--county', type=str, required=True,
                        help='County name to fetch data for (e.g., "Riverside County")')
    parser.add_argument('--simulation', type=str, required=True,
                        help='Name of the simulation to select')
    parser.add_argument('--warming-level', type=float, required=True,
                        help='Warming level to select (e.g., 2.0)')
    parser.add_argument('--output', type=str, required=True,
                        help='Path where to save the output NetCDF file')
    parser.add_argument('--generate-test-points', action='store_true',
                        help='Generate test points and save as CSV for validation')
    parser.add_argument('--bbox', type=float, nargs=4, metavar=('MIN_LON', 'MAX_LON', 'MIN_LAT', 'MAX_LAT'),
                        help='Bounding box to restrict test points (min_lon max_lon min_lat max_lat)')
    return parser.parse_args()

# Main entry point
if __name__ == "__main__":
    args = parse_arguments()
    
    # Process data with command line arguments
    processed_data = process_precipitation_data(
        county=args.county,
        simulation_name=args.simulation,
        warming_level=args.warming_level,
        output_path=args.output,
        generate_test_points=args.generate_test_points,
        bbox=args.bbox
    )
    
    print(f"Processing complete. Data saved to {args.output}")