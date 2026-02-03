from ep_processing import *

my_base_path = "~/Documents/research/experiment-outputs/{experiment_name}/{runid}/"
my_generic_file_path = "_day_CanESM5-1_{experiment_name}_r1i1p1f1_gn_{year}0101-{year}1231.nc"
my_pr_file_path = "pr" + my_generic_file_path
my_ps_file_path = "ps" + my_generic_file_path

my_experiment_name = "amip"
my_runid = "agm-amip-test"
my_var_name = "ps"
year_start = 2003
year_end = 2008 + 1
year_range = range(year_start, year_end)

my_lat = -7.0
my_lon = 100.

my_gridcell = {"lat": my_lat, "lon": my_lon}

# ds_ps_daily = get_ds(
#         my_var_name,
#         my_runid,
#         my_experiment_name,
#         year_range,
#         base_path = my_base_path,
#         file_path = my_ps_file_path,
# )

local_mean_epe_delta_ps = get_local_mean_epe_delta_ps(
    my_runid,
    my_experiment_name,
    year_range,
    my_gridcell,
    pr_file_path = my_pr_file_path,
    ps_file_path = my_ps_file_path,
    base_path = my_base_path,
)

print(local_mean_epe_delta_ps, "Pascal")