import argparse
import climakitae as ck 
from climakitae.core.data_interface import (
    get_data_options, 
    get_subsetting_options, 
    get_data
)

def process_precipitation_data(county, simulation_name, warming_level, output_path):
    """
    Process precipitation data for a specific county, simulation, and warming level.
    
    Args:
        county (str): County name to fetch data for
        simulation_name (str): Name of the simulation to select
        warming_level (float): Warming level to select
        output_path (str): Path where to save the output NetCDF file
    
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
    
    return precip_annual


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
    return parser.parse_args()

# Main entry point
if __name__ == "__main__":
    args = parse_arguments()
    
    # Process data with command line arguments
    processed_data = process_precipitation_data(
        county=args.county,
        simulation_name=args.simulation,
        warming_level=args.warming_level,
        output_path=args.output
    )
    
    print(f"Processing complete. Data saved to {args.output}")