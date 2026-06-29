import numpy as np
import xarray as xr

from loading_helpers import (
    join_paths,
    join_paths_areacell,
    BASE_PATH,
    FILE_PATH,
    AREACELL_PATH,
)

LAT_SLICE_HALFWIDTH = 13.
TROPICAL_HALFWIDTH = 23.4  # upper latitude in degrees by which we define the tropics. Default is tropic of Cancer
MM_PER_H_TO_MM_PER_D_CONVERSION_FACTOR = 86400.
GRID_DELTA = 3.


def get_annual_max(ds, var_name=None):
    """Returns a da or ds whose time-slices give maps of a variable's max over each year"""

    # if the var_name has already been peeled off, just catch this
    if var_name is None:
        return ds.groupby("time.year").max(dim="time")

    return ds[var_name].groupby("time.year").max(dim="time")


def get_mean_annual_max(ds, var_name):
    """Returns a ds which is a map of the temporal mean of the yearly maxes of a given var"""
    return get_annual_max(ds, var_name).mean(dim="year")


def get_ds(
        var_name,
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
):
    return xr.open_mfdataset(
        join_paths(
            var_name,
            year_range,
            runid=runid,
            experiment_name=experiment_name,
            base_path=base_path,
            file_path=file_path,
        ),
        decode_times=xr.coders.CFDatetimeCoder(use_cftime=True),
        data_vars="all",
    )


# TODO: adapt get_ep_info so that it works from a ds instead.
# Then wrap this to get_ep_info where it takes in a runid and experiment name. 
# The purpose of this is to try and do as little experiment loading as possible. 
# In general worry more about load-time efficiency in this code.

def get_day_of_extreme(da, year):
    """
    Return a map whose values are the dates where the DataArray "da"
    achieved its maximum in a given year.
    """
    return select_fixed_year(da, year).idxmax(dim="time")


def to_yearly_dataarray(da, da_processed, year_range):
    """
    Helper function for turning a list of DataArrays (where the list index is to be understood
    as a year index) into a new DataArray with a time dimension
    """
    return xr.DataArray(
        data=da_processed,
        dims=["time", "lat", "lon"],
        coords=dict(
            lon=da.lon.to_numpy(),
            lat=da.lat.to_numpy(),
            time=[year for year in year_range],
        ),
    )


def get_ep_info(
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
):
    """Returns all extreme precipitation DAs we need from a given experiment in a given year_range"""
    conv = MM_PER_H_TO_MM_PER_D_CONVERSION_FACTOR

    #First assemble those values we can just read from the data (total and convective)
    da_pr, da_prc = [
        conv * get_ds(
            var_name,
            runid,
            experiment_name,
            year_range,
            base_path=base_path,
            file_path=file_path,
        )[var_name]
        for var_name in ["pr", "prc"]
    ]

    # Now we pull out the extremes
    da_epr_as_temporal_list = []
    da_eprc_as_temporal_list = []

    for year in year_range:
        day_of_epe = get_day_of_extreme(da_pr, year)

        da_epr_current_year = da_pr.sel(time=day_of_epe)
        da_eprc_current_year = da_prc.sel(time=day_of_epe)

        da_epr_as_temporal_list.append(da_epr_current_year)
        da_eprc_as_temporal_list.append(da_eprc_current_year)

    da_epr = to_yearly_dataarray(da_pr, da_epr_as_temporal_list, year_range)
    da_eprc = to_yearly_dataarray(da_prc, da_eprc_as_temporal_list, year_range)

    # Conclude by getting the resolved precip
    da_eprr = da_epr - da_eprc

    return [da_epr, da_eprc, da_eprr]


def get_mean_ep_info(
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
):
    ep_info = get_ep_info(
        runid,
        experiment_name,
        year_range,
        base_path=base_path,
        file_path=file_path,
    )

    return [da.mean(dim="time") for da in ep_info]


def get_mean_info(
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
):
    """Returns all mean precipitation DAs we need from a given experiment in a given year_range"""
    conv = MM_PER_H_TO_MM_PER_D_CONVERSION_FACTOR

    "First assemble those values we can just read from the data (total and convective)"
    base_das = [
        conv *
        get_ds(
            var_name,
            runid,
            experiment_name,
            year_range,
            base_path=base_path,
            file_path=file_path,
        ).mean(dim="time")[var_name]
        for var_name in ["pr", "prc"]
    ]

    "Conclude by appending the resolved precip"
    base_das.append(base_das[0] - base_das[1])

    return base_das


def get_ds_areacell(
        runid,
        experiment_name,
        base_path=BASE_PATH,
        areacell_path=AREACELL_PATH,
):
    """Get a ds of areacells for a given experiment"""
    return xr.open_dataset(
        join_paths_areacell(
            runid,
            experiment_name,
            base_path=base_path,
            areacell_path=areacell_path,
        )
    )


def get_tropical_slice(tropical_halfwidth=TROPICAL_HALFWIDTH):
    """
    Returns a tropical slice of latitudes
    """
    return slice(-tropical_halfwidth, tropical_halfwidth)


def select_tropical_slice(da, tropical_halfwidth=TROPICAL_HALFWIDTH):
    """
    Returns a slice of a given array consisting only of tropical latitudes

    TODO: customization for different seasons? 
    """
    tropical_slice = get_tropical_slice(tropical_halfwidth=tropical_halfwidth)

    return da.sel(lat = tropical_slice)


def get_tropical_areamean(da, ds_areacell, tropical_halfwidth=TROPICAL_HALFWIDTH):
    """
    Compute the spatial mean over the tropics of a given DA
    """
    da_tropical = select_tropical_slice(da, tropical_halfwidth=tropical_halfwidth)

    # Figure out total area covered by the tropics
    tropical_area = ds_areacell.areacella.sel(
        lat=get_tropical_slice(tropical_halfwidth=tropical_halfwidth)
    ).sum(
        dim=['lon', 'lat']
    )

    return ((ds_areacell.areacella * da_tropical).sum(dim=['lon', 'lat']) / tropical_area).values


def get_tropical_ep_areamean_from_experiment(
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
        areacell_path=AREACELL_PATH,
        tropical_halfwidth=TROPICAL_HALFWIDTH,
):
    """Get the required means (total, convective, resolved) of *mean annual maximum precip* from a given run"""
    ds_areacell = get_ds_areacell(runid, experiment_name, base_path=base_path, areacell_path=areacell_path)
    return [
        get_tropical_areamean(
            da,
            ds_areacell,
            tropical_halfwidth=tropical_halfwidth,
        ) for da in get_mean_ep_info(runid, experiment_name, year_range, base_path=base_path, file_path=file_path)
    ]


def get_tropical_avgp_areamean_from_experiment(
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
        areacell_path=AREACELL_PATH,
        tropical_halfwidth=TROPICAL_HALFWIDTH,
):
    """Get the required means (total, convective, resolved) of *temporal averages* from a given run"""
    ds_areacell = get_ds_areacell(runid, experiment_name, base_path=base_path, areacell_path=areacell_path)
    return [
        get_tropical_areamean(
            da,
            ds_areacell,
            tropical_halfwidth=tropical_halfwidth,
        ) for da in get_mean_info(runid, experiment_name, year_range, base_path=base_path, file_path=file_path)
    ]

# TODO: this code is not dry compared to the analogous stuff for tropical! Condense this script and test to make sure
#  nothing breaks.
def get_lat_slice(central_latitude=0, halfwidth=LAT_SLICE_HALFWIDTH):
    """
    Returns a slice of latitudes of width = 2 x halfwidth centred at central_latitude
    """
    return slice(central_latitude - halfwidth, central_latitude + halfwidth)

def select_lat_slice(da, central_latitude=0., halfwidth=LAT_SLICE_HALFWIDTH):
    """
    Returns a slice of a given array consisting only of a particular latitude slice band
    """
    my_lat_slice = get_lat_slice(central_latitude = central_latitude, halfwidth = halfwidth)

    return da.sel(lat = my_lat_slice)

def select_midlat_slices(da, central_latitude = 45., halfwidth = LAT_SLICE_HALFWIDTH):
    """
    Select two symmetric midlatitude slices of da w/ desired halfwidth, located at +/- central_latitude.
    """
    sliceA = get_lat_slice(central_latitude, halfwidth = halfwidth)
    sliceB = get_lat_slice(-central_latitude, halfwidth = halfwidth)

    return xr.concat(
        [
            da.sel(lat = sliceA),
            da.sel(lat = sliceB),
        ],
        dim="lat",
    )

def get_lat_slice_areamean(da, ds_areacell, central_latitude=0, halfwidth=LAT_SLICE_HALFWIDTH):
    """
    Compute the spatial mean over a lat slice of a given DA
    """
    da_sliced = select_lat_slice(
        da,
        central_latitude = central_latitude,
        halfwidth = LAT_SLICE_HALFWIDTH,
    )

    # Figure out total area covered by slice
    slice_area = ds_areacell.areacella.sel(
        lat = get_lat_slice(
            central_latitude = central_latitude,
            halfwidth = halfwidth,
        ),
    ).sum(
        dim=['lon', 'lat'],
    )

    return ((ds_areacell.areacella * da_sliced).sum(dim=['lon', 'lat']) / slice_area).values

def get_midlat_areamean(da, ds_areacell, central_latitude=45., halfwidth=LAT_SLICE_HALFWIDTH):
    """
    Compute the spatial mean of da over midlatitudes
    """
    da_sliced = select_midlat_slices(
        da,
        central_latitude = central_latitude,
        halfwidth = LAT_SLICE_HALFWIDTH,
    )

    # Figure out total area covered by slice
    slice_area = select_midlat_slices(ds_areacell.areacella,
            central_latitude = central_latitude,
            halfwidth = halfwidth,
    ).sum(
        dim=['lon', 'lat'],
    )

    return ((ds_areacell.areacella * da_sliced).sum(dim=['lon', 'lat']) / slice_area).values

def get_lat_slice_ep_areamean_from_experiment(
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
        areacell_path=AREACELL_PATH,
        central_latitude=0,
        halfwidth=LAT_SLICE_HALFWIDTH,
):
    """Get the required means (total, convective, resolved) of *mean annual maximum precip* from a given run"""
    ds_areacell = get_ds_areacell(runid, experiment_name, base_path=base_path, areacell_path=areacell_path)
    return [
        get_lat_slice_areamean(
            da,
            ds_areacell,
            central_latitude=central_latitude,
            halfwidth=halfwidth,
        ) for da in get_mean_ep_info(runid, experiment_name, year_range, base_path=base_path, file_path=file_path)
    ]

def get_midlat_ep_areamean_from_experiment(
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
        areacell_path=AREACELL_PATH,
        central_latitude=45,
        halfwidth=LAT_SLICE_HALFWIDTH,
):
    """Get the required MIDLATITUDE means (total, convective, resolved) of *mean annual maximum precip* from a given run"""
    ds_areacell = get_ds_areacell(runid, experiment_name, base_path=base_path, areacell_path=areacell_path)

    return [
        get_midlat_areamean(
            da,
            ds_areacell,
            central_latitude=central_latitude,
            halfwidth=halfwidth,
        ) for da in get_mean_ep_info(runid, experiment_name, year_range, base_path=base_path, file_path=file_path)
    ]

def get_lat_slice_avgp_areamean_from_experiment(
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
        areacell_path=AREACELL_PATH,
        central_latitude=0,
        halfwidth=LAT_SLICE_HALFWIDTH,
):
    """Get the required means (total, convective, resolved) of *temporal averages* from a given run"""
    ds_areacell = get_ds_areacell(runid, experiment_name, base_path=base_path, areacell_path=areacell_path)
    return [
        get_lat_slice_areamean(
            da,
            ds_areacell,
            central_latitude=central_latitude,
            halfwidth=halfwidth,
        ) for da in get_mean_info(runid, experiment_name, year_range, base_path=base_path, file_path=file_path)
    ]

def get_midlat_avgp_areamean_from_experiment(
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
        areacell_path=AREACELL_PATH,
        central_latitude=45.,
        halfwidth=LAT_SLICE_HALFWIDTH,
):
    """Get the required MIDLATITUDE means (total, convective, resolved) of *temporal averages* from a given run"""
    ds_areacell = get_ds_areacell(runid, experiment_name, base_path=base_path, areacell_path=areacell_path)
    return [
        get_midlat_areamean(
            da,
            ds_areacell,
            central_latitude=central_latitude,
            halfwidth=halfwidth,
        ) for da in get_mean_info(runid, experiment_name, year_range, base_path=base_path, file_path=file_path)
    ]

def get_annual_mean_time_series(
        var_name,
        runid,
        experiment_name,
        year_range,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
        areacell_path=AREACELL_PATH,
):
    """Returns a time series of the annually averaged, 
    globally area-averaged (scalar) var_name in question"""

    ds = get_ds(
        var_name,
        runid,
        experiment_name,
        year_range,
        base_path=base_path,
        file_path=file_path,
    )

    ds_areacell = get_ds_areacell(runid, experiment_name, base_path=base_path, areacell_path=areacell_path)
    global_area = ds_areacell.areacella.sum(dim=['lon', 'lat'])

    spatial_mean = (ds_areacell.areacella * ds[var_name]).sum(
        dim=['lon', 'lat']) / global_area  # Properly area weighted mean of rate of flux
    return spatial_mean.groupby('time.year').mean(dim='time')


def unpack_gridcell(gridcell):
    return gridcell["lat"], gridcell["lon"]


def get_max_delta(da, gridcell, grid_delta=GRID_DELTA):
    """
    Returns the maximum change in a data array "da" between
    gridcell and its neighbours.
    """
    my_lat, my_lon = unpack_gridcell(gridcell)
    my_cell_value = da.sel(lat=my_lat, lon=my_lon, method="nearest").values

    shifts = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    nbhrs_values = [
        da.sel(
            lat=my_lat + grid_delta * shift[0],
            lon=my_lon + grid_delta * shift[1],
            method="nearest",
        ).values
        for shift in shifts
    ]

    return max(np.abs(np.array(nbhrs_values) - my_cell_value))

def get_day_of_epe(
        runid,
        experiment_name,
        year,
        gridcell,
        base_path=BASE_PATH,
        file_path=FILE_PATH,
):
    """
    Return the date of an EPE for a particular gridcell and year
    in a particular experiment
    """

    # Get precipitation ds
    ds_pr_daily = get_ds(
        "pr",
        runid,
        experiment_name,
        range(year, year + 1),  # technical reason for range instead of just "year"
        base_path=base_path,
        file_path=file_path,
    )

    my_lat, my_lon = unpack_gridcell(gridcell)

    return ds_pr_daily.pr.sel(
        lat=my_lat,
        lon=my_lon,
        method="nearest"
    ).idxmax(dim="time").values.item()


def get_local_mean_epe_delta_ps(
        runid,
        experiment_name,
        year_range,
        gridcell,
        pr_file_path,
        ps_file_path,
        base_path=BASE_PATH,
        grid_delta=GRID_DELTA,
):
    """
    Print the mean delta_ps on extreme precipitation days over year_range
    within a particular cell "my_gridcell".
    """

    # Get surface pressure ds
    ds_ps_daily = get_ds(
        "ps",
        runid,
        experiment_name,
        year_range,
        base_path=base_path,
        file_path=ps_file_path,
    )

    deltas = []

    for year in year_range:
        day_of_epe = get_day_of_epe(
            runid,
            experiment_name,
            year,
            gridcell,
            base_path=base_path,
            file_path=pr_file_path,
        )

        deltas.append(
            get_max_delta(
                ds_ps_daily.sel(
                    time=day_of_epe,
                    method="ffill",
                )["ps"],
                gridcell,
                grid_delta=grid_delta,
            )
        )

    return np.array(deltas).mean()


def get_abs_horiz_gradient(da, r_earth=6.37e3, r_earth_units="km"):
    """
    Returns a DataArray whose entries are (approx.) the magnitude of the
    spatial gradient of a da in units of

    da.units per r_earth_units.

    da must have lat, lon as its spatial coords., and it must
    also depend on time.

    The finite difference approx. uses a numpy utility function.
    Spherical coordinate corrections to the gradient are accounted for!
    """

    lat_band = np.deg2rad(da.lat.to_numpy())
    lon_band = np.deg2rad(da.lon.to_numpy())

    da_grad_as_nparr = np.gradient(
        da.to_numpy(),
        lat_band,  # coord arrays must be included AND ordered correctly argh! yucky
        lon_band,
        axis=[1, 2],
    )

    # For some reason I cannot fathom 
    # np.gradient() outputs a tuple of arrays
    # instead of an array. So I postprocess it
    # into a sane output here.
    da_grad_as_nparr = np.array(da_grad_as_nparr)

    # Manually correct the longitudinal derivatives bcz
    # np.gradient() assumed a Cartesian grid
    # (see Holton's "An Intro. to Dynamic Meteorology", appendix C). 
    for k in range(0, len(lat_band)):
        da_grad_as_nparr[1][:][k][:] /= np.cos(lat_band[k])

        # Divide by Earth's radius
    da_grad_as_nparr /= r_earth

    # Take the magnitude
    abs_da_grad_as_nparr = np.sqrt(da_grad_as_nparr[0, ...] ** 2 + da_grad_as_nparr[1, ...] ** 2)

    # Finally, return the result as a DataArray
    return xr.DataArray(
        data=abs_da_grad_as_nparr,
        dims=["time", "lat", "lon"],
        coords=dict(
            lon=da.lon.to_numpy(),
            lat=da.lat.to_numpy(),
            time=da.time.to_numpy(),
        ),
        attrs=dict(
            description=da.long_name + " Horizontal Gradient",
            units=da.units + "/" + r_earth_units,
        ),
    )


def select_fixed_year(da, year):
    return da.sel(time=da.time.dt.year == year)
