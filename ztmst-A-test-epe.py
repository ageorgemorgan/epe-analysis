"""
Test that our AMIP test w/ ztmst-A gives reasonable results, AND shows
partitioning 

author: AGM
"""
import matplotlib.pyplot as plt

from ep_processing import *

A = "n1"
my_experiment_name = "amip"
my_runid = "agm-ztmst-" + A
year_start = 2003
year_end = 2003 + 1
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
da_ep_resolved_max = da_ep_resolved.max().values

fig, ax = plt.subplots()
CS = da_ep_resolved.plot(vmin=0, vmax=da_ep_resolved_max, cbar_kwargs={"label": "pr resolved (mm/d)"})
plt.title("Resolved")
plt.show()

da_ep_convective.plot(vmin=0, vmax=da_ep_resolved_max, cbar_kwargs={"label": "prc (mm/d)"})
plt.title("Convective")
plt.show()

da_ep_total.plot(vmin=0, vmax=da_ep_resolved_max, cbar_kwargs={"label": "pr (mm/d)"})
plt.title("Total")
plt.show()

# mean_annual_pr_time_series = 86400 * get_annual_mean_time_series(
#     "pr",
#     my_runid,
#     my_experiment_name,
#     year_range,
#     base_path = my_base_path,
#     file_path = my_file_path,
#     areacell_path = my_areacell_path,
# )
#
# pr_mean = mean_annual_pr_time_series.mean(dim='year').values
#
# mean_annual_pr_time_series.plot(color="xkcd:lilac")
# plt.grid()
# plt.title("agm-amip-test Annual Total Precip.")
# plt.xlabel("Year (CE)")
# plt.ylabel("mm/day")
# plt.show()
