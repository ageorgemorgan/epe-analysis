"""
Look @ SM04 experiments.

Basically plotting the results of a parameter sweep.

Author: AGM
"""
import matplotlib.pyplot as plt

from ep_processing import *

my_experiment_name = "amip"
year_start = 2004
year_end = 2008 + 1
year_range = range(year_start, year_end)

default_markersize = 320

my_base_path = "~/Documents/research/experiment-outputs/{experiment_name}/{runid}/"
my_file_path = "{var_name}_day_CanESM5-1_{experiment_name}_r1i1p1f1_gn_{year}0101-{year}1231.nc"
my_areacell_path = "areacella_fx_CanESM5-1_amip_r1i1p1f1_gn.nc"

# First we load the baseline AMIP simulation (results of experiment 1)
baseline_runid = "agm-amip-test"

tropical_halfwidth = 13. 

# Means over all EPEs
pr_total_baseline, pr_convective_baseline, pr_resolved_baseline = get_tropical_ep_areamean_from_experiment(
    baseline_runid,
    my_experiment_name,
    year_range,
    base_path = my_base_path,
    file_path = my_file_path,
    areacell_path = my_areacell_path,
    tropical_halfwidth = tropical_halfwidth,
)

# Means over all days
avgpr_total_baseline, avgpr_convective_baseline, avgpr_resolved_baseline = get_tropical_avgp_areamean_from_experiment(
    baseline_runid,
    my_experiment_name,
    year_range,
    base_path = my_base_path,
    file_path = my_file_path,
    areacell_path = my_areacell_path,
    tropical_halfwidth = tropical_halfwidth ,
)

# ****ALPHA EXPERIMENTS****
alpha_str = ["2e6", "2e7", "2e8", "5e8", "2e9", "2e10"]
alpha = [float(a_str) for a_str in alpha_str]

pr_total_alpha = []
pr_convective_alpha = []
pr_resolved_alpha = []

avgpr_total_alpha = []
avgpr_convective_alpha = []
avgpr_resolved_alpha = []

# Load all other experimental results
for a_str in alpha_str:
    if a_str == "5e8":
        pr_total_experiment, pr_convective_experiment, pr_resolved_experiment = pr_total_baseline, pr_convective_baseline, pr_resolved_baseline
        avgpr_total_experiment, avgpr_convective_experiment, avgpr_resolved_experiment = avgpr_total_baseline, avgpr_convective_baseline, avgpr_resolved_baseline
    else:
        sm_runid = "agm-sm04-alpha-" + a_str
        pr_total_experiment, pr_convective_experiment, pr_resolved_experiment = get_tropical_ep_areamean_from_experiment(
            sm_runid,
            my_experiment_name,
            year_range,
            base_path = my_base_path,
            file_path = my_file_path,
            areacell_path = my_areacell_path,
            tropical_halfwidth=tropical_halfwidth ,
        )
        avgpr_total_experiment, avgpr_convective_experiment, avgpr_resolved_experiment = get_tropical_avgp_areamean_from_experiment(
            sm_runid,
            my_experiment_name,
            year_range,
            base_path=my_base_path,
            file_path=my_file_path,
            areacell_path=my_areacell_path,
            tropical_halfwidth=tropical_halfwidth ,
        )

    pr_total_alpha.append(pr_total_experiment)
    pr_convective_alpha.append(pr_convective_experiment)
    pr_resolved_alpha.append(pr_resolved_experiment)

    avgpr_total_alpha.append(avgpr_total_experiment)
    avgpr_convective_alpha.append(avgpr_convective_experiment)
    avgpr_resolved_alpha.append(avgpr_resolved_experiment)

# Make plots for alpha experiments
plt.semilogx(alpha,
             pr_total_alpha,
             color = "xkcd:emerald",
             marker = "s",
             linestyle = "solid",
             label= "Total",
             linewidth = 2,
            )
plt.semilogx(alpha,
             pr_convective_alpha,
             color = "xkcd:cerulean",
             marker = "o",
             linestyle = "solid",
             label = "Convective",
             linewidth = 2,
            )
plt.semilogx(alpha,
             pr_resolved_alpha,
             color = "xkcd:crimson",
             marker = "d",
             linestyle = "solid",
             label = "Resolved",
             linewidth = 2,
            )

plt.scatter(5e8,
            pr_total_baseline,
            color = "xkcd:emerald",
            marker= "*",
            s = default_markersize,
           )
plt.scatter(5e8,
            pr_convective_baseline,
            color = "xkcd:cerulean",
            marker= "*",
            s = default_markersize,
           )
plt.scatter(5e8,
            pr_resolved_baseline,
            color = "xkcd:crimson",
            marker= "*",
            s =  default_markersize,
           )

plt.ylabel("Mean Precip., EPEs Only (mm/day)", fontsize = 16)
plt.xlabel(r"$\alpha$ ($\mathrm{m}^4$/kg)", fontsize = 16)
plt.grid("on")
plt.xticks(fontsize = 16, rotation = 0)
plt.yticks(fontsize = 16, rotation = 0)
# plt.legend(fontsize = 16) # commented out only for formatting purposes in the report
plt.xlim(min(alpha), max(alpha))
plt.tight_layout()

plt.savefig("images/sm-experiments-alpha" + ".png", dpi = 600)
# plt.show
plt.clf()

plt.semilogx(alpha,
             avgpr_total_alpha,
             color = "xkcd:emerald",
             marker = "s",
             linestyle = "solid",
             label= "Total",
             linewidth = 2,
            )
plt.semilogx(alpha,
             avgpr_convective_alpha,
             color = "xkcd:cerulean",
             marker = "o",
             linestyle = "solid",
             label = "Convective",
             linewidth = 2,
            )
plt.semilogx(alpha,
             avgpr_resolved_alpha,
             color = "xkcd:crimson",
             marker = "d",
             linestyle = "solid",
             label = "Resolved",
             linewidth = 2,
            )

plt.scatter(5e8,
            avgpr_total_baseline,
            color = "xkcd:emerald",
            marker= "*",
            s =  default_markersize,
           )
plt.scatter(5e8,
            avgpr_convective_baseline,
            color = "xkcd:cerulean",
            marker= "*",
            s =  default_markersize,
           )
plt.scatter(5e8,
            avgpr_resolved_baseline,
            color = "xkcd:crimson",
            marker= "*",
            s =  default_markersize,
           )

plt.ylabel("Mean Precipitation (mm/day)", fontsize = 16)
plt.xlabel(r"$\alpha$ ($\mathrm{m}^4$/kg)", fontsize = 16)
plt.grid("on")
plt.xticks(fontsize = 16, rotation = 0)
plt.yticks(fontsize = 16, rotation = 0)
plt.legend(fontsize = 16, loc = (0.2, 0.6))
plt.xlim(min(alpha), max(alpha))
plt.tight_layout()

plt.savefig("images/sm-experiments-avg-alpha" + ".png", dpi = 600)
#plt.show()
plt.clf()

# ****TAU_D EXPERIMENTS****
taud_str = ["12e2", "8e3", "148e2", "21600", "284e2"]
taud = [float(t_str) for t_str in taud_str]

pr_total_taud = []
pr_convective_taud = []
pr_resolved_taud = []

avgpr_total_taud = []
avgpr_convective_taud = []
avgpr_resolved_taud = []

for t_str in taud_str:
    if t_str == "21600":
        pr_total_experiment, pr_convective_experiment, pr_resolved_experiment = pr_total_baseline, pr_convective_baseline, pr_resolved_baseline
        avgpr_total_experiment, avgpr_convective_experiment, avgpr_resolved_experiment = avgpr_total_baseline, avgpr_convective_baseline, avgpr_resolved_baseline

    else:
        sm_runid = "agm-sm04-taud-" + t_str
        pr_total_experiment, pr_convective_experiment, pr_resolved_experiment = get_tropical_ep_areamean_from_experiment(
            sm_runid,
            my_experiment_name,
            year_range,
            base_path = my_base_path,
            file_path = my_file_path,
            areacell_path = my_areacell_path,
            tropical_halfwidth=tropical_halfwidth ,
        )

        avgpr_total_experiment, avgpr_convective_experiment, avgpr_resolved_experiment = get_tropical_avgp_areamean_from_experiment(
            sm_runid,
            my_experiment_name,
            year_range,
            base_path=my_base_path,
            file_path=my_file_path,
            areacell_path=my_areacell_path,
            tropical_halfwidth=tropical_halfwidth ,
        )

    pr_total_taud.append(pr_total_experiment)
    pr_convective_taud.append(pr_convective_experiment)
    pr_resolved_taud.append(pr_resolved_experiment)

    avgpr_total_taud.append(avgpr_total_experiment)
    avgpr_convective_taud.append(avgpr_convective_experiment)
    avgpr_resolved_taud.append(avgpr_resolved_experiment)

plt.plot(taud,
         pr_total_taud,
         color = "xkcd:emerald",
         marker = "s",
         linestyle = "solid",
         label= "Total",
         linewidth = 2,
        )
plt.plot(taud,
         pr_convective_taud,
         color = "xkcd:cerulean",
         marker = "o",
         linestyle = "solid",
         label = "Convective",
         linewidth = 2,
        )
plt.plot(taud,
         pr_resolved_taud,
         color = "xkcd:crimson",
         marker = "d",
         linestyle = "solid",
         label = "Resolved",
         linewidth = 2,
        )

plt.scatter(21600,
            pr_total_baseline,
            color = "xkcd:emerald",
            marker= "*",
            s =  default_markersize,
           )
plt.scatter(21600,
            pr_convective_baseline,
            color = "xkcd:cerulean",
            marker= "*",
            s =  default_markersize,
            )
plt.scatter(21600,
            pr_resolved_baseline,
            color = "xkcd:crimson",
            marker= "*",
            s =  default_markersize,
           )

plt.grid("on")
plt.xticks(fontsize = 16, rotation = 0)
plt.yticks(fontsize = 16, rotation = 0)
plt.ylabel("Mean Precip., EPEs Only (mm/day)", fontsize = 16)
plt.xlabel(r"$\tau_{\mathrm{d}}$ (s)", fontsize = 16)
# plt.legend(fontsize = 12, loc = (0.05, 0.25))
plt.xlim(min(taud), max(taud))
plt.tight_layout()

plt.savefig("images/sm-experiments-taud" + ".png", dpi = 600)
#plt.show()
plt.clf()

plt.plot(taud,
         avgpr_total_taud,
         color = "xkcd:emerald",
         marker = "s",
         linestyle = "solid",
         label= "Total",
         linewidth = 2,
)
plt.plot(taud,
         avgpr_convective_taud,
         color = "xkcd:cerulean",
         marker = "o",
         linestyle = "solid",
         label = "Convective",
         linewidth = 2,
)
plt.plot(taud,
         avgpr_resolved_taud,
         color = "xkcd:crimson",
         marker = "d",
         linestyle = "solid",
         label = "Resolved",
         linewidth = 2,
)

plt.scatter(21600,
            avgpr_total_baseline,
            color = "xkcd:emerald",
            marker= "*",
            s =  default_markersize,
)
plt.scatter(21600,
            avgpr_convective_baseline,
            color = "xkcd:cerulean",
            marker= "*",
            s =  default_markersize,
)
plt.scatter(21600,
            avgpr_resolved_baseline,
            color = "xkcd:crimson",
            marker= "*",
            s =  default_markersize,
)

plt.grid("on")
plt.xticks(fontsize = 16, rotation = 0)
plt.yticks(fontsize = 16, rotation = 0)
plt.ylabel("Mean Precipitation (mm/day)", fontsize = 16)
plt.xlabel(r"$\tau_{\mathrm{d}}$ (s)", fontsize = 16)
# plt.legend(fontsize = 12, loc = "best")
plt.xlim(min(taud), max(taud))
plt.tight_layout()

plt.savefig("images/sm-experiments-avg-taud" + ".png", dpi = 600)
#plt.show()
