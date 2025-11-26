import xarray as xr

from loading_helpers import (
    join_paths,
    join_paths_areacell,
    BASE_PATH,
    FILE_PATH,
    AREACELL_PATH,
)

TROPICAL_HALFWIDTH = 23.4 # upper latitude in degrees by which we define the tropics. Default is tropic of Cancer
MM_PER_H_TO_MM_PER_D_CONVERSION_FACTOR = 86400. 

def get_annual_max(ds, var_name):
    """Returns a ds whose time-slices give maps of a variable's max over each year"""
    return ds[var_name].groupby("time.year").max(dim="time")

def get_mean_annual_max(ds, var_name):
    """Returns a ds which is a map of the temporal mean of the yearly maxes of a given var"""
    return get_annual_max(ds, var_name).mean(dim="year")

def get_ds(
           var_name,
           runid,
           experiment_name,
           year_range,
           base_path = BASE_PATH,
           file_path = FILE_PATH,
          ):
    return xr.open_mfdataset(
                            join_paths(
                                var_name, 
                                year_range, 
                                runid = runid, 
                                experiment_name = experiment_name,
                                base_path = base_path,
                                file_path = file_path,
                            ),
                            decode_times = xr.coders.CFDatetimeCoder(use_cftime=True),
                            data_vars = "all", 
    )

# TODO: adapt get_ep_info so that it works from a ds instead. 
# Then wrap this to get_ep_info where it takes in a runid and experiment name. 
# The purpose of this is to try and do as little experiment loading as possible. 
# In general worry more about load-time efficiency in this code. 

def get_ep_info(
           runid,
           experiment_name,
           year_range,
           base_path = BASE_PATH,
           file_path = FILE_PATH,
          ):
    """Returns all extreme precipitation DAs we need from a given experiment in a given year_range"""
    conv = MM_PER_H_TO_MM_PER_D_CONVERSION_FACTOR

    "First assemble those values we can just read from the data (total and convective)"
    base_das = [
        conv * get_mean_annual_max(
            get_ds(
                    var_name,
                    runid, 
                    experiment_name,
                    year_range,
                    base_path = base_path,
                    file_path = file_path,
            ),
            var_name,
    ) for var_name in ["pr", "prc"] ]

    "Conclude by appending the resolved precip"
    base_das.append(base_das[0] - base_das[1])
    
    return base_das

def get_ds_areacell(
                    runid, 
                    experiment_name,
                    base_path = BASE_PATH,
                    areacell_path = AREACELL_PATH,
                   ):  
    """Get a ds of areacells for a given experiment"""
    return xr.open_dataset(
        join_paths_areacell(
            runid, 
            experiment_name,
            base_path = base_path,
            areacell_path = areacell_path,
        )
    )

def get_tropical_areamean(da, ds_areacell, tropical_halfwidth = TROPICAL_HALFWIDTH): 
    """
    Compute the spatial mean over the tropics of a given DA
    
    """
    tropical_slice = slice(-tropical_halfwidth, tropical_halfwidth)

    # Restrict DA to the tropics
    da_tropical = da.sel(lat = tropical_slice)

    # Figure out total area covered by the tropics
    tropical_area = ds_areacell.areacella.sel(lat = tropical_slice).sum(dim=['lon', 'lat'])    
    
    return((ds_areacell.areacella * da_tropical).sum(dim=['lon', 'lat']) / tropical_area).values  

def get_tropical_ep_areamean_from_experiment(
                 runid, 
                 experiment_name,
                 year_range,
                 tropical_halfwidth = TROPICAL_HALFWIDTH,
                ):
    """Get the required means (total, convective, resolved) from a given run"""
    ds_areacell = get_ds_areacell(runid, experiment_name)
    return [
        get_tropical_areamean(
            da, 
            ds_areacell,
            tropical_halfwidth = tropical_halfwidth,
        ) for da in get_ep_info(runid, experiment_name, year_range)
]

def get_annual_mean_time_series(
                                var_name, 
                                runid, 
                                experiment_name,
                                year_range,
                                base_path = BASE_PATH,
                                file_path = FILE_PATH,
                                areacell_path = AREACELL_PATH,
):
    """Returns a time series of the annually averaged, 
    globally area-averaged (scalar) var_name in question"""

    ds = get_ds(
           var_name,
           runid,
           experiment_name,
           year_range,
           base_path = base_path,
           file_path = file_path,
    )
    
    ds_areacell = get_ds_areacell(runid, experiment_name, base_path = base_path, areacell_path = areacell_path)
    global_area = ds_areacell.areacella.sum(dim=['lon', 'lat'])         
    
    spatial_mean = (ds_areacell.areacella * ds[var_name]).sum(dim=['lon', 'lat']) / global_area # Properly area weighted mean of rate of flux
    return spatial_mean.groupby('time.year').mean(dim='time')