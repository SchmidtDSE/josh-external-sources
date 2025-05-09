import argparse
import os
from process_caladapt import process_climate_data

def main():
    # Define common parameters
    SIMULATION = "LOCA2_ACCESS-CM2_r2i1p1f1_historical+ssp245"
    WARMING_LEVEL = 2.0
    
    # Define combinations to process
    combinations = [
        ## Sum of precipitation
        ("Riverside County", "Precipitation (total)", "sum", "precip_riverside_annual"),
        ("San Bernardino County", "Precipitation (total)", "sum", "precip_sanbernardino_annual"),
        ("Tulare County", "Precipitation (total)", "sum", "precip_tulare_annual"),

        ## Maximum temperature of maximums
        ("Riverside County", "Maximum air temperature at 2m", "max", "maxtemp_riverside_annual"),
        ("San Bernardino County", "Maximum air temperature at 2m", "max", "maxtemp_sanbernardino_annual"),
        ("Tulare County", "Maximum air temperature at 2m", "max", "maxtemp_tulare_annual"),

        ## Minimum temperature of mininums
        ("Riverside County", "Minimum air temperature at 2m", "min", "mintemp_riverside_annual"),
        ("San Bernardino County", "Minimum air temperature at 2m", "min", "mintemp_sanbernardino_annual"),
        ("Tulare County", "Minimum air temperature at 2m", "min", "mintemp_tulare_annual"),

        ## Mean temperature (of maximum, since we don't have mean directly)
        ("Riverside County", "Maximum air temperature at 2m", "mean", "meantemp_riverside_annual"),
        ("San Bernardino County", "Maximum air temperature at 2m", "mean", "meantemp_sanbernardino_annual"),
        ("Tulare County", "Maximum air temperature at 2m", "mean", "meantemp_tulare_annual"),
    ]
    
    # Process all combinations
    for county, variable, aggregation, output_base in combinations:
        output_path = f"{output_base}.nc"
        print(f"Processing {variable} for {county}...")
        
        process_climate_data(
            county=county,
            variable_name=variable,
            simulation_name=SIMULATION,
            warming_level=WARMING_LEVEL,
            aggregation_method=aggregation,
            output_path=output_path,
            generate_test_points=True,
        )
        
        print(f"Data saved to {output_path}")

if __name__ == "__main__":
    main()