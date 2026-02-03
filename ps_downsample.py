# A rough-and-tumble script for manually converting the default 3hr ps files into daily ps files.
# TODO: make this more customizable!
from ep_processing import *

my_base_path = "~/Documents/research/experiment-outputs/{experiment_name}/{runid}/"
my_file_path = "{var_name}_3hr_CanESM5-1_{experiment_name}_r1i1p1f1_gn_{year}01010000-{year}12312100.nc"

my_experiment_name = "amip"
my_runid = "agm-amip-test"
my_var_name = "ps"
year_start = 2005
year_end = 2008 + 1
year_range = range(year_start, year_end)

ds_ps_3h = get_ds(
        my_var_name,
        my_runid,
        my_experiment_name,
        year_range,
        base_path = my_base_path,
        file_path = my_file_path,
)

ds_ps_daily = ds_ps_3h.resample(time="1D", label="left",).mean()
# Note that this records the daily values as taken @ midnight rather than noon but w/e

for year in year_range:
    my_outfile_path = "{var_name}_day_CanESM5-1_{experiment_name}_r1i1p1f1_gn_{year}0101-{year}1231.nc"
    my_total_out_path = (
        my_base_path.format(
            runid = my_runid,
            experiment_name = my_experiment_name,
        ) +
        my_outfile_path.format(
            var_name = my_var_name,
            year = year,
            experiment_name = my_experiment_name,
        )
        )

    ds_ps_daily.sel(time=ds_ps_daily.time.dt.year.isin(year)).to_netcdf(path = my_total_out_path)