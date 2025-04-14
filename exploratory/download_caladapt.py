import climakitae as ck 
from climakitae.core.data_interface import (
    get_data_options, 
    get_subsetting_options, 
    get_data
)

## Total Prcipitation for Riverside County
print("Downloading total precipitation data for Riverside County...")

precip_riverside = get_data(
    variable = "Precipitation (total)", 
    downscaling_method = "Statistical", 
    resolution = "3 km", 
    timescale = "monthly", 
    cached_area = "Riverside County", 
    approach = "Warming Level"
)

precip_riverside_annual = precip_riverside.sel(warming_level=2).sum(dim='time_delta').astype(float)

ck.export(precip_riverside_annual, filename="precip_riverside_annual", format="NetCDF") 

## Total Precipitation for San Bernardino County
print("Downloading total precipitation data for San Bernardino County...")

precip_sanbernardino = get_data(
    variable = "Precipitation (total)", 
    downscaling_method = "Statistical", 
    resolution = "3 km", 
    timescale = "monthly", 
    cached_area = "San Bernardino County", 
    approach = "Warming Level"
)

precip_sanbernardino_annual = precip_sanbernardino.sel(warming_level=2).sum(dim='time_delta').astype(float)

ck.export(precip_sanbernardino_annual, filename="precip_sanbernardino_annual", format="NetCDF")

