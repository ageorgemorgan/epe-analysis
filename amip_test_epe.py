"""
Test that our AMIP test gives reasonable results, AND shows
partitioning 

author: AGM
"""
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import sys

from ep_processing import *
from utils.visualization import draw_global_map, process_for_map

my_experiment_name = "amip"
my_runid = "agm-amip-test"
year_start = 2003
year_end = 2008 + 1
year_range = range(year_start, year_end)

my_base_path = "~/Documents/research/experiment-outputs/{experiment_name}/{runid}/"
my_file_path = "{var_name}_day_CanESM5-1_{experiment_name}_r1i1p1f1_gn_{year}0101-{year}1231.nc"
my_areacell_path = "areacella_fx_CanESM5-1_amip_r1i1p1f1_gn.nc"

da_ep_total, da_ep_convective, da_ep_resolved = get_ep_info(
    my_runid,
    my_experiment_name,
    year_range,
    base_path = my_base_path,
    file_path = my_file_path,
)
da_ep_total_max = da_ep_total.max().values

# da_list = [da_ep_resolved, da_ep_convective, da_ep_total]
# label_list = ["Resolved", "Convective", "Total"]
#
# for da, label in zip(da_list, label_list):
#
#     field_vals, lon_plt, lat_plt = process_for_map(da)
#     draw_global_map(
#         lon_plt,
#         lat_plt,
#         field_vals,
#         title = label,
#         filled = True,
#         show_fig = False,
#         save_fig = True,
#         levels = 16,
#         cmap = "Blues",
#         cbar_params = [0.95, 0.24, 0.05, 0.505], # position, upper offset, width, cbar length
#         vmin = 0,
#         vmax = da_ep_total_max,
#         draw_labels = False,
#         label_contours = False,
#         remove_cbar = True if label != "Total" else False,
#         fig = None,
#         projection = ccrs.PlateCarree(central_longitude = 180),
#         outfilename = "amip_baseline_experiment1" + label + ".png",
#     )

# Determining Anomalies
tropical_halfwidth = 23.4

da_conv_fraction, da_conv_fraction_spatial_mean = get_convective_ep_fraction_in_tropics(
        my_runid,
        my_experiment_name,
        year_range,
        my_base_path,
        my_file_path,
        my_areacell_path,
        tropical_halfwidth = tropical_halfwidth,
)

field_vals, lon_plt, lat_plt = process_for_map(da_conv_fraction)
draw_global_map(
        lon_plt,
        lat_plt,
        field_vals,
        title = None,
        filled = True,
        show_fig = True,
        save_fig = False,
        levels = 16,
        bbox = [0, 360, -tropical_halfwidth + 2, tropical_halfwidth - 2],
        cmap = "greys",
        cbar_params = [0.92, 0.35, 0.025, 0.22], # position, upper offset, width, cbar length
        xtickdelta = 60,
        ytickdelta = 10,
        figsize = (10, 3),
        #vmin = 0,
        #vmax = 1.0,
        draw_labels = False,
        label_contours = False,
        remove_cbar = False,
        fig = None,
        projection = ccrs.PlateCarree(central_longitude = 180),
        outfilename = "amip_baseline_convective_fraction_experiment1" + ".png",
)

print(f"Area-weighted spatial mean of convective fraction = {da_convective_fraction_spatial_mean}")

# print(
#     f"The maximum fraction of convective precipitation over all grid cells is {
#     100 * convective_fraction_max
#     } %."
# )
#
# print(
#     f"The global mean fraction of convective precipitation is {
#     100 * convective_fraction_mean
#     } %."
# )
# Comment the line out below to compare our results against RTD
sys.exit()

mean_annual_pr_time_series = 86400 * get_annual_mean_time_series(
    "pr",
    my_runid,
    my_experiment_name,
    year_range,
    base_path = my_base_path,
    file_path = my_file_path,
    areacell_path = my_areacell_path,
)

pr_mean = mean_annual_pr_time_series.mean(dim='year').values

mean_annual_pr_time_series.plot(color="xkcd:lilac")
plt.grid()
plt.title("agm-amip-test Annual Total Precip.")
plt.xlabel("Year (CE)")
plt.ylabel("mm/day")
plt.show()
