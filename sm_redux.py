import matplotlib.pyplot as plt
from mpl_toolkits import axisartist
import numpy as np

from ep_processing import *
from utils.visualization import *

# Plotting stuff
TITLE_FONT_SIZE = 16
TICK_FONT_SIZE = 12

plt.rc('axes', labelsize = TITLE_FONT_SIZE)
plt.rc('xtick', labelsize = TICK_FONT_SIZE)
plt.rc('ytick', labelsize = TICK_FONT_SIZE)

base_dir = "sm04-data/"

avgpr_convective_alpha = np.loadtxt(base_dir + "sm04-alpha-avg-param.txt")
avgpr_resolved_alpha = np.loadtxt(base_dir + "sm04-alpha-avg-resolved.txt")
avgpr_total_alpha = np.loadtxt(base_dir + "sm04-alpha-avg-total.txt")
ax00_content = np.stack([avgpr_convective_alpha, avgpr_resolved_alpha, avgpr_total_alpha])

pr_convective_alpha = np.loadtxt(base_dir + "sm04-alpha-epe-param.txt")
pr_resolved_alpha = np.loadtxt(base_dir + "sm04-alpha-epe-resolved.txt")
pr_total_alpha = np.loadtxt(base_dir + "sm04-alpha-epe-total.txt")
ax01_content = np.stack([pr_convective_alpha, pr_resolved_alpha, pr_total_alpha])

avgpr_convective_taud = np.loadtxt(base_dir + "sm04-taud-avg-param.txt")
avgpr_resolved_taud = np.loadtxt(base_dir + "sm04-taud-avg-resolved.txt")
avgpr_total_taud = np.loadtxt(base_dir + "sm04-taud-avg-total.txt")
ax10_content = np.stack([avgpr_convective_taud, avgpr_resolved_taud, avgpr_total_taud])

pr_convective_taud = np.loadtxt(base_dir + "sm04-taud-epe-param.txt")
pr_resolved_taud = np.loadtxt(base_dir + "sm04-taud-epe-resolved.txt")
pr_total_taud = np.loadtxt(base_dir + "sm04-taud-epe-total.txt")
ax11_content = np.stack([pr_convective_taud, pr_resolved_taud, pr_total_taud])

ax_contents = [ax00_content, ax01_content, ax10_content, ax11_content]

alpha_str = ["2e6", "2e7", "2e8", "5e8", "2e9", "2e10"]
alpha = [float(a_str) for a_str in alpha_str]

taud_str = ["12e2", "8e3", "148e2", "21600", "284e2"]
taud = [float(t_str) for t_str in taud_str]

fig = plt.figure(figsize=(12, 12))

gs = fig.add_gridspec(2, 2, width_ratios=[1, 1])
gs.update(wspace=0.3, hspace=0.3)

row_idx = 0
col_idx = 0

for ax_content in ax_contents[:2]:
    ax = fig.add_subplot(
        gs[row_idx, col_idx],
        axes_class=axisartist.axislines.AxesZero,
    )

    plt.grid("on")

    # plt.semilogx(5e8,
    #             avgpr_total_baseline,
    #             color = "xkcd:emerald",
    #             marker= "*",
    #             markersize =  default_markersize,
    #            )

    plt.semilogx(alpha,
                 ax_content[0],
                 color="xkcd:cerulean",
                 marker="o",
                 linestyle="solid",
                 label="Convective",
                 linewidth=2,
                 )

    # plt.semilogx(5e8,
    #             avgpr_convective_baseline,
    #             color = "xkcd:cerulean",
    #             marker= "*",
    #             markersize =  default_markersize,
    #            )

    plt.semilogx(alpha,
                 ax_content[1],
                 color="xkcd:crimson",
                 marker="d",
                 linestyle="solid",
                 label="Resolved",
                 linewidth=2,
                 )

    # plt.semilogx(5e8,
    #             avgpr_resolved_baseline,
    #             color = "xkcd:crimson",
    #             marker= "*",
    #             markersize =  default_markersize,
    #            )

    plt.semilogx(alpha,
                 ax_content[2],
                 color="xkcd:emerald",
                 marker="s",
                 linestyle="solid",
                 label="Total",
                 linewidth=2,
                 )

    plt.xlabel(r"$\alpha$ ($\mathrm{m}^4$/kg)", fontsize=TITLE_FONT_SIZE)
    # plt.xticks(fontsize = 16, rotation = 0)
    # plt.yticks(fontsize = 16, rotation = 0)

    ax.tick_params(
        direction="out",
        bottom=False,
        top=False,
        left=False,
        right=False,
    )

    if row_idx == 0:
        plt.xlim(min(alpha), max(alpha))

    if row_idx == 0 and col_idx == 0:
        plt.ylabel(r"Mean Precipitation (mm $\mathrm{d}^{-1}$)", fontsize=TITLE_FONT_SIZE)
        plt.legend(fontsize=16, loc=(0.2, 0.6))

    if row_idx == 0 and col_idx == 1:
        plt.ylabel(r"Mean Precip., EPEs Only (mm $\mathrm{d}^{-1}$)", fontsize=TITLE_FONT_SIZE)

    col_idx += 1
    col_idx = col_idx % 3

# Save output
# outfile_path = "images/" + "ps_anom_localized_gallery" + ".png"
# plt.savefig(outfile_path, dpi=600, bbox_inches='tight')

# plt.tight_layout()
    ax.tick_params(
        direction = "out",
        bottom = False,
        top = False,
        left = False,
        right = False,
    )

    if row_idx == 0 :
        plt.xlim(min(alpha), max(alpha))

    if row_idx == 0 and col_idx == 0:
        plt.ylabel(r"Mean Precipitation (mm $\mathrm{d}^{-1}$)", fontsize = TITLE_FONT_SIZE)
        plt.legend(fontsize = 16, loc = (0.2, 0.6))

    if row_idx == 0 and col_idx == 1:
        plt.ylabel(r"Mean Precip., EPEs Only (mm $\mathrm{d}^{-1}$)", fontsize = TITLE_FONT_SIZE)

    col_idx += 1
    col_idx = col_idx % 3


# Save output
#outfile_path = "images/" + "ps_anom_localized_gallery" + ".png"
#plt.savefig(outfile_path, dpi=600, bbox_inches='tight')

#plt.tight_layout()

plt.show()
plt.show()