import matplotlib.pyplot as plt
from mpl_toolkits import axisartist
from ep_processing import *

plt.rc('font', family='serif')

fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(3, 3, width_ratios=[1, 1, 0.03])
gs.update(wspace=0.2, hspace=0.4)

my_experiment_name = "amip"
my_runids = ["agm-ztmst-1", "agm-amip-test", "agm-ztmst-n1"]
my_titles = [
    [r"Resolved, $\Delta t_{\text{adv}} = 4\Delta t$", r"Convective, $\Delta t_{\text{adv}} = 4\Delta t$"],
    [r"$\Delta t_{\text{adv}} = 2\Delta t$ (Default)", r"$\Delta t_{\text{adv}} = 2\Delta t$ (Default)"],
    [r"$\Delta t_{\text{adv}} = \Delta t$", r"$\Delta t_{\text{adv}} = \Delta t$"],
]
year_start = 2003
year_end = 2003 + 1
year_range = range(year_start, year_end)

my_areacell_path = "areacella_fx_CanESM5-1_amip_r1i1p1f1_gn.nc"

da_ep_resolved_max = 305.2203 # obtained manually

cnt = 0

for my_runid in my_runids:
    my_base_path = "~/Documents/research/experiment-outputs/{experiment_name}/{runid}/"
    my_file_path = "{var_name}_day_CanESM5-1_{experiment_name}_r1i1p1f1_gn_{year}0101-{year}1231.nc"

    da_ep_total, da_ep_convective, da_ep_resolved = get_ep_info(
        my_runid,
        my_experiment_name,
        year_range,
        base_path = my_base_path,
        file_path = my_file_path,
    )

    ax_pr = fig.add_subplot(
        gs[cnt, 0],
        axes_class = axisartist.axislines.AxesZero,
    )

    ax_prc = fig.add_subplot(
        gs[cnt, 1],
        axes_class=axisartist.axislines.AxesZero,
    )

    ax_pr.set_title(my_titles[cnt][0])
    ax_prc.set_title(my_titles[cnt][1])

    if cnt == 2:
        ax_pr.set_xlabel("Longitude (deg. E)")
        ax_pr.set_ylabel("Latitude (deg. N)")

    da_ep_resolved.plot(
        ax = ax_pr,
        add_colorbar = False,
        add_labels = False,
        vmin=0,
        vmax=da_ep_resolved_max,
    )

    prc = da_ep_convective.plot(
        ax = ax_prc,
        add_colorbar = False,
        add_labels = False,
        vmin = 0,
        vmax = da_ep_resolved_max,
    )

    cnt += 1

# Hack to get the colorbar axes position looking good...manually
# massage the bbox!
my_cax = fig.add_subplot(gs[2,2])
pos = my_cax.get_position()
pos.x0 = 0.865
pos.x1 = pos.x0 + 0.015
my_cax.set_position(pos)

# Finally draw the colorbar itself
plt.colorbar(
            prc,
            ax = ax_prc,
            cax = my_cax,
            label = "Intensity (mm/day)",
)

plt.savefig("ztmst-summary" + ".png", dpi=600)
plt.show()